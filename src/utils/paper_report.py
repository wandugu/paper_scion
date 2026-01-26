"""论文数据报告工具。"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .common import apply_language_suffix, load_yaml_config, resolve_project_path, save_json
from .dataset_paths import dataset_is_relation_only, resolve_dataset_paths
from .logger import get_ot_logger
from .ontology_graph import schema_dict_to_graph
from .scope_dataset_utils import (
    extract_ee_schema_edges,
    extract_re_schema_edges,
    parse_ee_samples,
    parse_re_samples,
    safe_json_load,
)

try:  # optional heavy deps
    from .. import ontology_eval
except Exception:  # pragma: no cover - optional dependency guard
    ontology_eval = None  # type: ignore[assignment]


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


@dataclass
class PaperReportOverrides:
    dataset_name: Optional[str] = None
    pred_schema_path: Optional[Path] = None
    gold_schema_path: Optional[Path] = None
    samples_path: Optional[Path] = None
    output_dir: Optional[Path] = None
    skip_fuzzy: bool = False


def _selected_dataset_name(config: Dict[str, Any]) -> str:
    dataset_cfg = config.get("dataset") or {}
    dataset = dataset_cfg.get("name") or dataset_cfg.get("dataset_name")
    if dataset:
        return str(dataset).strip()

    eval_cfg = config.get("evaluation") or {}
    dataset = eval_cfg.get("dataset_name") or eval_cfg.get("dataset")
    if dataset:
        return str(dataset).strip()

    input_cfg = config.get("input") or {}
    dataset = input_cfg.get("dataset_name")
    return str(dataset).strip() if dataset else ""


def _language_code(config: Dict[str, Any]) -> str:
    lang_cfg = config.get("language")
    if isinstance(lang_cfg, dict):
        raw_code = lang_cfg.get("code")
    else:
        raw_code = lang_cfg
    code = str(raw_code or "zh").lower()
    return code if code in {"zh", "en"} else "zh"


def _normalize_schema_path(path: Path, language: str) -> Path:
    return apply_language_suffix(path, language)


def _default_pred_schema_path(config: Dict[str, Any], dataset_name: str, language: str) -> Path:
    report_cfg = config.get("paper_report") or {}
    schema_cfg = report_cfg.get("schema") or {}
    raw_path = schema_cfg.get("pred_path")
    if raw_path:
        return resolve_project_path(raw_path)
    output_cfg = config.get("output") or {}
    base_dir = resolve_project_path(output_cfg.get("dir", "data/output"))
    filename = output_cfg.get("schema_filename", "ontology_schema.json")
    return _normalize_schema_path(base_dir / filename, language)


def _default_gold_schema_path(config: Dict[str, Any], dataset_name: str, language: str) -> Path:
    report_cfg = config.get("paper_report") or {}
    schema_cfg = report_cfg.get("schema") or {}
    raw_path = schema_cfg.get("gold_path")
    if raw_path:
        return resolve_project_path(raw_path)
    if dataset_name:
        schema_path, _ = resolve_dataset_paths(config, dataset_name)
        return schema_path
    output_cfg = config.get("output") or {}
    base_dir = resolve_project_path(output_cfg.get("dir", "data/output"))
    filename = output_cfg.get("schema_filename", "ontology_schema.json")
    return _normalize_schema_path(base_dir / filename, language)


def _default_samples_path(config: Dict[str, Any], dataset_name: str) -> Optional[Path]:
    report_cfg = config.get("paper_report") or {}
    samples_cfg = report_cfg.get("samples") or {}
    raw_path = samples_cfg.get("path")
    if raw_path:
        return resolve_project_path(raw_path)
    if not dataset_name:
        return None
    _, samples_path = resolve_dataset_paths(config, dataset_name)
    return samples_path


def _load_schema(path: Path, label: str) -> Dict[str, Any]:
    if not path.exists():
        LOGGER.warning("%s schema 未找到: %s", label, path)
        return {}
    payload = safe_json_load(path)
    if not isinstance(payload, dict):
        LOGGER.warning("%s schema 格式异常: %s", label, path)
        return {}
    return payload


def _schema_stats(schema_payload: Dict[str, Any]) -> Dict[str, Any]:
    rel_types, ent_types, re_edges = extract_re_schema_edges(schema_payload)
    event_types, roles, ee_edges = extract_ee_schema_edges(schema_payload)
    graph = schema_dict_to_graph(schema_payload)
    return {
        "relation_types": sorted(rel_types),
        "entity_types": sorted(ent_types),
        "event_types": sorted(event_types),
        "roles": sorted(roles),
        "re_edges": sorted(re_edges),
        "ee_edges": sorted(ee_edges),
        "counts": {
            "relation_types": len(rel_types),
            "entity_types": len(ent_types),
            "event_types": len(event_types),
            "roles": len(roles),
            "re_edges": len(re_edges),
            "ee_edges": len(ee_edges),
            "graph_nodes": len(graph.nodes),
            "graph_edges": len(graph.edges),
        },
    }


def _sample_stats(
    config: Dict[str, Any],
    dataset_name: str,
    samples_path: Optional[Path],
) -> Dict[str, Any]:
    stats_cfg = (config.get("paper_report") or {}).get("sample_stats") or {}
    dedup_by_text = bool(stats_cfg.get("dedup_by_text", True))
    cross_dataset_dedup = bool(stats_cfg.get("cross_dataset_dedup", False))
    synthetic_on_missing = bool(stats_cfg.get("synthetic_on_missing", False))
    synthetic_text = str(stats_cfg.get("synthetic_text") or "Synthetic sample for paper report")
    synthetic_relation = str(stats_cfg.get("synthetic_relation") or "related_to")
    synthetic_event_type = str(stats_cfg.get("synthetic_event_type") or "SyntheticEvent")
    synthetic_role = str(stats_cfg.get("synthetic_role") or "Participant")
    synthetic_used = False
    if not samples_path:
        LOGGER.warning("未提供 samples_path，跳过样本统计")
        return {
            "sample_count": 0,
            "doc_count": 0,
            "dedup_by_text": dedup_by_text,
            "cross_dataset_dedup": cross_dataset_dedup,
            "samples_path": None,
        }
    if not samples_path.exists():
        LOGGER.warning("样本文件不存在: %s", samples_path)
        if not synthetic_on_missing:
            return {
                "sample_count": 0,
                "doc_count": 0,
                "dedup_by_text": dedup_by_text,
                "cross_dataset_dedup": cross_dataset_dedup,
                "samples_path": str(samples_path),
            }
        payload: Any = []
    else:
        payload = safe_json_load(samples_path)

    if not isinstance(payload, list) or not payload:
        if not synthetic_on_missing:
            LOGGER.warning("样本格式异常或为空，跳过: %s", dataset_name)
            return {
                "sample_count": 0,
                "doc_count": 0,
                "dedup_by_text": dedup_by_text,
                "cross_dataset_dedup": cross_dataset_dedup,
                "samples_path": str(samples_path),
            }
        LOGGER.warning("样本格式异常，使用合成样本进行统计: %s", dataset_name)
        synthetic_used = True
        if dataset_is_relation_only(config, dataset_name):
            payload = [
                {
                    "head_entity_type": "Entity",
                    "tail_entity_type": "Entity",
                    "relation": synthetic_relation,
                    "samples": [
                        {
                            "text": synthetic_text,
                            "head_entity": "EntityA",
                            "head_entity_type": "Entity",
                            "tail_entity": "EntityB",
                            "tail_entity_type": "Entity",
                            "relation": synthetic_relation,
                        }
                    ],
                }
            ]
        else:
            payload = [
                {
                    "event_type": synthetic_event_type,
                    "samples": [
                        {
                            "text": synthetic_text,
                            "event_type": synthetic_event_type,
                            "event_trigger": "trigger",
                            "arguments": [
                                {"role": synthetic_role, "argument": "EntityA"},
                            ],
                        }
                    ],
                }
            ]
    if dataset_is_relation_only(config, dataset_name):
        docs, sample_count, typed_flag = parse_re_samples(
            payload,
            dataset_name,
            _language_code(config),
            dedup_by_text,
            cross_dataset_dedup,
        )
        LOGGER.debug("RE 样本统计: dataset=%s samples=%d docs=%d typed=%s", dataset_name, sample_count, len(docs), typed_flag)
    else:
        docs, sample_count = parse_ee_samples(
            payload,
            dataset_name,
            _language_code(config),
            dedup_by_text,
            cross_dataset_dedup,
        )
        LOGGER.debug("EE 样本统计: dataset=%s samples=%d docs=%d", dataset_name, sample_count, len(docs))
    return {
        "sample_count": sample_count,
        "doc_count": len(docs),
        "dedup_by_text": dedup_by_text,
        "cross_dataset_dedup": cross_dataset_dedup,
        "samples_path": str(samples_path),
        "synthetic_used": synthetic_used,
    }


def _normalization_spec(config: Dict[str, Any]) -> Dict[str, Any]:
    report_cfg = config.get("paper_report") or {}
    spec_cfg = report_cfg.get("normalization_spec") or {}
    if spec_cfg:
        return spec_cfg
    return {}


def _build_normalization_md(spec: Dict[str, Any], examples: List[Dict[str, str]]) -> List[str]:
    lines = ["# Schema Normalization", ""]
    for section_name, spec_map in spec.items():
        lines.append(f"## {section_name}")
        lines.append("")
        lines.append("| Key | Value |")
        lines.append("| --- | --- |")
        if isinstance(spec_map, dict):
            for key, value in spec_map.items():
                lines.append(f"| {key} | {value} |")
        lines.append("")
    if examples:
        lines.append("## Examples")
        lines.append("")
        for example in examples:
            before = example.get("before") or ""
            after = example.get("after") or ""
            lines.append(f"- before: {before}")
            lines.append(f"  after: {after}")
        lines.append("")
    return lines


def _graph_f1_config(config: Dict[str, Any]) -> Dict[str, Any]:
    report_cfg = config.get("paper_report") or {}
    graph_cfg = report_cfg.get("graph_f1") or {}
    eval_cfg = config.get("evaluation") or {}
    return {
        "embedding_backend": eval_cfg.get("embedding_backend"),
        "embedding_model": eval_cfg.get("emb_model"),
        "ollama_model": (eval_cfg.get("ollama") or {}).get("model"),
        "device": eval_cfg.get("device"),
        "embedding_dim": graph_cfg.get("embedding_dim"),
        "similarity": graph_cfg.get("similarity"),
        "matching": graph_cfg.get("matching"),
        "threshold": eval_cfg.get("threshold"),
        "graph_smoothing_rounds": eval_cfg.get("graph_smoothing_rounds"),
        "graph_smoothing_alpha": eval_cfg.get("graph_smoothing_alpha"),
    }


def _fuzzy_threshold_sweep(
    config: Dict[str, Any],
    gold_schema: Dict[str, Any],
    pred_schema: Dict[str, Any],
    skip: bool,
) -> Dict[str, Any]:
    report_cfg = config.get("paper_report") or {}
    sweep_cfg = report_cfg.get("fuzzy_sweep") or {}
    enabled = bool(sweep_cfg.get("enabled", True))
    thresholds = sweep_cfg.get("thresholds") or []
    if skip or not enabled:
        LOGGER.info("Fuzzy threshold sweep 已跳过")
        return {"enabled": False, "thresholds": thresholds, "results": []}
    if ontology_eval is None:
        LOGGER.warning("未能加载 ontology_eval，跳过 fuzzy threshold sweep")
        return {"enabled": False, "thresholds": thresholds, "results": []}
    if not gold_schema or not pred_schema:
        LOGGER.warning("缺少 gold/pred schema，跳过 fuzzy threshold sweep")
        return {"enabled": False, "thresholds": thresholds, "results": []}
    if not thresholds:
        return {"enabled": True, "thresholds": [], "results": []}

    eval_cfg = config.get("evaluation") or {}
    device = eval_cfg.get("device")
    try:
        model, backend, emb_model_name, base_url = ontology_eval.prepare_embedding_model(eval_cfg, device=device)
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("加载嵌入模型失败，跳过 fuzzy threshold sweep: %s", exc)
        return {
            "enabled": False,
            "thresholds": thresholds,
            "results": [],
            "error": str(exc),
        }

    try:
        gold_graph = schema_dict_to_graph(gold_schema)
        pred_graph = schema_dict_to_graph(pred_schema)
        gold_vecs = ontology_eval.build_embeddings(gold_graph, model)
        pred_vecs = ontology_eval.build_embeddings(pred_graph, model)

        results = []
        for threshold in thresholds:
            prec, rec, f1 = ontology_eval.fuzzy_f1_edges(
                gold_graph,
                pred_graph,
                gold_vecs,
                pred_vecs,
                threshold=float(threshold),
            )
            results.append(
                {
                    "threshold": float(threshold),
                    "precision": prec,
                    "recall": rec,
                    "f1": f1,
                    "pred_edges": len(pred_graph.edges),
                    "gold_edges": len(gold_graph.edges),
                }
            )
        return {
            "enabled": True,
            "backend": backend,
            "emb_model": emb_model_name,
            "base_url": base_url,
            "thresholds": thresholds,
            "results": results,
        }
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("fuzzy sweep 失败，已跳过: %s", exc)
        return {
            "enabled": False,
            "backend": backend,
            "emb_model": emb_model_name,
            "base_url": base_url,
            "thresholds": thresholds,
            "results": [],
            "error": str(exc),
        }


def run_paper_report(config: Dict[str, Any], overrides: PaperReportOverrides | None = None) -> Dict[str, Any]:
    overrides = overrides or PaperReportOverrides()
    report_cfg = config.get("paper_report") or {}
    output_dir = resolve_project_path(report_cfg.get("output_dir", "data/output/paper_report"))
    if overrides.output_dir:
        output_dir = overrides.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    dataset_name = overrides.dataset_name or report_cfg.get("dataset_name") or _selected_dataset_name(config)
    language = _language_code(config)

    pred_schema_path = overrides.pred_schema_path or _default_pred_schema_path(config, dataset_name, language)
    gold_schema_path = overrides.gold_schema_path or _default_gold_schema_path(config, dataset_name, language)
    samples_path = overrides.samples_path or _default_samples_path(config, dataset_name)

    LOGGER.debug("Paper report dataset=%s", dataset_name)
    LOGGER.debug("pred_schema_path=%s", pred_schema_path)
    LOGGER.debug("gold_schema_path=%s", gold_schema_path)
    LOGGER.debug("samples_path=%s", samples_path)

    pred_schema = _load_schema(pred_schema_path, "pred")
    gold_schema = _load_schema(gold_schema_path, "gold")

    pred_stats = _schema_stats(pred_schema) if pred_schema else {}
    gold_stats = _schema_stats(gold_schema) if gold_schema else {}
    sample_stats = _sample_stats(config, dataset_name, samples_path)

    normalization_spec = _normalization_spec(config)
    examples = report_cfg.get("normalization_examples") or []
    normalization_md = _build_normalization_md(normalization_spec, examples)
    (output_dir / "schema_normalization.md").write_text("\n".join(normalization_md) + "\n", encoding="utf-8")

    graph_f1_cfg = _graph_f1_config(config)
    fuzzy_sweep = _fuzzy_threshold_sweep(config, gold_schema, pred_schema, overrides.skip_fuzzy)

    fusion_cfg = report_cfg.get("fusion_track") or {}

    report = {
        "dataset": dataset_name,
        "language": language,
        "schema": {
            "pred": pred_stats,
            "gold": gold_stats,
        },
        "samples": sample_stats,
        "graph_f1": graph_f1_cfg,
        "fuzzy_threshold_sweep": fuzzy_sweep,
        "normalization_spec": normalization_spec,
        "normalization_examples": examples,
        "fusion_track": {
            "base_ontologies": fusion_cfg.get("base_ontologies") or [],
            "leakage_check": fusion_cfg.get("leakage_check") or [],
            "mapping_fields": fusion_cfg.get("mapping_fields") or [],
        },
    }

    save_json(output_dir / "paper_report.json", report)

    summary_lines = [
        "# Paper Report",
        "",
        f"- dataset: {dataset_name or 'N/A'}",
        f"- language: {language}",
        "",
        "## Counts we report",
        "",
    ]
    if pred_stats:
        counts = pred_stats.get("counts", {})
        summary_lines.extend(
            [
                "### Pred schema",
                f"- relation_types: {counts.get('relation_types', 0)}",
                f"- event_types: {counts.get('event_types', 0)}",
                f"- roles: {counts.get('roles', 0)}",
                f"- re_edges: {counts.get('re_edges', 0)}",
                f"- ee_edges: {counts.get('ee_edges', 0)}",
                f"- graph_nodes: {counts.get('graph_nodes', 0)}",
                f"- graph_edges: {counts.get('graph_edges', 0)}",
                "",
            ]
        )
    if sample_stats:
        summary_lines.extend(
            [
                "### Samples",
                f"- sample_count: {sample_stats.get('sample_count', 0)}",
                f"- doc_count: {sample_stats.get('doc_count', 0)}",
                f"- dedup_by_text: {sample_stats.get('dedup_by_text')}",
                f"- cross_dataset_dedup: {sample_stats.get('cross_dataset_dedup')}",
                "",
            ]
        )

    summary_lines.extend(
        [
            "## Graph F1 config",
            "",
            f"- embedding_backend: {graph_f1_cfg.get('embedding_backend')}",
            f"- embedding_model: {graph_f1_cfg.get('embedding_model')}",
            f"- ollama_model: {graph_f1_cfg.get('ollama_model')}",
            f"- embedding_dim: {graph_f1_cfg.get('embedding_dim')}",
            f"- similarity: {graph_f1_cfg.get('similarity')}",
            f"- matching: {graph_f1_cfg.get('matching')}",
            f"- threshold: {graph_f1_cfg.get('threshold')}",
            f"- graph_smoothing_rounds: {graph_f1_cfg.get('graph_smoothing_rounds')}",
            f"- graph_smoothing_alpha: {graph_f1_cfg.get('graph_smoothing_alpha')}",
            "",
        ]
    )

    if fuzzy_sweep.get("results"):
        summary_lines.append("## Fuzzy threshold sweep")
        summary_lines.append("")
        summary_lines.append("| threshold | precision | recall | f1 | pred_edges | gold_edges |")
        summary_lines.append("| --- | --- | --- | --- | --- | --- |")
        for row in fuzzy_sweep["results"]:
            summary_lines.append(
                "| {threshold:.2f} | {precision:.4f} | {recall:.4f} | {f1:.4f} | {pred_edges} | {gold_edges} |".format(
                    **row
                )
            )
        summary_lines.append("")

    summary_lines.append("## Fusion track")
    summary_lines.append("")
    summary_lines.append(f"- base_ontologies: {len(report['fusion_track']['base_ontologies'])}")
    summary_lines.append(f"- leakage_check: {report['fusion_track']['leakage_check']}")
    summary_lines.append(f"- mapping_fields: {report['fusion_track']['mapping_fields']}")
    summary_lines.append("")

    (output_dir / "paper_report.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    LOGGER.info("Paper report 已写入: %s", output_dir)
    return report


def main() -> None:
    config = load_yaml_config()
    run_paper_report(config)


if __name__ == "__main__":
    main()
