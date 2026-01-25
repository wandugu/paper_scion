"""整合 RE/EE 公共数据集为 SCOPE 总库，并生成任务/子集/统计信息。"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import logging
import math
import itertools
import random
import statistics
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

import matplotlib
from tqdm import tqdm

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from utils.common import load_yaml_config, resolve_project_path, save_json
from utils.dataset_paths import resolve_dataset_paths
from utils.logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)

PLACEHOLDER_ENTITY_TYPES = {"entity", "na", "n/a", ""}

TQDM_SETTINGS: Dict[str, Any] = {
    "enabled": True,
    "mininterval": 0.1,
    "leave": False,
}

_MATPLOTLIB_PYPLOT = None


@dataclass
class DatasetEntry:
    name: str
    task: str
    language: str
    fmt: str
    schema_output_path: Path
    samples_output_path: Path
    data_files: List[str]
    schema_paths: List[str]


@dataclass
class ScopeDoc:
    doc_id: str
    text: str
    language: str
    source_dataset: str
    category: Optional[str]
    global_split: str
    relations: List[Dict[str, Any]]
    events: List[Dict[str, Any]]

    def to_json(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "text": self.text,
            "language": self.language,
            "source_dataset": self.source_dataset,
            "category": self.category,
            "global_split": self.global_split,
            "relations": self.relations,
            "events": self.events,
        }


def _apply_tqdm_settings(cfg: Dict[str, Any]) -> None:
    settings = cfg.get("tqdm") or {}
    TQDM_SETTINGS.update(
        {
            "enabled": bool(settings.get("enabled", TQDM_SETTINGS["enabled"])),
            "mininterval": float(settings.get("mininterval", TQDM_SETTINGS["mininterval"])),
            "leave": bool(settings.get("leave", TQDM_SETTINGS["leave"])),
        }
    )


def _wrap_tqdm(iterable: Iterable[Any], desc: str, total: int | None = None) -> Iterable[Any]:
    if not TQDM_SETTINGS.get("enabled", True):
        return iterable
    return tqdm(
        iterable,
        desc=desc,
        total=total,
        mininterval=TQDM_SETTINGS.get("mininterval", 0.1),
        leave=TQDM_SETTINGS.get("leave", False),
    )


def _get_matplotlib_pyplot(backend: str | None) -> Any:
    global _MATPLOTLIB_PYPLOT
    if _MATPLOTLIB_PYPLOT is None:
        if backend:
            matplotlib.use(backend)
        import matplotlib.pyplot as plt

        _MATPLOTLIB_PYPLOT = plt
    return _MATPLOTLIB_PYPLOT


def _safe_json_load(path: Path) -> Any:
    LOGGER.debug("读取 JSON: %s", path)
    return json.loads(path.read_text(encoding="utf-8"))


def _text_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def _split_by_hash(key: str, ratios: Sequence[float], seed: int) -> str:
    total = sum(ratios)
    if total <= 0:
        return "train"
    norm = [r / total for r in ratios]
    digest = hashlib.md5(f"{seed}:{key}".encode("utf-8")).hexdigest()
    value = int(digest, 16) / 2**128
    if value < norm[0]:
        return "train"
    if value < norm[0] + norm[1]:
        return "dev"
    return "test"


def _flatten_text_tokens(text: str) -> int:
    return len(text.strip().split())


def _write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        for record in records:
            fp.write(json.dumps(record, ensure_ascii=False) + "\n")


def _read_registry_from_config(config: Dict[str, Any]) -> List[DatasetEntry]:
    conv_cfg = config.get("dataset_conversion") or {}
    entries: List[DatasetEntry] = []
    for group_key in ("re", "ee"):
        group_cfg = conv_cfg.get(group_key) or {}
        for ds_cfg in group_cfg.get("dataset_configs", []) or []:
            if ds_cfg.get("enabled") is False:
                continue
            name = str(ds_cfg.get("name") or "").strip()
            if not name:
                continue
            task = str(ds_cfg.get("task") or group_key).lower()
            language = str(ds_cfg.get("language") or "zh").lower()
            fmt = str(ds_cfg.get("format") or "").lower()
            schema_path, samples_path = resolve_dataset_paths(config, name)
            data_files = [str(p) for p in ds_cfg.get("data_files", [])]
            schema_paths = []
            if ds_cfg.get("schema_path"):
                schema_paths.append(str(ds_cfg["schema_path"]))
            schema_paths.extend([str(p) for p in ds_cfg.get("schema_paths", [])])
            entries.append(
                DatasetEntry(
                    name=name,
                    task=task,
                    language=language,
                    fmt=fmt,
                    schema_output_path=schema_path,
                    samples_output_path=samples_path,
                    data_files=data_files,
                    schema_paths=schema_paths,
                )
            )
    LOGGER.debug("从配置加载数据集条目数量: %s", len(entries))
    return entries


def _normalize_entity_type(name: str | None) -> str:
    value = str(name or "").strip()
    if value.lower() in PLACEHOLDER_ENTITY_TYPES or not value:
        return "Entity"
    return value


def _merge_relations(existing: Dict[Tuple[str, str, str, str, str], Dict[str, Any]], relation: Dict[str, Any]) -> None:
    key = (
        relation["head"]["text"],
        relation["head"]["type"],
        relation["predicate"],
        relation["tail"]["text"],
        relation["tail"]["type"],
    )
    existing[key] = relation


def _merge_events(existing: Dict[Tuple[str, str, Tuple[Tuple[str, str], ...]], Dict[str, Any]], event: Dict[str, Any]) -> None:
    args = tuple(sorted((arg["role"], arg["text"]) for arg in event.get("arguments", [])))
    key = (event.get("event_type", ""), event.get("trigger", {}).get("text", ""), args)
    existing[key] = event


def _parse_re_samples(
    payload: Any,
    dataset_name: str,
    language: str,
    dedup_by_text: bool,
    cross_dataset_dedup: bool,
) -> Tuple[List[ScopeDoc], int, bool]:
    doc_map: Dict[str, Dict[str, Any]] = {}
    sample_count = 0
    typed_flag = True

    if not isinstance(payload, list):
        LOGGER.warning("RE 样本格式异常，跳过: %s", dataset_name)
        return [], 0, False

    for group in payload:
        if not isinstance(group, dict):
            continue
        group_head_type = group.get("head_entity_type")
        group_tail_type = group.get("tail_type") or group.get("tail_entity_type")
        for sample in group.get("samples", []) or []:
            if not isinstance(sample, dict):
                continue
            sample_count += 1
            text = str(sample.get("text") or sample.get("input") or "").strip()
            if not text:
                continue
            head_type = _normalize_entity_type(sample.get("head_entity_type") or group_head_type)
            tail_type = _normalize_entity_type(sample.get("tail_entity_type") or group_tail_type)
            if head_type == "Entity" or tail_type == "Entity":
                typed_flag = False
            doc_key_hash = _text_hash(text)
            if cross_dataset_dedup:
                doc_key = doc_key_hash
            elif dedup_by_text:
                doc_key = f"{dataset_name}::{language}::{doc_key_hash}"
            else:
                doc_key = f"{dataset_name}::{language}::{sample.get('id', doc_key_hash)}"
            doc_info = doc_map.setdefault(
                doc_key,
                {
                    "doc_id": f"{dataset_name}__{doc_key_hash}",
                    "text": text,
                    "language": language,
                    "source_dataset": dataset_name,
                    "categories": set(),
                    "relations": {},
                    "events": {},
                },
            )
            category = sample.get("category")
            if category:
                doc_info["categories"].add(str(category))
            relation = {
                "head": {"text": str(sample.get("head_entity") or ""), "type": head_type},
                "predicate": str(sample.get("relation") or sample.get("rel_type") or ""),
                "tail": {"text": str(sample.get("tail_entity") or ""), "type": tail_type},
            }
            _merge_relations(doc_info["relations"], relation)

    docs: List[ScopeDoc] = []
    for info in doc_map.values():
        categories = sorted(info["categories"])
        category = categories[0] if categories else None
        if len(categories) > 1:
            LOGGER.debug("RE 文档多分类，取首个: %s -> %s", info["doc_id"], categories)
        docs.append(
            ScopeDoc(
                doc_id=info["doc_id"],
                text=info["text"],
                language=info["language"],
                source_dataset=info["source_dataset"],
                category=category,
                global_split="",
                relations=list(info["relations"].values()),
                events=[],
            )
        )
    return docs, sample_count, typed_flag


def _parse_ee_samples(
    payload: Any,
    dataset_name: str,
    language: str,
    dedup_by_text: bool,
    cross_dataset_dedup: bool,
) -> Tuple[List[ScopeDoc], int]:
    doc_map: Dict[str, Dict[str, Any]] = {}
    sample_count = 0

    if not isinstance(payload, list):
        LOGGER.warning("EE 样本格式异常，跳过: %s", dataset_name)
        return [], 0

    for group in payload:
        if not isinstance(group, dict):
            continue
        group_event_type = group.get("event_type")
        for sample in group.get("samples", []) or []:
            if not isinstance(sample, dict):
                continue
            sample_count += 1
            text = str(sample.get("text") or sample.get("input") or "").strip()
            if not text:
                continue
            doc_key_hash = _text_hash(text)
            if cross_dataset_dedup:
                doc_key = doc_key_hash
            elif dedup_by_text:
                doc_key = f"{dataset_name}::{language}::{doc_key_hash}"
            else:
                doc_key = f"{dataset_name}::{language}::{sample.get('id', doc_key_hash)}"
            doc_info = doc_map.setdefault(
                doc_key,
                {
                    "doc_id": f"{dataset_name}__{doc_key_hash}",
                    "text": text,
                    "language": language,
                    "source_dataset": dataset_name,
                    "categories": set(),
                    "relations": {},
                    "events": {},
                },
            )
            event_type = str(sample.get("event_type") or group_event_type or "")
            trigger_text = str(sample.get("event_trigger") or sample.get("trigger") or "")
            arguments = []
            for arg in sample.get("arguments", []) or []:
                if not isinstance(arg, dict):
                    continue
                arguments.append(
                    {
                        "role": str(arg.get("role") or ""),
                        "text": str(arg.get("argument") or arg.get("text") or ""),
                    }
                )
            event = {
                "event_type": event_type,
                "trigger": {"text": trigger_text, "pos": sample.get("trigger_pos")},
                "arguments": arguments,
            }
            _merge_events(doc_info["events"], event)

    docs: List[ScopeDoc] = []
    for info in doc_map.values():
        categories = sorted(info["categories"])
        category = categories[0] if categories else None
        docs.append(
            ScopeDoc(
                doc_id=info["doc_id"],
                text=info["text"],
                language=info["language"],
                source_dataset=info["source_dataset"],
                category=category,
                global_split="",
                relations=[],
                events=list(info["events"].values()),
            )
        )
    return docs, sample_count


def _extract_ee_schema_edges(schema_payload: Dict[str, Any]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str]]]:
    event_types: Set[str] = set()
    roles: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()

    if isinstance(schema_payload.get("events"), list):
        for item in schema_payload.get("events", []):
            if not isinstance(item, dict):
                continue
            event_type = str(item.get("event_type") or "")
            if event_type:
                event_types.add(event_type)
            for role in item.get("roles", []) or []:
                role_name = str(role)
                if role_name:
                    roles.add(role_name)
                if event_type and role_name:
                    edges.add((event_type, role_name))

    mapping = schema_payload.get("event_type_roles") or schema_payload.get("event_type_role_map")
    if isinstance(mapping, dict):
        for event_type, role_list in mapping.items():
            event_type = str(event_type)
            event_types.add(event_type)
            for role in role_list or []:
                role_name = str(role)
                if role_name:
                    roles.add(role_name)
                if event_type and role_name:
                    edges.add((event_type, role_name))

    for event_type in schema_payload.get("event_types", []) or []:
        event_types.add(str(event_type))
    for role in schema_payload.get("roles", []) or []:
        roles.add(str(role))

    if isinstance(schema_payload.get("edges"), list):
        for item in schema_payload.get("edges", []):
            if not isinstance(item, dict):
                continue
            event_type = str(item.get("event_type") or item.get("head") or "")
            role = str(item.get("role") or item.get("tail") or "")
            if event_type:
                event_types.add(event_type)
            if role:
                roles.add(role)
            if event_type and role:
                edges.add((event_type, role))

    return event_types, roles, edges


def _infer_ee_schema_from_samples(docs: Sequence[ScopeDoc]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str]]]:
    event_types: Set[str] = set()
    roles: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()
    for doc in docs:
        for event in doc.events:
            event_type = str(event.get("event_type") or "")
            if event_type:
                event_types.add(event_type)
            for arg in event.get("arguments", []) or []:
                role = str(arg.get("role") or "")
                if role:
                    roles.add(role)
                if event_type and role:
                    edges.add((event_type, role))
    return event_types, roles, edges


def _extract_re_schema_edges(schema_payload: Dict[str, Any]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str, str]]]:
    rel_types: Set[str] = set()
    entity_types: Set[str] = set()
    edges: Set[Tuple[str, str, str]] = set()
    for item in schema_payload.get("relationships", []) or []:
        if not isinstance(item, dict):
            continue
        head = _normalize_entity_type(item.get("head_entity"))
        tail = _normalize_entity_type(item.get("tail_entity"))
        rel = str(item.get("rel_type") or "")
        if rel:
            rel_types.add(rel)
        entity_types.update([head, tail])
        if rel:
            edges.add((head, rel, tail))
    for ent in schema_payload.get("entities", []) or []:
        ent_name = _normalize_entity_type(ent)
        if ent_name:
            entity_types.add(ent_name)
    return rel_types, entity_types, edges


def _schema_edges_from_docs(docs: Sequence[ScopeDoc]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str, str]]]:
    rel_types: Set[str] = set()
    entity_types: Set[str] = set()
    edges: Set[Tuple[str, str, str]] = set()
    for doc in docs:
        for rel in doc.relations:
            rel_type = str(rel.get("predicate") or "")
            head_type = _normalize_entity_type(rel.get("head", {}).get("type"))
            tail_type = _normalize_entity_type(rel.get("tail", {}).get("type"))
            if rel_type:
                rel_types.add(rel_type)
            entity_types.update([head_type, tail_type])
            if rel_type:
                edges.add((head_type, rel_type, tail_type))
    return rel_types, entity_types, edges


def _schema_explosion_guard(
    entry: DatasetEntry,
    rel_edges: Set[Tuple[str, str, str]],
    docs: Sequence[ScopeDoc],
    threshold: int,
) -> Tuple[Set[Tuple[str, str, str]], bool]:
    if len(rel_edges) <= threshold:
        return rel_edges, False
    if entry.schema_paths:
        return rel_edges, False
    LOGGER.warning("触发 schema explosion guard: %s edges=%s", entry.name, len(rel_edges))
    rel_types = {rel.get("predicate") for doc in docs for rel in doc.relations if rel.get("predicate")}
    downgraded = {("Entity", rel_type, "Entity") for rel_type in rel_types}
    return downgraded, True


def _build_schema_payload(
    re_edges: Set[Tuple[str, str, str]],
    ee_edges: Set[Tuple[str, str]],
) -> List[Dict[str, Any]]:
    payload: List[Dict[str, Any]] = []
    for head, rel, tail in sorted(re_edges):
        payload.append(
            {
                "edge_kind": "re",
                "head_entity": head,
                "rel_type": rel,
                "tail_entity": tail,
            }
        )
    for event_type, role in sorted(ee_edges):
        payload.append(
            {
                "edge_kind": "ee",
                "event_type": event_type,
                "role": role,
            }
        )
    return payload


def _doc_edge_keys(doc: ScopeDoc) -> Set[Tuple[str, ...]]:
    edges: Set[Tuple[str, ...]] = set()
    for rel in doc.relations:
        edges.add(
            (
                "re",
                _normalize_entity_type(rel.get("head", {}).get("type")),
                str(rel.get("predicate") or ""),
                _normalize_entity_type(rel.get("tail", {}).get("type")),
            )
        )
    for event in doc.events:
        event_type = str(event.get("event_type") or "")
        for arg in event.get("arguments", []) or []:
            role = str(arg.get("role") or "")
            edges.add(("ee", event_type, role))
    return edges


def _schema_key_from_edge(edge: Dict[str, Any]) -> Tuple[str, ...]:
    if edge.get("edge_kind") == "ee":
        return ("ee", str(edge.get("event_type") or ""), str(edge.get("role") or ""))
    return (
        "re",
        _normalize_entity_type(edge.get("head_entity")),
        str(edge.get("rel_type") or ""),
        _normalize_entity_type(edge.get("tail_entity")),
    )


def _balanced_shards(items: List[str], sizes: Dict[str, int], shard_size: int) -> List[List[str]]:
    if not items:
        return []
    shard_count = max(1, math.ceil(len(items) / shard_size))
    shards: List[List[str]] = [[] for _ in range(shard_count)]
    shard_support = [0 for _ in range(shard_count)]
    for item in sorted(items, key=lambda name: sizes.get(name, 0), reverse=True):
        idx = shard_support.index(min(shard_support))
        shards[idx].append(item)
        shard_support[idx] += sizes.get(item, 0)
    return [shard for shard in shards if shard]


def _select_docs_by_rel_types(docs: Sequence[ScopeDoc], rel_types: Set[str]) -> List[ScopeDoc]:
    selected = []
    for doc in docs:
        if any(rel.get("predicate") in rel_types for rel in doc.relations):
            selected.append(doc)
    return selected


def _select_docs_by_event_types(docs: Sequence[ScopeDoc], event_types: Set[str]) -> List[ScopeDoc]:
    selected = []
    for doc in docs:
        if any(event.get("event_type") in event_types for event in doc.events):
            selected.append(doc)
    return selected


def _sample_docs_by_strategy(
    docs: Sequence[ScopeDoc],
    schema_edges: List[Dict[str, Any]],
    k: int,
    seed: int,
    strategy: str,
) -> List[ScopeDoc]:
    rng = random.Random(seed)
    if strategy == "random":
        return rng.sample(list(docs), k=min(k, len(docs)))

    schema_keys = [_schema_key_from_edge(edge) for edge in schema_edges]
    remaining = set(schema_keys)
    selected: List[ScopeDoc] = []
    candidates = list(docs)
    rng.shuffle(candidates)
    while candidates and len(selected) < k:
        best_idx = None
        best_gain = -1
        for idx, doc in enumerate(candidates):
            gain = len(_doc_edge_keys(doc) & remaining)
            if gain > best_gain:
                best_gain = gain
                best_idx = idx
        if best_idx is None:
            break
        doc = candidates.pop(best_idx)
        selected.append(doc)
        remaining -= _doc_edge_keys(doc)
        if not remaining:
            break
    if len(selected) < k and candidates:
        extra = candidates[: max(0, k - len(selected))]
        selected.extend(extra)
    return selected


def _apply_fusion_mask(
    reachable_edges: List[Dict[str, Any]],
    ratio: float,
    seed: int,
) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    if not reachable_edges:
        return []
    grouped: Dict[Tuple[str, str], List[Dict[str, Any]]] = defaultdict(list)
    for edge in reachable_edges:
        if edge.get("edge_kind") == "ee":
            key = ("ee", str(edge.get("event_type") or ""))
        else:
            key = ("re", str(edge.get("rel_type") or ""))
        grouped[key].append(edge)
    remaining = []
    for key, edges in grouped.items():
        keep_count = max(1, math.ceil(len(edges) * (1 - ratio)))
        rng.shuffle(edges)
        remaining.extend(edges[:keep_count])
    return remaining


def _write_csv(path: Path, header: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def _percentile(values: Sequence[float], p: float) -> float:
    if not values:
        return 0.0
    values_sorted = sorted(values)
    idx = int(math.ceil(p * len(values_sorted))) - 1
    idx = max(0, min(idx, len(values_sorted) - 1))
    return float(values_sorted[idx])


def _plot_schema_hist(
    path: Path,
    re_values: Sequence[int],
    ee_values: Sequence[int],
    backend: str | None,
) -> None:
    if not re_values and not ee_values:
        return
    plt = _get_matplotlib_pyplot(backend)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 4))
    if re_values:
        plt.hist(re_values, bins=min(30, max(5, len(set(re_values)))), alpha=0.7, label="RE")
    if ee_values:
        plt.hist(ee_values, bins=min(30, max(5, len(set(ee_values)))), alpha=0.7, label="EE")
    plt.title("Schema edges distribution")
    plt.xlabel("edges")
    plt.ylabel("count")
    plt.legend()
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _plot_scatter(
    path: Path, xs: Sequence[int], ys: Sequence[int], title: str, backend: str | None
) -> None:
    if not xs or not ys:
        return
    plt = _get_matplotlib_pyplot(backend)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 4))
    plt.scatter(xs, ys, alpha=0.6)
    plt.title(title)
    plt.xlabel("doc_count")
    plt.ylabel("schema_edges")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _plot_coverage_curve(
    path: Path,
    ks: Sequence[int],
    ratios: Sequence[float],
    title: str,
    backend: str | None,
) -> None:
    if not ks or not ratios:
        return
    plt = _get_matplotlib_pyplot(backend)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6, 4))
    plt.plot(ks, ratios, marker="o")
    plt.title(title)
    plt.xlabel("K")
    plt.ylabel("reachable_ratio")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def _collect_case_stats(
    stats_rows: List[List[Any]],
    task_id: str,
    case_id: str,
    k: int,
    seed: int,
    sampling: str,
    reachable_ratio: float,
    base_edge_counts: Dict[float, int],
) -> None:
    for ratio, edge_count in base_edge_counts.items():
        stats_rows.append(
            [
                task_id,
                case_id,
                k,
                seed,
                sampling,
                reachable_ratio,
                ratio,
                edge_count,
            ]
        )


def _build_summary_md(path: Path, summary_lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def build_scope_dataset(config: Dict[str, Any], args: argparse.Namespace) -> None:
    scope_cfg = config.get("scope_dataset") or {}
    _apply_tqdm_settings(scope_cfg)
    out_root = resolve_project_path(args.out_root or scope_cfg.get("out_root", "data/input/scope"))
    dedup_by_text = bool(args.dedup_by_text if args.dedup_by_text is not None else scope_cfg.get("dedup_by_text", True))
    cross_dataset_dedup = bool(
        args.cross_dataset_dedup if args.cross_dataset_dedup is not None else scope_cfg.get("cross_dataset_dedup", False)
    )
    ratios = args.global_split_ratios or scope_cfg.get("global_split_ratios", [0.8, 0.1, 0.1])
    split_seed = int(args.split_seed if args.split_seed is not None else scope_cfg.get("split_seed", 42))
    rel_shard_size = int(args.rel_shard_size or scope_cfg.get("rel_shard_size", 8))
    evt_shard_size = int(args.evt_shard_size or scope_cfg.get("evt_shard_size", 3))
    min_docs_per_type = int(args.min_docs_per_type or scope_cfg.get("min_docs_per_type", 200))
    make_category_subsets = bool(
        args.make_category_subsets if args.make_category_subsets is not None else scope_cfg.get("make_category_subsets", True)
    )
    category_min_docs = int(args.category_min_docs or scope_cfg.get("category_min_docs", 200))
    mix_pairs = int(args.mix_pairs or scope_cfg.get("mix_pairs", 200))
    mix_seed = int(args.mix_seed or scope_cfg.get("mix_seed", 7))
    case_sizes = args.case_sizes or scope_cfg.get("case_sizes", [200, 1000, 5000])
    case_seeds = args.case_seeds or scope_cfg.get("case_seeds", [1, 2, 3, 4, 5])
    sampling_strategies = args.sampling or scope_cfg.get("sampling", ["random", "coverage"])
    fusion_mask_ratios = args.fusion_mask_ratios or scope_cfg.get("fusion_mask_ratios", [0.3, 0.6])
    schema_explosion_guard = bool(
        args.schema_explosion_guard
        if args.schema_explosion_guard is not None
        else scope_cfg.get("schema_explosion_guard", True)
    )
    explosion_edge_threshold = int(
        args.explosion_edge_threshold or scope_cfg.get("explosion_edge_threshold", 200)
    )
    stats_cfg = scope_cfg.get("stats") or {}
    coverage_low_threshold = float(stats_cfg.get("coverage_low_threshold", 0.2))
    support_rare_threshold = int(stats_cfg.get("support_rare_threshold", 5))
    split_overlap_threshold = float(stats_cfg.get("split_overlap_threshold", 0.05))
    coverage_curve_ks = stats_cfg.get("coverage_curve_ks", [50, 100, 200, 500, 1000])
    matplotlib_backend = scope_cfg.get("matplotlib_backend")

    LOGGER.info("SCOPE 输出目录: %s", out_root)
    LOGGER.debug(
        "SCOPE 参数: dedup_by_text=%s cross_dataset_dedup=%s ratios=%s split_seed=%s",
        dedup_by_text,
        cross_dataset_dedup,
        ratios,
        split_seed,
    )
    LOGGER.debug(
        "SCOPE case 配置: sizes=%s seeds=%s sampling=%s mask_ratios=%s",
        case_sizes,
        case_seeds,
        sampling_strategies,
        fusion_mask_ratios,
    )
    out_root.mkdir(parents=True, exist_ok=True)
    failed_log = resolve_project_path(scope_cfg.get("failed_log", "logs/failed_datasets.txt"))
    failed_log.parent.mkdir(parents=True, exist_ok=True)
    failed_entries: List[str] = []

    registry = _read_registry_from_config(config)
    dataset_docs: Dict[str, List[ScopeDoc]] = {}
    dataset_schema: Dict[str, Dict[str, Any]] = {}
    dataset_stats: Dict[str, Dict[str, Any]] = {}
    dataset_sample_counts: Dict[str, int] = {}
    explosion_guard_datasets: List[str] = []

    for entry in _wrap_tqdm(registry, desc="解析数据集", total=len(registry)):
        LOGGER.info("处理数据集: %s (%s)", entry.name, entry.task)
        try:
            samples_payload = _safe_json_load(entry.samples_output_path)
            if entry.task == "re":
                docs, sample_count, typed_flag = _parse_re_samples(
                    samples_payload, entry.name, entry.language, dedup_by_text, cross_dataset_dedup
                )
                LOGGER.debug(
                    "RE 样本解析完成: dataset=%s docs=%s samples=%s typed_flag=%s",
                    entry.name,
                    len(docs),
                    sample_count,
                    typed_flag,
                )
                rel_types, ent_types, rel_edges = set(), set(), set()
                if entry.schema_output_path.exists():
                    schema_payload = _safe_json_load(entry.schema_output_path)
                    rel_types, ent_types, rel_edges = _extract_re_schema_edges(schema_payload)
                else:
                    LOGGER.warning("缺少 schema 文件，使用样本推断: %s", entry.schema_output_path)
                    rel_types, ent_types, rel_edges = _schema_edges_from_docs(docs)
                if schema_explosion_guard:
                    rel_edges, downgraded = _schema_explosion_guard(
                        entry, rel_edges, docs, explosion_edge_threshold
                    )
                    if downgraded:
                        explosion_guard_datasets.append(entry.name)
                        typed_flag = False
                LOGGER.debug(
                    "RE schema 汇总: dataset=%s rel_types=%s ent_types=%s edges=%s",
                    entry.name,
                    len(rel_types),
                    len(ent_types),
                    len(rel_edges),
                )
                dataset_schema[entry.name] = {
                    "task": "re",
                    "language": entry.language,
                    "rel_types": rel_types,
                    "entity_types": ent_types,
                    "edges": rel_edges,
                    "typed_flag": typed_flag,
                }
                dataset_docs[entry.name] = docs
                dataset_sample_counts[entry.name] = sample_count
            else:
                docs, sample_count = _parse_ee_samples(
                    samples_payload, entry.name, entry.language, dedup_by_text, cross_dataset_dedup
                )
                LOGGER.debug(
                    "EE 样本解析完成: dataset=%s docs=%s samples=%s",
                    entry.name,
                    len(docs),
                    sample_count,
                )
                if entry.schema_output_path.exists():
                    schema_payload = _safe_json_load(entry.schema_output_path)
                    event_types, roles, edges = _extract_ee_schema_edges(schema_payload)
                else:
                    LOGGER.warning("缺少 schema 文件，使用样本推断: %s", entry.schema_output_path)
                    event_types, roles, edges = _infer_ee_schema_from_samples(docs)
                LOGGER.debug(
                    "EE schema 汇总: dataset=%s event_types=%s roles=%s edges=%s",
                    entry.name,
                    len(event_types),
                    len(roles),
                    len(edges),
                )
                dataset_schema[entry.name] = {
                    "task": "ee",
                    "language": entry.language,
                    "event_types": event_types,
                    "roles": roles,
                    "edges": edges,
                    "typed_flag": True,
                }
                dataset_docs[entry.name] = docs
                dataset_sample_counts[entry.name] = sample_count
        except Exception as exc:  # noqa: BLE001
            LOGGER.exception("数据集处理失败: %s", entry.name)
            failed_entries.append(f"{entry.name}\t{exc}")
            continue

    if failed_entries:
        failed_log.write_text("\n".join(failed_entries) + "\n", encoding="utf-8")
        LOGGER.warning("失败数据集已写入: %s", failed_log)

    all_docs: List[ScopeDoc] = []
    for docs in dataset_docs.values():
        all_docs.extend(docs)

    LOGGER.info("SCOPE 总 doc 数: %s", len(all_docs))
    split_counter: Counter[str] = Counter()
    for doc in all_docs:
        split_key = _text_hash(doc.text)
        if not cross_dataset_dedup:
            split_key = f"{doc.source_dataset}::{split_key}"
        split = _split_by_hash(split_key, ratios, split_seed)
        doc.global_split = split
        split_counter[split] += 1

    scope_dir = out_root / "SCOPE"
    scope_dir.mkdir(parents=True, exist_ok=True)
    _write_jsonl(scope_dir / "docs.train.jsonl", (doc.to_json() for doc in all_docs if doc.global_split == "train"))
    _write_jsonl(scope_dir / "docs.dev.jsonl", (doc.to_json() for doc in all_docs if doc.global_split == "dev"))
    _write_jsonl(scope_dir / "docs.test.jsonl", (doc.to_json() for doc in all_docs if doc.global_split == "test"))

    registry_docs = {
        doc.doc_id: {
            "source_dataset": doc.source_dataset,
            "language": doc.language,
            "global_split": doc.global_split,
        }
        for doc in all_docs
    }
    save_json(scope_dir / "registry_docs.json", registry_docs)

    all_re_edges: Set[Tuple[str, str, str]] = set()
    all_ee_edges: Set[Tuple[str, str]] = set()
    for schema in dataset_schema.values():
        if schema.get("task") == "re":
            all_re_edges |= set(schema.get("edges") or [])
        else:
            all_ee_edges |= set(schema.get("edges") or [])
    save_json(scope_dir / "schema_full.json", _build_schema_payload(all_re_edges, all_ee_edges))

    subset_dir = out_root / "subsets"
    tasks_dir = out_root / "tasks"
    cases_dir = out_root / "cases"
    stats_dir = out_root / "stats"
    tables_dir = stats_dir / "tables"
    figs_dir = stats_dir / "figs"
    subset_dir.mkdir(parents=True, exist_ok=True)
    tasks_dir.mkdir(parents=True, exist_ok=True)
    cases_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)

    tasks: Dict[str, Dict[str, Any]] = {}
    task_stats_rows: List[List[Any]] = []
    case_stats_rows: List[List[Any]] = []
    manifest_rows: List[Dict[str, Any]] = []

    LOGGER.info("生成 subsets 与 tasks")
    for dataset_name, docs in _wrap_tqdm(
        list(dataset_docs.items()),
        desc="生成 subsets/tasks",
        total=len(dataset_docs),
    ):
        schema = dataset_schema.get(dataset_name) or {}
        task = schema.get("task")
        language = schema.get("language", "zh")
        subset_name = f"SCOPE_{task}_{language}_{dataset_name}"
        subset_path = subset_dir / subset_name
        subset_path.mkdir(parents=True, exist_ok=True)
        subset_docs = [doc for doc in docs]
        _write_jsonl(
            subset_path / "docs.train.jsonl",
            (doc.to_json() for doc in subset_docs if doc.global_split == "train"),
        )
        _write_jsonl(
            subset_path / "docs.dev.jsonl",
            (doc.to_json() for doc in subset_docs if doc.global_split == "dev"),
        )
        _write_jsonl(
            subset_path / "docs.test.jsonl",
            (doc.to_json() for doc in subset_docs if doc.global_split == "test"),
        )

        if task == "re":
            schema_edges = schema.get("edges") or set()
            subset_schema_payload = _build_schema_payload(schema_edges, set())
        else:
            subset_schema_payload = _build_schema_payload(set(), schema.get("edges") or set())
        save_json(subset_path / "schema.json", subset_schema_payload)

        if task == "re":
            rel_support = Counter()
            for doc in subset_docs:
                for rel in doc.relations:
                    rel_support[rel.get("predicate")] += 1
            rel_types = [rel for rel, count in rel_support.items() if count >= min_docs_per_type]
            shards = _balanced_shards(rel_types, rel_support, rel_shard_size)
            for idx, shard in enumerate(shards, start=1):
                shard_id = f"{subset_name}__relShard_{idx:03d}"
                shard_rel_types = set(shard)
                shard_docs = _select_docs_by_rel_types(subset_docs, shard_rel_types)
                shard_edges = {edge for edge in schema_edges if edge[1] in shard_rel_types}
                tasks[shard_id] = {
                    "docs": shard_docs,
                    "schema_re": shard_edges,
                    "schema_ee": set(),
                    "task_kind": "relShard",
                    "language": language,
                }

            if make_category_subsets:
                category_map: Dict[str, List[ScopeDoc]] = defaultdict(list)
                for doc in subset_docs:
                    if doc.category:
                        category_map[doc.category].append(doc)
                for category, cat_docs in category_map.items():
                    if len(cat_docs) < category_min_docs:
                        continue
                    cat_id = f"{subset_name}__cat_{category}"
                    cat_edges = {
                        edge for edge in schema_edges if edge[1] in {rel.get("predicate") for doc in cat_docs for rel in doc.relations}
                    }
                    tasks[cat_id] = {
                        "docs": cat_docs,
                        "schema_re": cat_edges,
                        "schema_ee": set(),
                        "task_kind": "cat",
                        "language": language,
                    }

        if task == "ee":
            evt_support = Counter()
            for doc in subset_docs:
                for event in doc.events:
                    evt_support[event.get("event_type")] += 1
            event_types = [evt for evt, count in evt_support.items() if count >= min_docs_per_type]
            shards = _balanced_shards(event_types, evt_support, evt_shard_size)
            for idx, shard in enumerate(shards, start=1):
                shard_id = f"{subset_name}__evtShard_{idx:03d}"
                shard_event_types = set(shard)
                shard_docs = _select_docs_by_event_types(subset_docs, shard_event_types)
                shard_edges = {edge for edge in (schema.get("edges") or set()) if edge[0] in shard_event_types}
                tasks[shard_id] = {
                    "docs": shard_docs,
                    "schema_re": set(),
                    "schema_ee": shard_edges,
                    "task_kind": "evtShard",
                    "language": language,
                }

    rel_tasks = {tid: info for tid, info in tasks.items() if info["task_kind"] == "relShard"}
    evt_tasks = {tid: info for tid, info in tasks.items() if info["task_kind"] == "evtShard"}
    rng_mix = random.Random(mix_seed)
    mix_candidates = [
        (rel_id, evt_id)
        for rel_id, rel_info in rel_tasks.items()
        for evt_id, evt_info in evt_tasks.items()
        if rel_info["language"] == evt_info["language"]
    ]
    rng_mix.shuffle(mix_candidates)
    for idx, (rel_id, evt_id) in enumerate(mix_candidates[:mix_pairs], start=1):
        rel_info = rel_tasks[rel_id]
        evt_info = evt_tasks[evt_id]
        language = rel_info["language"]
        mix_id = f"SCOPE_all_{language}__mix_rel{idx:03d}_evt{idx:03d}"
        mix_docs = list({doc.doc_id: doc for doc in rel_info["docs"] + evt_info["docs"]}.values())
        tasks[mix_id] = {
            "docs": mix_docs,
            "schema_re": rel_info["schema_re"],
            "schema_ee": evt_info["schema_ee"],
            "task_kind": "mix",
            "language": language,
        }

    LOGGER.info("任务总数: %s", len(tasks))
    for task_id, info in _wrap_tqdm(list(tasks.items()), desc="输出 tasks", total=len(tasks)):
        task_path = tasks_dir / task_id
        task_path.mkdir(parents=True, exist_ok=True)
        schema_payload = _build_schema_payload(info["schema_re"], info["schema_ee"])
        save_json(task_path / "schema.json", schema_payload)
        task_docs = info["docs"]
        _write_jsonl(
            task_path / "docs.train.jsonl",
            (doc.to_json() for doc in task_docs if doc.global_split == "train"),
        )
        _write_jsonl(
            task_path / "docs.dev.jsonl",
            (doc.to_json() for doc in task_docs if doc.global_split == "dev"),
        )
        _write_jsonl(
            task_path / "docs.test.jsonl",
            (doc.to_json() for doc in task_docs if doc.global_split == "test"),
        )
        docs_train = [doc for doc in task_docs if doc.global_split == "train"]
        typed_flag = any(edge[0] != "Entity" and edge[2] != "Entity" for edge in info["schema_re"]) if info["schema_re"] else False
        task_stats_rows.append(
            [
                task_id,
                info["task_kind"],
                len(docs_train),
                len(schema_payload),
                typed_flag,
            ]
        )

    LOGGER.info("生成 cases 与 manifest")
    for task_id, info in _wrap_tqdm(list(tasks.items()), desc="生成 cases", total=len(tasks)):
        task_docs = [doc for doc in info["docs"] if doc.global_split == "train"]
        schema_payload = _build_schema_payload(info["schema_re"], info["schema_ee"])
        if not task_docs:
            continue
        LOGGER.debug(
            "case 任务准备: task=%s train_docs=%s schema_edges=%s",
            task_id,
            len(task_docs),
            len(schema_payload),
        )
        case_total = len(case_sizes) * len(case_seeds) * len(sampling_strategies)
        case_iter = itertools.product(case_sizes, case_seeds, sampling_strategies)
        for k, seed, sampling in _wrap_tqdm(
            case_iter,
            desc=f"{task_id} cases",
            total=case_total,
        ):
            case_id = f"K{k}_seed{seed}_{sampling}"
            case_path = cases_dir / task_id / case_id
            case_path.mkdir(parents=True, exist_ok=True)
            induction_docs = _sample_docs_by_strategy(task_docs, schema_payload, k, seed, sampling)
            LOGGER.debug(
                "生成 case: task=%s case=%s docs=%s",
                task_id,
                case_id,
                len(induction_docs),
            )
            _write_jsonl(
                case_path / "induction_texts.jsonl",
                ({"doc_id": doc.doc_id, "text": doc.text} for doc in induction_docs),
            )
            _write_jsonl(case_path / "induction_docs.jsonl", (doc.to_json() for doc in induction_docs))
            reachable_edges = set()
            for doc in induction_docs:
                reachable_edges |= _doc_edge_keys(doc)
            gold_reachable = [edge for edge in schema_payload if _schema_key_from_edge(edge) in reachable_edges]
            save_json(case_path / "gold_full.schema.json", schema_payload)
            save_json(case_path / "gold_reachable.schema.json", gold_reachable)

            base_edge_counts: Dict[float, int] = {}
            for ratio in fusion_mask_ratios:
                masked = _apply_fusion_mask(gold_reachable, ratio, seed)
                base_edge_counts[ratio] = len(masked)
                save_json(case_path / f"base_mask_{ratio}.schema.json", masked)

            reachable_ratio = len(gold_reachable) / len(schema_payload) if schema_payload else 0.0
            stats_payload = {
                "task_id": task_id,
                "case_id": case_id,
                "k": k,
                "seed": seed,
                "sampling": sampling,
                "reachable_edges": len(gold_reachable),
                "reachable_ratio": reachable_ratio,
                "avg_length": statistics.mean(len(doc.text) for doc in induction_docs) if induction_docs else 0,
                "doc_id_hash": _text_hash("".join(doc.doc_id for doc in induction_docs)),
            }
            save_json(case_path / "stats.json", stats_payload)
            _collect_case_stats(
                case_stats_rows,
                task_id,
                case_id,
                k,
                seed,
                sampling,
                reachable_ratio,
                base_edge_counts,
            )
            manifest_rows.append(
                {
                    "task_id": task_id,
                    "case_id": case_id,
                    "case_path": str(case_path),
                    "k": k,
                    "seed": seed,
                    "sampling": sampling,
                }
            )

    _write_jsonl(out_root / "manifest.jsonl", manifest_rows)

    LOGGER.info("生成统计信息")
    schema_stats_rows: List[List[Any]] = []
    corpus_stats_rows: List[List[Any]] = []
    coverage_stats_rows: List[List[Any]] = []
    polysemy_stats_rows: List[List[Any]] = []

    schema_edges_counts_re: List[int] = []
    schema_edges_counts_ee: List[int] = []
    scatter_docs: List[int] = []
    scatter_edges: List[int] = []

    for dataset_name, docs in dataset_docs.items():
        schema = dataset_schema.get(dataset_name) or {}
        task = schema.get("task")
        language = schema.get("language")
        doc_count = len(docs)
        lengths = [len(doc.text) for doc in docs]
        token_lengths = [_flatten_text_tokens(doc.text) for doc in docs]
        avg_len = statistics.mean(lengths) if lengths else 0
        med_len = statistics.median(lengths) if lengths else 0
        p90_len = _percentile(lengths, 0.9)
        p99_len = _percentile(lengths, 0.99)
        sample_count = dataset_sample_counts.get(dataset_name, 0)
        dup_ratio = sample_count / doc_count if doc_count else 0

        if task == "re":
            rel_types = schema.get("rel_types") or set()
            ent_types = schema.get("entity_types") or set()
            edges = schema.get("edges") or set()
            typed_flag = bool(schema.get("typed_flag"))
            schema_edges_counts_re.append(len(edges))
            schema_stats_rows.append(
                [
                    dataset_name,
                    task,
                    language,
                    len(rel_types),
                    len(ent_types),
                    len(edges),
                    typed_flag,
                    sum(1 for t in ent_types if "/" in t) / len(ent_types) if ent_types else 0,
                ]
            )
            triples_per_doc = [len(doc.relations) for doc in docs]
            corpus_stats_rows.append(
                [
                    dataset_name,
                    task,
                    doc_count,
                    avg_len,
                    med_len,
                    p90_len,
                    p99_len,
                    statistics.mean(token_lengths) if token_lengths else 0,
                    statistics.mean(triples_per_doc) if triples_per_doc else 0,
                    "",
                    "",
                    dup_ratio,
                ]
            )
            edge_support = Counter()
            rel_domain_range = defaultdict(set)
            for doc in docs:
                for rel in doc.relations:
                    key = (
                        _normalize_entity_type(rel.get("head", {}).get("type")),
                        str(rel.get("predicate") or ""),
                        _normalize_entity_type(rel.get("tail", {}).get("type")),
                    )
                    edge_support[key] += 1
                    rel_domain_range[str(rel.get("predicate") or "")].add((key[0], key[2]))
            support_values = list(edge_support.values())
            if support_values:
                polysemy_counts = [len(domains) for domains in rel_domain_range.values()]
                polysemy_stats_rows.append(
                    [
                        dataset_name,
                        _percentile(polysemy_counts, 0.5),
                        _percentile(polysemy_counts, 0.9),
                        _percentile(polysemy_counts, 0.99),
                        sum(1 for count in polysemy_counts if count > 1) / len(polysemy_counts),
                        _percentile(support_values, 0.5),
                        _percentile(support_values, 0.9),
                        _percentile(support_values, 0.99),
                        sum(1 for v in support_values if v < support_rare_threshold) / len(support_values),
                    ]
                )
            else:
                polysemy_stats_rows.append([dataset_name, 0, 0, 0, 0, 0, 0, 0, 0])
            scatter_docs.append(doc_count)
            scatter_edges.append(len(edges))
        else:
            event_types = schema.get("event_types") or set()
            roles = schema.get("roles") or set()
            edges = schema.get("edges") or set()
            schema_edges_counts_ee.append(len(edges))
            schema_stats_rows.append(
                [
                    dataset_name,
                    task,
                    language,
                    len(event_types),
                    len(roles),
                    len(edges),
                    True,
                    "",
                ]
            )
            events_per_doc = [len(doc.events) for doc in docs]
            args_per_event = [
                len(event.get("arguments", [])) for doc in docs for event in doc.events
            ]
            corpus_stats_rows.append(
                [
                    dataset_name,
                    task,
                    doc_count,
                    avg_len,
                    med_len,
                    p90_len,
                    p99_len,
                    statistics.mean(token_lengths) if token_lengths else 0,
                    "",
                    statistics.mean(events_per_doc) if events_per_doc else 0,
                    statistics.mean(args_per_event) if args_per_event else 0,
                    dup_ratio,
                ]
            )
            scatter_docs.append(doc_count)
            scatter_edges.append(len(edges))

        reachable_edges = set()
        for doc in docs:
            if doc.global_split != "train":
                continue
            reachable_edges |= _doc_edge_keys(doc)
        if task == "re":
            schema_payload = _build_schema_payload(schema.get("edges") or set(), set())
        else:
            schema_payload = _build_schema_payload(set(), schema.get("edges") or set())
        schema_keys = {_schema_key_from_edge(edge) for edge in schema_payload}
        coverage_stats_rows.append(
            [
                dataset_name,
                len(schema_keys),
                len(schema_keys & reachable_edges),
                len(schema_keys & reachable_edges) / len(schema_keys) if schema_keys else 0,
            ]
        )

    _write_csv(
        tables_dir / "source_dataset_schema_stats.csv",
        ["dataset", "task", "language", "type_count_1", "type_count_2", "schema_edges", "typed_flag", "composite_ratio"],
        schema_stats_rows,
    )
    _write_csv(
        tables_dir / "source_dataset_corpus_stats.csv",
        [
            "dataset",
            "task",
            "doc_count",
            "avg_len",
            "median_len",
            "p90_len",
            "p99_len",
            "avg_tokens",
            "avg_triples_per_doc",
            "avg_events_per_doc",
            "avg_args_per_event",
            "dup_ratio",
        ],
        corpus_stats_rows,
    )
    _write_csv(
        tables_dir / "source_dataset_coverage_stats.csv",
        ["dataset", "schema_edges", "reachable_edges", "reachable_ratio"],
        coverage_stats_rows,
    )
    _write_csv(
        tables_dir / "extra_polysemy_support_stats.csv",
        [
            "dataset",
            "polysemy_p50",
            "polysemy_p90",
            "polysemy_p99",
            "polysemous_rel_ratio",
            "support_p50",
            "support_p90",
            "support_p99",
            "rare_edge_ratio",
        ],
        polysemy_stats_rows,
    )
    _write_csv(
        tables_dir / "task_stats.csv",
        ["task_id", "task_kind", "docs_train", "schema_edges", "typed_flag"],
        task_stats_rows,
    )
    _write_csv(
        tables_dir / "case_stats.csv",
        ["task_id", "case_id", "k", "seed", "sampling", "reachable_ratio", "mask_ratio", "edges_after_mask"],
        case_stats_rows,
    )

    overall_rows = [
        ["train", split_counter.get("train", 0)],
        ["dev", split_counter.get("dev", 0)],
        ["test", split_counter.get("test", 0)],
    ]
    _write_csv(tables_dir / "scope_overall_stats.csv", ["split", "doc_count"], overall_rows)

    _plot_schema_hist(
        figs_dir / "schema_edges_hist.png",
        schema_edges_counts_re,
        schema_edges_counts_ee,
        matplotlib_backend,
    )
    _plot_scatter(
        figs_dir / "corpus_vs_schema_scatter.png",
        scatter_docs,
        scatter_edges,
        "Corpus vs Schema",
        matplotlib_backend,
    )

    coverage_curve_lines: List[str] = []
    coverage_curve_dataset = None
    for dataset_name, docs in dataset_docs.items():
        if dataset_schema.get(dataset_name, {}).get("task") != "re":
            continue
        if len(docs) < max(coverage_curve_ks):
            continue
        coverage_curve_dataset = dataset_name
        schema_edges = dataset_schema[dataset_name].get("edges") or set()
        schema_payload = _build_schema_payload(schema_edges, set())
        ratios = []
        for k in coverage_curve_ks:
            sampled = _sample_docs_by_strategy(docs, schema_payload, k, split_seed, "coverage")
            reachable = set()
            for doc in sampled:
                reachable |= _doc_edge_keys(doc)
            schema_keys = {_schema_key_from_edge(edge) for edge in schema_payload}
            ratio = len(schema_keys & reachable) / len(schema_keys) if schema_keys else 0
            ratios.append(ratio)
        _plot_coverage_curve(
            figs_dir / "coverage_curve_example.png",
            coverage_curve_ks,
            ratios,
            f"Coverage curve ({dataset_name})",
            matplotlib_backend,
        )
        coverage_curve_lines.append(f"- {dataset_name}: {ratios}")
        break

    anomaly_lines = ["# SCOPE Anomaly Report", ""]
    if explosion_guard_datasets:
        anomaly_lines.append("## schema_explosion_guard 触发数据集")
        for name in explosion_guard_datasets:
            anomaly_lines.append(f"- {name}")
        anomaly_lines.append("")

    low_coverage = [
        row for row in coverage_stats_rows if row[3] < coverage_low_threshold
    ]
    if low_coverage:
        anomaly_lines.append("## reachable_ratio 过低的数据集")
        for dataset_name, _, _, ratio in low_coverage:
            anomaly_lines.append(f"- {dataset_name}: {ratio:.3f}")
        anomaly_lines.append("")

    split_overlap = []
    for dataset_name, docs in dataset_docs.items():
        train_hashes = {_text_hash(doc.text) for doc in docs if doc.global_split == "train"}
        test_hashes = {_text_hash(doc.text) for doc in docs if doc.global_split == "test"}
        if train_hashes and test_hashes:
            overlap = len(train_hashes & test_hashes) / len(train_hashes | test_hashes)
            if overlap > split_overlap_threshold:
                split_overlap.append((dataset_name, overlap))
    if split_overlap:
        anomaly_lines.append("## split overlap 警告")
        for name, overlap in split_overlap:
            anomaly_lines.append(f"- {name}: {overlap:.3f}")
        anomaly_lines.append("")

    _build_summary_md(stats_dir / "anomaly_report.md", anomaly_lines)

    total_docs = len(all_docs)
    re_only = sum(1 for doc in all_docs if doc.relations and not doc.events)
    ee_only = sum(1 for doc in all_docs if doc.events and not doc.relations)
    both = sum(1 for doc in all_docs if doc.relations and doc.events)
    summary_lines = [
        "# SCOPE Summary",
        "",
        f"- total_docs: {total_docs}",
        f"- split_train/dev/test: {split_counter.get('train', 0)}/{split_counter.get('dev', 0)}/{split_counter.get('test', 0)}",
        f"- RE-only docs: {re_only}",
        f"- EE-only docs: {ee_only}",
        f"- BOTH docs: {both}",
        f"- tasks total: {len(tasks)}",
        f"- rel_shards: {len(rel_tasks)}",
        f"- evt_shards: {len(evt_tasks)}",
        f"- mix tasks: {len([tid for tid, info in tasks.items() if info['task_kind'] == 'mix'])}",
    ]
    if coverage_curve_lines:
        summary_lines.append("")
        summary_lines.append("## Coverage curve samples")
        summary_lines.extend(coverage_curve_lines)
    _build_summary_md(stats_dir / "summary.md", summary_lines)

    LOGGER.info("SCOPE 构建完成，输出目录: %s", out_root)


def _str2bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    return str(value).lower() in {"1", "true", "yes", "y"}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build SCOPE dataset from converted RE/EE datasets.")
    parser.add_argument("--out_root")
    parser.add_argument("--dedup_by_text", type=_str2bool)
    parser.add_argument("--cross_dataset_dedup", type=_str2bool)
    parser.add_argument("--global_split_ratios", nargs=3, type=float)
    parser.add_argument("--split_seed", type=int)
    parser.add_argument("--rel_shard_size", type=int)
    parser.add_argument("--evt_shard_size", type=int)
    parser.add_argument("--min_docs_per_type", type=int)
    parser.add_argument("--make_category_subsets", type=_str2bool)
    parser.add_argument("--category_min_docs", type=int)
    parser.add_argument("--mix_pairs", type=int)
    parser.add_argument("--mix_seed", type=int)
    parser.add_argument("--case_sizes", nargs="*", type=int)
    parser.add_argument("--case_seeds", nargs="*", type=int)
    parser.add_argument("--sampling", nargs="*", type=str)
    parser.add_argument("--fusion_mask_ratios", nargs="*", type=float)
    parser.add_argument("--schema_explosion_guard", type=_str2bool)
    parser.add_argument("--explosion_edge_threshold", type=int)
    return parser.parse_args()


def main() -> None:
    config = load_yaml_config()
    args = _parse_args()
    build_scope_dataset(config, args)


if __name__ == "__main__":
    main()
