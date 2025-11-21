"""公开数据集 schema 与样例转换工具。"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .common import resolve_project_path, save_json


@dataclass(frozen=True)
class InstructIERelationMap:
    """InstructIE 关系到实体类型的映射。"""

    by_category: Dict[Tuple[str | None, str], Tuple[str, str]]
    by_relation: Dict[str, Tuple[str, str]]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_json_lines(paths: Sequence[Path]) -> Iterable[Dict[str, Any]]:
    for path in paths:
        text = path.read_text(encoding="utf-8")
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


def convert_instructie_schema(schema_path: Path, dataset_name: str, language: str) -> Tuple[Dict[str, Any], InstructIERelationMap]:
    raw_schema = _load_json(schema_path)
    relationships: List[Dict[str, str]] = []
    entities: set[str] = set()
    by_category: Dict[Tuple[str | None, str], Tuple[str, str]] = {}
    by_relation: Dict[str, Tuple[str, str]] = {}

    for category, payload in raw_schema.items():
        if not isinstance(payload, list) or len(payload) < 2:
            continue
        typed_relations, relation_labels = payload[0], payload[1]
        for typed, label in zip(typed_relations, relation_labels):
            parts = str(typed).split("_")
            if len(parts) < 3:
                continue
            head_type, tail_type = parts[0], parts[-1]
            rel_type = str(label).strip() or "_".join(parts[1:-1])
            entities.update([head_type, tail_type])
            relationships.append(
                {
                    "head_entity": head_type,
                    "tail_entity": tail_type,
                    "rel_type": rel_type,
                }
            )
            by_category[(category, rel_type)] = (head_type, tail_type)
            by_relation.setdefault(rel_type, (head_type, tail_type))

    schema_payload = {
        "dataset": dataset_name,
        "language": language,
        "entities": sorted(entities),
        "relationships": relationships,
    }
    return schema_payload, InstructIERelationMap(by_category=by_category, by_relation=by_relation)


def _infer_instructie_types(rel_type: str, category: str | None, mapping: InstructIERelationMap) -> Tuple[str, str]:
    if (category, rel_type) in mapping.by_category:
        return mapping.by_category[(category, rel_type)]
    if rel_type in mapping.by_relation:
        return mapping.by_relation[rel_type]
    return "", ""


def _new_sample_bucket() -> Dict[str, Any]:
    return {"items": [], "texts": set()}


def convert_instructie_inputs(
    data_paths: Sequence[Path],
    mapping: InstructIERelationMap,
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)

    for record in _iter_json_lines(data_paths):
        text = str(record.get("input", "")).strip()
        category = record.get("cate")
        if not text:
            continue
        for rel in record.get("relation", []):
            if not isinstance(rel, dict):
                continue
            rel_type = str(rel.get("relation", "")).strip()
            head = str(rel.get("head", "")).strip()
            tail = str(rel.get("tail", "")).strip()
            if not (rel_type and head and tail):
                continue
            head_type = str(rel.get("head_type", "")).strip()
            tail_type = str(rel.get("tail_type", "")).strip()
            if not (head_type and tail_type):
                head_type, tail_type = _infer_instructie_types(rel_type, category, mapping)
            if not (head_type and tail_type):
                continue

            key = (head_type, rel_type, tail_type)
            bucket = samples[key]
            if text in bucket["texts"]:
                continue
            if len(bucket["items"]) >= sample_limit:
                continue
            bucket["items"].append(
                {
                    "id": record.get("id", ""),
                    "category": category or "",
                    "text": text,
                    "head_entity": head,
                    "tail_entity": tail,
                    "dataset": dataset_name,
                    "language": language,
                }
            )
            bucket["texts"].add(text)

    results: List[Dict[str, Any]] = []
    for head_type, rel_type, tail_type in sorted(samples.keys(), key=lambda x: (x[0], x[1], x[2])):
        bucket = samples[(head_type, rel_type, tail_type)]
        results.append(
            {
                "head_entity_type": head_type,
                "rel_type": rel_type,
                "tail_type": tail_type,
                "samples": bucket["items"],
            }
        )
    return results


def convert_duie_schema(schema_path: Path, dataset_name: str, language: str) -> Dict[str, Any]:
    relationships: List[Dict[str, str]] = []
    entities: set[str] = set()

    for record in _iter_json_lines([schema_path]):
        subject_type = str(record.get("subject_type", "")).strip()
        predicate = str(record.get("predicate", "")).strip()
        obj_type_raw = record.get("object_type", {})
        if isinstance(obj_type_raw, dict):
            obj_type = str(obj_type_raw.get("@value", "")).strip()
        else:
            obj_type = str(obj_type_raw).strip()
        if not (subject_type and predicate and obj_type):
            continue
        entities.update([subject_type, obj_type])
        relationships.append(
            {
                "head_entity": subject_type,
                "tail_entity": obj_type,
                "rel_type": predicate,
            }
        )

    return {
        "dataset": dataset_name,
        "language": language,
        "entities": sorted(entities),
        "relationships": relationships,
    }


def convert_duie_inputs(
    data_paths: Sequence[Path], dataset_name: str, language: str, sample_limit: int
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)

    for record in _iter_json_lines(data_paths):
        text = str(record.get("text", "")).strip()
        if not text:
            continue
        for rel in record.get("spo_list", []):
            if not isinstance(rel, dict):
                continue
            head_type = str(rel.get("subject_type", "")).strip()
            rel_type = str(rel.get("predicate", "")).strip()
            head_entity = str(rel.get("subject", "")).strip()
            obj_raw = rel.get("object", {})
            tail_entity = ""
            if isinstance(obj_raw, dict):
                tail_entity = str(obj_raw.get("@value", "")).strip()
            else:
                tail_entity = str(obj_raw).strip()
            obj_type_raw = rel.get("object_type", {})
            tail_type = ""
            if isinstance(obj_type_raw, dict):
                tail_type = str(obj_type_raw.get("@value", "")).strip()
            else:
                tail_type = str(obj_type_raw).strip()

            if not (head_type and rel_type and tail_type and head_entity and tail_entity):
                continue

            key = (head_type, rel_type, tail_type)
            bucket = samples[key]
            if text in bucket["texts"]:
                continue
            if len(bucket["items"]) >= sample_limit:
                continue
            bucket["items"].append(
                {
                    "id": record.get("id", ""),
                    "category": record.get("category", ""),
                    "text": text,
                    "head_entity": head_entity,
                    "tail_entity": tail_entity,
                    "dataset": dataset_name,
                    "language": language,
                }
            )
            bucket["texts"].add(text)

    results: List[Dict[str, Any]] = []
    for head_type, rel_type, tail_type in sorted(samples.keys(), key=lambda x: (x[0], x[1], x[2])):
        bucket = samples[(head_type, rel_type, tail_type)]
        results.append(
            {
                "head_entity_type": head_type,
                "rel_type": rel_type,
                "tail_type": tail_type,
                "samples": bucket["items"],
            }
        )
    return results


def convert_from_config(config: Dict[str, Any]) -> Dict[str, List[Path]]:
    conv_cfg = config.get("dataset_conversion") or {}
    output_dir = resolve_project_path(conv_cfg.get("output_dir", "input"))
    sample_limit = int(conv_cfg.get("samples_per_relation", 5))

    results: Dict[str, List[Path]] = {"schemas": [], "samples": []}
    for dataset_cfg in conv_cfg.get("datasets", []):
        name = dataset_cfg.get("name")
        ds_type = str(dataset_cfg.get("type", "")).lower()
        language = dataset_cfg.get("language", "").lower() or "zh"
        if not name or ds_type not in {"instructie", "duie"}:
            continue

        schema_path = resolve_project_path(dataset_cfg.get("schema_path", ""))
        data_files = [resolve_project_path(p) for p in dataset_cfg.get("data_files", [])]

        schema_out = Path(dataset_cfg.get("schema_output") or f"golden_schema_{name}.json")
        samples_out = Path(dataset_cfg.get("samples_output") or f"golden_input_{name}.json")

        if not schema_out.is_absolute():
            schema_out = output_dir / schema_out
        if not samples_out.is_absolute():
            samples_out = output_dir / samples_out

        schema_path_out = resolve_project_path(schema_out)
        samples_path_out = resolve_project_path(samples_out)

        if ds_type == "instructie":
            schema_payload, mapping = convert_instructie_schema(schema_path, name, language)
            save_json(schema_path_out, schema_payload)
            samples_payload = convert_instructie_inputs(
                data_paths=data_files,
                mapping=mapping,
                dataset_name=name,
                language=language,
                sample_limit=sample_limit,
            )
        else:
            schema_payload = convert_duie_schema(schema_path, name, language)
            save_json(schema_path_out, schema_payload)
            samples_payload = convert_duie_inputs(
                data_paths=data_files,
                dataset_name=name,
                language=language,
                sample_limit=sample_limit,
            )

        save_json(samples_path_out, samples_payload)
        results["schemas"].append(schema_path_out)
        results["samples"].append(samples_path_out)

    return results


__all__ = [
    "convert_duie_inputs",
    "convert_duie_schema",
    "convert_from_config",
    "convert_instructie_inputs",
    "convert_instructie_schema",
    "InstructIERelationMap",
]
