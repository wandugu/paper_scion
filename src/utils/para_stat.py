"""输出论文复现实验参数统计。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

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
    default_dir = output_cfg.get("dir") or "data/dtaset_stat/para_stat"
    return resolve_project_path(default_dir)


def _default_output_filename(cfg: Dict[str, Any], fmt: str) -> str:
    output_cfg = (cfg.get("repro_settings") or {}).get("output") or {}
    if fmt == "json":
        return output_cfg.get("json_filename") or "repro_settings.json"
    return output_cfg.get("text_filename") or "repro_settings.txt"


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
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    config_path = resolve_project_path(args.config) if args.config else None
    LOGGER.debug("加载配置文件: %s", config_path or "config/config.yaml")
    cfg = load_yaml_config(config_path)
    settings = collect_repro_settings(cfg)

    if args.format == "json":
        payload = json.dumps(settings, ensure_ascii=False, indent=2)
    else:
        payload = format_text(settings)

    print(payload)

    output_dir = _default_output_dir(cfg)
    output_filename = _default_output_filename(cfg, args.format)
    output_path = resolve_project_path(args.output) if args.output else output_dir / output_filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")
    LOGGER.debug("参数统计已写入: %s", output_path)


if __name__ == "__main__":
    main()
