"""公开数据集 schema 与样例转换工具。"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .common import load_yaml_config, resolve_project_path, save_json
from .logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


RE_SAMPLE_FIELDS = (
    "id",
    "category",
    "text",
    "head_entity",
    "head_entity_type",
    "head_pos",
    "tail_entity",
    "tail_entity_type",
    "tail_pos",
    "relation",
    "dataset",
    "language",
    "task",
)

EE_SAMPLE_FIELDS = (
    "id",
    "text",
    "event_type",
    "event_trigger",
    "trigger_pos",
    "arguments",
    "entity",
    "dataset",
    "language",
    "task",
)

EE_ARGUMENT_FIELDS = (
    "argument",
    "role",
    "argument_pos",
)

EE_ENTITY_FIELDS = (
    "entity",
    "entity_type",
)


@dataclass(frozen=True)
class InstructIERelationMap:
    """InstructIE 关系到实体类型的映射。"""

    by_category: Dict[Tuple[str | None, str], Tuple[str, str]]
    by_relation: Dict[str, Tuple[str, str]]


@dataclass(frozen=True)
class RelationTypeMap:
    """关系类型到实体类型的映射。"""

    by_relation: Dict[str, Tuple[str, str]]


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_json_lines(paths: Sequence[Path]) -> Iterable[Dict[str, Any]]:
    for path in paths:
        text = path.read_text(encoding="utf-8")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None

        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    yield item
            continue
        if isinstance(payload, dict):
            yield payload
            continue

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if not line.startswith("{"):
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                yield payload


def _load_schema_lines(schema_path: Path) -> List[Any]:
    lines: List[Any] = []
    for line in schema_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            LOGGER.debug("跳过无法解析的 schema 行: %s", line)
            continue
        lines.append(payload)
    return lines


def _normalize_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (list, dict, set, tuple)) and len(value) == 0:
        return ""
    return value


def _normalize_sample(fields: Sequence[str], payload: Dict[str, Any]) -> Dict[str, Any]:
    sample = {field: "" for field in fields}
    for key, value in payload.items():
        if key not in sample:
            continue
        sample[key] = _normalize_value(value)
    return sample


def _normalize_arguments(arguments: Any) -> Any:
    if not isinstance(arguments, list) or not arguments:
        return ""
    normalized: List[Dict[str, Any]] = []
    for argument in arguments:
        if not isinstance(argument, dict):
            continue
        payload = {field: _normalize_value(argument.get(field, "")) for field in EE_ARGUMENT_FIELDS}
        normalized.append(payload)
    return normalized or ""


def _normalize_entities(entities: Any) -> Any:
    if not isinstance(entities, list) or not entities:
        return ""
    normalized: List[Dict[str, Any]] = []
    for entity in entities:
        if not isinstance(entity, dict):
            continue
        payload = {field: _normalize_value(entity.get(field, "")) for field in EE_ENTITY_FIELDS}
        normalized.append(payload)
    return normalized or ""


def _new_sample_bucket() -> Dict[str, Any]:
    return {"items": [], "texts": set(), "keys": set()}


def _extract_relation_labels(schema_lines: List[Any]) -> List[str]:
    for index in (1, 0):
        if len(schema_lines) > index and isinstance(schema_lines[index], list) and schema_lines[index]:
            return [str(item).strip() for item in schema_lines[index] if str(item).strip()]
    return []


def _build_relation_schema_from_typed(schema_path: Path, dataset_name: str, language: str) -> Tuple[Dict[str, Any], RelationTypeMap]:
    schema_lines = _load_schema_lines(schema_path)
    typed_relations = schema_lines[0] if schema_lines else []
    relation_labels = schema_lines[1] if len(schema_lines) > 1 else []
    relationships: List[Dict[str, str]] = []
    entities: set[str] = set()
    mapping: Dict[str, Tuple[str, str]] = {}

    for typed, label in zip(typed_relations, relation_labels or typed_relations):
        parts = str(typed).split("_")
        if len(parts) < 3:
            continue
        head_type, tail_type = parts[0], parts[-1]
        rel_type = str(label).strip() or "_".join(parts[1:-1])
        if not rel_type:
            continue
        entities.update([head_type, tail_type])
        relationships.append(
            {
                "head_entity": head_type,
                "tail_entity": tail_type,
                "rel_type": rel_type,
            }
        )
        mapping.setdefault(rel_type, (head_type, tail_type))

    schema_payload = {
        "dataset": dataset_name,
        "language": language,
        "entities": sorted(entities),
        "relationships": relationships,
    }
    return schema_payload, RelationTypeMap(by_relation=mapping)


def _build_relation_schema_from_labels(schema_path: Path, dataset_name: str, language: str) -> Dict[str, Any]:
    schema_lines = _load_schema_lines(schema_path)
    relations = _extract_relation_labels(schema_lines)
    relationships = [
        {
            "head_entity": "",
            "tail_entity": "",
            "rel_type": rel_type,
        }
        for rel_type in relations
    ]
    return {
        "dataset": dataset_name,
        "language": language,
        "entities": [],
        "relationships": relationships,
    }


def convert_instructie_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Tuple[Dict[str, Any], InstructIERelationMap]:
    if not isinstance(schema_path, Path):
        schema_path = next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")

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


def _infer_relation_types(rel_type: str, mapping: RelationTypeMap | None) -> Tuple[str, str]:
    if not mapping:
        return "", ""
    return mapping.by_relation.get(rel_type, ("", ""))


def _convert_relation_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    text_field: str = "text",
    relation_field: str = "relation",
    category_field: str | None = None,
    mapping: RelationTypeMap | InstructIERelationMap | None = None,
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)

    for record in _iter_json_lines(data_paths):
        text = str(record.get(text_field, "")).strip()
        if not text:
            continue
        category = record.get(category_field) if category_field else None
        relations = record.get(relation_field, [])
        if not isinstance(relations, list):
            continue

        for rel in relations:
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
                if isinstance(mapping, InstructIERelationMap):
                    head_type, tail_type = _infer_instructie_types(rel_type, category, mapping)
                else:
                    head_type, tail_type = _infer_relation_types(rel_type, mapping)

            head_pos = rel.get("head_pos", "")
            tail_pos = rel.get("tail_pos", "")

            key = (head_type, rel_type, tail_type)
            bucket = samples[key]
            if text in bucket["texts"]:
                continue
            if len(bucket["items"]) >= sample_limit:
                continue

            sample = _normalize_sample(
                RE_SAMPLE_FIELDS,
                {
                    "id": record.get("id", ""),
                    "category": category or record.get("category", ""),
                    "text": text,
                    "head_entity": head,
                    "head_entity_type": head_type,
                    "head_pos": head_pos,
                    "tail_entity": tail,
                    "tail_entity_type": tail_type,
                    "tail_pos": tail_pos,
                    "relation": rel_type,
                    "dataset": dataset_name,
                    "language": language,
                    "task": record.get("task", ""),
                },
            )

            bucket["items"].append(sample)
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


def convert_instructie_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: InstructIERelationMap | None = None,
) -> List[Dict[str, Any]]:
    if mapping is None:
        mapping = InstructIERelationMap(by_category={}, by_relation={})
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="input",
        relation_field="relation",
        category_field="cate",
        mapping=mapping,
    )


def convert_duie_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    if not isinstance(schema_path, Path):
        schema_path = next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")

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
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
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

            sample = _normalize_sample(
                RE_SAMPLE_FIELDS,
                {
                    "id": record.get("id", ""),
                    "category": record.get("category", ""),
                    "text": text,
                    "head_entity": head_entity,
                    "head_entity_type": head_type,
                    "head_pos": "",
                    "tail_entity": tail_entity,
                    "tail_entity_type": tail_type,
                    "tail_pos": "",
                    "relation": rel_type,
                    "dataset": dataset_name,
                    "language": language,
                    "task": record.get("task", ""),
                },
            )

            bucket["items"].append(sample)
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


def convert_cmeie_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Tuple[Dict[str, Any], RelationTypeMap]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_typed(schema_path, dataset_name, language)


def convert_cmeie_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_coae2016_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_coae2016_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_duie2_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Tuple[Dict[str, Any], RelationTypeMap]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_typed(schema_path, dataset_name, language)


def convert_duie2_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_ipre_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_ipre_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_ske2020_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Tuple[Dict[str, Any], RelationTypeMap]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_typed(schema_path, dataset_name, language)


def convert_ske2020_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_ade_corpus_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_ade_corpus_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_fewrel_0_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_fewrel_0_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_fewrel_1_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_1_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def convert_fewrel_2_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_2_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def convert_fewrel_3_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_3_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def convert_fewrel_4_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_4_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def convert_gids_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_gids_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_nyt11_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_nyt11_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_new_york_times_re_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_new_york_times_re_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_scierc_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_scierc_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_conll04_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Tuple[Dict[str, Any], RelationTypeMap]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_typed(schema_path, dataset_name, language)


def convert_conll04_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_kbp37_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_kbp37_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_semval_re_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_semval_re_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_wiki_0_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_path = schema_path if isinstance(schema_path, Path) else next(iter(schema_path), None)
    if schema_path is None:
        raise ValueError("schema_path 不能为空")
    return _build_relation_schema_from_labels(schema_path, dataset_name, language)


def convert_wiki_0_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
    )


def convert_wiki_1_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_1_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def convert_wiki_2_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_2_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def convert_wiki_3_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_3_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def convert_wiki_4_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_4_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(data_paths, dataset_name, language, sample_limit, mapping=mapping)


def _build_event_schema(schema_paths: Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    event_types: set[str] = set()
    roles: set[str] = set()

    for schema_path in schema_paths:
        schema_lines = _load_schema_lines(schema_path)
        if schema_lines and isinstance(schema_lines[0], list):
            event_types.update([str(item).strip() for item in schema_lines[0] if str(item).strip()])
        if len(schema_lines) > 1 and isinstance(schema_lines[1], list):
            roles.update([str(item).strip() for item in schema_lines[1] if str(item).strip()])

    return {
        "dataset": dataset_name,
        "language": language,
        "event_types": sorted(event_types),
        "roles": sorted(roles),
    }


def _convert_event_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    samples: Dict[str, Dict[str, Any]] = defaultdict(_new_sample_bucket)

    for record in _iter_json_lines(data_paths):
        text = str(record.get("text", "")).strip()
        if not text:
            continue
        events = record.get("event", [])
        if not isinstance(events, list):
            continue

        entities = _normalize_entities(record.get("entity", ""))
        for event in events:
            if not isinstance(event, dict):
                continue
            event_type = str(event.get("event_type", "")).strip()
            if not event_type:
                continue
            event_trigger = str(event.get("event_trigger", "")).strip()
            trigger_pos = _normalize_value(event.get("trigger_pos", ""))
            arguments = _normalize_arguments(event.get("arguments", ""))

            bucket = samples[event_type]
            sample_key = (text, event_trigger, json.dumps(arguments, ensure_ascii=False))
            if sample_key in bucket["keys"]:
                continue
            if len(bucket["items"]) >= sample_limit:
                continue

            sample = _normalize_sample(
                EE_SAMPLE_FIELDS,
                {
                    "id": record.get("id", ""),
                    "text": text,
                    "event_type": event_type,
                    "event_trigger": event_trigger,
                    "trigger_pos": trigger_pos,
                    "arguments": arguments,
                    "entity": entities,
                    "dataset": dataset_name,
                    "language": language,
                    "task": record.get("task", ""),
                },
            )

            bucket["items"].append(sample)
            bucket["keys"].add(sample_key)

    results: List[Dict[str, Any]] = []
    for event_type in sorted(samples.keys()):
        bucket = samples[event_type]
        results.append(
            {
                "event_type": event_type,
                "samples": bucket["items"],
            }
        )
    return results


def convert_casie_schema(schema_paths: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_list = [schema_paths] if isinstance(schema_paths, Path) else list(schema_paths)
    return _build_event_schema(schema_list, dataset_name, language)


def convert_casie_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_crude_oil_news_schema(schema_paths: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_list = [schema_paths] if isinstance(schema_paths, Path) else list(schema_paths)
    return _build_event_schema(schema_list, dataset_name, language)


def convert_crude_oil_news_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_phee_schema(schema_paths: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_list = [schema_paths] if isinstance(schema_paths, Path) else list(schema_paths)
    return _build_event_schema(schema_list, dataset_name, language)


def convert_phee_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_rams_schema(schema_paths: Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return _build_event_schema(schema_paths, dataset_name, language)


def convert_rams_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_wiki_events_schema(schema_paths: Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return _build_event_schema(schema_paths, dataset_name, language)


def convert_wiki_events_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_ccf_law_schema(schema_paths: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_list = [schema_paths] if isinstance(schema_paths, Path) else list(schema_paths)
    return _build_event_schema(schema_list, dataset_name, language)


def convert_ccf_law_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_duee_schema(schema_paths: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_list = [schema_paths] if isinstance(schema_paths, Path) else list(schema_paths)
    return _build_event_schema(schema_list, dataset_name, language)


def convert_duee_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_duee_fin_schema(schema_paths: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_list = [schema_paths] if isinstance(schema_paths, Path) else list(schema_paths)
    return _build_event_schema(schema_list, dataset_name, language)


def convert_duee_fin_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def convert_fewfc_schema(schema_paths: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_list = [schema_paths] if isinstance(schema_paths, Path) else list(schema_paths)
    return _build_event_schema(schema_list, dataset_name, language)


def convert_fewfc_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
) -> List[Dict[str, Any]]:
    return _convert_event_inputs(data_paths, dataset_name, language, sample_limit)


def _normalize_dataset_name(name: str | None) -> str:
    return str(name or "").strip().replace("-", "_").lower()


def _resolve_selected_datasets(targets: Any, available: Dict[str, Dict[str, Any]]) -> List[str]:
    if targets is None:
        return list(available.keys())
    if isinstance(targets, str):
        if targets.strip().lower() == "all":
            return list(available.keys())
        return [_normalize_dataset_name(targets)]
    if isinstance(targets, list):
        normalized = [_normalize_dataset_name(item) for item in targets]
        if any(item == "all" for item in normalized):
            return list(available.keys())
        return normalized
    return list(available.keys())


def _collect_paths(items: Sequence[str]) -> List[Path]:
    paths: List[Path] = []
    for item in items:
        if not item:
            continue
        paths.append(resolve_project_path(item))
    return paths


def _collect_files_from_dirs(dirs: Sequence[str], pattern: str) -> List[Path]:
    files: List[Path] = []
    for dir_path in dirs:
        base = resolve_project_path(dir_path)
        if not base.exists():
            LOGGER.debug("路径不存在，跳过: %s", base)
            continue
        for path in base.glob(pattern):
            if path.name == "schema.json":
                continue
            if path.is_file():
                files.append(path)
    return files


def _collect_schema_paths(dataset_cfg: Dict[str, Any]) -> List[Path]:
    schema_paths = _collect_paths(dataset_cfg.get("schema_paths", []) or [])
    schema_path = dataset_cfg.get("schema_path")
    if schema_path:
        schema_paths.append(resolve_project_path(schema_path))
    schema_dirs = dataset_cfg.get("schema_dirs", []) or []
    schema_glob = dataset_cfg.get("schema_glob") or "**/schema.json"
    schema_paths.extend(_collect_files_from_dirs(schema_dirs, schema_glob))
    resolved = [path for path in schema_paths if path.exists()]
    LOGGER.debug("已收集 schema 路径: %s", [str(path) for path in resolved])
    return resolved


def _collect_data_files(dataset_cfg: Dict[str, Any]) -> List[Path]:
    data_files = _collect_paths(dataset_cfg.get("data_files", []) or [])
    data_dirs = dataset_cfg.get("data_dirs", []) or []
    data_glob = dataset_cfg.get("data_glob") or "**/*.json"
    data_files.extend(_collect_files_from_dirs(data_dirs, data_glob))
    resolved = [path for path in data_files if path.exists()]
    LOGGER.debug("已收集 data 文件: %s", [str(path) for path in resolved])
    return resolved


def _resolve_output_paths(
    output_dir: Path,
    dataset_cfg: Dict[str, Any],
    dataset_name: str,
) -> Tuple[Path, Path]:
    schema_out = Path(dataset_cfg.get("schema_output") or f"golden_schema_{dataset_name}.json")
    samples_out = Path(dataset_cfg.get("samples_output") or f"golden_input_{dataset_name}.json")
    if not schema_out.is_absolute():
        schema_out = output_dir / schema_out
    if not samples_out.is_absolute():
        samples_out = output_dir / samples_out
    return resolve_project_path(schema_out), resolve_project_path(samples_out)


def _run_schema_converter(
    converter,
    schema_paths: Sequence[Path],
    dataset_name: str,
    language: str,
) -> Tuple[Dict[str, Any], Any]:
    schema_input: Path | Sequence[Path]
    if len(schema_paths) == 1:
        schema_input = schema_paths[0]
    else:
        schema_input = schema_paths
    result = converter(schema_input, dataset_name, language)
    if isinstance(result, tuple) and len(result) == 2:
        return result[0], result[1]
    return result, None


def _run_re_dataset_conversion(
    dataset_cfg: Dict[str, Any],
    output_dir: Path,
    sample_limit: int,
    results: Dict[str, List[Path]],
) -> None:
    name = dataset_cfg.get("name")
    language = dataset_cfg.get("language", "").lower() or "zh"
    format_key = _normalize_dataset_name(dataset_cfg.get("format") or dataset_cfg.get("type"))
    dataset_name = str(name)
    LOGGER.debug("准备处理关系抽取数据集: %s (format=%s, language=%s)", dataset_name, format_key, language)

    handlers = {
        "instructie": (convert_instructie_schema, convert_instructie_inputs),
        "duie": (convert_duie_schema, convert_duie_inputs),
        "cmeie": (convert_cmeie_schema, convert_cmeie_inputs),
        "coae2016": (convert_coae2016_schema, convert_coae2016_inputs),
        "duie2.0": (convert_duie2_schema, convert_duie2_inputs),
        "ipre": (convert_ipre_schema, convert_ipre_inputs),
        "ske2020": (convert_ske2020_schema, convert_ske2020_inputs),
        "ade_corpus": (convert_ade_corpus_schema, convert_ade_corpus_inputs),
        "fewrel_0": (convert_fewrel_0_schema, convert_fewrel_0_inputs),
        "fewrel_1": (convert_fewrel_1_schema, convert_fewrel_1_inputs),
        "fewrel_2": (convert_fewrel_2_schema, convert_fewrel_2_inputs),
        "fewrel_3": (convert_fewrel_3_schema, convert_fewrel_3_inputs),
        "fewrel_4": (convert_fewrel_4_schema, convert_fewrel_4_inputs),
        "gids": (convert_gids_schema, convert_gids_inputs),
        "nyt11": (convert_nyt11_schema, convert_nyt11_inputs),
        "new_york_times_re": (convert_new_york_times_re_schema, convert_new_york_times_re_inputs),
        "scierc": (convert_scierc_schema, convert_scierc_inputs),
        "conll04": (convert_conll04_schema, convert_conll04_inputs),
        "kbp37": (convert_kbp37_schema, convert_kbp37_inputs),
        "semval_re": (convert_semval_re_schema, convert_semval_re_inputs),
        "wiki_0": (convert_wiki_0_schema, convert_wiki_0_inputs),
        "wiki_1": (convert_wiki_1_schema, convert_wiki_1_inputs),
        "wiki_2": (convert_wiki_2_schema, convert_wiki_2_inputs),
        "wiki_3": (convert_wiki_3_schema, convert_wiki_3_inputs),
        "wiki_4": (convert_wiki_4_schema, convert_wiki_4_inputs),
    }

    if format_key not in handlers:
        LOGGER.warning("未找到关系抽取数据集 %s 的处理函数", dataset_name)
        return

    schema_paths = _collect_schema_paths(dataset_cfg)
    data_files = _collect_data_files(dataset_cfg)
    LOGGER.debug(
        "关系抽取数据集 %s schema_paths=%s data_files=%s",
        dataset_name,
        [str(path) for path in schema_paths],
        [str(path) for path in data_files],
    )
    if not schema_paths:
        LOGGER.warning("关系抽取数据集 %s 未配置 schema_path", dataset_name)
        return
    if not data_files:
        LOGGER.warning("关系抽取数据集 %s 未配置 data_files", dataset_name)
        return

    schema_out, samples_out = _resolve_output_paths(output_dir, dataset_cfg, dataset_name)
    schema_payload, mapping = _run_schema_converter(handlers[format_key][0], schema_paths, dataset_name, language)
    save_json(schema_out, schema_payload)

    samples_payload = handlers[format_key][1](
        data_files,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
    )

    save_json(samples_out, samples_payload)
    results["schemas"].append(schema_out)
    results["samples"].append(samples_out)

    total_samples = sum(len(item.get("samples", [])) for item in samples_payload)
    LOGGER.debug(
        "关系抽取数据集 %s 关系数=%s 样本数=%s", dataset_name, len(samples_payload), total_samples
    )
    LOGGER.debug(
        "完成关系抽取数据集 %s -> schema: %s, samples: %s", dataset_name, schema_out, samples_out
    )


def _run_ee_dataset_conversion(
    dataset_cfg: Dict[str, Any],
    output_dir: Path,
    sample_limit: int,
    results: Dict[str, List[Path]],
) -> None:
    name = dataset_cfg.get("name")
    language = dataset_cfg.get("language", "").lower() or "zh"
    format_key = _normalize_dataset_name(dataset_cfg.get("format") or dataset_cfg.get("type"))
    dataset_name = str(name)
    LOGGER.debug("准备处理事件抽取数据集: %s (format=%s, language=%s)", dataset_name, format_key, language)

    handlers = {
        "casie": (convert_casie_schema, convert_casie_inputs),
        "crudeoilnews": (convert_crude_oil_news_schema, convert_crude_oil_news_inputs),
        "phee": (convert_phee_schema, convert_phee_inputs),
        "rams": (convert_rams_schema, convert_rams_inputs),
        "wikievents": (convert_wiki_events_schema, convert_wiki_events_inputs),
        "ccf_law": (convert_ccf_law_schema, convert_ccf_law_inputs),
        "duee1.0": (convert_duee_schema, convert_duee_inputs),
        "duee_fin": (convert_duee_fin_schema, convert_duee_fin_inputs),
        "fewfc": (convert_fewfc_schema, convert_fewfc_inputs),
    }

    if format_key not in handlers:
        LOGGER.warning("未找到事件抽取数据集 %s 的处理函数", dataset_name)
        return

    schema_paths = _collect_schema_paths(dataset_cfg)
    data_files = _collect_data_files(dataset_cfg)
    LOGGER.debug(
        "事件抽取数据集 %s schema_paths=%s data_files=%s",
        dataset_name,
        [str(path) for path in schema_paths],
        [str(path) for path in data_files],
    )
    if not schema_paths:
        LOGGER.warning("事件抽取数据集 %s 未配置 schema_path", dataset_name)
        return
    if not data_files:
        LOGGER.warning("事件抽取数据集 %s 未配置 data_files", dataset_name)
        return

    schema_out, samples_out = _resolve_output_paths(output_dir, dataset_cfg, dataset_name)
    schema_payload, _ = _run_schema_converter(handlers[format_key][0], schema_paths, dataset_name, language)
    save_json(schema_out, schema_payload)

    samples_payload = handlers[format_key][1](
        data_files,
        dataset_name,
        language,
        sample_limit,
    )

    save_json(samples_out, samples_payload)
    results["schemas"].append(schema_out)
    results["samples"].append(samples_out)

    total_samples = sum(len(item.get("samples", [])) for item in samples_payload)
    LOGGER.debug("事件抽取数据集 %s 事件类型数=%s 样本数=%s", dataset_name, len(samples_payload), total_samples)
    LOGGER.debug(
        "完成事件抽取数据集 %s -> schema: %s, samples: %s", dataset_name, schema_out, samples_out
    )


def convert_from_config(config: Dict[str, Any]) -> Dict[str, List[Path]]:
    conv_cfg = config.get("dataset_conversion") or {}
    results: Dict[str, List[Path]] = {"schemas": [], "samples": []}

    re_cfg = conv_cfg.get("re")
    ee_cfg = conv_cfg.get("ee")
    if re_cfg or ee_cfg:
        LOGGER.debug("使用新版 dataset_conversion 配置。")
        if re_cfg:
            re_output_dir = resolve_project_path(re_cfg.get("output_dir", conv_cfg.get("output_dir", "data/input/re")))
            re_sample_limit = int(re_cfg.get("samples_per_relation", conv_cfg.get("samples_per_relation", 5)))
            re_entries = re_cfg.get("dataset_configs", []) or []
            re_map = {_normalize_dataset_name(entry.get("name")): entry for entry in re_entries if entry.get("name")}
            LOGGER.debug("关系抽取配置: output_dir=%s sample_limit=%s datasets=%s", re_output_dir, re_sample_limit, re_cfg.get("datasets"))
            for name in _resolve_selected_datasets(re_cfg.get("datasets", "all"), re_map):
                ds_cfg = re_map.get(name)
                if not ds_cfg:
                    LOGGER.warning("未找到关系抽取数据集配置: %s", name)
                    continue
                _run_re_dataset_conversion(ds_cfg, re_output_dir, re_sample_limit, results)

        if ee_cfg:
            ee_output_dir = resolve_project_path(ee_cfg.get("output_dir", conv_cfg.get("output_dir", "data/input/ee")))
            ee_sample_limit = int(ee_cfg.get("samples_per_event", conv_cfg.get("samples_per_event", 5)))
            ee_entries = ee_cfg.get("dataset_configs", []) or []
            ee_map = {_normalize_dataset_name(entry.get("name")): entry for entry in ee_entries if entry.get("name")}
            LOGGER.debug("事件抽取配置: output_dir=%s sample_limit=%s datasets=%s", ee_output_dir, ee_sample_limit, ee_cfg.get("datasets"))
            for name in _resolve_selected_datasets(ee_cfg.get("datasets", "all"), ee_map):
                ds_cfg = ee_map.get(name)
                if not ds_cfg:
                    LOGGER.warning("未找到事件抽取数据集配置: %s", name)
                    continue
                _run_ee_dataset_conversion(ds_cfg, ee_output_dir, ee_sample_limit, results)

        return results

    output_dir = resolve_project_path(conv_cfg.get("output_dir", "data/input"))
    sample_limit = int(conv_cfg.get("samples_per_relation", 5))
    LOGGER.debug("使用旧版 dataset_conversion 配置: output_dir=%s sample_limit=%s", output_dir, sample_limit)

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
                dataset_name=name,
                language=language,
                sample_limit=sample_limit,
                mapping=mapping,
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


def main() -> None:
    config = load_yaml_config()
    results = convert_from_config(config)
    if results["schemas"] or results["samples"]:
        LOGGER.info("转换完成：")
        for path in results["schemas"]:
            LOGGER.info("  schema -> %s", path)
        for path in results["samples"]:
            LOGGER.info("  samples -> %s", path)
    else:
        LOGGER.info("未找到可转换的数据集配置。")


if __name__ == "__main__":
    main()


__all__ = [
    "convert_duie_inputs",
    "convert_duie_schema",
    "convert_from_config",
    "convert_instructie_inputs",
    "convert_instructie_schema",
    "InstructIERelationMap",
    "RelationTypeMap",
]
