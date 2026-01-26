"""本体结构构建与加载的可复用工具。"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set

from .logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


def normalize_label(label: str | None) -> str:
    if label is None:
        return ""
    return str(label).strip().lower()


def _schema_from_sequence(items: Sequence[Any]) -> Dict[str, Any]:
    entities: Set[str] = set()
    relationships: List[Dict[str, str]] = []
    events: List[Dict[str, Any]] = []

    for idx, item in enumerate(items):
        if isinstance(item, str):
            label = item.strip()
            if label:
                entities.add(label)
            continue
        if not isinstance(item, dict):
            LOGGER.debug("跳过非字典/字符串的 schema 条目: index=%s type=%s", idx, type(item).__name__)
            continue

        if {"head_entity", "tail_entity", "rel_type"}.issubset(item.keys()):
            head = str(item.get("head_entity") or "").strip()
            tail = str(item.get("tail_entity") or "").strip()
            rel_type = str(item.get("rel_type") or "").strip()
            if not (head and tail and rel_type):
                LOGGER.debug("跳过不完整关系条目: index=%s item=%s", idx, item)
                continue
            entities.update([head, tail])
            relationships.append({"head_entity": head, "rel_type": rel_type, "tail_entity": tail})
            continue

        if "event_type" in item:
            event_type = str(item.get("event_type") or "").strip()
            if not event_type:
                LOGGER.debug("跳过空 event_type 条目: index=%s item=%s", idx, item)
                continue
            description = str(item.get("description") or "").strip()
            trigger_words = [str(word).strip() for word in item.get("trigger_words", []) if str(word).strip()]
            arguments: List[Dict[str, Any]] = []
            for arg in item.get("arguments", []) or []:
                if not isinstance(arg, dict):
                    continue
                role = str(arg.get("role") or "").strip()
                if not role:
                    continue
                arguments.append(
                    {
                        "role": role,
                        "description": str(arg.get("description") or "").strip(),
                        "required": bool(arg.get("required", False)),
                    }
                )
            events.append(
                {
                    "event_type": event_type,
                    "description": description,
                    "trigger_words": trigger_words,
                    "arguments": arguments,
                }
            )
            continue

        if "entity" in item:
            label = str(item.get("entity") or "").strip()
            if label:
                entities.add(label)
                continue

        LOGGER.debug("未识别的 schema 条目: index=%s keys=%s", idx, sorted(item.keys()))

    schema: Dict[str, Any] = {
        "entities": sorted(entities),
        "relationships": relationships,
    }
    if events:
        schema["events"] = events
    LOGGER.debug(
        "从列表 schema 生成结构: entities=%s relationships=%s events=%s",
        len(schema.get("entities", [])),
        len(schema.get("relationships", [])),
        len(schema.get("events", [])) if schema.get("events") else 0,
    )
    return schema


def load_schema_file(path: str | Path) -> Dict[str, Any]:
    schema_path = Path(path)
    if not schema_path.exists():
        raise FileNotFoundError(f"未找到本体文件: {schema_path}")
    LOGGER.debug("加载本体文件: %s", schema_path)
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        LOGGER.debug("本体文件为 JSON 对象: keys=%s", sorted(data.keys()))
        return data
    if isinstance(data, list):
        LOGGER.debug("本体文件为 JSON 数组: len=%s", len(data))
        return _schema_from_sequence(data)
    raise ValueError("本体文件必须是 JSON 对象。")


@dataclass(frozen=True)
class Edge:
    src: str
    tgt: str


@dataclass
class OntologyGraph:
    nodes: Dict[str, str]
    edges: Set[Edge]


class _SchemaGraphBuilder:
    def __init__(self) -> None:
        self.nodes: Dict[str, str] = {}
        self.edges: Set[Edge] = set()
        self._label_to_id: Dict[str, str] = {}
        self._counter = 0
        self.root_label = "__root__"
        self.root_id = self._ensure_node(self.root_label)

    def _ensure_node(self, label: str) -> str:
        normalized = normalize_label(label)
        key = normalized or label.strip().lower() or f"node-{self._counter}"
        if key in self._label_to_id:
            return self._label_to_id[key]
        node_id = f"n{self._counter:05d}"
        self._counter += 1
        self._label_to_id[key] = node_id
        self.nodes[node_id] = normalized or label.strip() or key
        return node_id

    def add_edge_by_labels(self, src_label: str, tgt_label: str) -> None:
        src_id = self._ensure_node(src_label)
        tgt_id = self._ensure_node(tgt_label)
        if src_id == tgt_id:
            return
        self.edges.add(Edge(src=src_id, tgt=tgt_id))

    def add_section(self, section_label: str) -> str:
        section_id = self._ensure_node(section_label)
        self.add_edge_by_labels(self.root_label, section_label)
        return section_id


def _normalize_entities(items: Sequence[Any] | None) -> List[str]:
    normalized: List[str] = []
    for item in items or []:
        label = ""
        if isinstance(item, str):
            label = item.strip()
        elif isinstance(item, dict):
            for key, value in item.items():
                key_str = str(key).strip()
                desc_str = str(value).strip()
                label = f"{key_str}: {desc_str}" if desc_str else key_str
                break
        if label:
            normalized.append(label)
    return normalized


def _normalize_relationships(items: Sequence[Any] | None) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        head = str(item.get("head_entity", "")).strip()
        tail = str(item.get("tail_entity", "")).strip()
        rel_type = str(item.get("rel_type", "")).strip()
        if not (head and tail and rel_type):
            continue
        normalized.append(
            {
                "head_entity": head,
                "tail_entity": tail,
                "rel_type": rel_type,
                "description": str(item.get("description", "")).strip(),
            }
        )
    return normalized


def _normalize_events(items: Sequence[Any] | None) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items or []:
        if not isinstance(item, dict):
            continue
        event_type = str(item.get("event_type", "")).strip()
        if not event_type:
            continue
        description = str(item.get("description", "")).strip()
        trigger_words = [str(word).strip() for word in item.get("trigger_words", []) if str(word).strip()]
        arguments: List[Dict[str, Any]] = []
        for arg in item.get("arguments", []):
            if not isinstance(arg, dict):
                continue
            role = str(arg.get("role", "")).strip()
            if not role:
                continue
            arguments.append(
                {
                    "role": role,
                    "description": str(arg.get("description", "")).strip(),
                    "required": bool(arg.get("required", False)),
                }
            )
        normalized.append(
            {
                "event_type": event_type,
                "description": description,
                "trigger_words": trigger_words,
                "arguments": arguments,
            }
        )
    return normalized


def schema_dict_to_graph(schema: Dict[str, Any]) -> OntologyGraph:
    builder = _SchemaGraphBuilder()

    entities = _normalize_entities(schema.get("entities"))
    if entities:
        section_label = "section::entities"
        builder.add_edge_by_labels(builder.root_label, section_label)
        for label in entities:
            builder.add_edge_by_labels(section_label, label)

    relationships = _normalize_relationships(schema.get("relationships"))
    if relationships:
        section_label = "section::relationships"
        builder.add_edge_by_labels(builder.root_label, section_label)
        for rel in relationships:
            rel_label = f"{rel['head_entity']} -> {rel['tail_entity']} ({rel['rel_type']})"
            builder.add_edge_by_labels(section_label, rel_label)
            builder.add_edge_by_labels(rel["head_entity"], rel_label)
            builder.add_edge_by_labels(rel_label, rel["tail_entity"])
            if rel.get("description"):
                builder.add_edge_by_labels(rel_label, f"desc::{rel['description']}")

    events = _normalize_events(schema.get("events"))
    if events:
        section_label = "section::events"
        builder.add_edge_by_labels(builder.root_label, section_label)
        for event in events:
            event_label = f"event::{event['event_type']}"
            builder.add_edge_by_labels(section_label, event_label)
            if event.get("description"):
                builder.add_edge_by_labels(event_label, f"desc::{event['description']}")
            for trig in event.get("trigger_words", []):
                builder.add_edge_by_labels(event_label, f"trigger::{event['event_type']}::{trig}")
            for arg in event.get("arguments", []):
                arg_label = f"argument::{event['event_type']}::{arg['role']}"
                builder.add_edge_by_labels(event_label, arg_label)
                if arg.get("description"):
                    builder.add_edge_by_labels(arg_label, f"desc::{arg['description']}")

    return OntologyGraph(nodes=builder.nodes, edges=builder.edges)


__all__ = [
    "Edge",
    "OntologyGraph",
    "load_schema_file",
    "normalize_label",
    "schema_dict_to_graph",
]
