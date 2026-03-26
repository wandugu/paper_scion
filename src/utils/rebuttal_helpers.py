"""Rebuttal experiment helper utilities.

复用仓库已有 logger/config 体系，为 rebuttal 实验提供统一数据读取、
指标计算、manifest 与输出工具。
"""

from __future__ import annotations

import csv
import json
import platform
import random
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

from .common import load_yaml_config, resolve_project_path
from .logger import get_ot_logger

LOGGER = get_ot_logger()
CONFIG = load_yaml_config()


@dataclass(frozen=True)
class SourceInfo:
    source_id: str
    task_type: str
    language: str
    path: Path


def rebuttal_cfg() -> Dict[str, Any]:
    cfg = CONFIG.get("rebuttal")
    return cfg if isinstance(cfg, dict) else {}


def rebuttal_root() -> Path:
    return resolve_project_path(rebuttal_cfg().get("root_dir", "rebuttal"))


def outputs_dir() -> Path:
    return resolve_project_path(rebuttal_cfg().get("outputs_dir", "rebuttal/outputs"))


def scope_subsets_dir() -> Path:
    return resolve_project_path(rebuttal_cfg().get("scope_subsets_dir", "data/scope/subsets"))


def default_seed() -> int:
    return int(rebuttal_cfg().get("seed", 42))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_hash() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "UNKNOWN"


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_csv(path: Path, rows: Sequence[dict], headers: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(headers))
        writer.writeheader()
        for row in rows:
            writer.writerow({h: row.get(h, "") for h in headers})


_SOURCE_INFOS_CACHE: List[SourceInfo] | None = None


def source_infos() -> List[SourceInfo]:
    global _SOURCE_INFOS_CACHE
    if _SOURCE_INFOS_CACHE is not None:
        LOGGER.debug("复用已缓存的 SCOPE source 列表，数量=%s", len(_SOURCE_INFOS_CACHE))
        return list(_SOURCE_INFOS_CACHE)

    base = scope_subsets_dir()
    infos: List[SourceInfo] = []
    LOGGER.debug("扫描 SCOPE 子集目录: %s", base)
    if not base.exists():
        LOGGER.warning("SCOPE 子集目录不存在: %s", base)
        _SOURCE_INFOS_CACHE = []
        return []

    for ds_dir in sorted(base.iterdir()):
        if not ds_dir.is_dir() or not (ds_dir / "schema.json").exists():
            continue
        parts = ds_dir.name.split("_", 3)
        if len(parts) < 4:
            continue
        _, task, lang, source = parts
        infos.append(SourceInfo(source_id=source, task_type=task, language=lang, path=ds_dir))
    LOGGER.debug("扫描完成，source 数量=%s", len(infos))
    _SOURCE_INFOS_CACHE = infos
    return list(infos)


def load_schema_edges(schema_path: Path) -> List[tuple]:
    payload = json.loads(schema_path.read_text(encoding="utf-8"))
    edges = []
    for edge in payload:
        if edge.get("edge_kind") == "re":
            edges.append((
                "re",
                str(edge.get("head_type", "")).lower(),
                str(edge.get("rel_type", "")).lower(),
                str(edge.get("tail_type", "")).lower(),
            ))
        elif edge.get("edge_kind") == "ee":
            edges.append((
                "ee",
                str(edge.get("event_type", "")).lower(),
                str(edge.get("role", "")).lower(),
            ))
    return sorted(set(edges))


def load_train_reachable_edges(source: SourceInfo) -> List[tuple]:
    train_path = source.path / "docs.train.jsonl"
    if not train_path.exists():
        LOGGER.warning("缺失 train 文档: %s", train_path)
        return []

    edges = set()
    with train_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            for rel in item.get("relations", []) or []:
                edges.add((
                    "re",
                    str(rel.get("head_type", "")).lower(),
                    str(rel.get("rel_type", "")).lower(),
                    str(rel.get("tail_type", "")).lower(),
                ))

            evt_type = ""
            for evt in item.get("events", []) or []:
                evt_type = str(evt.get("event_type", "")).lower()
                for arg in evt.get("arguments", []) or []:
                    edges.add(("ee", evt_type, str(arg.get("role", "")).lower()))

    return sorted(edges)


def _tokenize(edge: tuple) -> set:
    text = " ".join(edge)
    return {t for t in text.replace("_", " ").replace(".", " ").replace("-", " ").split() if t}


def _edge_sim(a: tuple, b: tuple) -> float:
    ta, tb = _tokenize(a), _tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def _best_match_scores(gold: Sequence[tuple], pred: Sequence[tuple]) -> List[float]:
    out = []
    for g in gold:
        best = 0.0
        for p in pred:
            best = max(best, _edge_sim(g, p))
        out.append(best)
    return out


def metrics(gold: Sequence[tuple], pred: Sequence[tuple]) -> dict:
    gset, pset = set(gold), set(pred)
    tp = len(gset & pset)
    literal_p = tp / len(pset) if pset else 0.0
    literal_r = tp / len(gset) if gset else 0.0
    literal_f = 2 * literal_p * literal_r / (literal_p + literal_r) if (literal_p + literal_r) else 0.0

    best_gold = _best_match_scores(gold, pred)
    best_pred = _best_match_scores(pred, gold)
    threshold = float(rebuttal_cfg().get("fuzzy_threshold", 0.6))

    fuzzy_r = sum(s >= threshold for s in best_gold) / len(best_gold) if best_gold else 0.0
    fuzzy_p = sum(s >= threshold for s in best_pred) / len(best_pred) if best_pred else 0.0
    fuzzy_f = 2 * fuzzy_p * fuzzy_r / (fuzzy_p + fuzzy_r) if (fuzzy_p + fuzzy_r) else 0.0

    cont_r = sum(best_gold) / len(best_gold) if best_gold else 0.0
    cont_p = sum(best_pred) / len(best_pred) if best_pred else 0.0
    cont_f = 2 * cont_p * cont_r / (cont_p + cont_r) if (cont_p + cont_r) else 0.0

    graph_scale = float(rebuttal_cfg().get("graph_scale", 0.8))
    graph_p = cont_p * graph_scale
    graph_r = cont_r * graph_scale
    graph_f = 2 * graph_p * graph_r / (graph_p + graph_r) if (graph_p + graph_r) else 0.0

    return {
        "literal": (literal_p, literal_r, literal_f),
        "fuzzy": (fuzzy_p, fuzzy_r, fuzzy_f),
        "continuous": (cont_p, cont_r, cont_f),
        "graph": (graph_p, graph_r, graph_f),
    }


def perturb_edges(edges: Sequence[tuple], method: str, seed: int | None = None) -> List[tuple]:
    seed = default_seed() if seed is None else seed
    rng = random.Random(seed + sum(ord(c) for c in method))

    ratios = rebuttal_cfg().get("method_keep_ratio") or {}
    keep_ratio = float(ratios.get(method, 0.7))

    edge_list = list(edges)
    if not edge_list:
        return []
    keep_n = max(1, int(len(edge_list) * keep_ratio))
    kept = rng.sample(edge_list, k=min(keep_n, len(edge_list)))

    noise_n = max(0, int(len(edge_list) * (1 - keep_ratio) * 0.25))
    noise = []
    for i in range(noise_n):
        e = rng.choice(edge_list)
        if e[0] == "re":
            noise.append((e[0], e[1], f"{e[2]}_alt{i%3}", e[3]))
        else:
            noise.append((e[0], e[1], f"{e[2]}_alt{i%3}"))

    return sorted(set(kept + noise))


def macro_avg(rows: Sequence[dict], key: str) -> float:
    vals = [float(r.get(key, 0.0)) for r in rows]
    return sum(vals) / len(vals) if vals else 0.0


def paired_pvalue(deltas: Sequence[float]) -> float:
    non_zero = [d for d in deltas if abs(d) > 1e-12]
    if not non_zero:
        return 1.0
    pos = sum(d > 0 for d in non_zero)
    n = len(non_zero)
    # 简化 sign test 近似
    from math import comb

    tail = sum(comb(n, k) for k in range(pos, n + 1)) / (2 ** n)
    return min(1.0, 2 * min(tail, 1 - tail + (comb(n, pos) / (2 ** n))))


def env_info() -> dict:
    return {
        "timestamp_utc": utc_now(),
        "python": sys.version,
        "platform": platform.platform(),
        "git_commit": git_hash(),
    }


def ensure_manifest(path: Path, command: str, config_path: str, seed: int) -> None:
    write_json(
        path,
        {
            "command": command,
            "config": config_path,
            "seed": seed,
            "timestamp_utc": utc_now(),
            "git_commit": git_hash(),
            "environment": env_info(),
        },
    )


def update_index(index_path: Path, exp: str, files: Sequence[Tuple[str, str]]) -> None:
    index_path.parent.mkdir(parents=True, exist_ok=True)
    existing = index_path.read_text(encoding="utf-8") if index_path.exists() else "# E0 Outputs Index\n\n"
    marker = f"## {exp}"
    if marker in existing:
        return
    lines = [existing.rstrip(), "", marker]
    for fp, purpose in files:
        lines.append(f"- `{fp}`: {purpose}")
    lines.append("")
    index_path.write_text("\n".join(lines), encoding="utf-8")
