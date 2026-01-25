"""公开数据集 schema 与样例转换工具。"""

from __future__ import annotations

import ast
import json
import logging
import math
import statistics
import re
from fnmatch import fnmatch
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from tqdm import tqdm

from .common import (
    apply_language_suffix,
    load_yaml_config,
    resolve_project_path,
    save_json,
)
from .llm_factory import instantiate_llm_client
from .benchmark_stats import DatasetConversionStats, build_conversion_summary, write_conversion_summary
from .logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)

TQDM_SETTINGS: Dict[str, Any] = {
    "enabled": True,
    "show_records": True,
    "mininterval": 0.1,
    "leave": False,
}

FEWREL_DEFAULT_CONFIG: Dict[str, Any] = {
    "episode_keys": ["meta_train", "meta_test", "meta_dev", "train", "test", "dev", "support", "query"],
    "relation_keys": ["relation", "rel_type", "label", "predicate", "rel"],
    "relation_name_keys": ["relation_name", "relation_text", "relation_label", "label_name", "name"],
    "text_keys": ["text", "sentence", "sent"],
    "head_keys": ["h", "head", "subj", "subject", "head_entity"],
    "tail_keys": ["t", "tail", "obj", "object", "tail_entity"],
    "relation_id_pattern": r"^P\d+$",
    "relation_name_map_files": [],
    "relation_name_map_dirs": [],
    "relation_name_map_glob": "",
    "relation_map_keys": [
        "pid2name",
        "id2rel",
        "id2relation",
        "relation2id",
        "rel2id",
        "rel2name",
        "relation2name",
        "relation_name_map",
    ],
}


RE_SAMPLE_FIELDS = (
    "id",
    "category",
    "input",
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
    "input",
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


def _extract_json_payload(response: str) -> Any:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}|\[.*\]", response, re.S)
        if match:
            return json.loads(match.group(0))
    raise ValueError("LLM 响应未包含合法的 JSON")


def _join_tokens(tokens: Sequence[str]) -> str:
    if not tokens:
        return ""
    text = " ".join(tokens)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = text.replace("``", '"').replace("''", '"')
    return text.strip()


def _format_relation_examples(relation_examples: Dict[str, List[Dict[str, Any]]], limit: int) -> str:
    payload: List[Dict[str, Any]] = []
    for rel_type, examples in relation_examples.items():
        for example in examples[:limit]:
            payload.append(
                {
                    "rel_type": rel_type,
                    "text": example.get("text", ""),
                    "head": example.get("head", ""),
                    "tail": example.get("tail", ""),
                }
            )
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _relation_generation_config(config: Dict[str, Any]) -> Dict[str, Any]:
    return (config.get("dataset_conversion") or {}).get("relation_schema_generation") or {}


def _normalize_task(task: str | None, default: str) -> str:
    task_value = str(task or "").strip().lower()
    if task_value not in {"re", "ee"}:
        task_value = str(default or "").strip().lower()
    return task_value if task_value in {"re", "ee"} else "re"


def _apply_tqdm_settings(config: Dict[str, Any]) -> None:
    settings = (config.get("dataset_conversion") or {}).get("tqdm") or {}
    TQDM_SETTINGS.update(
        {
            "enabled": bool(settings.get("enabled", TQDM_SETTINGS["enabled"])),
            "show_records": bool(settings.get("show_records", TQDM_SETTINGS["show_records"])),
            "mininterval": float(settings.get("mininterval", TQDM_SETTINGS["mininterval"])),
            "leave": bool(settings.get("leave", TQDM_SETTINGS["leave"])),
        }
    )


def _resolve_fewrel_config(config: Dict[str, Any], dataset_cfg: Dict[str, Any] | None = None) -> Dict[str, Any]:
    base_cfg = (config.get("dataset_conversion") or {}).get("fewrel") or {}
    dataset_cfg = dataset_cfg or {}
    override_cfg = dataset_cfg.get("fewrel") or {}
    merged = {
        **FEWREL_DEFAULT_CONFIG,
        **base_cfg,
        **override_cfg,
    }
    for key in (
        "episode_keys",
        "relation_keys",
        "relation_name_keys",
        "text_keys",
        "head_keys",
        "tail_keys",
        "relation_name_map_files",
        "relation_name_map_dirs",
        "relation_map_keys",
    ):
        if key in base_cfg or key in override_cfg:
            merged[key] = list(
                dict.fromkeys(
                    (override_cfg.get(key) or [])
                    + (base_cfg.get(key) or [])
                    + (FEWREL_DEFAULT_CONFIG.get(key) or [])
                )
            )
    return merged


def _extract_fewrel_rel_type(record: Dict[str, Any], fallback: str, cfg: Dict[str, Any]) -> str:
    relation_keys = cfg.get("relation_keys") or []
    rel_type = ""
    for key in relation_keys:
        if key in record:
            rel_type = str(record.get(key, "")).strip()
            if rel_type:
                break
    if not rel_type:
        rel_type = str(fallback or "").strip()
    return rel_type


def _is_fewrel_relation_id(rel_type: str, cfg: Dict[str, Any]) -> bool:
    pattern = str(cfg.get("relation_id_pattern") or r"^P\d+$")
    return bool(re.fullmatch(pattern, str(rel_type or "").strip()))


def _collect_fewrel_relation_name_map_paths(
    data_paths: Sequence[Path],
    cfg: Dict[str, Any],
) -> List[Path]:
    extra_paths = _collect_paths(cfg.get("relation_name_map_files", []) or [])
    map_dirs = cfg.get("relation_name_map_dirs", []) or []
    map_glob = cfg.get("relation_name_map_glob") or ""
    map_globs = map_glob if isinstance(map_glob, list) else [map_glob]
    for dir_path in map_dirs:
        base = resolve_project_path(dir_path)
        if not base.exists():
            LOGGER.debug("FewRel 关系名称映射目录不存在: %s", base)
            continue
        for pattern in map_globs:
            if not pattern:
                continue
            for path in base.glob(pattern):
                if path.is_file():
                    extra_paths.append(path)
    combined = list(dict.fromkeys([*data_paths, *extra_paths]))
    LOGGER.debug(
        "FewRel 关系名称映射候选文件: total=%s extra=%s",
        len(combined),
        len(extra_paths),
    )
    return combined


def _extract_fewrel_relation_name_map(
    payload: Any,
    cfg: Dict[str, Any],
    path: Path | None = None,
) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    if isinstance(payload, dict):
        for key in cfg.get("relation_map_keys") or []:
            if key in payload:
                mapping.update(_extract_fewrel_relation_name_map(payload[key], cfg, path))
        if payload and all(isinstance(value, str) for value in payload.values()):
            for key, value in payload.items():
                key_str = str(key).strip()
                value_str = str(value).strip()
                if not (key_str and value_str):
                    continue
                if _is_fewrel_relation_id(key_str, cfg):
                    mapping[key_str] = value_str
                elif _is_fewrel_relation_id(value_str, cfg):
                    mapping[value_str] = key_str
        return mapping
    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            rel_type = _extract_fewrel_rel_type(item, "", cfg)
            rel_name = ""
            for key in cfg.get("relation_name_keys") or []:
                candidate = str(item.get(key, "")).strip()
                if candidate:
                    rel_name = candidate
                    break
            if rel_type and rel_name and _is_fewrel_relation_id(rel_type, cfg):
                mapping[rel_type] = rel_name
    return mapping


def _collect_fewrel_relation_name_map(
    data_paths: Sequence[Path],
    cfg: Dict[str, Any],
) -> Dict[str, str]:
    relation_name_map: Dict[str, str] = {}
    map_paths = _collect_fewrel_relation_name_map_paths(data_paths, cfg)
    for path in map_paths:
        if not path.exists():
            LOGGER.debug("FewRel 关系名称映射文件不存在，跳过: %s", path)
            continue
        try:
            payload = _load_json(path)
        except json.JSONDecodeError as exc:
            LOGGER.warning("FewRel 关系名称映射解析失败，跳过: %s (%s)", path, exc)
            continue
        mapping = _extract_fewrel_relation_name_map(payload, cfg, path)
        if mapping:
            LOGGER.debug(
                "FewRel 关系名称映射文件: path=%s count=%s",
                path.name,
                len(mapping),
            )
            relation_name_map.update(mapping)
    if relation_name_map:
        LOGGER.debug("FewRel 关系名称映射汇总: count=%s", len(relation_name_map))
    else:
        LOGGER.debug("FewRel 未找到关系名称映射，保留原始 relation id。")
    return relation_name_map


def _normalize_fewrel_rel_type(
    rel_type: str,
    record: Dict[str, Any],
    cfg: Dict[str, Any],
    relation_name_map: Dict[str, str] | None = None,
) -> str:
    rel_type = str(rel_type or "").strip()
    if not rel_type:
        return ""
    relation_name_keys = cfg.get("relation_name_keys") or []
    if _is_fewrel_relation_id(rel_type, cfg):
        for key in relation_name_keys:
            candidate = str(record.get(key, "")).strip()
            if candidate:
                LOGGER.debug("FewRel 关系类型使用名称替换: pid=%s name=%s", rel_type, candidate)
                return candidate
        if relation_name_map and rel_type in relation_name_map:
            mapped = relation_name_map[rel_type]
            LOGGER.debug("FewRel 关系类型使用映射替换: pid=%s name=%s", rel_type, mapped)
            return mapped
        LOGGER.debug("FewRel 关系类型未找到映射: pid=%s", rel_type)
    return rel_type


def _extract_fewrel_text(record: Dict[str, Any], cfg: Dict[str, Any]) -> str:
    tokens = record.get("tokens")
    if isinstance(tokens, list):
        text = _join_tokens(tokens)
        if text:
            return text
    for key in cfg.get("text_keys") or []:
        value = str(record.get(key, "")).strip()
        if value:
            return value
    return ""


def _extract_fewrel_entity_payload(payload: Any) -> Tuple[str, Any]:
    if isinstance(payload, list):
        entity = str(payload[0]).strip() if payload else ""
        pos = payload[2] if len(payload) > 2 else ""
        return entity, pos
    if isinstance(payload, dict):
        entity = str(payload.get("name") or payload.get("entity") or payload.get("text") or "").strip()
        pos = payload.get("pos") or payload.get("positions") or payload.get("span") or ""
        return entity, pos
    return str(payload or "").strip(), ""


def _extract_fewrel_head_tail(record: Dict[str, Any], cfg: Dict[str, Any]) -> Tuple[str, Any, str, Any]:
    head_payload = None
    for key in cfg.get("head_keys") or []:
        if key in record:
            head_payload = record.get(key)
            break
    tail_payload = None
    for key in cfg.get("tail_keys") or []:
        if key in record:
            tail_payload = record.get(key)
            break
    head, head_pos = _extract_fewrel_entity_payload(head_payload)
    tail, tail_pos = _extract_fewrel_entity_payload(tail_payload)
    return head, head_pos, tail, tail_pos


def _wrap_tqdm(iterable: Iterable[Any], desc: str, unit: str, total: int | None = None) -> Iterable[Any]:
    if not TQDM_SETTINGS.get("enabled", True):
        return iterable
    return tqdm(
        iterable,
        desc=desc,
        unit=unit,
        total=total,
        mininterval=TQDM_SETTINGS.get("mininterval", 0.1),
        leave=TQDM_SETTINGS.get("leave", False),
    )


def _generate_relation_types_with_llm(
    config: Dict[str, Any],
    dataset_name: str,
    language: str,
    relation_examples: Dict[str, List[Dict[str, Any]]],
) -> Dict[str, Tuple[str, str]]:
    gen_cfg = _relation_generation_config(config)
    if not gen_cfg.get("enabled", True):
        LOGGER.debug("关系类型 LLM 生成已禁用，跳过。")
        return {}
    if not relation_examples:
        LOGGER.debug("未找到关系样例，跳过 LLM 生成。")
        return {}
    if not any(examples for examples in relation_examples.values()):
        LOGGER.debug("关系样例均为空，跳过 LLM 生成。")
        return {}

    prompt_cfg = gen_cfg.get("prompts", {})
    lang_cfg = prompt_cfg.get(language, {}) if isinstance(prompt_cfg, dict) else {}
    system_prompt = lang_cfg.get("system") or "You are a relation extraction schema expert."
    user_template = lang_cfg.get("user") or (
        "Dataset: {dataset_name}\n"
        "You will receive relation samples as JSON list: {relation_examples}\n"
        "Return JSON with key relationships, each item contains rel_type, head_entity, tail_entity, description."
    )

    sample_limit = int(gen_cfg.get("samples_per_relation", 3))
    user_message = user_template.format(
        dataset_name=dataset_name,
        relation_examples=_format_relation_examples(relation_examples, sample_limit),
    )
    LOGGER.debug("开始调用 LLM 生成关系类型: dataset=%s examples=%s", dataset_name, list(relation_examples.keys()))
    try:
        llm_client = instantiate_llm_client(config)
        response = llm_client.generate(user_message=user_message, system_message=system_prompt)
        payload = _extract_json_payload(response)
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("LLM 关系类型生成失败，使用空映射: %s", exc)
        return {}
    relationships = []
    if isinstance(payload, dict):
        relationships = payload.get("relationships", []) or payload.get("relations", [])
    elif isinstance(payload, list):
        relationships = payload

    mapping: Dict[str, Tuple[str, str]] = {}
    for rel in relationships or []:
        if not isinstance(rel, dict):
            continue
        rel_type = str(rel.get("rel_type", "")).strip()
        head_type = str(rel.get("head_entity", "")).strip()
        tail_type = str(rel.get("tail_entity", "")).strip()
        if not rel_type:
            continue
        mapping[rel_type] = (head_type, tail_type)
    LOGGER.debug("LLM 生成关系类型完成: %s", mapping)
    return mapping

def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_json_lines(
    paths: Sequence[Path],
    desc: str | None = None,
    stats: Dict[str, Any] | None = None,
) -> Iterable[Dict[str, Any]]:
    files = _wrap_tqdm(paths, desc=desc or "读取数据文件", unit="file", total=len(paths))
    for path in files:
        file_count = 0
        text = path.read_text(encoding="utf-8")
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None

        if isinstance(payload, list):
            items = payload
            iterable = items
            if TQDM_SETTINGS.get("show_records", True):
                iterable = _wrap_tqdm(items, desc=f"{path.name} 记录", unit="item", total=len(items))
            for item in iterable:
                if isinstance(item, dict):
                    file_count += 1
                    yield item
            if stats is not None:
                stats.setdefault("file_counts", {})[str(path)] = file_count
                stats["raw_records"] = stats.get("raw_records", 0) + file_count
            continue
        if isinstance(payload, dict):
            file_count = 1
            yield payload
            if stats is not None:
                stats.setdefault("file_counts", {})[str(path)] = file_count
                stats["raw_records"] = stats.get("raw_records", 0) + file_count
            continue

        lines = text.splitlines()
        iterable = lines
        if TQDM_SETTINGS.get("show_records", True):
            iterable = _wrap_tqdm(lines, desc=f"{path.name} 行", unit="line", total=len(lines))
        for line in iterable:
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
                file_count += 1
                yield payload

        if stats is not None:
            stats.setdefault("file_counts", {})[str(path)] = file_count
            stats["raw_records"] = stats.get("raw_records", 0) + file_count


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


def _dedupe_preserve_order(items: Sequence[str]) -> List[str]:
    seen: set[str] = set()
    deduped: List[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped


def _extract_relation_labels_from_payload(payload: Any) -> List[str]:
    if payload is None:
        return []
    if isinstance(payload, str):
        label = payload.strip()
        return [label] if label else []
    if isinstance(payload, list):
        labels: List[str] = []
        for item in payload:
            labels.extend(_extract_relation_labels_from_payload(item))
        return _dedupe_preserve_order([label for label in labels if label])
    if isinstance(payload, dict):
        for key in ("relations", "relation_types", "relation_labels", "labels", "relation_list", "schema", "relationships"):
            if key in payload:
                return _extract_relation_labels_from_payload(payload.get(key))
        for key in ("relation", "rel_type", "predicate", "label", "name"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                return [value.strip()]
    return []


def _extract_relations_from_schema_payload(payload: Any) -> List[Dict[str, str]]:
    relationships: List[Dict[str, str]] = []
    if payload is None:
        return relationships
    if isinstance(payload, list):
        for item in payload:
            relationships.extend(_extract_relations_from_schema_payload(item))
        return relationships
    if isinstance(payload, dict):
        for key in ("relations", "relation_schema", "schema", "relationships"):
            if key in payload:
                relationships.extend(_extract_relations_from_schema_payload(payload.get(key)))
                return relationships
        subject_type = str(payload.get("subject_type", "")).strip()
        predicate = str(payload.get("predicate", "")).strip()
        obj_type_raw = payload.get("object_type", "")
        if isinstance(obj_type_raw, dict):
            obj_type = str(obj_type_raw.get("@value", "")).strip()
        else:
            obj_type = str(obj_type_raw).strip()
        if subject_type or predicate or obj_type:
            rel_type = predicate or str(payload.get("relation", "") or payload.get("rel_type", "")).strip()
            head_type = subject_type or str(payload.get("head_type", "") or payload.get("head_entity", "")).strip()
            tail_type = obj_type or str(payload.get("tail_type", "") or payload.get("tail_entity", "")).strip()
            if rel_type:
                relationships.append(
                    {
                        "head_entity": head_type,
                        "tail_entity": tail_type,
                        "rel_type": rel_type,
                    }
                )
            return relationships
        rel_type = str(
            payload.get("relation", "")
            or payload.get("rel_type", "")
            or payload.get("predicate", "")
            or payload.get("name", "")
        ).strip()
        if rel_type:
            relationships.append(
                {
                    "head_entity": str(payload.get("head_type", "") or payload.get("subject_type", "")).strip(),
                    "tail_entity": str(payload.get("tail_type", "") or payload.get("object_type", "")).strip(),
                    "rel_type": rel_type,
                }
            )
    return relationships


def _parse_relation_schema_payload(payload: Any) -> Tuple[List[Dict[str, str]], List[str]]:
    relationships = _extract_relations_from_schema_payload(payload)
    labels = _extract_relation_labels_from_payload(payload)
    return relationships, labels


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
    LOGGER.debug(
        "解析 schema 标签文件: path=%s line_payloads=%s",
        schema_path,
        len(schema_lines),
    )
    relationships, labels = _parse_relation_schema_payload(schema_lines)
    raw_text = schema_path.read_text(encoding="utf-8").strip()
    try:
        payload = json.loads(raw_text) if raw_text else None
    except json.JSONDecodeError as exc:
        LOGGER.debug("schema 文件整体 JSON 解析失败: path=%s error=%s", schema_path, exc)
        payload = None
    if payload is not None:
        extra_relationships, extra_labels = _parse_relation_schema_payload(payload)
        if extra_relationships or extra_labels:
            LOGGER.debug(
                "schema 整体 JSON 解析结果: path=%s relations=%s labels=%s",
                schema_path,
                len(extra_relationships),
                len(extra_labels),
            )
        relationships.extend(extra_relationships)
        labels = _dedupe_preserve_order(labels + extra_labels)
    if relationships:
        entities: set[str] = set()
        normalized_relationships: List[Dict[str, str]] = []
        seen: set[Tuple[str, str, str]] = set()
        for rel in relationships:
            rel_type = str(rel.get("rel_type", "")).strip()
            head_type = str(rel.get("head_entity", "")).strip()
            tail_type = str(rel.get("tail_entity", "")).strip()
            if not rel_type:
                continue
            key = (head_type, rel_type, tail_type)
            if key in seen:
                continue
            seen.add(key)
            normalized_relationships.append(
                {
                    "head_entity": head_type,
                    "tail_entity": tail_type,
                    "rel_type": rel_type,
                }
            )
            if head_type:
                entities.add(head_type)
            if tail_type:
                entities.add(tail_type)
        LOGGER.debug(
            "schema 关系解析完成: path=%s relationships=%s entities=%s",
            schema_path,
            len(normalized_relationships),
            len(entities),
        )
        return {
            "dataset": dataset_name,
            "language": language,
            "entities": sorted(entities),
            "relationships": normalized_relationships,
        }
    if labels:
        labels = _dedupe_preserve_order([label for label in labels if label])
        LOGGER.debug("schema 标签解析完成: path=%s labels=%s", schema_path, len(labels))
    relationships = [
        {
            "head_entity": "",
            "tail_entity": "",
            "rel_type": rel_type,
        }
        for rel_type in labels
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


def _build_relation_schema_from_examples(
    dataset_name: str,
    language: str,
    relation_examples: Dict[str, List[Dict[str, Any]]],
    mapping: Dict[str, Tuple[str, str]] | None = None,
) -> Dict[str, Any]:
    relationships: List[Dict[str, str]] = []
    entities: set[str] = set()
    mapping = mapping or {}
    for rel_type in sorted(relation_examples.keys()):
        head_type, tail_type = mapping.get(rel_type, ("", ""))
        relationships.append(
            {
                "head_entity": head_type,
                "tail_entity": tail_type,
                "rel_type": rel_type,
            }
        )
        if head_type:
            entities.add(head_type)
        if tail_type:
            entities.add(tail_type)
    return {
        "dataset": dataset_name,
        "language": language,
        "entities": sorted(entities),
        "relationships": relationships,
    }


def _collect_relation_examples_from_json(
    data_paths: Sequence[Path],
    text_field: str,
    relation_field: str,
    desc: str | None = None,
) -> Dict[str, List[Dict[str, Any]]]:
    relation_examples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for record in _iter_json_lines(data_paths, desc=desc):
        text = str(record.get(text_field, "")).strip()
        if not text:
            continue
        relations = record.get(relation_field, [])
        if not isinstance(relations, list):
            continue
        for rel in relations:
            if not isinstance(rel, dict):
                continue
            rel_type = str(rel.get("relation", "")).strip()
            head = str(rel.get("head", "")).strip()
            tail = str(rel.get("tail", "")).strip()
            if not rel_type:
                continue
            relation_examples[rel_type].append({"text": text, "head": head, "tail": tail})
    return relation_examples


def _is_fewrel_episode_payload(payload: Any, cfg: Dict[str, Any]) -> bool:
    if not isinstance(payload, dict):
        return False
    episode_keys = cfg.get("episode_keys") or []
    return any(key in payload for key in episode_keys)


def _iter_fewrel_collection(
    payload: Any,
    rel_type: str,
    cfg: Dict[str, Any],
    path: Path,
) -> Iterable[Dict[str, Any]]:
    if isinstance(payload, list):
        for item in payload:
            yield from _iter_fewrel_collection(item, rel_type, cfg, path)
        return
    if not isinstance(payload, dict):
        return
    if _is_fewrel_episode_payload(payload, cfg):
        yield from _iter_fewrel_episode(payload, cfg, path)
        return
    resolved_rel = _extract_fewrel_rel_type(payload, rel_type, cfg)
    has_text = bool(_extract_fewrel_text(payload, cfg))
    has_entity = any(key in payload for key in (cfg.get("head_keys") or []) + (cfg.get("tail_keys") or []))
    if resolved_rel and (has_text or has_entity):
        yield {**payload, "rel_type": resolved_rel}
        return
    for key, value in payload.items():
        if key in (cfg.get("episode_keys") or []):
            yield from _iter_fewrel_collection(value, rel_type, cfg, path)
        else:
            yield from _iter_fewrel_collection(value, key, cfg, path)


def _iter_fewrel_episode(payload: Dict[str, Any], cfg: Dict[str, Any], path: Path) -> Iterable[Dict[str, Any]]:
    episode_keys = cfg.get("episode_keys") or []
    for key in episode_keys:
        if key not in payload:
            continue
        LOGGER.debug("FewRel episode 解析: file=%s key=%s", path.name, key)
        yield from _iter_fewrel_collection(payload[key], "", cfg, path)


def _iter_fewrel_records(
    data_paths: Sequence[Path],
    fewrel_cfg: Dict[str, Any],
    desc: str | None = None,
    stats: Dict[str, Any] | None = None,
    relation_name_map: Dict[str, str] | None = None,
) -> Iterable[Dict[str, Any]]:
    files = _wrap_tqdm(data_paths, desc=desc or "读取 FewRel 文件", unit="file", total=len(data_paths))
    for path in files:
        file_count = 0
        relation_types: set[str] = set()
        try:
            payload = _load_json(path)
        except json.JSONDecodeError as exc:
            LOGGER.warning("FewRel 文件解析失败，跳过: %s (%s)", path, exc)
            if stats is not None:
                stats.setdefault("file_counts", {})[str(path)] = file_count
            continue
        LOGGER.debug("FewRel 文件载入: path=%s type=%s", path, type(payload).__name__)
        if isinstance(payload, dict):
            if _is_fewrel_episode_payload(payload, fewrel_cfg):
                iterable = _iter_fewrel_episode(payload, fewrel_cfg, path)
            elif payload and all(not isinstance(value, (list, dict)) for value in payload.values()):
                LOGGER.debug("FewRel 跳过关系映射文件: %s", path.name)
                iterable = []
            else:
                iterable = (
                    {**item, "rel_type": rel_type}
                    for rel_type, items in payload.items()
                    if isinstance(items, list)
                    for item in items
                    if isinstance(item, dict)
                )
        elif isinstance(payload, list):
            iterable = _iter_fewrel_collection(payload, "", fewrel_cfg, path)
        else:
            iterable = []
        if TQDM_SETTINGS.get("show_records", True) and isinstance(iterable, list):
            iterable = _wrap_tqdm(iterable, desc=f"{path.name} 记录", unit="item", total=len(iterable))
        for item in iterable:
            if not isinstance(item, dict):
                continue
            rel_type = _extract_fewrel_rel_type(item, item.get("rel_type", ""), fewrel_cfg)
            rel_type = _normalize_fewrel_rel_type(rel_type, item, fewrel_cfg, relation_name_map)
            if not rel_type:
                continue
            file_count += 1
            relation_types.add(rel_type)
            yield {**item, "rel_type": rel_type}
        LOGGER.debug(
            "FewRel 文件解析完成: path=%s records=%s rel_types=%s",
            path.name,
            file_count,
            sorted(relation_types),
        )
        if stats is not None:
            stats.setdefault("file_counts", {})[str(path)] = file_count
            stats["raw_records"] = stats.get("raw_records", 0) + file_count


def _collect_relation_examples_from_fewrel(
    data_paths: Sequence[Path],
    fewrel_cfg: Dict[str, Any],
    desc: str | None = None,
) -> Dict[str, List[Dict[str, Any]]]:
    relation_name_map = _collect_fewrel_relation_name_map(data_paths, fewrel_cfg)
    relation_examples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for record in _iter_fewrel_records(
        data_paths,
        fewrel_cfg,
        desc=desc,
        relation_name_map=relation_name_map,
    ):
        rel_type = str(record.get("rel_type", "")).strip()
        text = _extract_fewrel_text(record, fewrel_cfg)
        if not (rel_type and text):
            continue
        head, _, tail, _ = _extract_fewrel_head_tail(record, fewrel_cfg)
        relation_examples[rel_type].append({"text": text, "head": head, "tail": tail})
    LOGGER.debug(
        "FewRel 样例汇总: relations=%s non_empty=%s",
        len(relation_examples),
        sum(1 for items in relation_examples.values() if items),
    )
    return relation_examples


def _parse_semeval_sentence(raw: str) -> Tuple[str, str, str, List[int], List[int]]:
    head_start = head_end = tail_start = tail_end = None
    output: List[str] = []
    idx = 0
    while idx < len(raw):
        if raw.startswith("<e1>", idx):
            head_start = len(output)
            idx += 4
            continue
        if raw.startswith("</e1>", idx):
            head_end = len(output)
            idx += 5
            continue
        if raw.startswith("<e2>", idx):
            tail_start = len(output)
            idx += 4
            continue
        if raw.startswith("</e2>", idx):
            tail_end = len(output)
            idx += 5
            continue
        output.append(raw[idx])
        idx += 1
    text = "".join(output)
    head_entity = text[head_start:head_end].strip() if head_start is not None and head_end is not None else ""
    tail_entity = text[tail_start:tail_end].strip() if tail_start is not None and tail_end is not None else ""
    head_pos = [head_start or 0, head_end or 0]
    tail_pos = [tail_start or 0, tail_end or 0]
    return text.strip(), head_entity, tail_entity, head_pos, tail_pos


def _clean_semeval_relation_label(raw: str) -> str:
    raw = raw.strip().strip('"')
    if not raw:
        return ""
    if ":" in raw:
        raw = raw.split(":")[-1]
    if "=" in raw:
        raw = raw.split("=")[-1]
    return raw.strip()


def _parse_semeval_relation(raw: str) -> Tuple[str, str]:
    raw = raw.strip()
    match = re.search(r"(.+?)\((e1|e2),(e1|e2)\)", raw)
    if not match:
        return _clean_semeval_relation_label(raw), ""
    rel_type = _clean_semeval_relation_label(match.group(1))
    direction = f"{match.group(2)},{match.group(3)}"
    return rel_type, direction


def _is_semeval_relation_line(raw: str) -> bool:
    raw = raw.strip()
    if not raw:
        return False
    if raw.lower() == "other":
        return True
    return bool(re.search(r".+\((e1|e2),(e1|e2)\)", raw))


def _is_semeval_comment_line(raw: str) -> bool:
    return raw.strip().lower().startswith("comment")


def _advance_semeval_index(lines: Sequence[str], idx: int) -> int:
    while idx < len(lines):
        peek = lines[idx].strip()
        if peek and "\t" in peek:
            break
        idx += 1
    return idx


def _read_semeval_record(
    lines: Sequence[str],
    idx: int,
    label_map: Dict[str, str],
    label_sources: Dict[str, str] | None = None,
) -> Tuple[Dict[str, Any] | None, int]:
    line = lines[idx].strip()
    if not line or "\t" not in line:
        return None, idx + 1

    parts = line.split("\t")
    sample_id = parts[0].strip()
    sentence = parts[1].strip().strip('"') if len(parts) > 1 else ""
    rel_line = ""
    rel_source = "missing"
    rel_line_from_file = False

    if len(parts) > 2:
        rel_line = "\t".join(parts[2:]).strip()
        rel_line_from_file = True
        rel_source = "inline"
        LOGGER.debug("SemEval 行 %s 发现行内关系标签: %s", idx + 1, rel_line)
        next_idx = idx + 1
    else:
        next_idx = idx + 1
        if idx + 1 < len(lines):
            candidate = lines[idx + 1].strip()
            if candidate:
                if _is_semeval_comment_line(candidate):
                    LOGGER.debug("SemEval 行 %s 识别为备注行，跳过: %s", idx + 2, candidate)
                elif _is_semeval_relation_line(candidate):
                    rel_line = candidate
                    rel_line_from_file = True
                    rel_source = "next_line"
                    LOGGER.debug("SemEval 行 %s 读取关系标签: %s", idx + 2, candidate)
                    next_idx = idx + 2
                elif "\t" in candidate:
                    LOGGER.debug("SemEval 行 %s 识别为下一条样本行，等待 label_map 补全。", idx + 2)
                else:
                    LOGGER.debug("SemEval 行 %s 关系标签格式异常，改用 label_map: %s", idx + 2, candidate)

    if not rel_line and sample_id in label_map:
        rel_line = label_map[sample_id]
        rel_source = "label_map"
        source_hint = label_sources.get(sample_id) if label_sources else None
        if source_hint:
            rel_source = source_hint
            LOGGER.debug("SemEval 样本 %s 使用 %s 关系标签: %s", sample_id, source_hint, rel_line)
        else:
            LOGGER.debug("SemEval 样本 %s 使用 label_map 关系标签: %s", sample_id, rel_line)

    if not rel_line:
        rel_line = "Other"
        rel_source = "default"
        LOGGER.debug("SemEval 样本 %s 未找到关系标签，回退为 Other", sample_id)

    next_idx = _advance_semeval_index(lines, next_idx)
    return (
        {
            "id": sample_id,
            "sentence": sentence,
            "relation_line": rel_line,
            "relation_source": rel_source,
            "relation_from_file": rel_line_from_file,
        },
        next_idx,
    )


def _load_semeval_key_labels(label_paths: Sequence[Path]) -> Dict[str, str]:
    label_map: Dict[str, str] = {}
    for label_path in label_paths:
        for line in label_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            parts = line.split("\t", 1)
            if len(parts) >= 2:
                label_map[parts[0].strip()] = parts[1].strip()
    return label_map


def _read_semeval_sentence_map(lines: Sequence[str]) -> Dict[str, str]:
    sentence_map: Dict[str, str] = {}
    for raw in lines:
        raw = raw.strip()
        if not raw or "\t" not in raw:
            continue
        parts = raw.split("\t", 1)
        sample_id = parts[0].strip()
        sentence = parts[1].strip().strip('"')
        if sample_id:
            sentence_map[sample_id] = sentence
    return sentence_map


def _load_semeval_full_labels(
    full_paths: Sequence[Path],
) -> Tuple[Dict[str, str], Dict[str, str]]:
    label_map: Dict[str, str] = {}
    sentence_map: Dict[str, str] = {}
    for full_path in full_paths:
        lines = full_path.read_text(encoding="utf-8").splitlines()
        idx = 0
        while idx < len(lines):
            record, next_idx = _read_semeval_record(lines, idx, {})
            if record is not None:
                label_map[record["id"]] = record["relation_line"]
                sentence_map[record["id"]] = record["sentence"]
            idx = next_idx
    return label_map, sentence_map


def _extract_semeval_relation_types_from_files(paths: Sequence[Path], dataset_name: str) -> List[str]:
    relation_types: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            LOGGER.warning("SemEval schema 文件读取失败: %s (%s)", path, exc)
            continue
        for raw in lines:
            line = raw.strip()
            if not line:
                continue
            if "\t" in line:
                line = line.split("\t")[-1].strip()
            if _is_semeval_comment_line(line):
                continue
            if not _is_semeval_relation_line(line):
                continue
            rel_type, _ = _parse_semeval_relation(line)
            if rel_type:
                relation_types.add(rel_type)
    sorted_types = sorted(relation_types)
    LOGGER.debug(
        "SemEval schema 关系类型统计: dataset=%s count=%s types=%s",
        dataset_name,
        len(sorted_types),
        sorted_types,
    )
    return sorted_types


def convert_semeval2010_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_paths = [schema_path] if isinstance(schema_path, Path) else list(schema_path or [])
    relation_types = _extract_semeval_relation_types_from_files(schema_paths, dataset_name)
    if not relation_types:
        LOGGER.warning("SemEval schema 未解析到关系类型: dataset=%s paths=%s", dataset_name, schema_paths)
    relationships = [
        {
            "head_entity": "",
            "tail_entity": "",
            "rel_type": rel_type,
        }
        for rel_type in relation_types
    ]
    return {
        "dataset": dataset_name,
        "language": language,
        "entities": [],
        "relationships": relationships,
    }


def _parse_semeval_distribution(path: Path) -> Dict[str, Dict[str, int]]:
    distributions: Dict[str, Dict[str, int]] = {}
    current_section: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("<<<") and line.endswith(">>>"):
            current_section = line.strip("<>").strip()
            distributions[current_section] = {}
            continue
        if ":" in line and current_section:
            left, right = line.split(":", 1)
            label = left.strip()
            count_text = right.strip().split()[0]
            try:
                distributions[current_section][label] = int(count_text)
            except ValueError:
                continue
    return distributions


def _summarize_semeval_aux_files(
    dataset_name: str,
    aux_files: Sequence[Path],
    ignore_patterns: Sequence[str] | None = None,
) -> None:
    ignore_patterns = [pattern for pattern in (ignore_patterns or []) if pattern]
    for path in aux_files:
        if not path.exists():
            continue
        if ignore_patterns and any(fnmatch(path.name, pattern) for pattern in ignore_patterns):
            LOGGER.debug("SemEval 附加文件过滤: %s", path.name)
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        lines = content.splitlines()
        filename = path.name
        if filename.endswith("_DISTRIB.TXT") or "DISTRIB" in filename.upper():
            distributions = _parse_semeval_distribution(path)
            LOGGER.debug(
                "SemEval 附加文件 %s 分布统计: %s",
                filename,
                {section: list(values.items())[:5] for section, values in distributions.items()},
            )
        elif "readme" in filename.lower():
            LOGGER.debug("SemEval 附加文件跳过 README: %s", filename)
        else:
            LOGGER.debug(
                "SemEval 附加文件 %s 已读取: 行数=%s 字符数=%s",
                filename,
                len(lines),
                len(content),
            )
    LOGGER.debug("SemEval 数据集 %s 附加文件处理完成。", dataset_name)


def _log_semeval_sentence_consistency(
    dataset_name: str,
    base_sentences: Dict[str, str],
    compare_sentences: Dict[str, str],
    compare_label: str,
) -> None:
    mismatches = 0
    for sample_id, sentence in base_sentences.items():
        other = compare_sentences.get(sample_id)
        if other is None:
            continue
        if sentence != other:
            mismatches += 1
            if mismatches <= 3:
                LOGGER.debug(
                    "SemEval %s 句子不一致: id=%s base=%s compare=%s",
                    compare_label,
                    sample_id,
                    sentence,
                    other,
                )
    LOGGER.debug(
        "SemEval %s 句子一致性检查: base=%s compare=%s 不一致=%s",
        dataset_name,
        len(base_sentences),
        len(compare_sentences),
        mismatches,
    )


def _collect_relation_examples_from_semeval(
    data_paths: Sequence[Path],
    label_paths: Sequence[Path],
    full_label_paths: Sequence[Path] | None = None,
    clean_paths: Sequence[Path] | None = None,
    desc: str | None = None,
) -> Dict[str, List[Dict[str, Any]]]:
    relation_examples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    label_sources: Dict[str, str] = {}
    label_map = _load_semeval_key_labels(label_paths)
    for sample_id in label_map:
        label_sources[sample_id] = "label_key"
    full_label_map: Dict[str, str] = {}
    full_sentences: Dict[str, str] = {}
    if full_label_paths:
        full_label_map, full_sentences = _load_semeval_full_labels(full_label_paths)
        for sample_id in full_label_map:
            label_sources[sample_id] = "label_full"
        label_map = {**label_map, **full_label_map}

    if clean_paths:
        clean_sentences: Dict[str, str] = {}
        for clean_path in clean_paths:
            clean_sentences.update(_read_semeval_sentence_map(clean_path.read_text(encoding="utf-8").splitlines()))
        if clean_sentences and full_sentences:
            _log_semeval_sentence_consistency(desc or "SemEval", full_sentences, clean_sentences, "full_vs_clean")

    files = _wrap_tqdm(data_paths, desc=desc or "读取 SemEval 数据", unit="file", total=len(data_paths))
    for data_path in files:
        file_count = 0
        lines = data_path.read_text(encoding="utf-8").splitlines()
        idx = 0
        while idx < len(lines):
            record, next_idx = _read_semeval_record(lines, idx, label_map, label_sources)
            if record is None:
                idx = next_idx
                continue
            rel_type, direction = _parse_semeval_relation(record["relation_line"])
            text, head_entity, tail_entity, _, _ = _parse_semeval_sentence(record["sentence"])
            if direction == "e2,e1":
                head_entity, tail_entity = tail_entity, head_entity
            relation_examples[rel_type].append({"text": text, "head": head_entity, "tail": tail_entity})
            idx = next_idx
    return relation_examples


def _collect_relation_examples_from_tacred(data_paths: Sequence[Path], desc: str | None = None) -> Dict[str, List[Dict[str, Any]]]:
    relation_examples: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for record in _iter_json_lines(data_paths, desc=desc):
        tokens = record.get("tokens", [])
        text = _join_tokens(tokens if isinstance(tokens, list) else [])
        if not text:
            continue
        rel_type = str(record.get("relation", "")).strip()
        head = str(record.get("subj", "") or record.get("subject", "")).strip()
        tail = str(record.get("obj", "") or record.get("object", "")).strip()
        if not rel_type:
            continue
        relation_examples[rel_type].append({"text": text, "head": head, "tail": tail})
    return relation_examples


def _iter_ast_string_literals(node: ast.AST) -> Iterable[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        yield node.value
        return
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        for item in node.elts:
            yield from _iter_ast_string_literals(item)
        return
    if isinstance(node, ast.Dict):
        for key in node.keys:
            if key is not None:
                yield from _iter_ast_string_literals(key)
        for value in node.values:
            if value is not None:
                yield from _iter_ast_string_literals(value)
        return
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.args:
        if node.func.id in {"set", "list", "tuple"}:
            for arg in node.args:
                yield from _iter_ast_string_literals(arg)


def _extract_tacred_relation_types_from_py(schema_path: Path) -> List[str]:
    relation_types: set[str] = set()
    try:
        tree = ast.parse(schema_path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError) as exc:
        LOGGER.warning("tacred schema Python 解析失败: %s (%s)", schema_path, exc)
        return []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            target_names = [
                target.id
                for target in node.targets
                if isinstance(target, ast.Name)
            ]
            if not target_names:
                continue
            target_hint = ",".join(target_names)
            lower_hint = target_hint.lower()
            if "ner" in lower_hint or "entity" in lower_hint:
                continue
            if not re.search(r"(rel|relation|label)", target_hint, re.IGNORECASE):
                continue
            for value in _iter_ast_string_literals(node.value):
                value = value.strip()
                if value:
                    relation_types.add(value)
    sorted_types = sorted(relation_types)
    LOGGER.debug(
        "tacred schema Python 关系类型统计: path=%s count=%s types=%s",
        schema_path,
        len(sorted_types),
        sorted_types,
    )
    return sorted_types


def _extract_tacred_relation_types(label_paths: Sequence[Path]) -> List[str]:
    relation_types: set[str] = set()
    for path in label_paths:
        if not path.exists():
            continue
        try:
            payload = _load_json(path)
        except json.JSONDecodeError as exc:
            LOGGER.warning("tacred 标签文件解析失败，跳过: %s (%s)", path, exc)
            continue
        if isinstance(payload, dict):
            for value in payload.values():
                rel_type = str(value).strip()
                if rel_type:
                    relation_types.add(rel_type)
            continue
        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    rel_type = str(item.get("relation", "")).strip()
                    if rel_type:
                        relation_types.add(rel_type)
                elif isinstance(item, str):
                    rel_type = item.strip()
                    if rel_type:
                        relation_types.add(rel_type)
    sorted_types = sorted(relation_types)
    LOGGER.debug("tacred 标签文件关系类型统计: count=%s types=%s", len(sorted_types), sorted_types)
    return sorted_types


def _collect_relation_examples_from_tacred_with_labels(
    data_paths: Sequence[Path],
    label_paths: Sequence[Path],
    desc: str | None = None,
) -> Dict[str, List[Dict[str, Any]]]:
    relation_examples = _collect_relation_examples_from_tacred(data_paths, desc=desc)
    label_types = _extract_tacred_relation_types(label_paths)
    for rel_type in label_types:
        relation_examples.setdefault(rel_type, [])
    non_empty = sum(1 for examples in relation_examples.values() if examples)
    LOGGER.debug(
        "tacred 样例汇总: relations=%s non_empty=%s label_only=%s",
        len(relation_examples),
        non_empty,
        len(relation_examples) - non_empty,
    )
    return relation_examples


def _relation_examples_for_format(
    config: Dict[str, Any],
    format_key: str,
    data_files: Sequence[Path],
    dataset_cfg: Dict[str, Any],
    dataset_name: str,
) -> Dict[str, List[Dict[str, Any]]]:
    if format_key == "fewrel":
        fewrel_cfg = _resolve_fewrel_config(config, dataset_cfg)
        return _collect_relation_examples_from_fewrel(
            data_files,
            fewrel_cfg,
            desc=f"{dataset_name} FewRel 样例",
        )
    if format_key == "semeval2010":
        label_files = _collect_paths(dataset_cfg.get("label_files", []) or [])
        full_label_files = _collect_paths(dataset_cfg.get("semeval_full_files", []) or [])
        clean_files = _collect_paths(dataset_cfg.get("semeval_clean_files", []) or [])
        return _collect_relation_examples_from_semeval(
            data_files,
            label_files,
            full_label_paths=full_label_files,
            clean_paths=clean_files,
            desc=f"{dataset_name} SemEval 样例",
        )
    if format_key == "tacred":
        label_files = _collect_label_files(dataset_cfg)
        return _collect_relation_examples_from_tacred_with_labels(
            data_files,
            label_files,
            desc=f"{dataset_name} TACRED 样例",
        )
    return _collect_relation_examples_from_json(
        data_files,
        text_field="text",
        relation_field="relation",
        desc=f"{dataset_name} 关系样例",
    )


def _needs_relation_type_generation(schema_payload: Dict[str, Any], require_entity_types: bool) -> bool:
    relationships = schema_payload.get("relationships", [])
    if not relationships:
        return True
    for rel in relationships:
        if not isinstance(rel, dict):
            continue
        rel_type = str(rel.get("rel_type", "")).strip()
        if not rel_type:
            return True
        if require_entity_types and (not rel.get("head_entity") or not rel.get("tail_entity")):
            return True
    return False


def _apply_relation_type_mapping(
    schema_payload: Dict[str, Any],
    mapping: Dict[str, Tuple[str, str]],
) -> Dict[str, Any]:
    entities: set[str] = set(schema_payload.get("entities") or [])
    relationships = []
    for rel in schema_payload.get("relationships", []):
        if not isinstance(rel, dict):
            continue
        rel_type = str(rel.get("rel_type", "")).strip()
        head_type = str(rel.get("head_entity", "")).strip()
        tail_type = str(rel.get("tail_entity", "")).strip()
        if rel_type in mapping:
            head_type = mapping[rel_type][0] or head_type
            tail_type = mapping[rel_type][1] or tail_type
        relationships.append(
            {
                "head_entity": head_type,
                "tail_entity": tail_type,
                "rel_type": rel_type,
            }
        )
        if head_type:
            entities.add(head_type)
        if tail_type:
            entities.add(tail_type)
    schema_payload["entities"] = sorted(entities)
    schema_payload["relationships"] = relationships
    return schema_payload


def _extract_relation_types(schema_payload: Dict[str, Any]) -> List[str]:
    relations = schema_payload.get("relationships", [])
    types: List[str] = []
    if isinstance(relations, list):
        for rel in relations:
            if isinstance(rel, dict):
                rel_type = str(rel.get("rel_type", "")).strip()
                if rel_type:
                    types.append(rel_type)
            elif isinstance(rel, str):
                rel_type = rel.strip()
                if rel_type:
                    types.append(rel_type)
    return sorted(set(types))


def _support_percentile(values: List[int], percentile: float) -> float:
    if not values:
        return 0.0
    values_sorted = sorted(values)
    index = int(math.ceil(percentile * len(values_sorted))) - 1
    index = max(0, min(index, len(values_sorted) - 1))
    return float(values_sorted[index])


def _compute_support_stats(samples_payload: Sequence[Dict[str, Any]]) -> Dict[str, float | str]:
    counts: List[int] = []
    for group in samples_payload:
        if not isinstance(group, dict):
            continue
        samples = group.get("samples", [])
        if isinstance(samples, list):
            counts.append(len(samples))
    if not counts:
        return {
            "support_min": "NA",
            "support_median": "NA",
            "support_p90": "NA",
            "support_p99": "NA",
            "support_max": "NA",
        }
    return {
        "support_min": min(counts),
        "support_median": round(statistics.median(counts), 4),
        "support_p90": round(_support_percentile(counts, 0.9), 4),
        "support_p99": round(_support_percentile(counts, 0.99), 4),
        "support_max": max(counts),
    }


def _convert_relation_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    text_field: str = "text",
    relation_field: str = "relation",
    category_field: str | None = None,
    mapping: RelationTypeMap | InstructIERelationMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)
    task_value = _normalize_task(task, "re")
    limit = sample_limit if sample_limit > 0 else None
    if limit is None:
        LOGGER.debug("数据集 %s 关系样本限制为全量输出。", dataset_name)

    iter_stats = stats if stats is not None else {}
    for record in _iter_json_lines(data_paths, desc=f"{dataset_name} 样本抽取", stats=iter_stats):
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
            if limit is not None and len(bucket["items"]) >= limit:
                continue

            sample = _normalize_sample(
                RE_SAMPLE_FIELDS,
                {
                    "id": record.get("id", ""),
                    "category": category or record.get("category", ""),
                    "input": text if include_input else "",
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
                    "task": _normalize_task(record.get("task", ""), task_value),
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
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
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)
    limit = sample_limit if sample_limit > 0 else None

    task_value = _normalize_task(task, "re")
    iter_stats = stats if stats is not None else {}
    for record in _iter_json_lines(data_paths, desc=f"{dataset_name} 样本抽取", stats=iter_stats):
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
            if limit is not None and len(bucket["items"]) >= limit:
                continue

            sample = _normalize_sample(
                RE_SAMPLE_FIELDS,
                {
                    "id": record.get("id", ""),
                    "category": record.get("category", ""),
                    "input": text if include_input else "",
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
                    "task": _normalize_task(record.get("task", ""), task_value),
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_fewrel_1_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_1_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_fewrel_2_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_2_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_fewrel_3_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_3_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_fewrel_4_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_fewrel_0_schema(schema_path, dataset_name, language)


def convert_fewrel_4_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_fewrel_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_fewrel_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    fewrel_cfg: Dict[str, Any] | None = None,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)
    mapping = mapping or RelationTypeMap(by_relation={})
    task_value = _normalize_task(task, "re")
    iter_stats = stats if stats is not None else {}
    limit = sample_limit if sample_limit > 0 else None
    fewrel_cfg = {**FEWREL_DEFAULT_CONFIG, **(fewrel_cfg or {})}
    relation_name_map = _collect_fewrel_relation_name_map(data_paths, fewrel_cfg)

    for record in _iter_fewrel_records(
        data_paths,
        fewrel_cfg,
        desc=f"{dataset_name} FewRel 样本",
        stats=iter_stats,
        relation_name_map=relation_name_map,
    ):
        rel_type = str(record.get("rel_type", "")).strip()
        text = _extract_fewrel_text(record, fewrel_cfg)
        if not (rel_type and text):
            continue
        head, head_pos, tail, tail_pos = _extract_fewrel_head_tail(record, fewrel_cfg)
        if not (head and tail):
            continue
        head_type, tail_type = _infer_relation_types(rel_type, mapping)
        key = (head_type, rel_type, tail_type)
        bucket = samples[key]
        if text in bucket["texts"]:
            continue
        if limit is not None and len(bucket["items"]) >= limit:
            continue
        sample = _normalize_sample(
            RE_SAMPLE_FIELDS,
            {
                "id": record.get("id", ""),
                "category": record.get("category", ""),
                "input": text if include_input else "",
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
                "task": _normalize_task(record.get("task", ""), task_value),
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


def convert_semeval2010_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    label_paths: Sequence[Path] | None = None,
    full_label_paths: Sequence[Path] | None = None,
    clean_paths: Sequence[Path] | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)
    mapping = mapping or RelationTypeMap(by_relation={})
    task_value = _normalize_task(task, "re")
    label_sources: Dict[str, str] = {}
    label_map: Dict[str, str] = {}
    limit = sample_limit if sample_limit > 0 else None
    label_map = _load_semeval_key_labels(label_paths or [])
    for sample_id in label_map:
        label_sources[sample_id] = "label_key"
    full_label_map: Dict[str, str] = {}
    full_sentences: Dict[str, str] = {}
    if full_label_paths:
        full_label_map, full_sentences = _load_semeval_full_labels(full_label_paths)
        for sample_id in full_label_map:
            label_sources[sample_id] = "label_full"
        label_map = {**label_map, **full_label_map}

    if clean_paths:
        clean_sentences: Dict[str, str] = {}
        for clean_path in clean_paths:
            clean_sentences.update(_read_semeval_sentence_map(clean_path.read_text(encoding="utf-8").splitlines()))
        if clean_sentences and full_sentences:
            _log_semeval_sentence_consistency(dataset_name, full_sentences, clean_sentences, "full_vs_clean")

    iter_stats = stats if stats is not None else {}
    files = _wrap_tqdm(data_paths, desc=f"{dataset_name} SemEval 样本", unit="file", total=len(data_paths))
    for data_path in files:
        file_count = 0
        lines = data_path.read_text(encoding="utf-8").splitlines()
        idx = 0
        while idx < len(lines):
            record, next_idx = _read_semeval_record(lines, idx, label_map, label_sources)
            if record is None:
                idx = next_idx
                continue
            rel_type, direction = _parse_semeval_relation(record["relation_line"])
            text, head_entity, tail_entity, head_pos, tail_pos = _parse_semeval_sentence(record["sentence"])
            iter_stats["raw_records"] = iter_stats.get("raw_records", 0) + 1
            file_count += 1
            if direction == "e2,e1":
                head_entity, tail_entity = tail_entity, head_entity
                head_pos, tail_pos = tail_pos, head_pos
            head_type, tail_type = _infer_relation_types(rel_type, mapping)
            key = (head_type, rel_type, tail_type)
            bucket = samples[key]
            if text in bucket["texts"]:
                idx = next_idx
                continue
            if limit is not None and len(bucket["items"]) >= limit:
                idx = next_idx
                continue
            sample = _normalize_sample(
                RE_SAMPLE_FIELDS,
                {
                    "id": record["id"],
                    "category": "",
                    "input": text if include_input else "",
                    "text": text,
                    "head_entity": head_entity,
                    "head_entity_type": head_type,
                    "head_pos": head_pos,
                    "tail_entity": tail_entity,
                    "tail_entity_type": tail_type,
                    "tail_pos": tail_pos,
                    "relation": rel_type,
                    "dataset": dataset_name,
                    "language": language,
                    "task": task_value,
                },
            )
            bucket["items"].append(sample)
            bucket["texts"].add(text)
            idx = next_idx
        iter_stats.setdefault("file_counts", {})[str(data_path)] = file_count

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


def convert_tacred_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    schema_paths = [schema_path] if isinstance(schema_path, Path) else list(schema_path or [])
    relation_types: List[str] = []
    for path in schema_paths:
        if path.suffix.lower() == ".py":
            relation_types.extend(_extract_tacred_relation_types_from_py(path))
        else:
            relation_types.extend(_extract_tacred_relation_types([path]))
    relation_types = _dedupe_preserve_order([item for item in relation_types if item])
    if not relation_types:
        LOGGER.warning("tacred schema 未解析到关系类型: dataset=%s paths=%s", dataset_name, schema_paths)
    relationships = [
        {
            "head_entity": "",
            "tail_entity": "",
            "rel_type": rel_type,
        }
        for rel_type in relation_types
    ]
    return {
        "dataset": dataset_name,
        "language": language,
        "entities": [],
        "relationships": relationships,
    }


def convert_tacred_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    samples: Dict[Tuple[str, str, str], Dict[str, Any]] = defaultdict(_new_sample_bucket)
    mapping = mapping or RelationTypeMap(by_relation={})
    task_value = _normalize_task(task, "re")
    iter_stats = stats if stats is not None else {}
    limit = sample_limit if sample_limit > 0 else None

    for record in _iter_json_lines(data_paths, desc=f"{dataset_name} TACRED 样本", stats=iter_stats):
        tokens = record.get("tokens", [])
        if not isinstance(tokens, list):
            continue
        text = _join_tokens(tokens)
        if not text:
            continue
        rel_type = str(record.get("relation", "")).strip()
        if not rel_type:
            continue
        head_start = record.get("subj_start")
        head_end = record.get("subj_end")
        tail_start = record.get("obj_start")
        tail_end = record.get("obj_end")
        head = str(record.get("subj", "")).strip()
        tail = str(record.get("obj", "")).strip()
        if head_start is not None and head_end is not None and not head:
            head = _join_tokens(tokens[int(head_start) : int(head_end) + 1])
        if tail_start is not None and tail_end is not None and not tail:
            tail = _join_tokens(tokens[int(tail_start) : int(tail_end) + 1])
        if not (head and tail):
            continue
        head_type = str(record.get("subj_type", "")).strip()
        tail_type = str(record.get("obj_type", "")).strip()
        if not (head_type and tail_type):
            head_type, tail_type = _infer_relation_types(rel_type, mapping)
        key = (head_type, rel_type, tail_type)
        bucket = samples[key]
        if text in bucket["texts"]:
            continue
        if limit is not None and len(bucket["items"]) >= limit:
            continue
        sample = _normalize_sample(
            RE_SAMPLE_FIELDS,
            {
                "id": record.get("id", ""),
                "category": record.get("category", ""),
                "input": text if include_input else "",
                "text": text,
                "head_entity": head,
                "head_entity_type": head_type,
                "head_pos": [head_start, head_end] if head_start is not None else "",
                "tail_entity": tail,
                "tail_entity_type": tail_type,
                "tail_pos": [tail_start, tail_end] if tail_start is not None else "",
                "relation": rel_type,
                "dataset": dataset_name,
                "language": language,
                "task": _normalize_task(record.get("task", ""), task_value),
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return _convert_relation_inputs(
        data_paths=data_paths,
        dataset_name=dataset_name,
        language=language,
        sample_limit=sample_limit,
        text_field="text",
        relation_field="relation",
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_wiki_1_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_1_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_wiki_2_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_2_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_wiki_3_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_3_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


def convert_wiki_4_schema(schema_path: Path | Sequence[Path], dataset_name: str, language: str) -> Dict[str, Any]:
    return convert_wiki_0_schema(schema_path, dataset_name, language)


def convert_wiki_4_inputs(
    data_paths: Sequence[Path],
    dataset_name: str,
    language: str,
    sample_limit: int,
    mapping: RelationTypeMap | None = None,
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    return convert_wiki_0_inputs(
        data_paths,
        dataset_name,
        language,
        sample_limit,
        mapping=mapping,
        task=task,
        include_input=include_input,
        stats=stats,
    )


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
    task: str | None = None,
    include_input: bool = False,
    stats: Dict[str, Any] | None = None,
) -> List[Dict[str, Any]]:
    samples: Dict[str, Dict[str, Any]] = defaultdict(_new_sample_bucket)
    task_value = _normalize_task(task, "ee")
    iter_stats = stats if stats is not None else {}
    limit = sample_limit if sample_limit > 0 else None
    if limit is None:
        LOGGER.debug("数据集 %s 事件样本限制为全量输出。", dataset_name)

    for record in _iter_json_lines(data_paths, desc=f"{dataset_name} 事件样本", stats=iter_stats):
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
            if limit is not None and len(bucket["items"]) >= limit:
                continue

            sample = _normalize_sample(
                EE_SAMPLE_FIELDS,
                {
                    "id": record.get("id", ""),
                    "input": text if include_input else "",
                    "text": text,
                    "event_type": event_type,
                    "event_trigger": event_trigger,
                    "trigger_pos": trigger_pos,
                    "arguments": arguments,
                    "entity": entities,
                    "dataset": dataset_name,
                    "language": language,
                    "task": _normalize_task(record.get("task", ""), task_value),
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


def _collect_label_files(dataset_cfg: Dict[str, Any]) -> List[Path]:
    label_files = _collect_paths(dataset_cfg.get("label_files", []) or [])
    label_dirs = dataset_cfg.get("label_dirs", []) or []
    label_glob = dataset_cfg.get("label_glob") or "**/*.txt"
    label_files.extend(_collect_files_from_dirs(label_dirs, label_glob))
    resolved = [path for path in label_files if path.exists()]
    LOGGER.debug("已收集 label 文件: %s", [str(path) for path in resolved])
    return resolved


def _resolve_output_paths(
    output_dir: Path,
    dataset_cfg: Dict[str, Any],
    dataset_name: str,
) -> Tuple[Path, Path]:
    language = str(dataset_cfg.get("language", "")).lower() or "zh"
    schema_out = Path(dataset_cfg.get("schema_output") or f"golden_schema_{dataset_name}.json")
    samples_out = Path(dataset_cfg.get("samples_output") or f"golden_input_{dataset_name}.json")
    schema_out = apply_language_suffix(schema_out, language)
    samples_out = apply_language_suffix(samples_out, language)
    if not schema_out.is_absolute():
        schema_out = output_dir / schema_out
    if not samples_out.is_absolute():
        samples_out = output_dir / samples_out
    return resolve_project_path(schema_out), resolve_project_path(samples_out)


def _resolve_sample_limit(dataset_cfg: Dict[str, Any], default_limit: int, key: str) -> int:
    dataset_limit = dataset_cfg.get(key)
    if dataset_limit is None:
        return default_limit
    try:
        return int(dataset_limit)
    except (TypeError, ValueError):
        return default_limit


def _describe_sample_limit(sample_limit: int) -> str:
    return "全量" if sample_limit <= 0 else str(sample_limit)


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
    config: Dict[str, Any],
    dataset_cfg: Dict[str, Any],
    output_dir: Path,
    sample_limit: int,
    results: Dict[str, List[Path]],
    stats: List[DatasetConversionStats],
) -> None:
    name = dataset_cfg.get("name")
    language = dataset_cfg.get("language", "").lower() or "zh"
    format_key = _normalize_dataset_name(dataset_cfg.get("format") or dataset_cfg.get("type"))
    task_value = _normalize_task(dataset_cfg.get("task"), "re")
    dataset_name = str(name)
    conv_cfg = config.get("dataset_conversion") or {}
    schema_gen_cfg = _relation_generation_config(config)
    require_entity_types = bool(schema_gen_cfg.get("require_entity_types", False))
    include_input = bool(dataset_cfg.get("include_input", conv_cfg.get("include_input", False)))
    resolved_limit = _resolve_sample_limit(dataset_cfg, sample_limit, "samples_per_relation")
    LOGGER.debug(
        "准备处理关系抽取数据集: %s (format=%s, language=%s, task=%s, include_input=%s, limit=%s)",
        dataset_name,
        format_key,
        language,
        task_value,
        include_input,
        _describe_sample_limit(resolved_limit),
    )

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
        "fewrel": (None, convert_fewrel_inputs),
        "semeval2010": (convert_semeval2010_schema, convert_semeval2010_inputs),
        "tacred": (convert_tacred_schema, convert_tacred_inputs),
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
    label_files = _collect_label_files(dataset_cfg)
    semeval_full_files = _collect_paths(dataset_cfg.get("semeval_full_files", []) or [])
    semeval_clean_files = _collect_paths(dataset_cfg.get("semeval_clean_files", []) or [])
    semeval_aux_files = _collect_paths(dataset_cfg.get("semeval_aux_files", []) or [])
    semeval_aux_ignore = (
        dataset_cfg.get("semeval_aux_ignore")
        or (config.get("dataset_conversion") or {}).get("semeval_aux_ignore")
        or []
    )
    LOGGER.debug(
        "关系抽取数据集 %s schema_paths=%s data_files=%s label_files=%s",
        dataset_name,
        [str(path) for path in schema_paths],
        [str(path) for path in data_files],
        [str(path) for path in label_files],
    )
    if format_key == "tacred" and not schema_paths and label_files:
        schema_paths = label_files
        LOGGER.debug(
            "tacred 未找到 schema_path，使用 label_files 作为 schema 来源: %s",
            [str(path) for path in schema_paths],
        )
    if format_key == "semeval2010":
        LOGGER.debug(
            "SemEval 附加文件: full=%s clean=%s aux=%s",
            [str(path) for path in semeval_full_files],
            [str(path) for path in semeval_clean_files],
            [str(path) for path in semeval_aux_files],
        )
        _summarize_semeval_aux_files(dataset_name, semeval_aux_files, semeval_aux_ignore)
    if not data_files:
        LOGGER.warning("关系抽取数据集 %s 未配置 data_files", dataset_name)
        return

    schema_out, samples_out = _resolve_output_paths(output_dir, dataset_cfg, dataset_name)
    schema_payload: Dict[str, Any]
    mapping: RelationTypeMap | None = None
    llm_attempted = False
    llm_generated_items: List[str] = []
    llm_used = False
    if handlers[format_key][0] and schema_paths:
        schema_payload, mapping = _run_schema_converter(handlers[format_key][0], schema_paths, dataset_name, language)
    else:
        LOGGER.info("数据集 %s 未提供 schema，尝试从数据生成。", dataset_name)
        relation_examples = _relation_examples_for_format(config, format_key, data_files, dataset_cfg, dataset_name)
        llm_mapping = _generate_relation_types_with_llm(config, dataset_name, language, relation_examples)
        llm_attempted = True
        if llm_mapping:
            llm_used = True
            llm_generated_items = sorted(llm_mapping.keys())
        schema_payload = _build_relation_schema_from_examples(dataset_name, language, relation_examples, llm_mapping)
        mapping = RelationTypeMap(by_relation=llm_mapping)

    if _needs_relation_type_generation(schema_payload, require_entity_types) and not llm_attempted:
        LOGGER.info(
            "数据集 %s 需要补全关系 schema: require_entity_types=%s, 启用 LLM 补全。",
            dataset_name,
            require_entity_types,
        )
        relation_examples = _relation_examples_for_format(config, format_key, data_files, dataset_cfg, dataset_name)
        llm_mapping = _generate_relation_types_with_llm(config, dataset_name, language, relation_examples)
        if llm_mapping:
            llm_used = True
            llm_generated_items = sorted(llm_mapping.keys())
            schema_payload = _apply_relation_type_mapping(schema_payload, llm_mapping)
            mapping = RelationTypeMap(by_relation=llm_mapping)
    elif not llm_attempted:
        LOGGER.debug(
            "数据集 %s schema 已满足要求: require_entity_types=%s, 跳过 LLM 补全。",
            dataset_name,
            require_entity_types,
        )
    if llm_used and llm_generated_items:
        LOGGER.debug("数据集 %s LLM 补全关系类型: %s", dataset_name, ", ".join(llm_generated_items))

    relation_types = _extract_relation_types(schema_payload)
    unique_relation_types = sorted(set(relation_types))
    LOGGER.debug(
        "数据集 %s 关系类型统计: 总数=%s 去重数=%s 列表=%s",
        dataset_name,
        len(relation_types),
        len(unique_relation_types),
        unique_relation_types,
    )
    save_json(schema_out, schema_payload)

    if format_key == "semeval2010":
        sample_stats: Dict[str, Any] = {"file_counts": {}}
        samples_payload = handlers[format_key][1](
            data_files,
            dataset_name,
            language,
            resolved_limit,
            mapping=mapping,
            label_paths=label_files,
            full_label_paths=semeval_full_files,
            clean_paths=semeval_clean_files,
            task=task_value,
            include_input=include_input,
            stats=sample_stats,
        )
    else:
        sample_stats = {"file_counts": {}}
        extra_kwargs: Dict[str, Any] = {}
        if format_key == "fewrel":
            extra_kwargs["fewrel_cfg"] = _resolve_fewrel_config(config, dataset_cfg)
        samples_payload = handlers[format_key][1](
            data_files,
            dataset_name,
            language,
            resolved_limit,
            mapping=mapping,
            task=task_value,
            include_input=include_input,
            stats=sample_stats,
            **extra_kwargs,
        )

    save_json(samples_out, samples_payload)
    results["schemas"].append(schema_out)
    results["samples"].append(samples_out)

    total_samples = sum(len(item.get("samples", [])) for item in samples_payload)
    raw_records = sample_stats.get("raw_records", 0)
    support_stats = _compute_support_stats(samples_payload)
    LOGGER.debug(
        "关系抽取数据集 %s 关系数=%s 样本数=%s 原始记录数=%s",
        dataset_name,
        len(samples_payload),
        total_samples,
        raw_records,
    )
    for file_path, count in sample_stats.get("file_counts", {}).items():
        if count == 0:
            LOGGER.warning("关系抽取数据集 %s 文件未解析到记录: %s", dataset_name, file_path)
    LOGGER.debug(
        "完成关系抽取数据集 %s -> schema: %s, samples: %s", dataset_name, schema_out, samples_out
    )
    schema_count = len(schema_payload.get("relationships", []))
    relation_types = _extract_relation_types(schema_payload)
    relation_types_source = "schema_file" if schema_paths else "generated"
    stats.append(
        DatasetConversionStats(
            name=dataset_name,
            task=task_value,
            language=language,
            format_key=format_key,
            schema_count=schema_count,
            schema_roles=0,
            sample_count=total_samples,
            raw_records=raw_records,
            sample_limit=resolved_limit,
            include_input=include_input,
            schema_output=str(schema_out),
            samples_output=str(samples_out),
            data_files=[str(path) for path in data_files],
            schema_paths=[str(path) for path in schema_paths],
            schema_has_file=bool(schema_paths),
            relation_types=relation_types,
            relation_types_source=relation_types_source,
            relation_types_llm_generated=llm_used,
            relation_types_llm_items=llm_generated_items,
            support_min=support_stats["support_min"],
            support_median=support_stats["support_median"],
            support_p90=support_stats["support_p90"],
            support_p99=support_stats["support_p99"],
            support_max=support_stats["support_max"],
        )
    )


def _run_ee_dataset_conversion(
    dataset_cfg: Dict[str, Any],
    output_dir: Path,
    sample_limit: int,
    default_include_input: bool,
    results: Dict[str, List[Path]],
    stats: List[DatasetConversionStats],
) -> None:
    name = dataset_cfg.get("name")
    language = dataset_cfg.get("language", "").lower() or "zh"
    format_key = _normalize_dataset_name(dataset_cfg.get("format") or dataset_cfg.get("type"))
    task_value = _normalize_task(dataset_cfg.get("task"), "ee")
    dataset_name = str(name)
    include_input = bool(dataset_cfg.get("include_input", default_include_input))
    resolved_limit = _resolve_sample_limit(dataset_cfg, sample_limit, "samples_per_event")
    LOGGER.debug(
        "准备处理事件抽取数据集: %s (format=%s, language=%s, task=%s, include_input=%s, limit=%s)",
        dataset_name,
        format_key,
        language,
        task_value,
        include_input,
        _describe_sample_limit(resolved_limit),
    )

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

    sample_stats: Dict[str, Any] = {"file_counts": {}}
    samples_payload = _convert_event_inputs(
        data_files,
        dataset_name,
        language,
        resolved_limit,
        task=task_value,
        include_input=include_input,
        stats=sample_stats,
    )

    save_json(samples_out, samples_payload)
    results["schemas"].append(schema_out)
    results["samples"].append(samples_out)

    total_samples = sum(len(item.get("samples", [])) for item in samples_payload)
    raw_records = sample_stats.get("raw_records", 0)
    support_stats = _compute_support_stats(samples_payload)
    LOGGER.debug(
        "事件抽取数据集 %s 事件类型数=%s 样本数=%s 原始记录数=%s",
        dataset_name,
        len(samples_payload),
        total_samples,
        raw_records,
    )
    for file_path, count in sample_stats.get("file_counts", {}).items():
        if count == 0:
            LOGGER.warning("事件抽取数据集 %s 文件未解析到记录: %s", dataset_name, file_path)
    LOGGER.debug(
        "完成事件抽取数据集 %s -> schema: %s, samples: %s", dataset_name, schema_out, samples_out
    )
    event_types = schema_payload.get("event_types", [])
    roles = schema_payload.get("roles", [])
    stats.append(
        DatasetConversionStats(
            name=dataset_name,
            task=task_value,
            language=language,
            format_key=format_key,
            schema_count=len(event_types) if isinstance(event_types, list) else 0,
            schema_roles=len(roles) if isinstance(roles, list) else 0,
            sample_count=total_samples,
            raw_records=raw_records,
            sample_limit=resolved_limit,
            include_input=include_input,
            schema_output=str(schema_out),
            samples_output=str(samples_out),
            data_files=[str(path) for path in data_files],
            schema_paths=[str(path) for path in schema_paths],
            schema_has_file=bool(schema_paths),
            relation_types=[],
            relation_types_source="na",
            relation_types_llm_generated=False,
            relation_types_llm_items=[],
            support_min=support_stats["support_min"],
            support_median=support_stats["support_median"],
            support_p90=support_stats["support_p90"],
            support_p99=support_stats["support_p99"],
            support_max=support_stats["support_max"],
        )
    )


def convert_from_config(config: Dict[str, Any]) -> Dict[str, List[Path]]:
    _apply_tqdm_settings(config)
    conv_cfg = config.get("dataset_conversion") or {}
    results: Dict[str, List[Path]] = {"schemas": [], "samples": [], "stats": []}
    stats: List[DatasetConversionStats] = []

    re_cfg = conv_cfg.get("re")
    ee_cfg = conv_cfg.get("ee")
    if re_cfg or ee_cfg:
        LOGGER.debug("使用新版 dataset_conversion 配置。")
        if re_cfg:
            re_output_dir = resolve_project_path(re_cfg.get("output_dir", conv_cfg.get("output_dir", "data/input/re")))
            re_sample_limit = int(conv_cfg.get("samples_per_relation", 0))
            re_entries = re_cfg.get("dataset_configs", []) or []
            re_map = {_normalize_dataset_name(entry.get("name")): entry for entry in re_entries if entry.get("name")}
            selected_names = list(_resolve_selected_datasets(re_cfg.get("datasets", "all"), re_map))
            LOGGER.debug(
                "关系抽取配置: output_dir=%s sample_limit=%s datasets=%s total=%s",
                re_output_dir,
                re_sample_limit,
                re_cfg.get("datasets"),
                len(selected_names),
            )
            for name in _wrap_tqdm(
                selected_names,
                desc="关系抽取数据集",
                unit="dataset",
                total=len(selected_names),
            ):
                ds_cfg = re_map.get(name)
                if not ds_cfg:
                    LOGGER.warning("未找到关系抽取数据集配置: %s", name)
                    continue
                _run_re_dataset_conversion(config, ds_cfg, re_output_dir, re_sample_limit, results, stats)

        if ee_cfg:
            ee_output_dir = resolve_project_path(ee_cfg.get("output_dir", conv_cfg.get("output_dir", "data/input/ee")))
            ee_sample_limit = int(conv_cfg.get("samples_per_event", 0))
            ee_entries = ee_cfg.get("dataset_configs", []) or []
            ee_map = {_normalize_dataset_name(entry.get("name")): entry for entry in ee_entries if entry.get("name")}
            selected_names = list(_resolve_selected_datasets(ee_cfg.get("datasets", "all"), ee_map))
            LOGGER.debug(
                "事件抽取配置: output_dir=%s sample_limit=%s datasets=%s total=%s",
                ee_output_dir,
                ee_sample_limit,
                ee_cfg.get("datasets"),
                len(selected_names),
            )
            for name in _wrap_tqdm(
                selected_names,
                desc="事件抽取数据集",
                unit="dataset",
                total=len(selected_names),
            ):
                ds_cfg = ee_map.get(name)
                if not ds_cfg:
                    LOGGER.warning("未找到事件抽取数据集配置: %s", name)
                    continue
                _run_ee_dataset_conversion(
                    ds_cfg,
                    ee_output_dir,
                    ee_sample_limit,
                    bool(conv_cfg.get("include_input", False)),
                    results,
                    stats,
                )

        results["stats"] = stats
        summary_path = resolve_project_path(
            conv_cfg.get("data_info_path", conv_cfg.get("output_dir", "data/input") + "/data_info.txt")
        )
        if stats:
            summary_text = build_conversion_summary(stats)
            LOGGER.info("\n%s", summary_text)
            write_conversion_summary(summary_path, stats)
        else:
            LOGGER.info("未生成任何数据集统计信息，跳过汇总写入。")
        return results

    output_dir = resolve_project_path(conv_cfg.get("output_dir", "data/input"))
    sample_limit = int(conv_cfg.get("samples_per_relation", 0))
    LOGGER.debug("使用旧版 dataset_conversion 配置: output_dir=%s sample_limit=%s", output_dir, sample_limit)
    legacy_datasets = [
        dataset_cfg
        for dataset_cfg in conv_cfg.get("datasets", [])
        if dataset_cfg.get("name") and str(dataset_cfg.get("type", "")).lower() in {"instructie", "duie"}
    ]
    LOGGER.debug("旧版配置待处理数据集数量: %s", len(legacy_datasets))

    for dataset_cfg in _wrap_tqdm(
        legacy_datasets,
        desc="旧版数据集",
        unit="dataset",
        total=len(legacy_datasets),
    ):
        name = dataset_cfg.get("name")
        ds_type = str(dataset_cfg.get("type", "")).lower()
        language = dataset_cfg.get("language", "").lower() or "zh"

        schema_path = resolve_project_path(dataset_cfg.get("schema_path", ""))
        data_files = [resolve_project_path(p) for p in dataset_cfg.get("data_files", [])]

        schema_out = apply_language_suffix(
            Path(dataset_cfg.get("schema_output") or f"golden_schema_{name}.json"),
            language,
        )
        samples_out = apply_language_suffix(
            Path(dataset_cfg.get("samples_output") or f"golden_input_{name}.json"),
            language,
        )

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
                task=dataset_cfg.get("task"),
                include_input=bool(dataset_cfg.get("include_input", conv_cfg.get("include_input", False))),
            )
        else:
            schema_payload = convert_duie_schema(schema_path, name, language)
            save_json(schema_path_out, schema_payload)
            samples_payload = convert_duie_inputs(
                data_paths=data_files,
                dataset_name=name,
                language=language,
                sample_limit=sample_limit,
                task=dataset_cfg.get("task"),
                include_input=bool(dataset_cfg.get("include_input", conv_cfg.get("include_input", False))),
            )

        save_json(samples_path_out, samples_payload)
        results["schemas"].append(schema_path_out)
        results["samples"].append(samples_path_out)

    results["stats"] = stats
    summary_path = resolve_project_path(
        conv_cfg.get("data_info_path", conv_cfg.get("output_dir", "data/input") + "/data_info.txt")
    )
    if stats:
        summary_text = build_conversion_summary(stats)
        LOGGER.info("\n%s", summary_text)
        write_conversion_summary(summary_path, stats)
    else:
        LOGGER.info("未生成任何数据集统计信息，跳过汇总写入。")
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
