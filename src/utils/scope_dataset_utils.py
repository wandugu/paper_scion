"""SCOPE 数据集构建/统计公用工具。"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

from .common import save_json
from .dataset_paths import resolve_dataset_paths
from .logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)

PLACEHOLDER_ENTITY_TYPES = {"entity", "na", "n/a", ""}

TQDM_SETTINGS: Dict[str, Any] = {
    "enabled": True,
    "mininterval": 0.1,
    "leave": False,
}


@dataclass
class DatasetEntry:
    name: str
    task: str
    language: str
    fmt: str
    schema_output_path: Path
    samples_output_path: Path
    data_files: List[str]
    schema_paths: List[str]


@dataclass
class ScopeDoc:
    doc_id: str
    text: str
    language: str
    source_dataset: str
    category: Optional[str]
    global_split: str
    relations: List[Dict[str, Any]]
    events: List[Dict[str, Any]]

    def to_json(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "text": self.text,
            "language": self.language,
            "source_dataset": self.source_dataset,
            "category": self.category,
            "global_split": self.global_split,
            "relations": self.relations,
            "events": self.events,
        }


def apply_tqdm_settings(cfg: Dict[str, Any]) -> None:
    settings = cfg.get("tqdm") or {}
    TQDM_SETTINGS.update(
        {
            "enabled": bool(settings.get("enabled", TQDM_SETTINGS["enabled"])),
            "mininterval": float(settings.get("mininterval", TQDM_SETTINGS["mininterval"])),
            "leave": bool(settings.get("leave", TQDM_SETTINGS["leave"])),
        }
    )


def wrap_tqdm(iterable: Iterable[Any], desc: str, total: int | None = None) -> Iterable[Any]:
    if not TQDM_SETTINGS.get("enabled", True):
        return iterable
    from tqdm import tqdm

    return tqdm(
        iterable,
        desc=desc,
        total=total,
        mininterval=TQDM_SETTINGS.get("mininterval", 0.1),
        leave=TQDM_SETTINGS.get("leave", False),
    )


def safe_json_load(path: Path) -> Any:
    LOGGER.debug("读取 JSON: %s", path)
    content = path.read_text(encoding="utf-8")
    if content.lstrip().startswith("version https://git-lfs.github.com/spec/v1"):
        LOGGER.warning("检测到 Git LFS 指针文件，跳过解析: %s", path)
        return {}
    return json.loads(content)


def text_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def hash_to_int(text: str) -> int:
    return int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16)


def split_by_hash(key: str, ratios: Sequence[float], seed: int) -> str:
    total = sum(ratios)
    if total <= 0:
        return "train"
    norm = [r / total for r in ratios]
    digest = hashlib.md5(f"{seed}:{key}".encode("utf-8")).hexdigest()
    value = int(digest, 16) / 2**128
    if value < norm[0]:
        return "train"
    if value < norm[0] + norm[1]:
        return "dev"
    return "test"


def flatten_text_tokens(text: str) -> int:
    return len(text.strip().split())


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fp:
        for record in records:
            fp.write(json.dumps(record, ensure_ascii=False) + "\n")


def read_registry_from_config(config: Dict[str, Any]) -> List[DatasetEntry]:
    conv_cfg = config.get("dataset_conversion") or {}
    entries: List[DatasetEntry] = []
    for group_key in ("re", "ee"):
        group_cfg = conv_cfg.get(group_key) or {}
        for ds_cfg in group_cfg.get("dataset_configs", []) or []:
            if ds_cfg.get("enabled") is False:
                continue
            name = str(ds_cfg.get("name") or "").strip()
            if not name:
                continue
            task = str(ds_cfg.get("task") or group_key).lower()
            language = str(ds_cfg.get("language") or "zh").lower()
            fmt = str(ds_cfg.get("format") or "").lower()
            schema_path, samples_path = resolve_dataset_paths(config, name)
            data_files = [str(p) for p in ds_cfg.get("data_files", [])]
            schema_paths = []
            if ds_cfg.get("schema_path"):
                schema_paths.append(str(ds_cfg["schema_path"]))
            schema_paths.extend([str(p) for p in ds_cfg.get("schema_paths", [])])
            entries.append(
                DatasetEntry(
                    name=name,
                    task=task,
                    language=language,
                    fmt=fmt,
                    schema_output_path=schema_path,
                    samples_output_path=samples_path,
                    data_files=data_files,
                    schema_paths=schema_paths,
                )
            )
    LOGGER.debug("从配置加载数据集条目数量: %s", len(entries))
    return entries


def normalize_entity_type(name: str | None) -> str:
    value = str(name or "").strip()
    if value.lower() in PLACEHOLDER_ENTITY_TYPES or not value:
        return "Entity"
    return value


def _merge_relations(existing: Dict[Tuple[str, str, str, str, str], Dict[str, Any]], relation: Dict[str, Any]) -> None:
    key = (
        relation["head"]["text"],
        relation["head"]["type"],
        relation["predicate"],
        relation["tail"]["text"],
        relation["tail"]["type"],
    )
    existing[key] = relation


def _merge_events(existing: Dict[Tuple[str, str, Tuple[Tuple[str, str], ...]], Dict[str, Any]], event: Dict[str, Any]) -> None:
    args = tuple(sorted((arg["role"], arg["text"]) for arg in event.get("arguments", [])))
    key = (event.get("event_type", ""), event.get("trigger", {}).get("text", ""), args)
    existing[key] = event


def parse_re_samples(
    payload: Any,
    dataset_name: str,
    language: str,
    dedup_by_text: bool,
    cross_dataset_dedup: bool,
) -> Tuple[List[ScopeDoc], int, bool]:
    doc_map: Dict[str, Dict[str, Any]] = {}
    sample_count = 0
    typed_flag = True

    if not isinstance(payload, list):
        LOGGER.warning("RE 样本格式异常，跳过: %s", dataset_name)
        return [], 0, False

    for group in payload:
        if not isinstance(group, dict):
            continue
        group_head_type = group.get("head_entity_type")
        group_tail_type = group.get("tail_type") or group.get("tail_entity_type")
        for sample in group.get("samples", []) or []:
            if not isinstance(sample, dict):
                continue
            sample_count += 1
            text = str(sample.get("text") or sample.get("input") or "").strip()
            if not text:
                continue
            head_type = normalize_entity_type(sample.get("head_entity_type") or group_head_type)
            tail_type = normalize_entity_type(sample.get("tail_entity_type") or group_tail_type)
            if head_type == "Entity" or tail_type == "Entity":
                typed_flag = False
            doc_key_hash = text_hash(text)
            if cross_dataset_dedup:
                doc_key = doc_key_hash
            elif dedup_by_text:
                doc_key = f"{dataset_name}::{language}::{doc_key_hash}"
            else:
                doc_key = f"{dataset_name}::{language}::{sample.get('id', doc_key_hash)}"
            doc_info = doc_map.setdefault(
                doc_key,
                {
                    "doc_id": f"{dataset_name}__{doc_key_hash}",
                    "text": text,
                    "language": language,
                    "source_dataset": dataset_name,
                    "categories": set(),
                    "relations": {},
                    "events": {},
                },
            )
            category = sample.get("category")
            if category:
                doc_info["categories"].add(str(category))
            relation = {
                "head": {"text": str(sample.get("head_entity") or ""), "type": head_type},
                "predicate": str(sample.get("relation") or sample.get("rel_type") or ""),
                "tail": {"text": str(sample.get("tail_entity") or ""), "type": tail_type},
            }
            _merge_relations(doc_info["relations"], relation)

    docs: List[ScopeDoc] = []
    for info in doc_map.values():
        categories = sorted(info["categories"])
        category = categories[0] if categories else None
        if len(categories) > 1:
            LOGGER.debug("RE 文档多分类，取首个: %s -> %s", info["doc_id"], categories)
        docs.append(
            ScopeDoc(
                doc_id=info["doc_id"],
                text=info["text"],
                language=info["language"],
                source_dataset=info["source_dataset"],
                category=category,
                global_split="",
                relations=list(info["relations"].values()),
                events=[],
            )
        )
    return docs, sample_count, typed_flag


def parse_ee_samples(
    payload: Any,
    dataset_name: str,
    language: str,
    dedup_by_text: bool,
    cross_dataset_dedup: bool,
) -> Tuple[List[ScopeDoc], int]:
    doc_map: Dict[str, Dict[str, Any]] = {}
    sample_count = 0

    if not isinstance(payload, list):
        LOGGER.warning("EE 样本格式异常，跳过: %s", dataset_name)
        return [], 0

    for group in payload:
        if not isinstance(group, dict):
            continue
        group_event_type = group.get("event_type")
        for sample in group.get("samples", []) or []:
            if not isinstance(sample, dict):
                continue
            sample_count += 1
            text = str(sample.get("text") or sample.get("input") or "").strip()
            if not text:
                continue
            doc_key_hash = text_hash(text)
            if cross_dataset_dedup:
                doc_key = doc_key_hash
            elif dedup_by_text:
                doc_key = f"{dataset_name}::{language}::{doc_key_hash}"
            else:
                doc_key = f"{dataset_name}::{language}::{sample.get('id', doc_key_hash)}"
            doc_info = doc_map.setdefault(
                doc_key,
                {
                    "doc_id": f"{dataset_name}__{doc_key_hash}",
                    "text": text,
                    "language": language,
                    "source_dataset": dataset_name,
                    "categories": set(),
                    "relations": {},
                    "events": {},
                },
            )
            event_type = str(sample.get("event_type") or group_event_type or "")
            trigger_text = str(sample.get("event_trigger") or sample.get("trigger") or "")
            arguments = []
            for arg in sample.get("arguments", []) or []:
                if not isinstance(arg, dict):
                    continue
                arguments.append(
                    {
                        "role": str(arg.get("role") or ""),
                        "text": str(arg.get("argument") or arg.get("text") or ""),
                    }
                )
            event = {
                "event_type": event_type,
                "trigger": {"text": trigger_text, "pos": sample.get("trigger_pos")},
                "arguments": arguments,
            }
            _merge_events(doc_info["events"], event)

    docs: List[ScopeDoc] = []
    for info in doc_map.values():
        categories = sorted(info["categories"])
        category = categories[0] if categories else None
        docs.append(
            ScopeDoc(
                doc_id=info["doc_id"],
                text=info["text"],
                language=info["language"],
                source_dataset=info["source_dataset"],
                category=category,
                global_split="",
                relations=[],
                events=list(info["events"].values()),
            )
        )
    return docs, sample_count


def extract_ee_schema_edges(schema_payload: Dict[str, Any]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str]]]:
    event_types: Set[str] = set()
    roles: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()

    if isinstance(schema_payload.get("events"), list):
        for item in schema_payload.get("events", []):
            if not isinstance(item, dict):
                continue
            event_type = str(item.get("event_type") or "")
            if event_type:
                event_types.add(event_type)
            for role in item.get("roles", []) or []:
                role_name = str(role)
                if role_name:
                    roles.add(role_name)
                if event_type and role_name:
                    edges.add((event_type, role_name))

    mapping = schema_payload.get("event_type_roles") or schema_payload.get("event_type_role_map")
    if isinstance(mapping, dict):
        for event_type, role_list in mapping.items():
            event_type = str(event_type)
            event_types.add(event_type)
            for role in role_list or []:
                role_name = str(role)
                if role_name:
                    roles.add(role_name)
                if event_type and role_name:
                    edges.add((event_type, role_name))

    for event_type in schema_payload.get("event_types", []) or []:
        event_types.add(str(event_type))
    for role in schema_payload.get("roles", []) or []:
        roles.add(str(role))

    if isinstance(schema_payload.get("edges"), list):
        for item in schema_payload.get("edges", []):
            if not isinstance(item, dict):
                continue
            event_type = str(item.get("event_type") or item.get("head") or "")
            role = str(item.get("role") or item.get("tail") or "")
            if event_type:
                event_types.add(event_type)
            if role:
                roles.add(role)
            if event_type and role:
                edges.add((event_type, role))

    return event_types, roles, edges


def infer_ee_schema_from_samples(docs: Sequence[ScopeDoc]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str]]]:
    event_types: Set[str] = set()
    roles: Set[str] = set()
    edges: Set[Tuple[str, str]] = set()
    for doc in docs:
        for event in doc.events:
            event_type = str(event.get("event_type") or "")
            if event_type:
                event_types.add(event_type)
            for arg in event.get("arguments", []) or []:
                role = str(arg.get("role") or "")
                if role:
                    roles.add(role)
                if event_type and role:
                    edges.add((event_type, role))
    return event_types, roles, edges


def extract_re_schema_edges(schema_payload: Dict[str, Any]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str, str]]]:
    rel_types: Set[str] = set()
    entity_types: Set[str] = set()
    edges: Set[Tuple[str, str, str]] = set()
    for item in schema_payload.get("relationships", []) or []:
        if not isinstance(item, dict):
            continue
        head = normalize_entity_type(item.get("head_entity"))
        tail = normalize_entity_type(item.get("tail_entity"))
        rel = str(item.get("rel_type") or "")
        if rel:
            rel_types.add(rel)
        entity_types.update([head, tail])
        if rel:
            edges.add((head, rel, tail))
    for ent in schema_payload.get("entities", []) or []:
        ent_name = normalize_entity_type(ent)
        if ent_name:
            entity_types.add(ent_name)
    return rel_types, entity_types, edges


def schema_edges_from_docs(docs: Sequence[ScopeDoc]) -> Tuple[Set[str], Set[str], Set[Tuple[str, str, str]]]:
    rel_types: Set[str] = set()
    entity_types: Set[str] = set()
    edges: Set[Tuple[str, str, str]] = set()
    for doc in docs:
        for rel in doc.relations:
            rel_type = str(rel.get("predicate") or "")
            head_type = normalize_entity_type(rel.get("head", {}).get("type"))
            tail_type = normalize_entity_type(rel.get("tail", {}).get("type"))
            if rel_type:
                rel_types.add(rel_type)
            entity_types.update([head_type, tail_type])
            if rel_type:
                edges.add((head_type, rel_type, tail_type))
    return rel_types, entity_types, edges


def schema_explosion_guard(
    entry: DatasetEntry,
    rel_edges: Set[Tuple[str, str, str]],
    docs: Sequence[ScopeDoc],
    threshold: int,
) -> Tuple[Set[Tuple[str, str, str]], bool]:
    if len(rel_edges) <= threshold:
        return rel_edges, False
    if entry.schema_paths:
        return rel_edges, False
    LOGGER.warning("触发 schema explosion guard: %s edges=%s", entry.name, len(rel_edges))
    rel_types = {rel.get("predicate") for doc in docs for rel in doc.relations if rel.get("predicate")}
    downgraded = {("Entity", rel_type, "Entity") for rel_type in rel_types}
    return downgraded, True


def build_schema_payload(
    re_edges: Set[Tuple[str, str, str]],
    ee_edges: Set[Tuple[str, str]],
) -> List[Dict[str, Any]]:
    payload: List[Dict[str, Any]] = []
    for head, rel, tail in sorted(re_edges):
        payload.append(
            {
                "edge_kind": "re",
                "head_entity": head,
                "rel_type": rel,
                "tail_entity": tail,
            }
        )
    for event_type, role in sorted(ee_edges):
        payload.append(
            {
                "edge_kind": "ee",
                "event_type": event_type,
                "role": role,
            }
        )
    return payload


def doc_edge_keys(doc: ScopeDoc) -> Set[Tuple[str, ...]]:
    edges: Set[Tuple[str, ...]] = set()
    for rel in doc.relations:
        edges.add(
            (
                "re",
                normalize_entity_type(rel.get("head", {}).get("type")),
                str(rel.get("predicate") or ""),
                normalize_entity_type(rel.get("tail", {}).get("type")),
            )
        )
    for event in doc.events:
        event_type = str(event.get("event_type") or "")
        for arg in event.get("arguments", []) or []:
            role = str(arg.get("role") or "")
            edges.add(("ee", event_type, role))
    return edges


def schema_key_from_edge(edge: Dict[str, Any]) -> Tuple[str, ...]:
    if edge.get("edge_kind") == "ee":
        return ("ee", str(edge.get("event_type") or ""), str(edge.get("role") or ""))
    return (
        "re",
        normalize_entity_type(edge.get("head_entity")),
        str(edge.get("rel_type") or ""),
        normalize_entity_type(edge.get("tail_entity")),
    )


def write_csv(path: Path, header: Sequence[str], rows: Sequence[Sequence[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(header)
        writer.writerows(rows)


def percentile(values: Sequence[float], p: float) -> float:
    if not values:
        return 0.0
    if p <= 0:
        return float(min(values))
    if p >= 1:
        return float(max(values))
    values_sorted = sorted(values)
    idx = int((p * len(values_sorted) + (1 - p))) - 1
    idx = max(0, min(idx, len(values_sorted) - 1))
    return float(values_sorted[idx])


def save_registry_docs(path: Path, docs: Sequence[ScopeDoc]) -> None:
    payload = {
        doc.doc_id: {
            "source_dataset": doc.source_dataset,
            "language": doc.language,
            "global_split": doc.global_split,
        }
        for doc in docs
    }
    save_json(path, payload)


__all__ = [
    "DatasetEntry",
    "ScopeDoc",
    "apply_tqdm_settings",
    "wrap_tqdm",
    "safe_json_load",
    "text_hash",
    "hash_to_int",
    "split_by_hash",
    "flatten_text_tokens",
    "write_jsonl",
    "read_registry_from_config",
    "normalize_entity_type",
    "parse_re_samples",
    "parse_ee_samples",
    "extract_ee_schema_edges",
    "infer_ee_schema_from_samples",
    "extract_re_schema_edges",
    "schema_edges_from_docs",
    "schema_explosion_guard",
    "build_schema_payload",
    "doc_edge_keys",
    "schema_key_from_edge",
    "write_csv",
    "percentile",
    "save_registry_docs",
]
