"""SCOPE 数据集统计与发布辅助。"""

from __future__ import annotations

import argparse
import json
import logging
import re
import statistics
import random
import importlib.util
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from utils.common import load_yaml_config, resolve_project_path
from utils.logger import get_ot_logger
from utils.scope_dataset_utils import (
    ScopeDoc,
    apply_tqdm_settings,
    build_schema_payload,
    doc_edge_keys,
    extract_ee_schema_edges,
    extract_re_schema_edges,
    flatten_text_tokens,
    infer_ee_schema_from_samples,
    normalize_entity_type,
    parse_ee_samples,
    parse_re_samples,
    percentile,
    read_registry_from_config,
    safe_json_load,
    schema_edges_from_docs,
    schema_explosion_guard,
    schema_key_from_edge,
    split_by_hash,
    text_hash,
    write_csv,
)


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)

NORMALIZATION_SPEC: Dict[str, Any] = {
    "RE": {
        "direction_policy": "directed",
        "symmetric_policy": "none",
        "missing_type_policy": "Entity",
        "type_path_policy": "keep_atomic",
        "label_for_embedding": "replace '/' -> ' '",
    },
    "EE": {
        "label_casing_en": "lower",
        "separator_policy": "collapse_whitespace + unify(_,-)",
        "edge_form": "(event_type, role, ARG)",
        "ARG_semantics": "placeholder",
    },
    "DEDUP": {
        "dedup_mode": "normalized",
        "normalize_text_en": "strip + collapse spaces (+ optional lowercase)",
        "normalize_text_zh": "strip + collapse spaces",
        "provenance_fields_kept": "source_sample_ids, source_groups, source_dataset",
    },
}


def _get_matplotlib_pyplot(backend: str | None) -> Any:
    if importlib.util.find_spec("matplotlib") is None:
        LOGGER.warning("matplotlib 未安装，跳过绘图输出")
        return None
    import matplotlib
    import matplotlib.pyplot as plt

    if backend:
        matplotlib.use(backend)
    return plt


def _plot_schema_hist(path: Path, re_counts: Sequence[int], ee_counts: Sequence[int], backend: str | None) -> None:
    if not re_counts and not ee_counts:
        return
    plt = _get_matplotlib_pyplot(backend)
    if plt is None:
        return
    plt.figure(figsize=(6, 4))
    if re_counts:
        plt.hist(re_counts, bins=30, alpha=0.6, label="RE")
    if ee_counts:
        plt.hist(ee_counts, bins=30, alpha=0.6, label="EE")
    plt.xlabel("#schema_edges")
    plt.ylabel("count")
    plt.legend()
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)
    plt.close()


def _plot_scatter(path: Path, docs: Sequence[int], edges: Sequence[int], title: str, backend: str | None) -> None:
    if not docs or not edges:
        return
    plt = _get_matplotlib_pyplot(backend)
    if plt is None:
        return
    plt.figure(figsize=(5, 4))
    plt.scatter(docs, edges, alpha=0.6)
    plt.xlabel("#docs")
    plt.ylabel("#schema_edges")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)
    plt.close()


def _plot_coverage_curve(path: Path, ks: Sequence[int], ratios: Sequence[float], title: str, backend: str | None) -> None:
    if not ks:
        return
    plt = _get_matplotlib_pyplot(backend)
    if plt is None:
        return
    plt.figure(figsize=(6, 4))
    plt.plot(ks, ratios, marker="o")
    plt.title(title)
    plt.xlabel("K")
    plt.ylabel("reachable_ratio")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path)
    plt.close()


def _build_summary_md(path: Path, summary_lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


def _render_spec_table(title: str, spec: Dict[str, Any]) -> List[str]:
    lines = [f"## {title}", "", "| Key | Value |", "| --- | --- |"]
    for key, value in spec.items():
        lines.append(f"| {key} | {value} |")
    lines.append("")
    return lines


def _write_normalization_docs(stats_dir: Path, symmetric_relations: Set[str]) -> None:
    normalization_lines = ["# Schema Normalization Spec", ""]
    re_spec = dict(NORMALIZATION_SPEC["RE"])
    re_spec["symmetric_policy"] = "list" if symmetric_relations else "none"
    normalization_lines.extend(_render_spec_table("RE", re_spec))
    normalization_lines.extend(_render_spec_table("EE", NORMALIZATION_SPEC["EE"]))
    stats_dir.mkdir(parents=True, exist_ok=True)
    (stats_dir / "schema_normalization.md").write_text("\n".join(normalization_lines) + "\n", encoding="utf-8")

    dedup_lines = ["# Dedup Policy", ""]
    dedup_lines.extend(_render_spec_table("DEDUP", NORMALIZATION_SPEC["DEDUP"]))
    (stats_dir / "dedup_policy.md").write_text("\n".join(dedup_lines) + "\n", encoding="utf-8")


def _normalize_re_edge(
    head_type: str,
    rel_type: str,
    tail_type: str,
    symmetric_relations: Set[str],
) -> Tuple[str, str, str]:
    head = normalize_entity_type(head_type)
    tail = normalize_entity_type(tail_type)
    rel = str(rel_type or "")
    if rel in symmetric_relations and head > tail:
        head, tail = tail, head
    return head, rel, tail


def _canonicalize_edge_key(
    edge_key: Tuple[str, ...],
    symmetric_relations: Set[str],
) -> Tuple[str, ...]:
    if not edge_key or edge_key[0] != "re" or len(edge_key) != 4:
        return edge_key
    _, head, rel, tail = edge_key
    if rel in symmetric_relations and head > tail:
        return ("re", tail, rel, head)
    return edge_key


def _load_symmetric_relations(path: Optional[str]) -> Set[str]:
    if not path:
        return set()
    file_path = Path(path)
    if not file_path.exists():
        LOGGER.warning("未找到对称关系文件: %s", file_path)
        return set()
    relations = {
        line.strip()
        for line in file_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    LOGGER.debug("对称关系加载数量: %s", len(relations))
    return relations


def _has_illegal_char(text: str) -> bool:
    return any((not ch.isprintable() and not ch.isspace()) for ch in text)


def _validate_docs(
    dataset_name: str,
    docs: Sequence[ScopeDoc],
    schema_edges: Sequence[Tuple[str, ...]],
    symmetric_relations: Set[str],
    validation_log: Path,
) -> List[str]:
    warnings: List[str] = []
    empty_text_count = sum(1 for doc in docs if not doc.text.strip())
    if empty_text_count:
        warnings.append(f"{dataset_name}: empty_text={empty_text_count}")

    illegal_text_count = sum(1 for doc in docs if _has_illegal_char(doc.text))
    if illegal_text_count:
        warnings.append(f"{dataset_name}: illegal_text={illegal_text_count}")

    empty_label_count = 0
    dup_edge_count = 0
    for doc in docs:
        rel_labels = [str(rel.get("predicate") or "") for rel in doc.relations]
        empty_label_count += sum(1 for label in rel_labels if not label.strip())
        for event in doc.events:
            if not str(event.get("event_type") or "").strip():
                empty_label_count += 1
            for arg in event.get("arguments", []) or []:
                if not str(arg.get("role") or "").strip():
                    empty_label_count += 1

        edge_keys = [
            _canonicalize_edge_key(edge, symmetric_relations)
            for edge in doc_edge_keys(doc)
        ]
        if len(edge_keys) != len(set(edge_keys)):
            dup_edge_count += 1

    if empty_label_count:
        warnings.append(f"{dataset_name}: empty_label={empty_label_count}")
    if dup_edge_count:
        warnings.append(f"{dataset_name}: duplicate_edges={dup_edge_count}")

    if not schema_edges:
        warnings.append(f"{dataset_name}: schema_edges=0")

    with validation_log.open("a", encoding="utf-8") as fp:
        for warning in warnings:
            fp.write(warning + "\n")
    return warnings


def _write_dataset_card(
    path: Path,
    title: str,
    language: str,
    task: str,
    doc_count: int,
    schema_edges: int,
    typed_flag: bool,
    eval_script: Optional[str],
) -> None:
    lines = [f"# {title}", "", "## Metadata", ""]
    lines.extend(
        [
            f"- language: {language}",
            f"- task: {task}",
            f"- #docs_dedup: {doc_count}",
            f"- #schema_edges: {schema_edges}",
            f"- typed_flag: {typed_flag}",
        ]
    )
    lines.extend(
        [
            "",
            "## Limitations",
            "- 未标注实体类型的关系统一使用 Entity 占位。",
            "- EE 任务 role 不包含实体 typing。",
            "- Fusion Track 定义：Track-1 单源归纳；Track-2 partial schema completion；Track-3 多源 fusion。",
        ]
    )
    lines.append("")
    lines.append("## Evaluation")
    if eval_script:
        lines.append(f"- 评测脚本: `{eval_script}`")
    else:
        lines.append("- 评测脚本: TODO（暂无 evaluate.py）")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _normalize_re_edge_for_stats(
    edge: Tuple[str, str, str],
    symmetric_relations: Set[str],
) -> Tuple[str, str, str]:
    head, rel, tail = edge
    return _normalize_re_edge(head, rel, tail, symmetric_relations)


def summarize_scope_dataset(config: Dict[str, Any], args: argparse.Namespace) -> None:
    scope_cfg = config.get("scope_dataset") or {}
    apply_tqdm_settings(scope_cfg)
    out_root = resolve_project_path(args.out_root or scope_cfg.get("out_root", "data/input/scope"))
    dedup_by_text = bool(args.dedup_by_text if args.dedup_by_text is not None else scope_cfg.get("dedup_by_text", True))
    cross_dataset_dedup = bool(
        args.cross_dataset_dedup if args.cross_dataset_dedup is not None else scope_cfg.get("cross_dataset_dedup", False)
    )
    ratios = args.global_split_ratios or scope_cfg.get("global_split_ratios", [0.8, 0.1, 0.1])
    split_seed = int(args.split_seed if args.split_seed is not None else scope_cfg.get("split_seed", 42))
    min_docs_per_type = int(args.min_docs_per_type or scope_cfg.get("min_docs_per_type", 200))
    schema_explosion_guard_enabled = bool(
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
    symmetric_relations_file = args.symmetric_relations_file or scope_cfg.get("symmetric_relations_file")
    symmetric_relations = _load_symmetric_relations(symmetric_relations_file)

    LOGGER.info("SCOPE 统计输出目录: %s", out_root)
    LOGGER.debug("统计参数: dedup_by_text=%s cross_dataset_dedup=%s split_seed=%s", dedup_by_text, cross_dataset_dedup, split_seed)

    stats_dir = out_root / "stats"
    tables_dir = stats_dir / "tables"
    figs_dir = stats_dir / "figs"
    logs_dir = out_root / "logs"
    dataset_cards_dir = out_root / "dataset_cards"
    stats_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    figs_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    dataset_cards_dir.mkdir(parents=True, exist_ok=True)

    validation_log = logs_dir / "validation_warnings.log"
    if validation_log.exists():
        validation_log.unlink()

    _write_normalization_docs(stats_dir, symmetric_relations)

    registry = read_registry_from_config(config)
    dataset_docs: Dict[str, List[ScopeDoc]] = {}
    dataset_schema: Dict[str, Dict[str, Any]] = {}
    dataset_sample_counts: Dict[str, int] = {}
    explosion_guard_datasets: List[str] = []

    for entry in wrap_tqdm(registry, desc="解析数据集", total=len(registry)):
        LOGGER.info("统计处理数据集: %s (%s)", entry.name, entry.task)
        try:
            samples_payload = safe_json_load(entry.samples_output_path)
            if entry.task == "re":
                docs, sample_count, typed_flag = parse_re_samples(
                    samples_payload, entry.name, entry.language, dedup_by_text, cross_dataset_dedup
                )
                rel_types, ent_types, rel_edges = set(), set(), set()
                if entry.schema_output_path.exists():
                    schema_payload = safe_json_load(entry.schema_output_path)
                    rel_types, ent_types, rel_edges = extract_re_schema_edges(schema_payload)
                else:
                    LOGGER.warning("缺少 schema 文件，使用样本推断: %s", entry.schema_output_path)
                    rel_types, ent_types, rel_edges = schema_edges_from_docs(docs)
                if schema_explosion_guard_enabled:
                    rel_edges, downgraded = schema_explosion_guard(
                        entry, rel_edges, docs, explosion_edge_threshold
                    )
                    if downgraded:
                        explosion_guard_datasets.append(entry.name)
                        typed_flag = False
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
                if entry.schema_output_path.exists():
                    schema_payload = safe_json_load(entry.schema_output_path)
                    event_types, roles, edges = extract_ee_schema_edges(schema_payload)
                else:
                    LOGGER.warning("缺少 schema 文件，使用样本推断: %s", entry.schema_output_path)
                    event_types, roles, edges = infer_ee_schema_from_samples(docs)
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
            LOGGER.exception("统计数据集处理失败: %s", entry.name)
            with validation_log.open("a", encoding="utf-8") as fp:
                fp.write(f"{entry.name}: exception={exc}\n")
            continue

    all_docs: List[ScopeDoc] = []
    split_counter: Counter[str] = Counter()
    for docs in dataset_docs.values():
        all_docs.extend(docs)
    for doc in all_docs:
        split_key = text_hash(doc.text)
        if not cross_dataset_dedup:
            split_key = f"{doc.source_dataset}::{split_key}"
        split = split_by_hash(split_key, ratios, split_seed)
        doc.global_split = split
        split_counter[split] += 1

    schema_stats_rows: List[List[Any]] = []
    corpus_stats_rows: List[List[Any]] = []
    coverage_stats_rows: List[List[Any]] = []
    polysemy_stats_rows: List[List[Any]] = []

    schema_edges_counts_re: List[int] = []
    schema_edges_counts_ee: List[int] = []
    scatter_docs: List[int] = []
    scatter_edges: List[int] = []

    validation_warnings: List[str] = []

    for dataset_name, docs in dataset_docs.items():
        schema = dataset_schema.get(dataset_name) or {}
        task = schema.get("task")
        language = schema.get("language")
        doc_count = len(docs)
        lengths = [len(doc.text) for doc in docs]
        token_lengths = [flatten_text_tokens(doc.text) for doc in docs]
        avg_len = statistics.mean(lengths) if lengths else 0
        med_len = statistics.median(lengths) if lengths else 0
        p90_len = percentile(lengths, 0.9)
        p99_len = percentile(lengths, 0.99)
        sample_count = dataset_sample_counts.get(dataset_name, 0)
        dup_ratio = sample_count / doc_count if doc_count else 0

        validation_warnings.extend(
            _validate_docs(
                dataset_name,
                docs,
                schema.get("edges") or set(),
                symmetric_relations,
                validation_log,
            )
        )
        if sample_count and doc_count and sample_count != doc_count:
            warning = f"{dataset_name}: dedup_docs {sample_count} -> {doc_count}"
            validation_warnings.append(warning)
            with validation_log.open("a", encoding="utf-8") as fp:
                fp.write(warning + "\n")

        if task == "re":
            rel_types = schema.get("rel_types") or set()
            ent_types = schema.get("entity_types") or set()
            edges = schema.get("edges") or set()
            typed_flag = bool(schema.get("typed_flag"))
            normalized_edges = {
                _normalize_re_edge_for_stats(edge, symmetric_relations) for edge in edges
            }
            symmetric_rel_count = sum(1 for edge in normalized_edges if edge[1] in symmetric_relations)
            rel_labels = {edge[1] for edge in normalized_edges}
            typed_edges = normalized_edges
            core_typed_edges = typed_edges
            if edges:
                types_in_edges = {head for head, _, _ in edges} | {tail for _, _, tail in edges}
                isolated_types = sorted(ent_types - types_in_edges)
                if isolated_types:
                    warning = f"{dataset_name}: isolated_types={len(isolated_types)}"
                    validation_warnings.append(warning)
                    with validation_log.open("a", encoding="utf-8") as fp:
                        fp.write(warning + "\n")

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
                    len(rel_labels),
                    len(typed_edges),
                    len(core_typed_edges),
                    symmetric_rel_count,
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

            edge_support: Counter[Tuple[str, str, str]] = Counter()
            rel_domain_range: Dict[str, Set[Tuple[str, str]]] = defaultdict(set)
            for doc in docs:
                doc_edge_set: Set[Tuple[str, str, str]] = set()
                for rel in doc.relations:
                    key = _normalize_re_edge(
                        rel.get("head", {}).get("type"),
                        rel.get("predicate"),
                        rel.get("tail", {}).get("type"),
                        symmetric_relations,
                    )
                    if not key[1]:
                        continue
                    doc_edge_set.add(key)
                for key in doc_edge_set:
                    edge_support[key] += 1
                    rel_domain_range[key[1]].add((key[0], key[2]))

            support_values = list(edge_support.values())
            if support_values:
                pairs_per_rel = [len(domains) for domains in rel_domain_range.values()]
                polysemy_stats_rows.append(
                    [
                        dataset_name,
                        sum(1 for count in pairs_per_rel if count > 1) / len(pairs_per_rel)
                        if pairs_per_rel
                        else 0,
                        statistics.mean(pairs_per_rel) if pairs_per_rel else 0,
                        max(pairs_per_rel) if pairs_per_rel else 0,
                        percentile(support_values, 0.5),
                        percentile(support_values, 0.9),
                        percentile(support_values, 0.99),
                        max(support_values),
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
                    "",
                    "",
                    "",
                    "",
                ]
            )
            events_per_doc = [len(doc.events) for doc in docs]
            args_per_event = [len(event.get("arguments", [])) for doc in docs for event in doc.events]
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
            for edge_key in doc_edge_keys(doc):
                reachable_edges.add(_canonicalize_edge_key(edge_key, symmetric_relations))

        if task == "re":
            schema_payload = build_schema_payload(schema.get("edges") or set(), set())
        else:
            schema_payload = build_schema_payload(set(), schema.get("edges") or set())
        schema_keys = {
            _canonicalize_edge_key(schema_key_from_edge(edge), symmetric_relations) for edge in schema_payload
        }
        coverage_stats_rows.append(
            [
                dataset_name,
                len(schema_keys),
                len(schema_keys & reachable_edges),
                len(schema_keys & reachable_edges) / len(schema_keys) if schema_keys else 0,
            ]
        )

    write_csv(
        tables_dir / "source_dataset_schema_stats.csv",
        [
            "dataset",
            "task",
            "language",
            "type_count_1",
            "type_count_2",
            "schema_edges",
            "typed_flag",
            "composite_ratio",
            "RelLabels",
            "TypedEdges",
            "CoreTypedEdges",
            "symmetric_rel_count",
        ],
        schema_stats_rows,
    )
    write_csv(
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
    write_csv(
        tables_dir / "source_dataset_coverage_stats.csv",
        ["dataset", "schema_edges", "reachable_edges", "reachable_ratio"],
        coverage_stats_rows,
    )
    write_csv(
        tables_dir / "extra_polysemy_support_stats.csv",
        [
            "dataset",
            "polysemous_rel_ratio",
            "avg_pairs_per_rel",
            "max_pairs_per_rel",
            "support_p50",
            "support_p90",
            "support_p99",
            "support_max",
            "rare_edge_ratio",
        ],
        polysemy_stats_rows,
    )

    cases_dir = out_root / "cases"
    case_stats_rows: List[List[Any]] = []
    fusion_case_rows: List[List[Any]] = []
    if cases_dir.exists():
        for stats_path in cases_dir.glob("**/stats.json"):
            stats_payload = safe_json_load(stats_path)
            case_dir = stats_path.parent
            task_id = stats_payload.get("task_id") or case_dir.parent.name
            case_id = stats_payload.get("case_id") or case_dir.name
            reachable_ratio = stats_payload.get("reachable_ratio", 0)
            k = stats_payload.get("k")
            seed = stats_payload.get("seed")
            sampling = stats_payload.get("sampling")
            for mask_file in case_dir.glob("base_mask_*.schema.json"):
                match = re.search(r"base_mask_(.+)\.schema\.json", mask_file.name)
                mask_ratio = float(match.group(1)) if match else None
                edges_after_mask = len(safe_json_load(mask_file))
                case_stats_rows.append(
                    [
                        task_id,
                        case_id,
                        k,
                        seed,
                        sampling,
                        reachable_ratio,
                        mask_ratio,
                        edges_after_mask,
                        "masked",
                    ]
                )
            cross_source_path = case_dir / "base_cross_source.schema.json"
            if cross_source_path.exists():
                edges_after_mask = len(safe_json_load(cross_source_path))
                case_stats_rows.append(
                    [
                        task_id,
                        case_id,
                        k,
                        seed,
                        sampling,
                        reachable_ratio,
                        None,
                        edges_after_mask,
                        "cross_source",
                    ]
                )

        manifest_path = out_root / "manifest.jsonl"
        if manifest_path.exists():
            for line in manifest_path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("mode") != "fuse":
                    continue
                schema_in_path = row.get("schema_in")
                schema_out_path = row.get("schema_out")
                if not schema_in_path or not schema_out_path:
                    continue
                schema_in = safe_json_load(Path(schema_in_path))
                schema_out = safe_json_load(Path(schema_out_path))
                schema_in_edges = len(schema_in)
                full_edges = len(schema_out)
                completeness = schema_in_edges / full_edges if full_edges else 0
                fusion_case_rows.append(
                    [
                        row.get("task_id"),
                        row.get("case_id"),
                        "train",
                        "fuse",
                        row.get("k"),
                        row.get("seed"),
                        row.get("sampling"),
                        full_edges,
                        schema_in_edges,
                        completeness,
                        row.get("mask_ratio"),
                        0,
                    ]
                )

    write_csv(
        tables_dir / "case_stats.csv",
        [
            "task_id",
            "case_id",
            "k",
            "seed",
            "sampling",
            "reachable_ratio",
            "mask_ratio",
            "edges_after_mask",
            "fusion_mode",
        ],
        case_stats_rows,
    )

    if fusion_case_rows:
        write_csv(
            tables_dir / "fusion_case_stats.csv",
            [
                "task_id",
                "case_id",
                "split",
                "mode",
                "K",
                "seed",
                "sampling",
                "full_edges",
                "schema_in_edges",
                "schema_in_completeness",
                "mask_ratio",
                "injected_noise_edges",
            ],
            fusion_case_rows,
        )
        split_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: {"total": 0, "fuse": 0})
        completeness_values: List[float] = []
        mask_ratio_counts: Counter[float] = Counter()
        for row in fusion_case_rows:
            split = str(row[2])
            mode = str(row[3])
            split_counts[split]["total"] += 1
            if mode == "fuse":
                split_counts[split]["fuse"] += 1
                if split == "train":
                    completeness_values.append(float(row[9]))
                if row[10] is not None:
                    mask_ratio_counts[float(row[10])] += 1
        fuse_ratio_train = (
            split_counts["train"]["fuse"] / split_counts["train"]["total"]
            if split_counts["train"]["total"]
            else 0.0
        )
        fuse_ratio_dev = (
            split_counts["dev"]["fuse"] / split_counts["dev"]["total"] if split_counts["dev"]["total"] else 0.0
        )
        fuse_ratio_test = (
            split_counts["test"]["fuse"] / split_counts["test"]["total"] if split_counts["test"]["total"] else 0.0
        )
        avg_completeness = statistics.mean(completeness_values) if completeness_values else 0.0
        mask_ratio_distribution = json.dumps(mask_ratio_counts, ensure_ascii=False)
        write_csv(
            tables_dir / "fusion_summary.csv",
            [
                "#cases_total",
                "#cases_fuse",
                "fuse_ratio_train",
                "fuse_ratio_dev",
                "fuse_ratio_test",
                "avg_schema_in_completeness_train",
                "mask_ratio_distribution",
            ],
            [
                [
                    len(fusion_case_rows),
                    sum(1 for row in fusion_case_rows if row[3] == "fuse"),
                    fuse_ratio_train,
                    fuse_ratio_dev,
                    fuse_ratio_test,
                    avg_completeness,
                    mask_ratio_distribution,
                ]
            ],
        )

    overall_rows = [
        ["train", split_counter.get("train", 0)],
        ["dev", split_counter.get("dev", 0)],
        ["test", split_counter.get("test", 0)],
    ]
    write_csv(tables_dir / "scope_overall_stats.csv", ["split", "doc_count"], overall_rows)

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
    for dataset_name, docs in dataset_docs.items():
        if dataset_schema.get(dataset_name, {}).get("task") != "re":
            continue
        if len(docs) < max(coverage_curve_ks):
            continue
        schema_edges = dataset_schema[dataset_name].get("edges") or set()
        schema_payload = build_schema_payload(schema_edges, set())
        ratios_list = []
        for k in coverage_curve_ks:
            sampled = _sample_docs_by_strategy(
                docs,
                schema_payload,
                k,
                split_seed,
                "coverage",
                symmetric_relations,
            )
            reachable = set()
            for doc in sampled:
                for edge_key in doc_edge_keys(doc):
                    reachable.add(_canonicalize_edge_key(edge_key, symmetric_relations))
            schema_keys = {
                _canonicalize_edge_key(schema_key_from_edge(edge), symmetric_relations) for edge in schema_payload
            }
            ratio = len(schema_keys & reachable) / len(schema_keys) if schema_keys else 0
            ratios_list.append(ratio)
        _plot_coverage_curve(
            figs_dir / "coverage_curve_example.png",
            coverage_curve_ks,
            ratios_list,
            f"Coverage curve ({dataset_name})",
            matplotlib_backend,
        )
        coverage_curve_lines.append(f"- {dataset_name}: {ratios_list}")
        break

    anomaly_lines = ["# SCOPE Anomaly Report", ""]
    if explosion_guard_datasets:
        anomaly_lines.append("## schema_explosion_guard 触发数据集")
        for name in explosion_guard_datasets:
            anomaly_lines.append(f"- {name}")
        anomaly_lines.append("")

    low_coverage = [row for row in coverage_stats_rows if row[3] < coverage_low_threshold]
    if low_coverage:
        anomaly_lines.append("## reachable_ratio 过低的数据集")
        for dataset_name, _, _, ratio in low_coverage:
            anomaly_lines.append(f"- {dataset_name}: {ratio:.3f}")
        anomaly_lines.append("")

    split_overlap = []
    for dataset_name, docs in dataset_docs.items():
        train_hashes = {text_hash(doc.text) for doc in docs if doc.global_split == "train"}
        dev_hashes = {text_hash(doc.text) for doc in docs if doc.global_split == "dev"}
        test_hashes = {text_hash(doc.text) for doc in docs if doc.global_split == "test"}
        overlap = len(train_hashes & dev_hashes) + len(train_hashes & test_hashes) + len(dev_hashes & test_hashes)
        total = len(train_hashes | dev_hashes | test_hashes)
        ratio = overlap / total if total else 0
        if ratio > split_overlap_threshold:
            split_overlap.append((dataset_name, ratio))
    if split_overlap:
        anomaly_lines.append("## split overlap 警告")
        for name, overlap in split_overlap:
            anomaly_lines.append(f"- {name}: {overlap:.3f}")
        anomaly_lines.append("")

    if validation_warnings:
        anomaly_lines.append("## validation warnings")
        for warning in validation_warnings:
            anomaly_lines.append(f"- {warning}")
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
    ]
    if coverage_curve_lines:
        summary_lines.append("")
        summary_lines.append("## Coverage curve samples")
        summary_lines.extend(coverage_curve_lines)
    summary_lines.extend(
        [
            "",
            "## InstructIE 统计口径说明",
            "RelLabels 表示关系类型去重数；TypedEdges 表示归一化后的 (head_type, rel, tail) 唯一边数；",
            "CoreTypedEdges 若无 core filter 则与 TypedEdges 相同。",
        ]
    )
    _build_summary_md(stats_dir / "summary.md", summary_lines)

    tracks_payload = {
        "Track-1": {
            "name": "single_source_induction",
            "description": "单源归纳：仅提供语料，输出完整 schema",
        },
        "Track-2": {
            "name": "induction_with_partial_base_schema",
            "description": "提供部分 base schema，完成剩余 schema",
        },
        "Track-3": {
            "name": "multi_source_fusion",
            "description": "多源 fusion：base 来自另一来源，gold 为双源 union",
        },
    }
    (out_root / "tracks.json").write_text(
        json.dumps(tracks_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    eval_script = (scope_cfg.get("dataset_cards") or {}).get("eval_script")
    _write_dataset_card(
        dataset_cards_dir / "SCOPE.md",
        "SCOPE",
        "mixed",
        "RE+EE",
        total_docs,
        sum(
            len(schema.get("edges") or set()) for schema in dataset_schema.values() if schema.get("task") == "re"
        )
        + sum(len(schema.get("edges") or set()) for schema in dataset_schema.values() if schema.get("task") == "ee"),
        True,
        eval_script,
    )

    for dataset_name, schema in dataset_schema.items():
        task = schema.get("task")
        language = schema.get("language", "zh")
        docs = dataset_docs.get(dataset_name, [])
        doc_count = len(docs)
        typed_flag = bool(schema.get("typed_flag"))
        schema_edges = len(schema.get("edges") or set())
        _write_dataset_card(
            dataset_cards_dir / f"{dataset_name}.md",
            dataset_name,
            language,
            task,
            doc_count,
            schema_edges,
            typed_flag,
            eval_script,
        )

    LOGGER.info("SCOPE 统计完成，输出目录: %s", out_root)


def _sample_docs_by_strategy(
    docs: Sequence[ScopeDoc],
    schema_payload: Sequence[Dict[str, Any]],
    k: int,
    seed: int,
    sampling: str,
    symmetric_relations: Optional[Set[str]] = None,
) -> List[ScopeDoc]:
    symmetric_relations = symmetric_relations or set()
    if k <= 0:
        return []
    if sampling == "random":
        rng = random.Random(seed)
        return rng.sample(list(docs), min(k, len(docs)))
    if sampling == "coverage":
        remaining = {
            _canonicalize_edge_key(schema_key_from_edge(edge), symmetric_relations) for edge in schema_payload
        }
        selected = []
        for doc in sorted(docs, key=lambda d: len(doc_edge_keys(d)), reverse=True):
            gain = len(
                {_canonicalize_edge_key(edge, symmetric_relations) for edge in doc_edge_keys(doc)} & remaining
            )
            if gain <= 0:
                continue
            selected.append(doc)
            remaining -= {
                _canonicalize_edge_key(edge, symmetric_relations) for edge in doc_edge_keys(doc)
            }
            if len(selected) >= k:
                break
        if len(selected) < k:
            selected.extend(docs[: max(0, k - len(selected))])
        return selected
    return list(docs)[:k]


def _str2bool(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    return str(value).lower() in {"1", "true", "yes", "y"}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize SCOPE dataset stats.")
    parser.add_argument("--out_root")
    parser.add_argument("--dedup_by_text", type=_str2bool)
    parser.add_argument("--cross_dataset_dedup", type=_str2bool)
    parser.add_argument("--global_split_ratios", nargs=3, type=float)
    parser.add_argument("--split_seed", type=int)
    parser.add_argument("--min_docs_per_type", type=int)
    parser.add_argument("--schema_explosion_guard", type=_str2bool)
    parser.add_argument("--explosion_edge_threshold", type=int)
    parser.add_argument("--symmetric_relations_file")
    return parser.parse_args()


def main() -> None:
    config = load_yaml_config()
    args = _parse_args()
    summarize_scope_dataset(config, args)


if __name__ == "__main__":
    main()
