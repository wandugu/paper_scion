"""输出论文复现实验参数统计。"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .common import load_yaml_config, resolve_project_path
from .logger import get_ot_logger


LOGGER = get_ot_logger()


def _get_nested(cfg: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = cfg
    for key in keys:
        if not isinstance(current, dict):
            return default
        current = current.get(key)
    return current if current is not None else default


def _resolve_llm_max_tokens(llm_cfg: Dict[str, Any]) -> int | None:
    provider = (llm_cfg.get("provider") or "").lower()
    LOGGER.debug("解析 LLM provider: %s", provider)
    provider_cfg = llm_cfg.get(provider) if provider else None
    if isinstance(provider_cfg, dict) and provider_cfg.get("max_tokens") is not None:
        return int(provider_cfg["max_tokens"])
    if provider == "openrouter":
        openrouter_cfg = llm_cfg.get("openrouter") or {}
        if openrouter_cfg.get("max_tokens") is not None:
            return int(openrouter_cfg["max_tokens"])
    if provider == "openai":
        openai_cfg = llm_cfg.get("openai") or {}
        if openai_cfg.get("max_tokens") is not None:
            return int(openai_cfg["max_tokens"])
    if provider == "deepseek":
        deepseek_cfg = llm_cfg.get("deepseek") or {}
        if deepseek_cfg.get("max_tokens") is not None:
            return int(deepseek_cfg["max_tokens"])
    return None


def collect_repro_settings(cfg: Dict[str, Any]) -> Dict[str, Any]:
    repro_cfg = cfg.get("repro_settings") or {}
    chunk_cfg = repro_cfg.get("chunking") or {}
    chunk_size = chunk_cfg.get("max_tokens_per_chunk")
    if chunk_size is None:
        chunk_size = _get_nested(cfg, "input", "chunk_size", default="")
        LOGGER.debug("未配置 max_tokens_per_chunk，回退 input.chunk_size=%s", chunk_size)
    overlap = chunk_cfg.get("overlap", 0)
    segmentation_rule = chunk_cfg.get(
        "segmentation_rule", "split on whitespace; accumulate char length until >= chunk_size"
    )

    nlp_cfg = repro_cfg.get("nlp_preprocessing") or {}
    candidate_cfg = repro_cfg.get("candidate_mining") or {}
    clustering_cfg = repro_cfg.get("clustering") or {}
    randomness_cfg = repro_cfg.get("randomness_control") or {}

    eval_cfg = cfg.get("evaluation") or {}
    llm_cfg = cfg.get("llm") or {}

    settings = {
        "chunking": {
            "max_tokens_per_chunk": chunk_size,
            "overlap": overlap,
            "segmentation_rule": segmentation_rule,
        },
        "nlp_preprocessing": {
            "sentence_splitter": nlp_cfg.get("sentence_splitter", "none"),
            "tokenizer_pos_dep_parser": nlp_cfg.get("tokenizer_pos_dep_parser", "none"),
        },
        "candidate_mining": {
            "term_extractor": candidate_cfg.get("term_extractor", "none"),
            "predicate_dep_patterns": candidate_cfg.get("predicate_dep_patterns", "none"),
            "event_sketches": candidate_cfg.get("event_sketches", "none"),
        },
        "clustering": {
            "embedding_model": clustering_cfg.get("embedding_model", "none"),
            "algorithm": clustering_cfg.get("algorithm", "none"),
            "cluster_selection": clustering_cfg.get("cluster_selection", "none"),
        },
        "fuzzy_threshold": float(eval_cfg.get("threshold", 0.45)),
        "graph_smoothing": {
            "alpha": float(eval_cfg.get("graph_smoothing_alpha", 0.5)),
            "K": int(eval_cfg.get("graph_smoothing_rounds", 2)),
        },
        "llm_decoding": {
            "temperature": float(llm_cfg.get("temperature", 0.0)),
            "top_p": float(llm_cfg.get("top_p", 1.0)),
            "max_tokens": _resolve_llm_max_tokens(llm_cfg),
        },
        "randomness_control": {
            "seeds": randomness_cfg.get("seeds", "not set"),
            "runs_per_source": randomness_cfg.get("runs_per_source", 1),
            "reported_aggregation": randomness_cfg.get("reported_aggregation", "single run"),
        },
    }

    LOGGER.debug("复现参数汇总: %s", settings)
    return settings


def format_text(settings: Dict[str, Any]) -> str:
    chunking = settings["chunking"]
    nlp = settings["nlp_preprocessing"]
    mining = settings["candidate_mining"]
    clustering = settings["clustering"]
    fuzzy = settings["fuzzy_threshold"]
    smoothing = settings["graph_smoothing"]
    llm = settings["llm_decoding"]
    random_ctrl = settings["randomness_control"]
    max_tokens = llm.get("max_tokens") if llm.get("max_tokens") is not None else "not set"
    return "\n".join(
        [
            (
                "Chunking: max tokens per chunk = {max_tokens}; overlap = {overlap}; "
                "segmentation rule = {segmentation_rule}."
            ).format(
                max_tokens=chunking["max_tokens_per_chunk"],
                overlap=chunking["overlap"],
                segmentation_rule=chunking["segmentation_rule"],
            ),
            (
                "NLP preprocessing: sentence splitter = {sentence_splitter}; "
                "tokenizer/POS/dep parser = {tokenizer_pos_dep_parser}."
            ).format(**nlp),
            (
                "Candidate mining: term extractor = {term_extractor}; predicate/dep patterns = "
                "{predicate_dep_patterns}; event sketches = {event_sketches}."
            ).format(**mining),
            (
                "Clustering: embedding model = {embedding_model}; algorithm = {algorithm}; "
                "#clusters selection = {cluster_selection}."
            ).format(**clustering),
            f"Fuzzy threshold: τ = {fuzzy}.",
            f"Graph smoothing: α = {smoothing['alpha']}, K = {smoothing['K']}.",
            f"LLM decoding: temperature = {llm['temperature']}; top_p = {llm['top_p']}; "
            f"max_tokens = {max_tokens}.",
            (
                "Randomness control: seed(s) = {seeds}; runs per source = {runs_per_source}; "
                "reported aggregation = {reported_aggregation}."
            ).format(**random_ctrl),
        ]
    )


def _default_output_dir(cfg: Dict[str, Any]) -> Path:
    output_cfg = (cfg.get("repro_settings") or {}).get("output") or {}
    default_dir = output_cfg.get("dir") or "data/dataset_stat/para_stat"
    return resolve_project_path(default_dir)


def _default_output_filename(cfg: Dict[str, Any], fmt: str) -> str:
    output_cfg = (cfg.get("repro_settings") or {}).get("output") or {}
    if fmt == "json":
        return output_cfg.get("json_filename") or "repro_settings.json"
    return output_cfg.get("text_filename") or "repro_settings.txt"


def _controllability_summary_cfg(cfg: Dict[str, Any]) -> Dict[str, Any]:
    stats_cfg = cfg.get("stats") or {}
    summary_cfg = stats_cfg.get("controllability_summary") or {}
    return summary_cfg if isinstance(summary_cfg, dict) else {}


def _efficiency_cost_cfg(cfg: Dict[str, Any]) -> Dict[str, Any]:
    stats_cfg = cfg.get("stats") or {}
    efficiency_cfg = stats_cfg.get("efficiency_cost") or {}
    return efficiency_cfg if isinstance(efficiency_cfg, dict) else {}


def _human_audit_cfg(cfg: Dict[str, Any]) -> Dict[str, Any]:
    stats_cfg = cfg.get("stats") or {}
    audit_cfg = stats_cfg.get("human_audit") or {}
    return audit_cfg if isinstance(audit_cfg, dict) else {}


def _resolve_controllability_input_dir(cfg: Dict[str, Any], input_dir: str | None = None) -> Path:
    summary_cfg = _controllability_summary_cfg(cfg)
    path_value = (
        input_dir or summary_cfg.get("input_dir") or "data/dataset_stat/para_stat/controllability_runs"
    )
    resolved = resolve_project_path(path_value)
    LOGGER.debug("Controllability 输入目录: %s", resolved)
    return resolved


def _resolve_efficiency_input_dir(cfg: Dict[str, Any], input_dir: str | None = None) -> Path:
    efficiency_cfg = _efficiency_cost_cfg(cfg)
    path_value = (
        input_dir
        or efficiency_cfg.get("input_dir")
        or "data/dataset_stat/para_stat/efficiency_runs"
    )
    resolved = resolve_project_path(path_value)
    LOGGER.debug("Efficiency/cost 输入目录: %s", resolved)
    return resolved


def _resolve_human_audit_input_dir(cfg: Dict[str, Any], input_dir: str | None = None) -> Path:
    audit_cfg = _human_audit_cfg(cfg)
    path_value = (
        input_dir or audit_cfg.get("input_dir") or "data/dataset_stat/para_stat/human_audit_pairs"
    )
    resolved = resolve_project_path(path_value)
    LOGGER.debug("Human audit 输入目录: %s", resolved)
    return resolved


def _resolve_controllability_output_dir(cfg: Dict[str, Any]) -> Path:
    summary_cfg = _controllability_summary_cfg(cfg)
    output_dir = (
        summary_cfg.get("output_dir") or "data/dataset_stat/para_stat/controllability_summary"
    )
    resolved = resolve_project_path(output_dir)
    LOGGER.debug("Controllability 输出目录: %s", resolved)
    return resolved


def _resolve_efficiency_output_dir(cfg: Dict[str, Any]) -> Path:
    efficiency_cfg = _efficiency_cost_cfg(cfg)
    output_dir = efficiency_cfg.get("output_dir") or "data/dataset_stat/para_stat/efficiency_cost"
    resolved = resolve_project_path(output_dir)
    LOGGER.debug("Efficiency/cost 输出目录: %s", resolved)
    return resolved


def _resolve_human_audit_output_dir(cfg: Dict[str, Any]) -> Path:
    audit_cfg = _human_audit_cfg(cfg)
    output_dir = audit_cfg.get("output_dir") or "data/dataset_stat/para_stat/human_audit"
    resolved = resolve_project_path(output_dir)
    LOGGER.debug("Human audit 输出目录: %s", resolved)
    return resolved


def _default_controllability_filename(cfg: Dict[str, Any], fmt: str) -> str:
    summary_cfg = _controllability_summary_cfg(cfg)
    if fmt == "json":
        return summary_cfg.get("json_filename") or "controllability_summary.json"
    return summary_cfg.get("text_filename") or "controllability_summary.txt"


def _default_efficiency_filename(cfg: Dict[str, Any], fmt: str) -> str:
    efficiency_cfg = _efficiency_cost_cfg(cfg)
    if fmt == "json":
        return efficiency_cfg.get("json_filename") or "efficiency_cost.json"
    return efficiency_cfg.get("text_filename") or "efficiency_cost.txt"


def _default_human_audit_filename(cfg: Dict[str, Any], fmt: str) -> str:
    audit_cfg = _human_audit_cfg(cfg)
    if fmt == "json":
        return audit_cfg.get("json_filename") or "human_audit.json"
    return audit_cfg.get("text_filename") or "human_audit.txt"


def _load_expected_datasets(cfg: Dict[str, Any]) -> List[str]:
    summary_cfg = _controllability_summary_cfg(cfg)
    datasets = summary_cfg.get("datasets")
    if isinstance(datasets, list) and datasets:
        expected = [str(item).strip() for item in datasets if str(item).strip()]
        LOGGER.debug("使用配置 datasets 过滤: %s", expected)
        return expected
    subset_dir_value = summary_cfg.get("subset_dir")
    if not subset_dir_value:
        return []
    subset_dir = resolve_project_path(subset_dir_value)
    if not subset_dir.exists():
        LOGGER.debug("subset_dir 不存在，跳过过滤: %s", subset_dir)
        return []
    subset_names = sorted([path.name for path in subset_dir.iterdir() if path.is_dir()])
    LOGGER.debug("从 subset_dir 收集 datasets: %s", subset_names)
    return subset_names


def _load_efficiency_settings(cfg: Dict[str, Any]) -> List[Dict[str, str]]:
    efficiency_cfg = _efficiency_cost_cfg(cfg)
    settings = efficiency_cfg.get("settings")
    if isinstance(settings, list) and settings:
        normalized = []
        for item in settings:
            if not isinstance(item, dict):
                continue
            key = str(item.get("key") or "").strip()
            label = str(item.get("label") or "").strip()
            if not key or not label:
                continue
            normalized.append({"key": key, "label": label})
        if normalized:
            LOGGER.debug("使用配置的 efficiency settings: %s", normalized)
            return normalized
    fallback = [
        {"key": "scion_o", "label": r"SCION ($\mathcal{O}$)"},
        {"key": "scion_o_fusion", "label": r"SCION ($\mathcal{O}_{\text{fusion}}$)"},
    ]
    LOGGER.debug("未配置 efficiency settings，使用默认设置: %s", fallback)
    return fallback


def _iter_controllability_files(
    cfg: Dict[str, Any], input_dir: Path, glob_pattern: str | None = None
) -> Iterable[Path]:
    summary_cfg = _controllability_summary_cfg(cfg)
    pattern = glob_pattern or summary_cfg.get("glob") or "**/controllability_stats.json"
    LOGGER.debug("Controllability 文件匹配模式: %s", pattern)
    return input_dir.glob(pattern)


def _iter_efficiency_files(
    cfg: Dict[str, Any], input_dir: Path, glob_pattern: str | None = None
) -> Iterable[Path]:
    efficiency_cfg = _efficiency_cost_cfg(cfg)
    pattern = glob_pattern or efficiency_cfg.get("glob") or "**/efficiency_stats.json"
    LOGGER.debug("Efficiency/cost 文件匹配模式: %s", pattern)
    return input_dir.glob(pattern)


def _iter_human_audit_files(
    cfg: Dict[str, Any], input_dir: Path, glob_pattern: str | None = None
) -> Iterable[Path]:
    audit_cfg = _human_audit_cfg(cfg)
    pattern = glob_pattern or audit_cfg.get("glob") or "**/mapping_pairs.json"
    LOGGER.debug("Human audit 文件匹配模式: %s", pattern)
    return input_dir.glob(pattern)


def _parse_efficiency_tokens(payload: Dict[str, Any]) -> tuple[int, int]:
    tokens_in = payload.get("tokens_in")
    tokens_out = payload.get("tokens_out")
    if tokens_in is not None or tokens_out is not None:
        return int(tokens_in or 0), int(tokens_out or 0)
    token_bundle = payload.get("tokens")
    if isinstance(token_bundle, dict):
        return int(token_bundle.get("input", 0)), int(token_bundle.get("output", 0))
    prompt_tokens = payload.get("prompt_tokens")
    completion_tokens = payload.get("completion_tokens")
    return int(prompt_tokens or 0), int(completion_tokens or 0)


def _normalize_efficiency_record(payload: Dict[str, Any], source: Path) -> Dict[str, Any] | None:
    setting = str(payload.get("setting") or payload.get("mode") or payload.get("name") or "").strip()
    if not setting:
        LOGGER.debug("跳过缺少 setting 的记录: %s", source)
        return None
    tokens_in, tokens_out = _parse_efficiency_tokens(payload)
    record = {
        "setting": setting,
        "dataset": str(payload.get("dataset") or "").strip(),
        "docs": int(payload.get("docs") or payload.get("documents") or 0),
        "chunks": int(payload.get("chunks") or payload.get("chunk_count") or 0),
        "llm_calls": int(payload.get("llm_calls") or payload.get("calls") or 0),
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "time_s": float(payload.get("time_s") or payload.get("elapsed_s") or payload.get("time") or 0.0),
        "cost": float(payload.get("cost") or payload.get("cost_usd") or 0.0),
    }
    LOGGER.debug("解析 efficiency 记录: %s", record)
    return record


def collect_efficiency_cost_summary(cfg: Dict[str, Any], input_dir: Path) -> Dict[str, Any]:
    efficiency_cfg = _efficiency_cost_cfg(cfg)
    dataset_label = efficiency_cfg.get("dataset_label") or "SCOPE (24)"
    aggregation = (efficiency_cfg.get("aggregation") or "total").lower()
    settings = _load_efficiency_settings(cfg)
    setting_keys = [item["key"] for item in settings]
    records: List[Dict[str, Any]] = []
    files: List[str] = []

    for stats_path in sorted(_iter_efficiency_files(cfg, input_dir)):
        try:
            payload = json.loads(stats_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            LOGGER.debug("跳过损坏文件: %s (%s)", stats_path, exc)
            continue
        files.append(str(stats_path))
        payload_records = payload.get("records") if isinstance(payload, dict) else None
        if isinstance(payload_records, list):
            LOGGER.debug("读取 efficiency records: %s (%s)", stats_path, len(payload_records))
            for item in payload_records:
                if not isinstance(item, dict):
                    continue
                record = _normalize_efficiency_record(item, stats_path)
                if record:
                    records.append(record)
            continue
        if isinstance(payload, dict):
            record = _normalize_efficiency_record(payload, stats_path)
            if record:
                records.append(record)
        elif isinstance(payload, list):
            for item in payload:
                if not isinstance(item, dict):
                    continue
                record = _normalize_efficiency_record(item, stats_path)
                if record:
                    records.append(record)

    LOGGER.debug("Efficiency/cost 汇总: files=%s records=%s", len(files), len(records))
    aggregates: Dict[str, Dict[str, Any]] = {}
    for key in setting_keys:
        aggregates[key] = {
            "docs": 0,
            "chunks": 0,
            "llm_calls": 0,
            "tokens_in": 0,
            "tokens_out": 0,
            "time_s": 0.0,
            "cost": 0.0,
            "records": 0,
        }

    for record in records:
        setting = record["setting"]
        if setting not in aggregates:
            LOGGER.debug("跳过未配置 setting: %s", setting)
            continue
        target = aggregates[setting]
        target["docs"] += record["docs"]
        target["chunks"] += record["chunks"]
        target["llm_calls"] += record["llm_calls"]
        target["tokens_in"] += record["tokens_in"]
        target["tokens_out"] += record["tokens_out"]
        target["time_s"] += record["time_s"]
        target["cost"] += record["cost"]
        target["records"] += 1
        LOGGER.debug("累计 setting=%s stats=%s", setting, target)

    if aggregation == "macro":
        for key, stats in aggregates.items():
            count = stats["records"] or 1
            LOGGER.debug("macro 平均: setting=%s records=%s", key, count)
            for field in ("docs", "chunks", "llm_calls", "tokens_in", "tokens_out"):
                stats[field] = round(stats[field] / count)
            stats["time_s"] = stats["time_s"] / count
            stats["cost"] = stats["cost"] / count

    summary = {
        "dataset_label": dataset_label,
        "aggregation": aggregation,
        "files": files,
        "settings": settings,
        "stats": aggregates,
    }
    LOGGER.debug("Efficiency/cost 汇总结果: %s", summary)
    return summary


def _normalize_human_audit_source(raw_source: str | None, fallback: str) -> str:
    source = str(raw_source or "").strip()
    if source:
        return source
    return fallback


def _collect_human_audit_pairs(
    cfg: Dict[str, Any], input_dir: Path
) -> tuple[Dict[str, List[Dict[str, Any]]], List[str]]:
    audit_cfg = _human_audit_cfg(cfg)
    synthetic_on_missing = bool(audit_cfg.get("synthetic_on_missing", False))
    synthetic_source = str(audit_cfg.get("synthetic_source") or "SyntheticSource")
    synthetic_pair = audit_cfg.get("synthetic_pair") or {
        "source_label": "EntityA",
        "target_label": "EntityB",
        "relation": "equivalent",
    }

    pairs_by_source: Dict[str, List[Dict[str, Any]]] = {}
    files: List[str] = []
    for stats_path in sorted(_iter_human_audit_files(cfg, input_dir)):
        try:
            payload = json.loads(stats_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            LOGGER.debug("跳过损坏文件: %s (%s)", stats_path, exc)
            continue
        files.append(str(stats_path))
        if isinstance(payload, dict):
            fallback_source = stats_path.parent.name
            source_value = payload.get("source") or payload.get("dataset") or payload.get("name")
            pairs = payload.get("pairs") or payload.get("mapping_pairs") or []
            if isinstance(pairs, list):
                for item in pairs:
                    if not isinstance(item, dict):
                        continue
                    source_name = _normalize_human_audit_source(
                        item.get("source") or source_value, fallback_source
                    )
                    pairs_by_source.setdefault(source_name, []).append(item)
            else:
                LOGGER.debug("human audit pairs 格式不符合 list: %s", stats_path)
        elif isinstance(payload, list):
            fallback_source = stats_path.parent.name
            for item in payload:
                if not isinstance(item, dict):
                    continue
                source_name = _normalize_human_audit_source(
                    item.get("source") or item.get("dataset"), fallback_source
                )
                pairs_by_source.setdefault(source_name, []).append(item)
        else:
            LOGGER.debug("human audit 文件格式不支持: %s", stats_path)

    if not pairs_by_source and synthetic_on_missing:
        LOGGER.warning("human audit 未找到数据，使用合成样本进行自测。")
        pairs_by_source[synthetic_source] = [
            {"source": synthetic_source, **synthetic_pair},
        ]

    LOGGER.debug(
        "human audit 读取完成: files=%s sources=%s",
        len(files),
        list(pairs_by_source.keys()),
    )
    return pairs_by_source, files


def collect_human_audit_summary(cfg: Dict[str, Any], input_dir: Path) -> Dict[str, Any]:
    audit_cfg = _human_audit_cfg(cfg)
    sample_per_source = int(audit_cfg.get("sample_per_source") or 0)
    sample_overall = int(audit_cfg.get("sample_overall") or 0)
    random_seed = audit_cfg.get("random_seed")
    rng = random.Random(random_seed)
    pairs_by_source, files = _collect_human_audit_pairs(cfg, input_dir)

    pair_counts = {source: len(pairs) for source, pairs in pairs_by_source.items()}
    total_pairs = sum(pair_counts.values())
    LOGGER.debug("human audit pairs 计数: %s (total=%s)", pair_counts, total_pairs)

    sampled_pairs_per_source: Dict[str, List[Dict[str, Any]]] = {}
    for source, pairs in pairs_by_source.items():
        if sample_per_source <= 0:
            sampled_pairs_per_source[source] = []
            continue
        sample_size = min(sample_per_source, len(pairs))
        sampled = rng.sample(pairs, sample_size) if sample_size else []
        sampled_pairs_per_source[source] = sampled
        LOGGER.debug("human audit 抽样: source=%s size=%s", source, sample_size)

    overall_pairs: List[Dict[str, Any]] = []
    for source, pairs in pairs_by_source.items():
        for item in pairs:
            record = dict(item)
            record.setdefault("source", source)
            overall_pairs.append(record)
    overall_sampled = []
    if sample_overall > 0 and overall_pairs:
        sample_size = min(sample_overall, len(overall_pairs))
        overall_sampled = rng.sample(overall_pairs, sample_size)
        LOGGER.debug("human audit overall 抽样: size=%s", sample_size)

    summary = {
        "sample_per_source": sample_per_source,
        "sample_overall": sample_overall,
        "random_seed": random_seed,
        "files": files,
        "pair_counts": pair_counts,
        "total_pairs": total_pairs,
        "sampled_pairs_per_source": sampled_pairs_per_source,
        "sampled_pairs_overall": overall_sampled,
    }
    LOGGER.debug("Human audit 汇总结果: %s", summary)
    return summary


def collect_controllability_summary(
    cfg: Dict[str, Any], input_dir: Path, expected_datasets: List[str]
) -> Dict[str, Any]:
    summary_cfg = _controllability_summary_cfg(cfg)
    dataset_label = summary_cfg.get("dataset_label") or "SCOPE (24)"
    totals = {
        "ontology": {"attempts": 0, "success": 0, "fallback": 0},
        "events": {"attempts": 0, "success": 0, "fallback": 0},
    }
    files: List[str] = []
    datasets: List[str] = []

    for stats_path in sorted(_iter_controllability_files(cfg, input_dir)):
        try:
            payload = json.loads(stats_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            LOGGER.debug("跳过损坏文件: %s (%s)", stats_path, exc)
            continue
        dataset = payload.get("dataset") or stats_path.parent.name
        if expected_datasets and dataset not in expected_datasets:
            LOGGER.debug("跳过非目标数据集: %s", dataset)
            continue
        files.append(str(stats_path))
        datasets.append(dataset)

        json_parse = payload.get("json_parse") or {}
        fallback = payload.get("fallback") or {}
        for section in ("ontology", "events"):
            section_parse = json_parse.get(section) or {}
            section_fallback = fallback.get(section) or {}
            totals[section]["attempts"] += int(section_parse.get("attempts", 0))
            totals[section]["success"] += int(section_parse.get("success", 0))
            totals[section]["fallback"] += int(section_fallback.get("count", 0))
            LOGGER.debug(
                "累计 %s: attempts=%s success=%s fallback=%s",
                section,
                totals[section]["attempts"],
                totals[section]["success"],
                totals[section]["fallback"],
            )

    LOGGER.debug("统计完成: files=%s datasets=%s", len(files), len(datasets))
    overall_attempts = totals["ontology"]["attempts"] + totals["events"]["attempts"]
    overall_success = totals["ontology"]["success"] + totals["events"]["success"]
    overall_fallback = totals["ontology"]["fallback"] + totals["events"]["fallback"]

    def _ratio(numerator: int, denominator: int) -> float:
        return round(numerator / denominator, 6) if denominator else 0.0

    summary = {
        "dataset_label": dataset_label,
        "expected_datasets": expected_datasets,
        "observed_datasets": datasets,
        "files": files,
        "module_stats": {
            "ontology": {
                "calls": totals["ontology"]["attempts"],
                "parse_success": _ratio(totals["ontology"]["success"], totals["ontology"]["attempts"]),
                "fallback_rate": _ratio(totals["ontology"]["fallback"], totals["ontology"]["attempts"]),
            },
            "events": {
                "calls": totals["events"]["attempts"],
                "parse_success": _ratio(totals["events"]["success"], totals["events"]["attempts"]),
                "fallback_rate": _ratio(totals["events"]["fallback"], totals["events"]["attempts"]),
            },
            "overall": {
                "calls": overall_attempts,
                "parse_success": _ratio(overall_success, overall_attempts),
                "fallback_rate": _ratio(overall_fallback, overall_attempts),
            },
        },
    }
    LOGGER.debug("Controllability 汇总结果: %s", summary)
    return summary


def _format_rate(value: float, precision: int) -> str:
    return f"{value:.{precision}f}"


def format_controllability_rows(summary: Dict[str, Any], precision: int) -> str:
    dataset_label = summary.get("dataset_label", "SCOPE (24)")
    module_stats = summary.get("module_stats") or {}
    rows = []
    for module_key, module_name in (
        ("ontology", "Ontology module"),
        ("events", "Event-schema module"),
        ("overall", "Overall"),
    ):
        stats = module_stats.get(module_key) or {}
        rows.append(
            " & ".join(
                [
                    dataset_label,
                    module_name,
                    str(stats.get("calls", 0)),
                    _format_rate(float(stats.get("parse_success", 0.0)), precision),
                    _format_rate(float(stats.get("fallback_rate", 0.0)), precision),
                ]
            )
            + r" \\"
        )
    return "\n".join(rows)


def _format_time(value: float, unit: str, precision: int) -> str:
    if unit == "min":
        return f"{value / 60:.{precision}f}m"
    if unit == "h":
        return f"{value / 3600:.{precision}f}h"
    return f"{value:.{precision}f}s"


def format_efficiency_cost_rows(summary: Dict[str, Any], cfg: Dict[str, Any]) -> str:
    efficiency_cfg = _efficiency_cost_cfg(cfg)
    time_unit = efficiency_cfg.get("time_unit") or "s"
    cost_unit = efficiency_cfg.get("cost_unit") or "USD"
    time_precision = int(efficiency_cfg.get("time_precision", 2))
    cost_precision = int(efficiency_cfg.get("cost_precision", 4))
    rows = []
    stats = summary.get("stats") or {}
    for setting in summary.get("settings") or []:
        key = setting["key"]
        label = setting["label"]
        data = stats.get(key) or {}
        tokens = f"{int(data.get('tokens_in', 0))}/{int(data.get('tokens_out', 0))}"
        time_value = _format_time(float(data.get("time_s", 0.0)), time_unit, time_precision)
        cost_value = f"{float(data.get('cost', 0.0)):.{cost_precision}f}"
        rows.append(
            " & ".join(
                [
                    label,
                    str(int(data.get("docs", 0))),
                    str(int(data.get("chunks", 0))),
                    str(int(data.get("llm_calls", 0))),
                    tokens,
                    f"{time_value} / {cost_value} {cost_unit}",
                ]
            )
            + r" \\"
        )
    return "\n".join(rows)


def format_human_audit_text(summary: Dict[str, Any]) -> str:
    sample_per_source = summary.get("sample_per_source", 0)
    sample_overall = summary.get("sample_overall", 0)
    total_pairs = summary.get("total_pairs", 0)
    source_count = len(summary.get("pair_counts") or {})
    return "\n".join(
        [
            "Human audit (estimated mapping precision)",
            f"- sample_per_source: {sample_per_source}",
            f"- sample_overall: {sample_overall}",
            f"- sources: {source_count}",
            f"- total_pairs: {total_pairs}",
        ]
    )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="统计复现实验参数。")
    parser.add_argument("--config", type=str, default=None, help="配置文件路径（默认读取 config/config.yaml）")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="输出格式，text 为可直接填写表格的文本。",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="可选输出文件路径；未指定时写入 repro_settings.output.dir",
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default=None,
        help="controllability 模式的输入目录（默认读取 stats.controllability_summary.input_dir）",
    )
    parser.add_argument(
        "--efficiency-input-dir",
        type=str,
        default=None,
        help="efficiency/cost 模式的输入目录（默认读取 stats.efficiency_cost.input_dir）",
    )
    parser.add_argument(
        "--human-audit-input-dir",
        type=str,
        default=None,
        help="human audit 模式的输入目录（默认读取 stats.human_audit.input_dir）",
    )
    return parser.parse_args()


def _resolve_para_stat_modes(cfg: Dict[str, Any]) -> List[str]:
    """解析统计模式配置（支持模式: repro / controllability / efficiency_cost / all）。"""
    modes_cfg = _get_nested(cfg, "stats", "para_stat", "modes", default=[])
    if isinstance(modes_cfg, str):
        modes = [modes_cfg]
    elif isinstance(modes_cfg, list):
        modes = [str(item).strip() for item in modes_cfg]
    else:
        modes = []

    normalized = []
    for mode in modes:
        if not mode:
            continue
        normalized.append(mode.lower())

    if not normalized or "all" in normalized:
        LOGGER.debug("para_stat 模式配置为空或包含 all，默认运行全部模式。")
        return ["repro", "controllability", "efficiency_cost"]

    supported = {"repro", "controllability", "efficiency_cost", "human_audit"}
    selected = [mode for mode in normalized if mode in supported]
    skipped = [mode for mode in normalized if mode not in supported]
    if skipped:
        LOGGER.debug("忽略不支持的 para_stat 模式: %s", skipped)
    if not selected:
        LOGGER.debug("未配置有效 para_stat 模式，默认运行全部模式。")
        return ["repro", "controllability", "efficiency_cost"]
    return selected


def _run_repro(cfg: Dict[str, Any], args: argparse.Namespace) -> None:
    settings = collect_repro_settings(cfg)
    if args.format == "json":
        payload = json.dumps(settings, ensure_ascii=False, indent=2)
    else:
        payload = format_text(settings)
    output_dir = _default_output_dir(cfg)
    output_filename = _default_output_filename(cfg, args.format)
    _write_payload(payload, args, output_dir, output_filename, "repro")


def _run_controllability(cfg: Dict[str, Any], args: argparse.Namespace) -> None:
    input_dir = _resolve_controllability_input_dir(cfg, args.input_dir)
    expected_datasets = _load_expected_datasets(cfg)
    summary = collect_controllability_summary(cfg, input_dir, expected_datasets)
    precision = int(_controllability_summary_cfg(cfg).get("rate_precision", 4))
    if args.format == "json":
        payload = json.dumps(summary, ensure_ascii=False, indent=2)
    else:
        payload = format_controllability_rows(summary, precision)
    output_dir = _resolve_controllability_output_dir(cfg)
    output_filename = _default_controllability_filename(cfg, args.format)
    _write_payload(payload, args, output_dir, output_filename, "controllability")


def _run_efficiency_cost(cfg: Dict[str, Any], args: argparse.Namespace) -> None:
    input_dir = _resolve_efficiency_input_dir(cfg, args.efficiency_input_dir)
    summary = collect_efficiency_cost_summary(cfg, input_dir)
    if args.format == "json":
        payload = json.dumps(summary, ensure_ascii=False, indent=2)
    else:
        payload = format_efficiency_cost_rows(summary, cfg)
    output_dir = _resolve_efficiency_output_dir(cfg)
    output_filename = _default_efficiency_filename(cfg, args.format)
    _write_payload(payload, args, output_dir, output_filename, "efficiency_cost")


def _run_human_audit(cfg: Dict[str, Any], args: argparse.Namespace) -> None:
    input_dir = _resolve_human_audit_input_dir(cfg, args.human_audit_input_dir)
    summary = collect_human_audit_summary(cfg, input_dir)
    if args.format == "json":
        payload = json.dumps(summary, ensure_ascii=False, indent=2)
    else:
        payload = format_human_audit_text(summary)
    output_dir = _resolve_human_audit_output_dir(cfg)
    output_filename = _default_human_audit_filename(cfg, args.format)
    _write_payload(payload, args, output_dir, output_filename, "human_audit")


def _write_payload(
    payload: str, args: argparse.Namespace, output_dir: Path, output_filename: str, mode: str
) -> None:
    print(payload)

    output_path = resolve_project_path(args.output) if args.output else output_dir / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    LOGGER.debug("[%s] 参数统计已写入: %s", mode, output_path)


def main() -> None:
    args = _parse_args()
    config_path = resolve_project_path(args.config) if args.config else None
    LOGGER.debug("加载配置文件: %s", config_path or "config/config.yaml")
    cfg = load_yaml_config(config_path)
    modes = _resolve_para_stat_modes(cfg)
    LOGGER.debug("para_stat 将运行模式: %s", modes)
    for mode in modes:
        if mode == "repro":
            _run_repro(cfg, args)
        elif mode == "controllability":
            _run_controllability(cfg, args)
        elif mode == "efficiency_cost":
            _run_efficiency_cost(cfg, args)
        elif mode == "human_audit":
            _run_human_audit(cfg, args)


if __name__ == "__main__":
    main()
