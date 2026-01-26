"""整合 RE/EE 公共数据集为 SCOPE 总库，并生成任务/子集后调用统计脚本。"""

from __future__ import annotations

import argparse
import logging
import math
import itertools
import random
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from utils.common import load_yaml_config, resolve_project_path, save_json
from utils.logger import get_ot_logger
from utils.summarize_scope_dataset import summarize_scope_dataset
from utils.scope_dataset_utils import (
    ScopeDoc,
    apply_tqdm_settings,
    build_schema_payload,
    doc_edge_keys,
    extract_ee_schema_edges,
    extract_re_schema_edges,
    hash_to_int,
    infer_ee_schema_from_samples,
    normalize_entity_type,
    parse_ee_samples,
    parse_re_samples,
    read_registry_from_config,
    safe_json_load,
    schema_edges_from_docs,
    schema_explosion_guard,
    schema_key_from_edge,
    split_by_hash,
    text_hash,
    wrap_tqdm,
    write_jsonl,
)


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


def _choose_by_ratio(key: str, ratio: float, seed: int) -> bool:
    if ratio <= 0:
        return False
    if ratio >= 1:
        return True
    value = hash_to_int(f"{seed}:{key}") / 2**128
    return value < ratio


def _select_mask_ratio(mask_ratios: Sequence[float], key: str, seed: int) -> Optional[float]:
    if not mask_ratios:
        return None
    if len(mask_ratios) == 1:
        return float(mask_ratios[0])
    idx = hash_to_int(f"{seed}:{key}") % len(mask_ratios)
    return float(list(mask_ratios)[idx])


def _derive_mask_seed(
    global_seed: int,
    seed_offset: int,
    task_id: str,
    case_id: str,
    mask_ratio: float,
) -> int:
    hash_value = hash_to_int(f"{task_id}:{case_id}:{mask_ratio}")
    return int(global_seed + seed_offset + (hash_value % 1000003))


def _select_cross_source_partner(
    source_dataset: str,
    task: str,
    language: str,
    dataset_schema: Dict[str, Dict[str, Any]],
) -> Optional[str]:
    candidates = [
        name
        for name, schema in dataset_schema.items()
        if schema.get("task") == task
        and schema.get("language") == language
        and name != source_dataset
    ]
    if not candidates:
        return None
    candidates = sorted(candidates)
    idx = hash_to_int(f"{source_dataset}:{task}:{language}") % len(candidates)
    return candidates[idx]


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

    schema_keys = [schema_key_from_edge(edge) for edge in schema_edges]
    remaining = set(schema_keys)
    selected: List[ScopeDoc] = []
    candidates = list(docs)
    rng.shuffle(candidates)
    while candidates and len(selected) < k:
        best_idx = None
        best_gain = -1
        for idx, doc in enumerate(candidates):
            gain = len(doc_edge_keys(doc) & remaining)
            if gain > best_gain:
                best_gain = gain
                best_idx = idx
        if best_idx is None:
            break
        doc = candidates.pop(best_idx)
        selected.append(doc)
        remaining -= doc_edge_keys(doc)
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


def _inject_noise_edges(
    schema_in: List[Dict[str, Any]],
    gold_full: List[Dict[str, Any]],
    global_schema: List[Dict[str, Any]],
    noise_ratio: float,
    seed: int,
) -> Tuple[List[Dict[str, Any]], int]:
    if noise_ratio <= 0 or not schema_in:
        return schema_in, 0
    gold_keys = {schema_key_from_edge(edge) for edge in gold_full}
    existing_keys = {schema_key_from_edge(edge) for edge in schema_in}
    candidates = [
        edge
        for edge in global_schema
        if schema_key_from_edge(edge) not in gold_keys
        and schema_key_from_edge(edge) not in existing_keys
    ]
    if not candidates:
        return schema_in, 0
    desired = int(math.ceil(len(schema_in) * noise_ratio))
    desired = min(desired, len(candidates))
    rng = random.Random(seed)
    rng.shuffle(candidates)
    noise_edges = candidates[:desired]
    return schema_in + noise_edges, len(noise_edges)


def _write_case_input(
    path: Path,
    task_id: str,
    case_id: str,
    texts_path: str,
    schema_in_path: Optional[str],
    schema_in_mode: str,
    schema_in_mask_ratio: Optional[float],
    schema_out_path: str,
) -> None:
    payload = {
        "task_id": task_id,
        "case_id": case_id,
        "texts_path": texts_path,
        "schema_in_path": schema_in_path,
        "schema_in_mode": schema_in_mode,
        "schema_in_mask_ratio": schema_in_mask_ratio,
        "schema_out_path": schema_out_path,
    }
    save_json(path, payload)


def _build_schema_in(
    base_schema_source: str,
    base_case_path: Path,
    gold_full: List[Dict[str, Any]],
    gold_reachable: List[Dict[str, Any]],
    mask_ratio: float,
    task_id: str,
    case_id: str,
    global_seed: int,
    seed_offset: int,
    scope_schema_full: List[Dict[str, Any]],
    inject_noise: bool,
    noise_edge_ratio: float,
) -> Tuple[List[Dict[str, Any]], int, str]:
    schema_in_source = base_schema_source
    mask_seed = _derive_mask_seed(global_seed, seed_offset, task_id, case_id, mask_ratio)
    if base_schema_source == "base_mask":
        base_mask_path = base_case_path / f"base_mask_{mask_ratio}.schema.json"
        if base_mask_path.exists():
            LOGGER.debug("使用 base_mask 作为 schema_in: case=%s ratio=%s", case_id, mask_ratio)
            schema_in = safe_json_load(base_mask_path)
            schema_in_source = "base_mask"
        else:
            LOGGER.warning("缺少 base_mask 文件，回退到 mask_full: %s", base_mask_path)
            schema_in_source = "mask_full"
            schema_in = _apply_fusion_mask(gold_full, mask_ratio, mask_seed)
    else:
        if base_schema_source not in {"mask_full", "mask_reachable"}:
            LOGGER.warning("未知 base_schema_source=%s，回退到 mask_full", base_schema_source)
            schema_in_source = "mask_full"
        base_edges = gold_reachable if schema_in_source == "mask_reachable" else gold_full
        schema_in = _apply_fusion_mask(base_edges, mask_ratio, mask_seed)
    noise_count = 0
    if inject_noise:
        schema_in, noise_count = _inject_noise_edges(
            schema_in,
            gold_full,
            scope_schema_full,
            noise_edge_ratio,
            mask_seed + 77,
        )
        LOGGER.debug("注入噪声边: case=%s count=%s", case_id, noise_count)
    return schema_in, noise_count, schema_in_source


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


def build_scope_dataset(config: Dict[str, Any], args: argparse.Namespace) -> None:
    scope_cfg = config.get("scope_dataset") or {}
    apply_tqdm_settings(scope_cfg)
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
    base_mask_ratios = (
        args.base_mask_ratios
        or scope_cfg.get("base_mask_ratios")
        or scope_cfg.get("fusion_mask_ratios", [0.3, 0.6])
    )
    enable_fusion = bool(args.enable_fusion if args.enable_fusion is not None else scope_cfg.get("enable_fusion", True))
    fusion_mode = str(args.fusion_mode or scope_cfg.get("fusion_mode", "paired")).lower()
    fusion_case_ratio = float(args.fusion_case_ratio or scope_cfg.get("fusion_case_ratio", 0.6))
    fusion_task_ratio = float(args.fusion_task_ratio or scope_cfg.get("fusion_task_ratio", 0.6))
    base_schema_source = str(args.base_schema_source or scope_cfg.get("base_schema_source", "base_mask")).lower()
    base_mask_seed_offset = int(args.base_mask_seed_offset or scope_cfg.get("base_mask_seed_offset", 10000))
    fusion_eval_target = str(args.fusion_eval_target or scope_cfg.get("fusion_eval_target", "full")).lower()
    inject_noise = bool(args.inject_noise if args.inject_noise is not None else scope_cfg.get("inject_noise", False))
    noise_edge_ratio = float(args.noise_edge_ratio or scope_cfg.get("noise_edge_ratio", 0.05))
    cross_source_cfg = scope_cfg.get("cross_source_fusion") or {}
    cross_source_enabled = bool(cross_source_cfg.get("enabled", True))
    cross_source_corpus_mode = str(cross_source_cfg.get("corpus_mode", "a")).lower()
    if fusion_mode not in {"paired", "ratio", "task_ratio"}:
        LOGGER.warning("未知 fusion_mode=%s，回退为 paired", fusion_mode)
        fusion_mode = "paired"
    enable_schema_explosion_guard = bool(
        args.schema_explosion_guard
        if args.schema_explosion_guard is not None
        else scope_cfg.get("schema_explosion_guard", True)
    )
    explosion_edge_threshold = int(
        args.explosion_edge_threshold or scope_cfg.get("explosion_edge_threshold", 200)
    )

    LOGGER.info("SCOPE 输出目录: %s", out_root)
    LOGGER.debug(
        "SCOPE 参数: dedup_by_text=%s cross_dataset_dedup=%s ratios=%s split_seed=%s",
        dedup_by_text,
        cross_dataset_dedup,
        ratios,
        split_seed,
    )
    LOGGER.debug(
        "Schema guard 配置: enable=%s edge_threshold=%s",
        enable_schema_explosion_guard,
        explosion_edge_threshold,
    )
    LOGGER.debug(
        "SCOPE case 配置: sizes=%s seeds=%s sampling=%s mask_ratios=%s",
        case_sizes,
        case_seeds,
        sampling_strategies,
        base_mask_ratios,
    )
    LOGGER.debug(
        "Fusion 配置: enable=%s mode=%s case_ratio=%s task_ratio=%s base_source=%s eval_target=%s inject_noise=%s",
        enable_fusion,
        fusion_mode,
        fusion_case_ratio,
        fusion_task_ratio,
        base_schema_source,
        fusion_eval_target,
        inject_noise,
    )
    LOGGER.debug(
        "Cross-source fusion 配置: enabled=%s corpus_mode=%s",
        cross_source_enabled,
        cross_source_corpus_mode,
    )
    out_root.mkdir(parents=True, exist_ok=True)
    failed_log = resolve_project_path(scope_cfg.get("failed_log", "logs/failed_datasets.txt"))
    failed_log.parent.mkdir(parents=True, exist_ok=True)
    failed_entries: List[str] = []

    registry = read_registry_from_config(config)
    dataset_docs: Dict[str, List[ScopeDoc]] = {}
    dataset_schema: Dict[str, Dict[str, Any]] = {}
    dataset_stats: Dict[str, Dict[str, Any]] = {}
    dataset_sample_counts: Dict[str, int] = {}
    explosion_guard_datasets: List[str] = []

    for entry in wrap_tqdm(registry, desc="解析数据集", total=len(registry)):
        LOGGER.info("处理数据集: %s (%s)", entry.name, entry.task)
        try:
            samples_payload = safe_json_load(entry.samples_output_path)
            if entry.task == "re":
                docs, sample_count, typed_flag = parse_re_samples(
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
                    schema_payload = safe_json_load(entry.schema_output_path)
                    rel_types, ent_types, rel_edges = extract_re_schema_edges(schema_payload)
                else:
                    LOGGER.warning("缺少 schema 文件，使用样本推断: %s", entry.schema_output_path)
                    rel_types, ent_types, rel_edges = schema_edges_from_docs(docs)
                if enable_schema_explosion_guard:
                    rel_edges, downgraded = schema_explosion_guard(
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
                docs, sample_count = parse_ee_samples(
                    samples_payload, entry.name, entry.language, dedup_by_text, cross_dataset_dedup
                )
                LOGGER.debug(
                    "EE 样本解析完成: dataset=%s docs=%s samples=%s",
                    entry.name,
                    len(docs),
                    sample_count,
                )
                if entry.schema_output_path.exists():
                    schema_payload = safe_json_load(entry.schema_output_path)
                    event_types, roles, edges = extract_ee_schema_edges(schema_payload)
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
        split_key = text_hash(doc.text)
        if not cross_dataset_dedup:
            split_key = f"{doc.source_dataset}::{split_key}"
        split = split_by_hash(split_key, ratios, split_seed)
        doc.global_split = split
        split_counter[split] += 1

    scope_dir = out_root / "SCOPE"
    scope_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(scope_dir / "docs.train.jsonl", (doc.to_json() for doc in all_docs if doc.global_split == "train"))
    write_jsonl(scope_dir / "docs.dev.jsonl", (doc.to_json() for doc in all_docs if doc.global_split == "dev"))
    write_jsonl(scope_dir / "docs.test.jsonl", (doc.to_json() for doc in all_docs if doc.global_split == "test"))

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
    scope_schema_full = build_schema_payload(all_re_edges, all_ee_edges)
    save_json(scope_dir / "schema_full.json", scope_schema_full)

    subset_dir = out_root / "subsets"
    tasks_dir = out_root / "tasks"
    cases_dir = out_root / "cases"
    subset_dir.mkdir(parents=True, exist_ok=True)
    tasks_dir.mkdir(parents=True, exist_ok=True)
    cases_dir.mkdir(parents=True, exist_ok=True)

    tasks: Dict[str, Dict[str, Any]] = {}
    manifest_rows: List[Dict[str, Any]] = []
    fusion_failed_cases: List[str] = []

    LOGGER.info("生成 subsets 与 tasks")
    for dataset_name, docs in wrap_tqdm(
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
        write_jsonl(
            subset_path / "docs.train.jsonl",
            (doc.to_json() for doc in subset_docs if doc.global_split == "train"),
        )
        write_jsonl(
            subset_path / "docs.dev.jsonl",
            (doc.to_json() for doc in subset_docs if doc.global_split == "dev"),
        )
        write_jsonl(
            subset_path / "docs.test.jsonl",
            (doc.to_json() for doc in subset_docs if doc.global_split == "test"),
        )

        if task == "re":
            schema_edges = schema.get("edges") or set()
            subset_schema_payload = build_schema_payload(schema_edges, set())
        else:
            subset_schema_payload = build_schema_payload(set(), schema.get("edges") or set())
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
    for task_id, info in wrap_tqdm(list(tasks.items()), desc="输出 tasks", total=len(tasks)):
        task_path = tasks_dir / task_id
        task_path.mkdir(parents=True, exist_ok=True)
        schema_payload = build_schema_payload(info["schema_re"], info["schema_ee"])
        save_json(task_path / "schema.json", schema_payload)
        task_docs = info["docs"]
        write_jsonl(
            task_path / "docs.train.jsonl",
            (doc.to_json() for doc in task_docs if doc.global_split == "train"),
        )
        write_jsonl(
            task_path / "docs.dev.jsonl",
            (doc.to_json() for doc in task_docs if doc.global_split == "dev"),
        )
        write_jsonl(
            task_path / "docs.test.jsonl",
            (doc.to_json() for doc in task_docs if doc.global_split == "test"),
        )
        LOGGER.debug("输出 task schema 完成: %s schema_edges=%s", task_id, len(schema_payload))

    if enable_fusion and fusion_mode == "task_ratio":
        fusion_task_seed = split_seed + base_mask_seed_offset
        fusion_task_ids = {
            task_id
            for task_id in tasks
            if _choose_by_ratio(task_id, fusion_task_ratio, fusion_task_seed)
        }
        LOGGER.debug(
            "Fusion task_ratio: 选中任务=%s/%s",
            len(fusion_task_ids),
            len(tasks),
        )
    else:
        fusion_task_ids = set()

    LOGGER.info("生成 cases 与 manifest")
    for task_id, info in wrap_tqdm(list(tasks.items()), desc="生成 cases", total=len(tasks)):
        task_docs = [doc for doc in info["docs"] if doc.global_split == "train"]
        schema_payload = build_schema_payload(info["schema_re"], info["schema_ee"])
        if not task_docs:
            continue
        source_datasets = {doc.source_dataset for doc in info["docs"]}
        task_type = None
        if info["schema_re"] and not info["schema_ee"]:
            task_type = "re"
        elif info["schema_ee"] and not info["schema_re"]:
            task_type = "ee"
        cross_source_base_payload: Optional[List[Dict[str, Any]]] = None
        cross_source_union_payload: Optional[List[Dict[str, Any]]] = None
        if cross_source_enabled and task_type and len(source_datasets) == 1:
            source_dataset = next(iter(source_datasets))
            cross_source_partner = _select_cross_source_partner(
                source_dataset,
                task_type,
                info["language"],
                dataset_schema,
            )
            if cross_source_partner:
                if cross_source_corpus_mode == "a+b":
                    LOGGER.debug("cross_source corpus_mode=a+b，当前仍使用任务 A 的训练语料")
                source_edges = dataset_schema[source_dataset].get("edges") or set()
                partner_edges = dataset_schema[cross_source_partner].get("edges") or set()
                if task_type == "re":
                    cross_source_base_payload = build_schema_payload(partner_edges, set())
                    cross_source_union_payload = build_schema_payload(source_edges | partner_edges, set())
                else:
                    cross_source_base_payload = build_schema_payload(set(), partner_edges)
                    cross_source_union_payload = build_schema_payload(set(), source_edges | partner_edges)
                LOGGER.debug(
                    "Cross-source fusion partner: task=%s source=%s partner=%s union_edges=%s",
                    task_id,
                    source_dataset,
                    cross_source_partner,
                    len(cross_source_union_payload),
                )
        LOGGER.debug(
            "case 任务准备: task=%s train_docs=%s schema_edges=%s",
            task_id,
            len(task_docs),
            len(schema_payload),
        )
        case_total = len(case_sizes) * len(case_seeds) * len(sampling_strategies)
        case_iter = itertools.product(case_sizes, case_seeds, sampling_strategies)
        for k, seed, sampling in wrap_tqdm(
            case_iter,
            desc=f"{task_id} cases",
            total=case_total,
        ):
            case_id = f"K{k}_seed{seed}_{sampling}"
            case_path = cases_dir / task_id / case_id
            case_path.mkdir(parents=True, exist_ok=True)
            try:
                induction_docs = _sample_docs_by_strategy(task_docs, schema_payload, k, seed, sampling)
                LOGGER.debug(
                    "生成 case: task=%s case=%s docs=%s",
                    task_id,
                    case_id,
                    len(induction_docs),
                )
                write_jsonl(
                    case_path / "induction_texts.jsonl",
                    ({"doc_id": doc.doc_id, "text": doc.text} for doc in induction_docs),
                )
                write_jsonl(case_path / "induction_docs.jsonl", (doc.to_json() for doc in induction_docs))
                reachable_edges = set()
                for doc in induction_docs:
                    reachable_edges |= doc_edge_keys(doc)
                gold_reachable = [edge for edge in schema_payload if schema_key_from_edge(edge) in reachable_edges]
                save_json(case_path / "gold_full.schema.json", schema_payload)
                save_json(case_path / "gold_reachable.schema.json", gold_reachable)

                base_edge_counts: Dict[float, int] = {}
                for ratio in base_mask_ratios:
                    masked = _apply_fusion_mask(gold_reachable, ratio, seed)
                    base_edge_counts[ratio] = len(masked)
                    save_json(case_path / f"base_mask_{ratio}.schema.json", masked)

                if cross_source_base_payload and cross_source_union_payload:
                    save_json(case_path / "base_cross_source.schema.json", cross_source_base_payload)
                    save_json(case_path / "gold_fusion_union.schema.json", cross_source_union_payload)

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
                    "doc_id_hash": text_hash("".join(doc.doc_id for doc in induction_docs)),
                }
                save_json(case_path / "stats.json", stats_payload)
                LOGGER.debug(
                    "case stats: task=%s case=%s reachable_ratio=%.4f masks=%s",
                    task_id,
                    case_id,
                    reachable_ratio,
                    base_edge_counts,
                )
            except Exception as exc:  # noqa: BLE001
                LOGGER.exception("case 生成失败: task=%s case=%s", task_id, case_id)
                fusion_failed_cases.append(f"{task_id}\t{case_id}\t{exc}")
                continue

            schema_out_filename = (
                "gold_reachable.schema.json" if fusion_eval_target == "reachable" else "gold_full.schema.json"
            )

            if enable_fusion:
                if fusion_mode == "ratio":
                    fuse_enabled = _choose_by_ratio(
                        f"{task_id}:{case_id}",
                        fusion_case_ratio,
                        split_seed + base_mask_seed_offset,
                    )
                elif fusion_mode == "task_ratio":
                    fuse_enabled = task_id in fusion_task_ids
                else:
                    fuse_enabled = False

                mask_ratio = _select_mask_ratio(
                    base_mask_ratios,
                    f"{task_id}:{case_id}",
                    split_seed + base_mask_seed_offset,
                )

                if fuse_enabled and mask_ratio is not None:
                    try:
                        schema_in, noise_count, schema_in_source = _build_schema_in(
                            base_schema_source,
                            case_path,
                            schema_payload,
                            gold_reachable,
                            mask_ratio,
                            task_id,
                            case_id,
                            split_seed,
                            base_mask_seed_offset,
                            scope_schema_full,
                            inject_noise,
                            noise_edge_ratio,
                        )

                        save_json(case_path / "schema_in.partial.json", schema_in)
                        _write_case_input(
                            case_path / "case_input.json",
                            task_id,
                            case_id,
                            "induction_texts.jsonl",
                            "schema_in.partial.json",
                            "fuse",
                            mask_ratio,
                            schema_out_filename,
                        )
                        manifest_rows.append(
                            {
                                "task_id": task_id,
                                "case_id": case_id,
                                "case_path": str(case_path),
                                "k": k,
                                "seed": seed,
                                "sampling": sampling,
                                "mode": "fuse",
                                "schema_in": str(case_path / "schema_in.partial.json"),
                                "schema_out": str(case_path / schema_out_filename),
                                "mask_ratio": mask_ratio,
                                "schema_in_source": schema_in_source,
                            }
                        )
                        LOGGER.debug(
                            "fusion case 输出: task=%s case=%s schema_in_edges=%s noise=%s",
                            task_id,
                            case_id,
                            len(schema_in),
                            noise_count,
                        )
                    except Exception as exc:  # noqa: BLE001
                        LOGGER.exception("fusion schema_in 生成失败: task=%s case=%s", task_id, case_id)
                        fusion_failed_cases.append(f"{task_id}\t{case_id}\t{exc}")
                        continue
                else:
                    _write_case_input(
                        case_path / "case_input.json",
                        task_id,
                        case_id,
                        "induction_texts.jsonl",
                        None,
                        "construct",
                        None,
                        schema_out_filename,
                    )
                    manifest_rows.append(
                        {
                            "task_id": task_id,
                            "case_id": case_id,
                            "case_path": str(case_path),
                            "k": k,
                            "seed": seed,
                            "sampling": sampling,
                            "mode": "construct",
                            "schema_in": None,
                            "schema_out": str(case_path / schema_out_filename),
                            "mask_ratio": None,
                        }
                    )
                    LOGGER.debug("construct case 输出: task=%s case=%s", task_id, case_id)
            else:
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

            if enable_fusion and fusion_mode == "paired":
                mask_ratio = _select_mask_ratio(
                    base_mask_ratios,
                    f"{task_id}:{case_id}:paired",
                    split_seed + base_mask_seed_offset,
                )
                if mask_ratio is None:
                    continue
                fuse_case_id = f"{case_id}__fuse_r{mask_ratio}"
                fuse_case_path = cases_dir / task_id / fuse_case_id
                fuse_case_path.mkdir(parents=True, exist_ok=True)
                try:
                    for filename in (
                        "induction_texts.jsonl",
                        "induction_docs.jsonl",
                        "gold_full.schema.json",
                        "gold_reachable.schema.json",
                        "stats.json",
                        "base_cross_source.schema.json",
                        "gold_fusion_union.schema.json",
                    ):
                        src = case_path / filename
                        if src.exists():
                            shutil.copy2(src, fuse_case_path / filename)
                    schema_in, noise_count, schema_in_source = _build_schema_in(
                        base_schema_source,
                        case_path,
                        schema_payload,
                        gold_reachable,
                        mask_ratio,
                        task_id,
                        fuse_case_id,
                        split_seed,
                        base_mask_seed_offset,
                        scope_schema_full,
                        inject_noise,
                        noise_edge_ratio,
                    )

                    save_json(fuse_case_path / "schema_in.partial.json", schema_in)
                    _write_case_input(
                        fuse_case_path / "case_input.json",
                        task_id,
                        fuse_case_id,
                        "induction_texts.jsonl",
                        "schema_in.partial.json",
                        "fuse",
                        mask_ratio,
                        schema_out_filename,
                    )
                    manifest_rows.append(
                        {
                            "task_id": task_id,
                            "case_id": fuse_case_id,
                            "case_path": str(fuse_case_path),
                            "k": k,
                            "seed": seed,
                            "sampling": sampling,
                            "mode": "fuse",
                            "schema_in": str(fuse_case_path / "schema_in.partial.json"),
                            "schema_out": str(fuse_case_path / schema_out_filename),
                            "mask_ratio": mask_ratio,
                            "schema_in_source": schema_in_source,
                        }
                    )
                    LOGGER.debug(
                        "paired fusion case 输出: task=%s case=%s schema_in_edges=%s noise=%s",
                        task_id,
                        fuse_case_id,
                        len(schema_in),
                        noise_count,
                    )
                except Exception as exc:  # noqa: BLE001
                    LOGGER.exception("paired fuse case 生成失败: task=%s case=%s", task_id, fuse_case_id)
                    fusion_failed_cases.append(f"{task_id}\t{fuse_case_id}\t{exc}")
                    continue

    write_jsonl(out_root / "manifest.jsonl", manifest_rows)
    if fusion_failed_cases:
        LOGGER.warning("Fusion case 失败数量: %s", len(fusion_failed_cases))

    LOGGER.info("调用统计脚本生成汇总信息")
    summarize_scope_dataset(config, args)
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
    parser.add_argument("--enable_fusion", type=_str2bool)
    parser.add_argument("--fusion_mode", type=str)
    parser.add_argument("--fusion_case_ratio", type=float)
    parser.add_argument("--fusion_task_ratio", type=float)
    parser.add_argument("--base_schema_source", type=str)
    parser.add_argument("--base_mask_ratios", nargs="*", type=float)
    parser.add_argument("--base_mask_seed_offset", type=int)
    parser.add_argument("--fusion_eval_target", type=str)
    parser.add_argument("--inject_noise", type=_str2bool)
    parser.add_argument("--noise_edge_ratio", type=float)
    parser.add_argument("--fusion_mask_ratios", nargs="*", type=float)
    parser.add_argument("--schema_explosion_guard", type=_str2bool)
    parser.add_argument("--explosion_edge_threshold", type=int)
    parser.add_argument("--symmetric_relations_file")
    return parser.parse_args()


def main() -> None:
    config = load_yaml_config()
    args = _parse_args()
    build_scope_dataset(config, args)


if __name__ == "__main__":
    main()
