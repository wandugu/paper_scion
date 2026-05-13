"""Reusable schema loading and graph-conversion utilities."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set

from .logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


def normalize_label(label: str | None) -> str:
    if label is None:
        return ""
    return str(label).strip().lower()


def _first_text(item: Dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = item.get(key)
        text = str(value or "").strip()
        if text:
            return text
    return ""


def _dedupe_dicts_by_key(items: Sequence[Dict[str, Any]], key: str) -> List[Dict[str, Any]]:
    seen: Set[str] = set()
    deduped: List[Dict[str, Any]] = []
    for item in items:
        value = str(item.get(key) or "").strip()
        normalized = normalize_label(value)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(item)
    return deduped


def _argument_from_role(role: str, description: str = "", required: bool = False) -> Dict[str, Any] | None:
    role = str(role or "").strip()
    if not role:
        return None
    return {"role": role, "description": str(description or "").strip(), "required": bool(required)}


def _argument_from_item(item: Any) -> Dict[str, Any] | None:
    if isinstance(item, str):
        return _argument_from_role(item)
    if not isinstance(item, dict):
        return None
    role = _first_text(item, ["role", "arg_role", "argument_role", "role_type", "name"])
    return _argument_from_role(
        role,
        description=str(item.get("description") or "").strip(),
        required=bool(item.get("required", False)),
    )


def _event_arguments(item: Dict[str, Any]) -> List[Dict[str, Any]]:
    arguments: List[Dict[str, Any]] = []

    raw_arguments = item.get("arguments") or item.get("args") or []
    if isinstance(raw_arguments, list):
        for arg in raw_arguments:
            payload = _argument_from_item(arg)
            if payload:
                arguments.append(payload)

    raw_roles = item.get("roles", [])
    if isinstance(raw_roles, list):
        for role in raw_roles:
            payload = _argument_from_item(role)
            if payload:
                arguments.append(payload)
    elif raw_roles:
        payload = _argument_from_role(str(raw_roles))
        if payload:
            arguments.append(payload)

    direct_role = _first_text(item, ["role", "arg_role", "argument_role", "role_type"])
    payload = _argument_from_role(direct_role)
    if payload:
        arguments.append(payload)

    return _dedupe_dicts_by_key(arguments, "role")


def _trigger_words(item: Dict[str, Any]) -> List[str]:
    raw_triggers = item.get("trigger_words") or item.get("triggers") or []
    if isinstance(raw_triggers, str):
        raw_triggers = [raw_triggers]
    if not isinstance(raw_triggers, list):
        return []
    seen: Set[str] = set()
    triggers: List[str] = []
    for word in raw_triggers:
        text = str(word or "").strip()
        normalized = normalize_label(text)
        if text and normalized not in seen:
            seen.add(normalized)
            triggers.append(text)
    return triggers


def _merge_event(target: Dict[str, Dict[str, Any]], event: Dict[str, Any]) -> None:
    event_type = str(event.get("event_type") or "").strip()
    if not event_type:
        return
    if event_type not in target:
        target[event_type] = {
            "event_type": event_type,
            "description": str(event.get("description") or "").strip(),
            "trigger_words": [],
            "arguments": [],
        }
    current = target[event_type]
    if not current.get("description") and event.get("description"):
        current["description"] = str(event.get("description") or "").strip()

    current["trigger_words"] = _merge_strings(current.get("trigger_words", []), event.get("trigger_words", []))
    current["arguments"] = _dedupe_dicts_by_key(
        list(current.get("arguments", [])) + list(event.get("arguments", [])),
        "role",
    )


def _merge_strings(primary: Sequence[str], secondary: Sequence[str]) -> List[str]:
    seen: Set[str] = set()
    merged: List[str] = []
    for value in list(primary) + list(secondary):
        text = str(value or "").strip()
        normalized = normalize_label(text)
        if text and normalized not in seen:
            seen.add(normalized)
            merged.append(text)
    return merged


def _relationship_from_item(item: Dict[str, Any]) -> Dict[str, str] | None:
    if str(item.get("edge_kind") or "").strip().lower() == "ee":
        return None
    head = _first_text(item, ["head_entity", "head_type", "head", "source_entity", "src"])
    tail = _first_text(item, ["tail_entity", "tail_type", "tail", "target_entity", "tgt"])
    rel_type = _first_text(item, ["rel_type", "relation", "relationship", "predicate", "type"])
    if not (head and tail and rel_type):
        return None
    return {
        "head_entity": head,
        "tail_entity": tail,
        "rel_type": rel_type,
        "description": str(item.get("description") or "").strip(),
    }


def _event_from_item(item: Dict[str, Any]) -> Dict[str, Any] | None:
    edge_kind = str(item.get("edge_kind") or "").strip().lower()
    if edge_kind and edge_kind != "ee" and "event_type" not in item:
        return None
    event_type = _first_text(item, ["event_type", "event", "type"])
    if not event_type:
        return None
    return {
        "event_type": event_type,
        "description": str(item.get("description") or "").strip(),
        "trigger_words": _trigger_words(item),
        "arguments": _event_arguments(item),
    }


def _schema_from_sequence(items: Sequence[Any]) -> Dict[str, Any]:
    entities: Set[str] = set()
    relationships: List[Dict[str, str]] = []
    events_by_type: Dict[str, Dict[str, Any]] = {}

    for idx, item in enumerate(items):
        if isinstance(item, str):
            label = item.strip()
            if label:
                entities.add(label)
            continue
        if not isinstance(item, dict):
            LOGGER.debug("Skip unsupported schema item: index=%s type=%s", idx, type(item).__name__)
            continue

        relationship = _relationship_from_item(item)
        if relationship:
            entities.update([relationship["head_entity"], relationship["tail_entity"]])
            relationships.append(relationship)
            continue

        event = _event_from_item(item)
        if event:
            _merge_event(events_by_type, event)
            continue

        label = _first_text(item, ["entity", "label", "name"])
        if label:
            entities.add(label)
            continue

        LOGGER.debug("Unrecognized schema item: index=%s keys=%s", idx, sorted(item.keys()))

    schema: Dict[str, Any] = {
        "entities": sorted(entities),
        "relationships": relationships,
    }
    if events_by_type:
        schema["events"] = list(events_by_type.values())
    LOGGER.debug(
        "Loaded sequence schema: entities=%s relationships=%s events=%s",
        len(schema.get("entities", [])),
        len(schema.get("relationships", [])),
        len(schema.get("events", [])),
    )
    return schema


def load_schema_file(path: str | Path) -> Dict[str, Any]:
    schema_path = Path(path)
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    LOGGER.debug("Loading schema file: %s", schema_path)
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        LOGGER.debug("Schema file is a JSON object: keys=%s", sorted(data.keys()))
        return data
    if isinstance(data, list):
        LOGGER.debug("Schema file is a JSON array: len=%s", len(data))
        return _schema_from_sequence(data)
    raise ValueError("Schema file must be a JSON object or JSON array.")


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
        key = normalized or str(label or "").strip().lower() or f"node-{self._counter}"
        if key in self._label_to_id:
            return self._label_to_id[key]
        node_id = f"n{self._counter:05d}"
        self._counter += 1
        self._label_to_id[key] = node_id
        self.nodes[node_id] = normalized or str(label or "").strip() or key
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
            entity_name = _first_text(item, ["entity", "label", "name"])
            if entity_name:
                description = str(item.get("description") or "").strip()
                label = f"{entity_name}: {description}" if description else entity_name
            else:
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
        relationship = _relationship_from_item(item)
        if relationship:
            normalized.append(relationship)
    return normalized


def _normalize_events(items: Sequence[Any] | None) -> List[Dict[str, Any]]:
    events_by_type: Dict[str, Dict[str, Any]] = {}
    for item in items or []:
        if not isinstance(item, dict):
            continue
        event = _event_from_item(item)
        if event:
            _merge_event(events_by_type, event)
    return list(events_by_type.values())


def _events_from_schema_dict(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    raw_events: List[Any] = []
    if isinstance(schema.get("events"), list):
        raw_events.extend(schema.get("events") or [])
    if isinstance(schema.get("edges"), list):
        raw_events.extend(schema.get("edges") or [])

    event_type_roles = schema.get("event_type_roles") or schema.get("event_type_role_map")
    if isinstance(event_type_roles, dict):
        for event_type, roles in event_type_roles.items():
            raw_events.append({"event_type": event_type, "roles": roles})

    event_types = schema.get("event_types")
    if isinstance(event_types, list):
        global_roles = schema.get("roles", [])
        for event_type in event_types:
            raw_events.append({"event_type": event_type, "roles": global_roles})

    return _normalize_events(raw_events)


def schema_dict_to_graph(schema: Dict[str, Any]) -> OntologyGraph:
    builder = _SchemaGraphBuilder()

    entities = _normalize_entities(schema.get("entities"))
    if entities:
        section_label = "section::entities"
        builder.add_edge_by_labels(builder.root_label, section_label)
        for label in entities:
            builder.add_edge_by_labels(section_label, label)

    raw_relationships: List[Any] = []
    if isinstance(schema.get("relationships"), list):
        raw_relationships.extend(schema.get("relationships") or [])
    if isinstance(schema.get("edges"), list):
        raw_relationships.extend(schema.get("edges") or [])
    relationships = _normalize_relationships(raw_relationships)
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

    events = _events_from_schema_dict(schema)
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
