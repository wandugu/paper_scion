"""命令行工具：对比预测与金标准本体，输出多种评测指标。

参数全部来自 ``config/config.yaml``，无需再传入命令行参数。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from utils.common import load_yaml_config, resolve_project_path, save_json
from utils.dataset_paths import resolve_dataset_paths
from utils.ontology_eval import compute_ontology_metrics, load_schema_file, schema_dict_to_graph

CONFIG = load_yaml_config()


SUPPORTED_LANG_CODES = {"zh", "en"}


def _language_code() -> str:
    lang_cfg = CONFIG.get("language")
    if isinstance(lang_cfg, dict):
        raw_code = lang_cfg.get("code")
    else:
        raw_code = lang_cfg
    code = str(raw_code or "zh").lower()
    return code if code in SUPPORTED_LANG_CODES else "zh"


LANGUAGE_CODE = _language_code()
LANGUAGE_SUFFIX = f"_{LANGUAGE_CODE}"


def _apply_language_suffix(path: Path) -> Path:
    suffix = LANGUAGE_SUFFIX
    ext = path.suffix
    target_suffix = f"{suffix}{ext}" if ext else suffix
    if path.name.endswith(target_suffix):
        return path
    if ext:
        return path.with_name(f"{path.stem}{suffix}{ext}")
    return path.with_name(f"{path.name}{suffix}")


def evaluation_config() -> Dict:
    cfg = CONFIG.get("evaluation")
    return cfg if isinstance(cfg, dict) else {}


def _selected_dataset_name() -> str:
    cfg = evaluation_config()
    dataset = cfg.get("dataset_name") or cfg.get("dataset")
    if dataset:
        return str(dataset).strip()
    input_cfg = CONFIG.get("input") or {}
    dataset = input_cfg.get("dataset_name")
    return str(dataset).strip() if dataset else ""


def _resolve_pred_schema_path() -> Path:
    eval_cfg = evaluation_config()
    raw_pred = eval_cfg.get("pred_schema_path")
    if raw_pred:
        return resolve_project_path(raw_pred)

    output_cfg = CONFIG.get("output", {})
    base_dir = resolve_project_path(output_cfg.get("dir", "output"))
    schema_name = output_cfg.get("schema_filename", "ontology_schema.json")
    return _apply_language_suffix(base_dir / schema_name)


def _resolve_golden_schema_path(dataset_name: str) -> Path:
    eval_cfg = evaluation_config()
    raw_gold = eval_cfg.get("golden_schema_path")
    if raw_gold:
        return resolve_project_path(raw_gold)
    if not dataset_name:
        raise ValueError("未配置 dataset_name，无法推断金标准本体路径。")
    schema_path, _ = resolve_dataset_paths(CONFIG, dataset_name)
    return schema_path


def evaluation_output_path(base_dir: Path) -> Path:
    cfg = evaluation_config()
    raw_path = cfg.get("output_json")
    if isinstance(raw_path, str) and raw_path.strip():
        return resolve_project_path(raw_path)
    filename = f"ontology_eval_metrics{LANGUAGE_SUFFIX}.json"
    return base_dir / filename


def _coerce_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def main() -> None:
    eval_cfg = evaluation_config()
    dataset_name = _selected_dataset_name()
    gold_schema_path = _resolve_golden_schema_path(dataset_name)
    pred_schema_path = _resolve_pred_schema_path()

    gold_schema = load_schema_file(gold_schema_path)
    pred_schema = load_schema_file(pred_schema_path)

    gold_graph = schema_dict_to_graph(gold_schema)
    pred_graph = schema_dict_to_graph(pred_schema)

    metrics = compute_ontology_metrics(
        gold_graph=gold_graph,
        pred_graph=pred_graph,
        emb_model=str(eval_cfg.get("emb_model") or "BAAI/bge-m3"),
        threshold=_coerce_float(eval_cfg.get("threshold"), 0.45),
        graph_smoothing_rounds=_coerce_int(eval_cfg.get("graph_smoothing_rounds"), 2),
        graph_smoothing_alpha=_coerce_float(eval_cfg.get("graph_smoothing_alpha"), 0.5),
    )

    for name, result in metrics.items():
        print(
            f"[{name}] Precision={result['precision']:.4f} "
            f"Recall={result['recall']:.4f} F1={result['f1']:.4f}"
        )

    output_dir = resolve_project_path(CONFIG.get("output", {}).get("dir", "output"))
    output_path = evaluation_output_path(output_dir)
    save_json(output_path, metrics)
    print(f"评测指标已写入: {output_path}")


if __name__ == "__main__":
    main()
