"""输出论文复现实验参数统计。"""

from __future__ import annotations

import argparse
import json
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


def _resolve_controllability_input_dir(cfg: Dict[str, Any], input_dir: str | None = None) -> Path:
    summary_cfg = _controllability_summary_cfg(cfg)
    path_value = (
        input_dir or summary_cfg.get("input_dir") or "data/dataset_stat/para_stat/controllability_runs"
    )
    resolved = resolve_project_path(path_value)
    LOGGER.debug("Controllability 输入目录: %s", resolved)
    return resolved


def _resolve_controllability_output_dir(cfg: Dict[str, Any]) -> Path:
    summary_cfg = _controllability_summary_cfg(cfg)
    output_dir = (
        summary_cfg.get("output_dir") or "data/dataset_stat/para_stat/controllability_summary"
    )
    resolved = resolve_project_path(output_dir)
    LOGGER.debug("Controllability 输出目录: %s", resolved)
    return resolved


def _default_controllability_filename(cfg: Dict[str, Any], fmt: str) -> str:
    summary_cfg = _controllability_summary_cfg(cfg)
    if fmt == "json":
        return summary_cfg.get("json_filename") or "controllability_summary.json"
    return summary_cfg.get("text_filename") or "controllability_summary.txt"


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


def _iter_controllability_files(
    cfg: Dict[str, Any], input_dir: Path, glob_pattern: str | None = None
) -> Iterable[Path]:
    summary_cfg = _controllability_summary_cfg(cfg)
    pattern = glob_pattern or summary_cfg.get("glob") or "**/controllability_stats.json"
    LOGGER.debug("Controllability 文件匹配模式: %s", pattern)
    return input_dir.glob(pattern)


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
    return parser.parse_args()


def _resolve_para_stat_modes(cfg: Dict[str, Any]) -> List[str]:
    """解析统计模式配置（支持模式: repro / controllability / all）。"""
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
        return ["repro", "controllability"]

    supported = {"repro", "controllability"}
    selected = [mode for mode in normalized if mode in supported]
    skipped = [mode for mode in normalized if mode not in supported]
    if skipped:
        LOGGER.debug("忽略不支持的 para_stat 模式: %s", skipped)
    if not selected:
        LOGGER.debug("未配置有效 para_stat 模式，默认运行全部模式。")
        return ["repro", "controllability"]
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


if __name__ == "__main__":
    main()
