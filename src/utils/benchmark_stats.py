"""公开数据集 benchmark 统计工具。"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import math
import re
import statistics
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .common import load_yaml_config, resolve_project_path, save_json
from .logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


@dataclass(frozen=True)
class DatasetConversionStats:
    """数据集转换统计信息。"""

    name: str
    task: str
    language: str
    format_key: str
    schema_count: int
    schema_roles: int
    sample_count: int
    raw_records: int
    sample_limit: int
    include_input: bool
    schema_output: str
    samples_output: str
    data_files: List[str]
    schema_paths: List[str]
    schema_has_file: bool
    relation_types: List[str]
    relation_types_source: str
    relation_types_llm_generated: bool
    relation_types_llm_items: List[str]


def build_conversion_summary(stats: Sequence[DatasetConversionStats]) -> str:
    total_datasets = len(stats)
    total_samples = sum(item.sample_count for item in stats)
    total_raw = sum(item.raw_records for item in stats)
    total_schema = sum(item.schema_count for item in stats)
    re_stats = [item for item in stats if item.task == "re"]
    ee_stats = [item for item in stats if item.task == "ee"]
    re_zh = [item for item in re_stats if item.language == "zh"]
    re_en = [item for item in re_stats if item.language == "en"]
    ee_zh = [item for item in ee_stats if item.language == "zh"]
    ee_en = [item for item in ee_stats if item.language == "en"]

    lines = [
        "公开数据集转换汇总信息",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"数据集总数: {total_datasets}",
        f"RE 总数: {len(re_stats)} (RE-zh: {len(re_zh)} / RE-en: {len(re_en)})",
        f"EE 总数: {len(ee_stats)} (EE-zh: {len(ee_zh)} / EE-en: {len(ee_en)})",
        f"Schema 总条目数: {total_schema}",
        f"样本总数(输出): {total_samples}",
        f"原始记录总数(输入): {total_raw}",
        "",
        "各数据集明细:",
    ]

    for item in stats:
        lines.extend(
            [
                f"- 数据集: {item.name}",
                f"  任务/语言/格式: {item.task}/{item.language}/{item.format_key}",
                f"  schema 条目: {item.schema_count} (roles: {item.schema_roles})",
                f"  schema 来源: {'external' if item.schema_has_file else 'generated'}",
                f"  输出样本数: {item.sample_count}",
                f"  原始记录数: {item.raw_records}",
                f"  samples_limit: {item.sample_limit}",
                f"  include_input: {item.include_input}",
                f"  relation_types({len(item.relation_types)}): {', '.join(item.relation_types) if item.relation_types else 'None'}",
                f"  relation_types_source: {item.relation_types_source}",
                (
                    "  relation_types_llm_generated:"
                    f" {item.relation_types_llm_generated} ({', '.join(item.relation_types_llm_items) if item.relation_types_llm_items else 'None'})"
                ),
                f"  schema 输出: {item.schema_output}",
                f"  samples 输出: {item.samples_output}",
                f"  data_files({len(item.data_files)}): {', '.join(item.data_files)}",
                f"  schema_paths({len(item.schema_paths)}): {', '.join(item.schema_paths)}",
                "",
            ]
        )
    lines.extend(_build_schema_summary(stats))
    return "\n".join(lines)


def _build_schema_summary(stats: Sequence[DatasetConversionStats]) -> List[str]:
    with_schema = [item.name for item in stats if item.schema_has_file]
    without_schema = [item.name for item in stats if not item.schema_has_file]
    with_relation_types = [item.name for item in stats if item.relation_types]
    without_relation_types = [item.name for item in stats if not item.relation_types]
    llm_generated = [
        f"{item.name}({', '.join(item.relation_types_llm_items) if item.relation_types_llm_items else 'None'})"
        for item in stats
        if item.relation_types_llm_generated
    ]

    return [
        "Schema/关系类型汇总:",
        f"  有 schema({len(with_schema)}): {', '.join(with_schema) if with_schema else 'None'}",
        f"  无 schema({len(without_schema)}): {', '.join(without_schema) if without_schema else 'None'}",
        f"  有关系类型({len(with_relation_types)}): {', '.join(with_relation_types) if with_relation_types else 'None'}",
        f"  无关系类型({len(without_relation_types)}): {', '.join(without_relation_types) if without_relation_types else 'None'}",
        (
            "  模型生成关系类型("
            f"{len(llm_generated)}): {', '.join(llm_generated) if llm_generated else 'None'}"
        ),
        "",
    ]


def write_conversion_summary(summary_path: Path, stats: Sequence[DatasetConversionStats]) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    content = build_conversion_summary(stats)
    summary_path.write_text(content, encoding="utf-8")
    LOGGER.info("汇总信息已写入: %s", summary_path)


def run_benchmark_stats(config: Dict[str, Any]) -> Dict[str, Any]:
    benchmark_cfg = config.get("benchmark_stats") or {}
    summary_txt = resolve_project_path(
        benchmark_cfg.get("summary_txt", "data/input/data_info.txt")
    )
    out_dir = resolve_project_path(benchmark_cfg.get("out_dir", "data/output/benchmark_stats"))
    out_dir.mkdir(parents=True, exist_ok=True)
    if not summary_txt.exists():
        LOGGER.warning("未找到 summary_txt: %s", summary_txt)
        return {}

    registry = _parse_summary_file(summary_txt)
    save_json(out_dir / "registry.json", registry)
    LOGGER.debug("registry.json 已输出: %s", out_dir / "registry.json")

    schema_stats: List[Dict[str, Any]] = []
    corpus_stats: List[Dict[str, Any]] = []
    coverage_stats: List[Dict[str, Any]] = []
    anomalies: List[Dict[str, Any]] = []
    all_text_lengths: List[int] = []
    schema_edges_all: List[int] = []

    for entry in registry:
        LOGGER.debug("处理数据集: %s", entry["dataset_name"])
        schema_info = _analyze_schema(entry, benchmark_cfg)
        schema_stats.append(schema_info)
        schema_edges_all.append(schema_info.get("schema_edges") or 0)

        corpus_info, corpus_text_lengths, corpus_anomalies = _analyze_corpus(entry, benchmark_cfg)
        corpus_stats.append(corpus_info)
        all_text_lengths.extend(corpus_text_lengths)
        anomalies.extend(corpus_anomalies)

        coverage_info, coverage_anomalies = _analyze_coverage(entry, schema_info, benchmark_cfg)
        coverage_stats.append(coverage_info)
        anomalies.extend(coverage_anomalies)

    tables_dir = out_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    _write_csv(tables_dir / "schema_stats.csv", schema_stats)
    _write_csv(tables_dir / "corpus_stats.csv", corpus_stats)
    _write_csv(tables_dir / "coverage_stats.csv", coverage_stats)

    _write_anomaly_report(out_dir / "anomaly_report.md", anomalies)
    _write_figs(out_dir / "figs", schema_stats, corpus_stats)
    _write_final_summary(out_dir / "summary.md", registry, schema_stats, corpus_stats, coverage_stats, all_text_lengths, benchmark_cfg)

    LOGGER.info("benchmark 统计已完成，输出目录: %s", out_dir)
    return {
        "registry": registry,
        "schema_stats": schema_stats,
        "corpus_stats": corpus_stats,
        "coverage_stats": coverage_stats,
        "anomalies": anomalies,
    }


def _parse_summary_file(summary_path: Path) -> List[Dict[str, Any]]:
    text = summary_path.read_text(encoding="utf-8")
    return _parse_summary_text(text)


def _parse_summary_text(text: str) -> List[Dict[str, Any]]:
    lines = [line.rstrip() for line in text.splitlines()]
    registry: List[Dict[str, Any]] = []
    current: Dict[str, Any] | None = None

    def finalize_current() -> None:
        if current:
            registry.append(current)

    for line in lines:
        if line.startswith("- 数据集:"):
            finalize_current()
            current = {
                "dataset_name": line.split(":", 1)[1].strip(),
                "task": "",
                "lang": "",
                "format": "",
                "schema_count": 0,
                "schema_roles": 0,
                "schema_output_path": "",
                "samples_output_path": "",
                "data_files": [],
                "schema_paths": [],
                "output_samples_count": 0,
                "raw_records_count": 0,
                "include_input": False,
                "samples_limit": 0,
            }
            continue
        if current is None:
            continue
        if line.strip().startswith("任务/语言/格式:"):
            payload = line.split(":", 1)[1].strip()
            parts = payload.split("/")
            current["task"] = parts[0].strip() if len(parts) > 0 else ""
            current["lang"] = parts[1].strip() if len(parts) > 1 else ""
            current["format"] = parts[2].strip() if len(parts) > 2 else ""
        elif line.strip().startswith("schema 条目:"):
            current["schema_count"], current["schema_roles"] = _parse_schema_count_line(line)
        elif line.strip().startswith("输出样本数:"):
            current["output_samples_count"] = _safe_int(line.split(":", 1)[1].strip())
        elif line.strip().startswith("原始记录数:"):
            current["raw_records_count"] = _safe_int(line.split(":", 1)[1].strip())
        elif line.strip().startswith("samples_limit:"):
            current["samples_limit"] = _safe_int(line.split(":", 1)[1].strip())
        elif line.strip().startswith("include_input:"):
            current["include_input"] = line.split(":", 1)[1].strip().lower() == "true"
        elif line.strip().startswith("schema 输出:"):
            current["schema_output_path"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("samples 输出:"):
            current["samples_output_path"] = line.split(":", 1)[1].strip()
        elif line.strip().startswith("data_files("):
            current["data_files"] = _parse_list_field(line)
        elif line.strip().startswith("schema_paths("):
            current["schema_paths"] = _parse_list_field(line)

    finalize_current()
    LOGGER.debug("解析 summary 数据集条目数: %s", len(registry))
    return registry


def _parse_list_field(line: str) -> List[str]:
    parts = line.split(":", 1)
    if len(parts) < 2:
        return []
    payload = parts[1].strip()
    if not payload:
        return []
    return [item.strip() for item in payload.split(",") if item.strip()]


def _parse_schema_count_line(line: str) -> Tuple[int, int]:
    payload = line.split(":", 1)[1].strip()
    match = re.match(r"(\\d+)\\s*\\(roles:\\s*(\\d+)\\)", payload)
    if match:
        return int(match.group(1)), int(match.group(2))
    return _safe_int(payload), 0


def _safe_int(raw: str) -> int:
    try:
        return int(raw)
    except ValueError:
        return 0


def _analyze_schema(entry: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
    schema_paths = [Path(path) for path in entry.get("schema_paths", []) if path]
    schema_output = Path(entry.get("schema_output_path", "")) if entry.get("schema_output_path") else None
    schema_payload = _load_schema_payload(schema_output, schema_paths)
    placeholder_types = set(cfg.get("schema_placeholder_types", ["Entity", "entity", "NA", "N/A", ""]))

    schema_items_count = entry.get("schema_count") or _schema_items_count(schema_payload)
    schema_info: Dict[str, Any] = {
        "dataset": entry.get("dataset_name", ""),
        "task": entry.get("task", ""),
        "lang": entry.get("lang", ""),
        "format": entry.get("format", ""),
        "schema_has_external_file": bool(schema_paths),
        "schema_items_count": schema_items_count,
        "schema_edges": 0,
        "rel_types": "NA",
        "ent_types": "NA",
        "schema_edges_count": 0,
        "typed_flag": False,
        "event_types": "NA",
        "role_types": "NA",
        "event_role_edges": 0,
        "trigger_in_schema_flag": False,
    }

    if entry.get("task") == "ee":
        ee_edges, event_types, role_types, trigger_flag = _normalize_ee_schema(schema_payload)
        schema_info.update(
            {
                "event_types": len(event_types),
                "role_types": len(role_types),
                "event_role_edges": len(ee_edges),
                "schema_edges": len(ee_edges),
                "trigger_in_schema_flag": trigger_flag,
            }
        )
    else:
        re_edges, rel_types, ent_types, typed_flag = _normalize_re_schema(schema_payload, placeholder_types)
        schema_info.update(
            {
                "rel_types": len(rel_types),
                "ent_types": len(ent_types) if typed_flag else "NA",
                "schema_edges": len(re_edges) if typed_flag else len(rel_types),
                "schema_edges_count": len(re_edges),
                "typed_flag": typed_flag,
            }
        )

    LOGGER.debug("schema 统计: %s -> %s", entry.get("dataset_name"), schema_info)
    return schema_info


def _schema_items_count(schema_payload: Any) -> int:
    if isinstance(schema_payload, dict):
        for key in ("relationships", "events", "event_types"):
            if isinstance(schema_payload.get(key), list):
                return len(schema_payload[key])
        return len(schema_payload)
    if isinstance(schema_payload, list):
        return len(schema_payload)
    return 0


def _normalize_re_schema(
    schema_payload: Any, placeholder_types: set[str]
) -> Tuple[List[Tuple[str, str, str]], List[str], List[str], bool]:
    relationships: List[Any] = []
    if isinstance(schema_payload, dict):
        if isinstance(schema_payload.get("relationships"), list):
            relationships = schema_payload["relationships"]
        elif isinstance(schema_payload.get("relations"), list):
            relationships = schema_payload["relations"]
        else:
            relationships = [schema_payload]
    elif isinstance(schema_payload, list):
        relationships = schema_payload

    edges: List[Tuple[str, str, str]] = []
    rel_types: set[str] = set()
    ent_types: set[str] = set()
    typed_flag = False

    for rel in relationships:
        if isinstance(rel, str):
            predicate = rel.strip()
            if not predicate:
                continue
            rel_types.add(predicate)
            edges.append(("Entity", predicate, "Entity"))
            continue
        if isinstance(rel, (list, tuple)) and len(rel) >= 3:
            domain, predicate, range_ = rel[0], rel[1], rel[2]
        elif isinstance(rel, dict):
            domain = _extract_first_value(rel, ["subject_type", "head_type", "domain", "head_entity", "h"])
            range_ = _extract_first_value(rel, ["object_type", "tail_type", "range", "tail_entity", "t"])
            predicate = _extract_first_value(rel, ["predicate", "relation", "rel_type", "r"])
        else:
            continue

        domain = str(domain).strip() if domain is not None else ""
        range_ = str(range_).strip() if range_ is not None else ""
        predicate = str(predicate).strip() if predicate is not None else ""
        if not predicate:
            continue
        rel_types.add(predicate)

        if not domain or domain in placeholder_types:
            domain = "Entity"
        if not range_ or range_ in placeholder_types:
            range_ = "Entity"
        edges.append((domain, predicate, range_))

        if domain not in placeholder_types and range_ not in placeholder_types:
            typed_flag = True
            ent_types.update([domain, range_])

    return sorted(set(edges)), sorted(rel_types), sorted(ent_types), typed_flag


def _normalize_ee_schema(
    schema_payload: Any,
) -> Tuple[List[Tuple[str, str, str]], List[str], List[str], bool]:
    edges: List[Tuple[str, str, str]] = []
    event_types: set[str] = set()
    role_types: set[str] = set()
    trigger_flag = False

    events: List[Any] = []
    if isinstance(schema_payload, dict):
        if isinstance(schema_payload.get("events"), list):
            events = schema_payload["events"]
        elif isinstance(schema_payload.get("event_types"), list):
            events = [{"event_type": item, "roles": schema_payload.get("roles", [])} for item in schema_payload["event_types"]]
        else:
            events = [schema_payload]
    elif isinstance(schema_payload, list):
        events = schema_payload

    for item in events:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            event_type = str(item[0]).strip()
            role = str(item[1]).strip()
            arg = str(item[2]).strip() if len(item) > 2 else "ARG"
            if event_type and role:
                edges.append((event_type, role, arg))
                event_types.add(event_type)
                role_types.add(role)
            continue
        if not isinstance(item, dict):
            continue
        event_type = str(item.get("event_type") or item.get("type") or "").strip()
        if not event_type:
            continue
        event_types.add(event_type)
        roles = item.get("roles", [])
        if any(key in item for key in ("trigger", "trigger_words", "triggers", "event_trigger")):
            trigger_flag = True
        if isinstance(roles, list) and roles:
            for role_item in roles:
                role = ""
                arg = "ARG"
                if isinstance(role_item, dict):
                    role = str(role_item.get("role") or role_item.get("name") or "").strip()
                    arg = str(role_item.get("arg") or role_item.get("argument") or "ARG").strip()
                elif isinstance(role_item, str):
                    role = role_item.strip()
                if role:
                    edges.append((event_type, role, arg))
                    role_types.add(role)
        elif roles:
            role = str(roles).strip()
            if role:
                edges.append((event_type, role, "ARG"))
                role_types.add(role)

    return sorted(set(edges)), sorted(event_types), sorted(role_types), trigger_flag


def _extract_first_value(payload: Dict[str, Any], keys: Sequence[str]) -> Any:
    for key in keys:
        if key not in payload:
            continue
        value = payload.get(key)
        if isinstance(value, dict):
            for inner_key in ("@value", "value", "name"):
                if inner_key in value:
                    return value[inner_key]
            if value:
                return next(iter(value.values()))
        return value
    return ""


def _load_schema_payload(schema_output: Path | None, schema_paths: Sequence[Path]) -> Any:
    candidates = [path for path in [schema_output, *schema_paths] if path]
    for path in candidates:
        if not path.exists():
            LOGGER.debug("schema 文件不存在: %s", path)
            continue
        try:
            text = path.read_text(encoding="utf-8")
            return json.loads(text)
        except json.JSONDecodeError:
            lines = []
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    lines.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            if lines:
                return lines
        except OSError as exc:
            LOGGER.warning("读取 schema 失败: %s (%s)", path, exc)
            continue
    return {}


def _analyze_corpus(
    entry: Dict[str, Any], cfg: Dict[str, Any]
) -> Tuple[Dict[str, Any], List[int], List[Dict[str, Any]]]:
    data_files = [Path(path) for path in entry.get("data_files", []) if path]
    task = entry.get("task", "")
    split_aliases = cfg.get(
        "split_aliases",
        {"train": ["train"], "dev": ["dev", "valid", "val"], "test": ["test"]},
    )
    text_fields = cfg.get("text_fields", ["text", "sentence", "contents", "content"])
    anomalies: List[Dict[str, Any]] = []
    split_counts = {"train": "NA", "dev": "NA", "test": "NA"}
    doc_texts: List[str] = []
    doc_texts_hash: set[str] = set()
    text_lengths: List[int] = []
    token_lengths: List[int] = []
    triples_per_doc: List[int] = []
    events_per_doc: List[int] = []
    args_per_event: List[int] = []
    parsed_any = False

    for data_path in data_files:
        split = _infer_split(data_path, split_aliases)
        file_records = 0
        if not data_path.exists():
            anomalies.append(
                {
                    "dataset": entry.get("dataset_name", ""),
                    "issue": "raw_file_missing",
                    "detail": f"缺失原始文件: {data_path}",
                    "suggestion": "检查 data_files 配置路径。",
                }
            )
            continue
        LOGGER.debug("解析原始数据文件: %s", data_path)
        reader = _iter_dataset_records(data_path, entry.get("format", ""), cfg)
        for record in reader:
            parsed_any = True
            file_records += 1
            text = _extract_text(record, text_fields)
            if text:
                doc_texts.append(text)
                text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
                doc_texts_hash.add(text_hash)
                text_lengths.append(len(text))
                token_lengths.append(len(text.split()))
            if task == "re":
                triples_per_doc.append(_count_re_triples(record))
            else:
                event_count, arg_count = _count_ee_events(record)
                events_per_doc.append(event_count)
                if event_count > 0:
                    args_per_event.extend([arg_count / max(event_count, 1)])

        if split and split in split_counts:
            split_counts[split] = _safe_add(split_counts.get(split), file_records)

    if not parsed_any:
        anomalies.append(
            {
                "dataset": entry.get("dataset_name", ""),
                "issue": "raw_parse_failed",
                "detail": "未能解析原始数据文件。",
                "suggestion": "检查原始数据格式与 reader 适配规则。",
            }
        )

    if not doc_texts and cfg.get("output_text_fallback", True):
        LOGGER.debug("原始数据未抽取到文本，尝试使用转换产物文本。")
        fallback_texts = _extract_texts_from_samples(entry.get("samples_output_path", ""))
        doc_texts = fallback_texts
        text_lengths = [len(text) for text in fallback_texts]
        token_lengths = [len(text.split()) for text in fallback_texts]

    doc_count_dedup = len(doc_texts_hash) if doc_texts_hash else "NA"

    raw_records_count = entry.get("raw_records_count", 0)
    duplicate_ratio = "NA"
    if isinstance(doc_count_dedup, int) and raw_records_count:
        duplicate_ratio = round(1 - doc_count_dedup / raw_records_count, 4)

    corpus_info: Dict[str, Any] = {
        "dataset": entry.get("dataset_name", ""),
        "task": task,
        "lang": entry.get("lang", ""),
        "split_train": split_counts["train"],
        "split_dev": split_counts["dev"],
        "split_test": split_counts["test"],
        "doc_count_dedup": doc_count_dedup,
        "output_samples_count": entry.get("output_samples_count", 0),
        "raw_records_count": raw_records_count,
        "duplicate_ratio": duplicate_ratio,
        "avg_chars": _safe_mean(text_lengths),
        "median_chars": _safe_median(text_lengths),
        "p90_chars": _safe_percentile(text_lengths, 0.9),
        "p99_chars": _safe_percentile(text_lengths, 0.99),
        "avg_tokens_ws": _safe_mean(token_lengths),
        "median_tokens_ws": _safe_median(token_lengths),
        "avg_triples_per_doc": _safe_mean(triples_per_doc) if task == "re" else "NA",
        "median_triples_per_doc": _safe_median(triples_per_doc) if task == "re" else "NA",
        "avg_events_per_doc": _safe_mean(events_per_doc) if task == "ee" else "NA",
        "median_events_per_doc": _safe_median(events_per_doc) if task == "ee" else "NA",
        "avg_args_per_event": _safe_mean(args_per_event) if task == "ee" else "NA",
    }

    if doc_count_dedup == "NA":
        anomalies.append(
            {
                "dataset": entry.get("dataset_name", ""),
                "issue": "missing_text",
                "detail": "未能解析到 text 字段。",
                "suggestion": "补充 text 字段或增加 reader 的字段映射。",
            }
        )

    if split_counts["dev"] == "NA" or split_counts["test"] == "NA":
        anomalies.append(
            {
                "dataset": entry.get("dataset_name", ""),
                "issue": "split_missing",
                "detail": f"split_counts={split_counts}",
                "suggestion": "检查是否缺少 dev/test 文件。",
            }
        )

    output_samples_count = entry.get("output_samples_count", 0)
    if raw_records_count and output_samples_count > raw_records_count * float(cfg.get("output_sample_ratio_high_threshold", 2.0)):
        anomalies.append(
            {
                "dataset": entry.get("dataset_name", ""),
                "issue": "output_samples_excessive",
                "detail": f"output_samples_count={output_samples_count}, raw_records_count={raw_records_count}",
                "suggestion": "检查是否出现样本重复或 flatten。",
            }
        )

    LOGGER.debug("语料统计: %s -> %s", entry.get("dataset_name"), corpus_info)
    return corpus_info, text_lengths, anomalies


def _iter_dataset_records(path: Path, format_key: str, cfg: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    if format_key == "semeval2010" or path.suffix.lower() == ".txt":
        for record in _iter_semeval_records(path):
            yield record
        return

    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, list):
        for item in payload:
            if isinstance(item, dict):
                yield item
        return
    if isinstance(payload, dict):
        list_items = _extract_list_from_payload(payload)
        if list_items:
            for item in list_items:
                if isinstance(item, dict):
                    yield item
            return
        yield payload
        return

    for line in text.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            yield payload


def _extract_list_from_payload(payload: Dict[str, Any]) -> List[Any]:
    for key in ("data", "instances", "samples", "records"):
        if isinstance(payload.get(key), list):
            return payload[key]
    for value in payload.values():
        if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
            return value
    return []


def _iter_semeval_records(path: Path) -> Iterable[Dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if not line or "\t" not in line:
            idx += 1
            continue
        sample_id, sentence = line.split("\t", 1)
        sentence = sentence.strip().strip('"')
        rel_line = ""
        if idx + 1 < len(lines):
            candidate = lines[idx + 1].strip()
            if _is_semeval_relation_line(candidate):
                rel_line = candidate
        rel_type, _ = _parse_semeval_relation(rel_line or "Other")
        yield {"id": sample_id, "text": _strip_semeval_tags(sentence), "relation": [{"relation": rel_type}]}
        if rel_line:
            idx += 2
            while idx < len(lines):
                peek = lines[idx].strip()
                if peek and "\t" in peek:
                    break
                idx += 1
        else:
            idx += 1


def _strip_semeval_tags(sentence: str) -> str:
    sentence = re.sub(r"</?e1>", "", sentence)
    sentence = re.sub(r"</?e2>", "", sentence)
    return sentence


def _parse_semeval_relation(raw: str) -> Tuple[str, str]:
    raw = raw.strip()
    match = re.match(r"(.+?)\((e1|e2),(e1|e2)\)", raw)
    if not match:
        return raw, ""
    rel_type = match.group(1).strip()
    direction = f"{match.group(2)},{match.group(3)}"
    return rel_type, direction


def _is_semeval_relation_line(raw: str) -> bool:
    raw = raw.strip()
    if not raw:
        return False
    return bool(re.match(r".+\((e1|e2),(e1|e2)\)$", raw))


def _infer_split(path: Path, split_aliases: Dict[str, List[str]]) -> str | None:
    lowered = path.name.lower()
    for split, aliases in split_aliases.items():
        for alias in aliases:
            if alias in lowered:
                return split
    return None


def _extract_text(record: Dict[str, Any], text_fields: Sequence[str]) -> str:
    for field in text_fields:
        if field in record and isinstance(record[field], str):
            return record[field].strip()
    return ""


def _count_re_triples(record: Dict[str, Any]) -> int:
    if isinstance(record.get("relation"), list):
        return len(record["relation"])
    if isinstance(record.get("relations"), list):
        return len(record["relations"])
    if isinstance(record.get("spo_list"), list):
        return len(record["spo_list"])
    if isinstance(record.get("triples"), list):
        return len(record["triples"])
    return 0


def _extract_re_edges(record: Dict[str, Any], placeholder: str) -> List[Tuple[str, str, str]]:
    edges: List[Tuple[str, str, str]] = []
    relations = record.get("relation")
    if isinstance(relations, list):
        for rel in relations:
            if not isinstance(rel, dict):
                continue
            predicate = str(rel.get("relation") or rel.get("predicate") or rel.get("rel_type") or "").strip()
            domain = str(rel.get("head_type") or rel.get("subject_type") or rel.get("head_entity_type") or "").strip()
            range_ = str(rel.get("tail_type") or rel.get("object_type") or rel.get("tail_entity_type") or "").strip()
            if not predicate:
                continue
            if not domain:
                domain = placeholder
            if not range_:
                range_ = placeholder
            edges.append((domain, predicate, range_))
        return edges

    spo_list = record.get("spo_list")
    if isinstance(spo_list, list):
        for spo in spo_list:
            if not isinstance(spo, dict):
                continue
            predicate = str(spo.get("predicate") or "").strip()
            domain = str(spo.get("subject_type") or placeholder).strip()
            obj_type = spo.get("object_type", "")
            if isinstance(obj_type, dict):
                range_ = str(obj_type.get("@value") or placeholder).strip()
            else:
                range_ = str(obj_type or placeholder).strip()
            if predicate:
                edges.append((domain or placeholder, predicate, range_ or placeholder))
        return edges

    return edges


def _count_ee_events(record: Dict[str, Any]) -> Tuple[int, int]:
    events = record.get("event") or record.get("events") or []
    if not isinstance(events, list):
        return 0, 0
    event_count = 0
    arg_count = 0
    for event in events:
        if not isinstance(event, dict):
            continue
        event_count += 1
        arguments = event.get("arguments") or event.get("args") or []
        if isinstance(arguments, list):
            arg_count += len(arguments)
    return event_count, arg_count


def _extract_ee_edges(record: Dict[str, Any]) -> List[Tuple[str, str, str]]:
    edges: List[Tuple[str, str, str]] = []
    events = record.get("event") or record.get("events") or []
    if not isinstance(events, list):
        return edges
    for event in events:
        if not isinstance(event, dict):
            continue
        event_type = str(event.get("event_type") or event.get("type") or "").strip()
        if not event_type:
            continue
        arguments = event.get("arguments") or event.get("args") or []
        if isinstance(arguments, list):
            for arg in arguments:
                if not isinstance(arg, dict):
                    continue
                role = str(arg.get("role") or arg.get("argument_role") or arg.get("role_type") or "").strip()
                if role:
                    edges.append((event_type, role, "ARG"))
    return edges


def _analyze_coverage(
    entry: Dict[str, Any],
    schema_info: Dict[str, Any],
    cfg: Dict[str, Any],
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    placeholder = cfg.get("coverage_placeholder", "Entity")
    anomalies: List[Dict[str, Any]] = []
    data_files = [Path(path) for path in entry.get("data_files", []) if path]
    split_aliases = cfg.get(
        "split_aliases",
        {"train": ["train"], "dev": ["dev", "valid", "val"], "test": ["test"]},
    )

    schema_edges_count = schema_info.get("schema_edges") or 0
    reachable_edges = set()

    for data_path in data_files:
        split = _infer_split(data_path, split_aliases)
        if split != "train":
            continue
        if not data_path.exists():
            continue
        for record in _iter_dataset_records(data_path, entry.get("format", ""), cfg):
            if entry.get("task") == "ee":
                reachable_edges.update(_extract_ee_edges(record))
            else:
                reachable_edges.update(_extract_re_edges(record, placeholder))

    reachable_ratio_train = "NA"
    if schema_edges_count:
        reachable_ratio_train = round(len(reachable_edges) / schema_edges_count, 4)

    coverage_info = {
        "dataset": entry.get("dataset_name", ""),
        "task": entry.get("task", ""),
        "lang": entry.get("lang", ""),
        "schema_edges": schema_edges_count,
        "reachable_edges_train": len(reachable_edges),
        "reachable_ratio_train": reachable_ratio_train,
    }

    if isinstance(reachable_ratio_train, float) and reachable_ratio_train < float(cfg.get("reachable_ratio_low_threshold", 0.2)):
        anomalies.append(
            {
                "dataset": entry.get("dataset_name", ""),
                "issue": "reachable_ratio_low",
                "detail": f"reachable_ratio_train={reachable_ratio_train}",
                "suggestion": "检查 schema 与训练集标注是否对齐。",
            }
        )

    schema_paths = entry.get("schema_paths", [])
    if not schema_paths and schema_edges_count > int(cfg.get("schema_edge_large_threshold", 200)):
        anomalies.append(
            {
                "dataset": entry.get("dataset_name", ""),
                "issue": "schema_edges_large_without_external_schema",
                "detail": f"schema_edges={schema_edges_count}",
                "suggestion": "检查是否误把实例级数据当 schema。",
            }
        )

    return coverage_info, anomalies


def _extract_texts_from_samples(samples_path: str) -> List[str]:
    if not samples_path:
        return []
    path = Path(samples_path)
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    texts: List[str] = []
    if isinstance(payload, list):
        for group in payload:
            if not isinstance(group, dict):
                continue
            for sample in group.get("samples", []):
                if isinstance(sample, dict):
                    text = sample.get("text")
                    if isinstance(text, str) and text.strip():
                        texts.append(text.strip())
    return texts


def _safe_add(value: Any, addition: int) -> Any:
    if value == "NA":
        return addition
    if isinstance(value, int):
        return value + addition
    return addition


def _safe_mean(values: Sequence[float]) -> Any:
    return round(sum(values) / len(values), 4) if values else "NA"


def _safe_median(values: Sequence[float]) -> Any:
    return round(statistics.median(values), 4) if values else "NA"


def _safe_percentile(values: Sequence[float], percentile: float) -> Any:
    if not values:
        return "NA"
    values_sorted = sorted(values)
    index = int(math.ceil(percentile * len(values_sorted))) - 1
    index = max(0, min(index, len(values_sorted) - 1))
    return values_sorted[index]


def _write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        LOGGER.warning("CSV 输出为空: %s", path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    LOGGER.info("表格已输出: %s", path)


def _write_anomaly_report(path: Path, anomalies: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# 异常与质量报告", ""]
    if not anomalies:
        lines.append("暂无异常。")
    else:
        for item in anomalies:
            lines.append(f"- 数据集: {item.get('dataset', '')}")
            lines.append(f"  - 问题: {item.get('issue', '')}")
            lines.append(f"  - 详情: {item.get('detail', '')}")
            lines.append(f"  - 建议: {item.get('suggestion', '')}")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("异常报告已输出: %s", path)


def _write_figs(out_dir: Path, schema_stats: List[Dict[str, Any]], corpus_stats: List[Dict[str, Any]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        LOGGER.warning("matplotlib 未安装，跳过绘图: %s", exc)
        return

    re_edges = [row["schema_edges"] for row in schema_stats if row.get("task") == "re" and isinstance(row.get("schema_edges"), int)]
    ee_edges = [row["schema_edges"] for row in schema_stats if row.get("task") == "ee" and isinstance(row.get("schema_edges"), int)]
    plt.figure()
    if re_edges:
        plt.hist(re_edges, bins=30, alpha=0.7, label="RE")
    if ee_edges:
        plt.hist(ee_edges, bins=30, alpha=0.7, label="EE")
    plt.xlabel("SchemaEdges / EventRoleEdges")
    plt.ylabel("Count")
    plt.legend()
    hist_path = out_dir / "schema_edges_hist.png"
    plt.savefig(hist_path)
    plt.close()
    LOGGER.info("输出图表: %s", hist_path)

    scatter_path = out_dir / "corpus_vs_schema_scatter.png"
    plt.figure()
    for row in corpus_stats:
        schema_edge = _find_schema_edges(schema_stats, row.get("dataset"))
        x = row.get("doc_count_dedup")
        if x == "NA":
            x = row.get("raw_records_count")
        y = schema_edge
        if isinstance(x, int) and isinstance(y, int):
            marker = "o" if row.get("task") == "re" else "s"
            plt.scatter(x, y, marker=marker, label=row.get("task"))
    plt.xlabel("Doc Count (dedup/raw)")
    plt.ylabel("Schema Edges")
    plt.savefig(scatter_path)
    plt.close()
    LOGGER.info("输出图表: %s", scatter_path)


def _find_schema_edges(schema_stats: List[Dict[str, Any]], dataset: str) -> int | None:
    for row in schema_stats:
        if row.get("dataset") == dataset:
            return row.get("schema_edges") if isinstance(row.get("schema_edges"), int) else None
    return None


def _write_final_summary(
    path: Path,
    registry: List[Dict[str, Any]],
    schema_stats: List[Dict[str, Any]],
    corpus_stats: List[Dict[str, Any]],
    coverage_stats: List[Dict[str, Any]],
    text_lengths: List[int],
    cfg: Dict[str, Any],
) -> None:
    total = len(registry)
    re_count = len([item for item in registry if item.get("task") == "re"])
    ee_count = len([item for item in registry if item.get("task") == "ee"])
    zh_count = len([item for item in registry if item.get("lang") == "zh"])
    en_count = len([item for item in registry if item.get("lang") == "en"])

    schema_edges_values = [row["schema_edges"] for row in schema_stats if isinstance(row.get("schema_edges"), int)]
    schema_edges_summary = _summary_min_median_max(schema_edges_values)

    text_summary = {
        "p50": _safe_percentile(text_lengths, 0.5),
        "p90": _safe_percentile(text_lengths, 0.9),
        "p99": _safe_percentile(text_lengths, 0.99),
    }

    core_candidates = _select_core_candidates(schema_stats, corpus_stats, coverage_stats, cfg)

    lines = [
        "# 数据集统计汇总",
        "",
        f"- 数据集数量: {total}",
        f"- RE 数量: {re_count}",
        f"- EE 数量: {ee_count}",
        f"- 中文数量: {zh_count}",
        f"- 英文数量: {en_count}",
        "",
        "## SchemaEdges 分布",
        f"- min/median/max: {schema_edges_summary}",
        "",
        "## 文本长度分布",
        f"- p50/p90/p99: {text_summary}",
        "",
        "## 推荐核心集候选",
    ]
    if core_candidates:
        lines.extend([f"- {name}" for name in core_candidates])
    else:
        lines.append("- 暂无满足条件的数据集。")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.info("汇总报告已输出: %s", path)


def _summary_min_median_max(values: List[int]) -> str:
    if not values:
        return "NA"
    return f"{min(values)}/{statistics.median(values)}/{max(values)}"


def _select_core_candidates(
    schema_stats: List[Dict[str, Any]],
    corpus_stats: List[Dict[str, Any]],
    coverage_stats: List[Dict[str, Any]],
    cfg: Dict[str, Any],
) -> List[str]:
    core_cfg = cfg.get("core_set", {})
    min_schema_edges = int(core_cfg.get("min_schema_edges", 5))
    max_schema_edges = int(core_cfg.get("max_schema_edges", 200))
    min_reachable = float(core_cfg.get("min_reachable_ratio", 0.4))
    min_docs = int(core_cfg.get("min_docs", 100))
    max_docs = int(core_cfg.get("max_docs", 100000))
    require_schema_file = bool(core_cfg.get("require_schema_file", True))

    coverage_map = {row["dataset"]: row for row in coverage_stats}
    corpus_map = {row["dataset"]: row for row in corpus_stats}
    core: List[str] = []

    for row in schema_stats:
        dataset = row.get("dataset")
        schema_edges = row.get("schema_edges")
        if not isinstance(schema_edges, int):
            continue
        if schema_edges < min_schema_edges or schema_edges > max_schema_edges:
            continue
        if require_schema_file and not row.get("schema_has_external_file"):
            continue

        corpus = corpus_map.get(dataset, {})
        doc_count = corpus.get("doc_count_dedup")
        if doc_count == "NA":
            doc_count = corpus.get("raw_records_count")
        if not isinstance(doc_count, int) or doc_count < min_docs or doc_count > max_docs:
            continue

        coverage = coverage_map.get(dataset, {})
        reachable_ratio = coverage.get("reachable_ratio_train")
        if isinstance(reachable_ratio, (int, float)) and reachable_ratio < min_reachable:
            continue

        core.append(dataset)

    return core


def main() -> None:
    config = load_yaml_config()
    run_benchmark_stats(config)


if __name__ == "__main__":
    main()
