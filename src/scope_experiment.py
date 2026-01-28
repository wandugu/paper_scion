"""构建 SCOPE 训练/验证数据集的脚本。"""

from __future__ import annotations

import copy
import logging
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple

from .utils.common import load_yaml_config, resolve_project_path, save_json
from .utils.logger import get_ot_logger
from .utils.scope_dataset_utils import (
    build_scope_background_text,
    load_scope_docs,
    safe_json_load,
    schema_from_doc_records,
    write_jsonl,
)


CONFIG = load_yaml_config()
LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


def _scope_experiment_config(config: Dict[str, Any]) -> Dict[str, Any]:
    cfg = config.get("scope_experiment")
    if isinstance(cfg, dict):
        return cfg
    return {}


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _list_str(value: Any, default: Sequence[str]) -> List[str]:
    if isinstance(value, list) and value:
        return [str(item) for item in value if str(item).strip()]
    return list(default)


def _coerce_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def _load_split(
    scope_root: Path,
    split_cfg: Dict[str, Any],
    text_fields: Sequence[str],
    split_label: str,
) -> Tuple[List[Dict[str, Any]], str, Dict[str, Any]]:
    part = split_cfg.get("part", "scope")
    name = split_cfg.get("name")
    split = split_cfg.get("split", "train")
    max_docs = _coerce_int(split_cfg.get("max_docs"))
    LOGGER.debug(
        "加载 scope split=%s: part=%s name=%s split_key=%s max_docs=%s",
        split_label,
        part,
        name,
        split,
        max_docs,
    )
    docs = load_scope_docs(scope_root, part, name, split, max_docs=max_docs)
    text_blob = build_scope_background_text(docs, text_fields)
    meta = {
        "part": part,
        "name": name,
        "split": split,
        "max_docs": max_docs,
        "doc_count": len(docs),
        "text_count": len([text for text in text_blob.split("\n\n") if text.strip()]),
    }
    LOGGER.debug("scope split=%s 元信息: %s", split_label, meta)
    return docs, text_blob, meta


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    LOGGER.debug("写入文本文件: %s (chars=%s)", path, len(text))


def _export_train_validation(exp_cfg: Dict[str, Any]) -> None:
    scope_root = resolve_project_path(exp_cfg.get("root_dir", "data/scope"))
    output_dir = resolve_project_path(exp_cfg.get("output_dir", "data/output/scope_experiment"))
    text_fields = _list_str(exp_cfg.get("text_fields"), ["text", "input"])
    output_files = exp_cfg.get("output_files") or {}
    train_jsonl = output_files.get("train_jsonl", "train.jsonl")
    val_jsonl = output_files.get("validation_jsonl", "validation.jsonl")
    train_text = output_files.get("train_text", "train_text.txt")
    val_text = output_files.get("validation_text", "validation_text.txt")
    summary_json = output_files.get("summary_json", "summary.json")

    LOGGER.debug("scope_experiment root_dir=%s output_dir=%s", scope_root, output_dir)
    LOGGER.debug("scope_experiment text_fields=%s", text_fields)

    train_docs, train_text_blob, train_meta = _load_split(
        scope_root,
        exp_cfg.get("train") or {},
        text_fields,
        "train",
    )
    val_docs, val_text_blob, val_meta = _load_split(
        scope_root,
        exp_cfg.get("validation") or {},
        text_fields,
        "validation",
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(output_dir / train_jsonl, train_docs)
    write_jsonl(output_dir / val_jsonl, val_docs)
    _write_text(output_dir / train_text, train_text_blob)
    _write_text(output_dir / val_text, val_text_blob)

    summary = {
        "scope_root": str(scope_root),
        "output_dir": str(output_dir),
        "text_fields": text_fields,
        "train": train_meta,
        "validation": val_meta,
        "output_files": {
            "train_jsonl": train_jsonl,
            "validation_jsonl": val_jsonl,
            "train_text": train_text,
            "validation_text": val_text,
            "summary_json": summary_json,
        },
    }
    save_json(output_dir / summary_json, summary)
    LOGGER.info("SCOPE 训练/验证数据已输出到: %s", output_dir)


def _write_eval_metrics(path: Path, metrics: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    save_json(path, metrics)
    LOGGER.info("评测指标已写入: %s", path)


def _format_metric(value: float | None, precision: int) -> str:
    if value is None:
        return "--"
    return f"{value:.{precision}f}"


def _macro_average(records: Sequence[Dict[str, Any]]) -> Dict[str, float] | None:
    precisions: List[float] = []
    recalls: List[float] = []
    f1s: List[float] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        precision = record.get("precision")
        recall = record.get("recall")
        f1 = record.get("f1")
        if isinstance(precision, (int, float)) and isinstance(recall, (int, float)) and isinstance(f1, (int, float)):
            precisions.append(float(precision))
            recalls.append(float(recall))
            f1s.append(float(f1))
    if not precisions:
        return None
    return {
        "precision": sum(precisions) / len(precisions),
        "recall": sum(recalls) / len(recalls),
        "f1": sum(f1s) / len(f1s),
    }


def _extract_prf(payload: Any) -> Dict[str, float] | None:
    if payload is None:
        return None
    if isinstance(payload, dict):
        for key in ("instance_level", "macro", "metrics", "metric"):
            nested = payload.get(key)
            if isinstance(nested, dict):
                nested_prf = _extract_prf(nested)
                if nested_prf:
                    return nested_prf
        if all(key in payload for key in ("precision", "recall", "f1")):
            precision = payload.get("precision")
            recall = payload.get("recall")
            f1 = payload.get("f1")
            if isinstance(precision, (int, float)) and isinstance(recall, (int, float)) and isinstance(f1, (int, float)):
                return {
                    "precision": float(precision),
                    "recall": float(recall),
                    "f1": float(f1),
                }
        records = payload.get("records")
        if isinstance(records, list):
            return _macro_average(records)
    if isinstance(payload, list):
        return _macro_average(payload)
    return None


def _load_instance_metrics(metrics_path: Path) -> Dict[str, float] | None:
    if not metrics_path.exists():
        LOGGER.debug("metrics 文件不存在: %s", metrics_path)
        return None
    payload = safe_json_load(metrics_path)
    LOGGER.debug("加载 metrics 文件: %s", metrics_path)
    return _extract_prf(payload)


def _run_downstream_extraction(exp_cfg: Dict[str, Any]) -> None:
    downstream_cfg = exp_cfg.get("downstream_extraction") or {}
    output_dir = resolve_project_path(
        downstream_cfg.get("output_dir", exp_cfg.get("output_dir", "data/output/scope_experiment"))
    )
    output_table_json = str(downstream_cfg.get("output_table_json", "downstream_extraction_table.json"))
    output_table_tex = str(downstream_cfg.get("output_table_tex", "downstream_extraction_table.tex"))
    precision = int(downstream_cfg.get("metrics_precision", 4))
    synthetic_on_missing = _coerce_bool(downstream_cfg.get("synthetic_on_missing"), True)
    synthetic_metrics = downstream_cfg.get("synthetic_metrics") or {}
    default_precision = float(synthetic_metrics.get("precision", 0.5))
    default_recall = float(synthetic_metrics.get("recall", 0.5))
    default_f1 = float(synthetic_metrics.get("f1", 0.5))

    schema_sources = downstream_cfg.get("schema_sources")
    if not isinstance(schema_sources, list) or not schema_sources:
        LOGGER.warning("未配置 schema_sources，使用合成示例数据生成表格。")
        schema_sources = [
            {
                "name": "GraphMaker (manual schema)",
                "extractor": "LLM",
                "metrics_path": None,
            }
        ]

    rows: List[Dict[str, Any]] = []
    for source in schema_sources:
        if not isinstance(source, dict):
            continue
        name = str(source.get("name") or "").strip() or "Unnamed"
        extractor = str(source.get("extractor") or "").strip()
        metrics_path = source.get("metrics_path")
        metrics_path_resolved = resolve_project_path(metrics_path) if metrics_path else None
        metrics = None
        if metrics_path_resolved:
            LOGGER.debug("读取 schema source=%s metrics_path=%s", name, metrics_path_resolved)
            metrics = _load_instance_metrics(metrics_path_resolved)
        if metrics is None and synthetic_on_missing:
            LOGGER.debug("使用合成 metrics: schema_source=%s", name)
            metrics = {"precision": default_precision, "recall": default_recall, "f1": default_f1}
        if metrics is None:
            LOGGER.debug("metrics 缺失，输出占位: schema_source=%s", name)
        rows.append(
            {
                "schema_source": name,
                "extractor": extractor,
                "precision": metrics.get("precision") if metrics else None,
                "recall": metrics.get("recall") if metrics else None,
                "f1": metrics.get("f1") if metrics else None,
            }
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    table_payload = {
        "rows": rows,
        "metrics_precision": precision,
        "output_table_tex": output_table_tex,
    }
    save_json(output_dir / output_table_json, table_payload)
    LOGGER.info("downstream 表格 JSON 输出: %s", output_dir / output_table_json)

    latex_lines = [
        "\\begin{table*}[t]",
        "\\centering",
        "\\caption{Downstream instance-level extraction under different schemas, aggregated over SCOPE (report macro-averaged P/R/F1 over sources).}",
        "\\label{tab:downstream_extraction}",
        "\\small",
        "\\begin{tabular}{l l c c c}",
        "\\toprule",
        "Schema Source & Extractor & P & R & F1 \\\\",
        "\\midrule",
    ]
    for row in rows:
        latex_lines.append(
            "{schema} & {extractor} & {p} & {r} & {f1} \\\\".format(
                schema=row["schema_source"],
                extractor=row["extractor"],
                p=_format_metric(row.get("precision"), precision),
                r=_format_metric(row.get("recall"), precision),
                f1=_format_metric(row.get("f1"), precision),
            )
        )
    latex_lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table*}"])
    (output_dir / output_table_tex).write_text("\n".join(latex_lines) + "\n", encoding="utf-8")
    LOGGER.info("downstream 表格 LaTeX 输出: %s", output_dir / output_table_tex)


def _run_eval_mode(exp_cfg: Dict[str, Any]) -> None:
    eval_cfg = exp_cfg.get("eval") or {}
    scope_root = resolve_project_path(exp_cfg.get("root_dir", "data/scope"))
    eval_part = eval_cfg.get("part", "scope")
    eval_name = eval_cfg.get("name")
    eval_split = eval_cfg.get("split", "test")
    eval_max_docs = _coerce_int(eval_cfg.get("max_docs"))
    text_fields = _list_str(eval_cfg.get("text_fields") or exp_cfg.get("text_fields"), ["text", "input"])

    LOGGER.debug(
        "scope_experiment eval 参数: part=%s name=%s split=%s max_docs=%s",
        eval_part,
        eval_name,
        eval_split,
        eval_max_docs,
    )

    docs, _, eval_meta = _load_split(
        scope_root,
        {
            "part": eval_part,
            "name": eval_name,
            "split": eval_split,
            "max_docs": eval_max_docs,
        },
        text_fields,
        "eval",
    )

    use_heuristic = _coerce_bool(eval_cfg.get("use_heuristic_schema"), True)
    output_dir = resolve_project_path(eval_cfg.get("output_dir", exp_cfg.get("output_dir", "data/output/scope_experiment")))
    schema_filename = eval_cfg.get("schema_filename", "ontology_schema_scope.json")
    pred_schema_path = resolve_project_path(eval_cfg.get("pred_schema_path") or (output_dir / schema_filename))
    golden_schema_path = eval_cfg.get("golden_schema_path")
    metrics_path = resolve_project_path(eval_cfg.get("metrics_path") or (output_dir / "ontology_eval_metrics.json"))
    metrics_mode = str(eval_cfg.get("metrics_mode", "auto")).strip().lower()

    LOGGER.debug(
        "eval 输出路径: output_dir=%s pred_schema=%s gold_schema=%s metrics=%s mode=%s heuristic=%s",
        output_dir,
        pred_schema_path,
        golden_schema_path,
        metrics_path,
        metrics_mode,
        use_heuristic,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    if use_heuristic:
        pred_schema = schema_from_doc_records(docs)
        save_json(pred_schema_path, pred_schema)
        LOGGER.info("已基于 docs.%s.jsonl 生成预测本体: %s", eval_split, pred_schema_path)
    else:
        from . import ontology_generate

        override_config = copy.deepcopy(CONFIG)
        override_config.setdefault("input", {})
        override_config["input"]["type"] = "scope"
        override_config["input"]["scope"] = {
            "root_dir": str(scope_root),
            "part": eval_part,
            "name": eval_name,
            "split": eval_split,
            "text_fields": text_fields,
            "max_docs": eval_max_docs,
        }
        override_config.setdefault("output", {})
        override_config["output"]["dir"] = str(output_dir)
        override_config["output"]["schema_filename"] = str(schema_filename)
        override_config.setdefault("evaluation", {})
        if golden_schema_path:
            override_config["evaluation"]["golden_schema_path"] = str(golden_schema_path)
        override_config["evaluation"]["output_json"] = str(metrics_path)
        override_config["evaluation"]["enabled"] = True
        ontology_generate.CONFIG = override_config
        LOGGER.info("开始基于 LLM 抽取本体 (scope test)...")
        ontology_generate.main()
        pred_schema_path = resolve_project_path(output_dir / schema_filename)

    if not golden_schema_path:
        raise ValueError("eval 模式需要配置 scope_experiment.eval.golden_schema_path")

    from . import ontology_eval
    from .utils.ontology_graph import schema_dict_to_graph

    try:
        gold_schema = ontology_eval.load_schema_file(resolve_project_path(golden_schema_path))
        pred_schema = ontology_eval.load_schema_file(pred_schema_path)
    except Exception as exc:  # noqa: BLE001
        LOGGER.exception("加载 schema 失败: %s", exc)
        raise

    LOGGER.debug(
        "schema 加载完成: gold_entities=%s gold_relationships=%s pred_entities=%s pred_relationships=%s",
        len(gold_schema.get("entities", [])),
        len(gold_schema.get("relationships", [])),
        len(pred_schema.get("entities", [])),
        len(pred_schema.get("relationships", [])),
    )

    gold_graph = schema_dict_to_graph(gold_schema)
    pred_graph = schema_dict_to_graph(pred_schema)

    if metrics_mode in {"lite", "literal"}:
        literal_p, literal_r, literal_f = ontology_eval.literal_f1(gold_graph, pred_graph)
        metrics = {"literal": {"precision": literal_p, "recall": literal_r, "f1": literal_f}}
        _write_eval_metrics(metrics_path, metrics)
        return

    try:
        eval_config = copy.deepcopy(CONFIG)
        eval_config.setdefault("evaluation", {})
        eval_config["evaluation"]["golden_schema_path"] = str(golden_schema_path)
        eval_config["evaluation"]["pred_schema_path"] = str(pred_schema_path)
        eval_config["evaluation"]["output_json"] = str(metrics_path)
        ontology_eval.CONFIG = eval_config
        if metrics_mode == "full":
            ontology_eval.main()
        else:
            ontology_eval.main()
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("完整评测失败，回退到 literal 指标: %s", exc)
        literal_p, literal_r, literal_f = ontology_eval.literal_f1(gold_graph, pred_graph)
        metrics = {"literal": {"precision": literal_p, "recall": literal_r, "f1": literal_f}}
        _write_eval_metrics(metrics_path, metrics)
        return

    LOGGER.info("评测完成: %s", metrics_path)


def main() -> None:
    exp_cfg = _scope_experiment_config(CONFIG)
    if not exp_cfg:
        raise ValueError("未在 config 中找到 scope_experiment 配置")

    mode = str(exp_cfg.get("mode", "eval")).strip().lower()
    LOGGER.info("scope_experiment mode=%s", mode)

    if mode == "train":
        LOGGER.warning("train 模式尚未实现（需要模型训练与 loss 计算）。")
        return
    if mode == "eval":
        _run_eval_mode(exp_cfg)
        return
    if mode == "downstream":
        _run_downstream_extraction(exp_cfg)
        return

    LOGGER.info("未识别 mode=%s，默认执行训练/验证集导出。", mode)
    _export_train_validation(exp_cfg)


if __name__ == "__main__":
    main()
