"""Candidate-space utilities for SCION-style schema induction.

The functions in this module are intentionally lightweight and dependency-free.
They provide a native candidate package, evidence pointers, deterministic
fallback schemas, and contract validation for the LLM schema-engineer path.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Sequence, Tuple


STOPWORDS_EN = {
    "about",
    "after",
    "again",
    "against",
    "also",
    "among",
    "because",
    "before",
    "between",
    "could",
    "during",
    "first",
    "from",
    "have",
    "into",
    "more",
    "only",
    "other",
    "over",
    "said",
    "same",
    "than",
    "that",
    "their",
    "there",
    "these",
    "this",
    "those",
    "through",
    "under",
    "were",
    "when",
    "where",
    "which",
    "while",
    "with",
    "would",
}


COMMON_ROLES_EN = ["agent", "participant", "place", "time", "target", "source", "destination"]
COMMON_ROLES_ZH = ["发起方", "参与方", "地点", "时间", "目标", "来源", "受影响方"]


def normalize_candidate_label(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = text.replace("_", " ").replace("-", " ").replace("/", " ")
    text = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", " ", text)
    return " ".join(text.split())


def _hint_label_and_description(item: Any) -> Tuple[str, str]:
    if isinstance(item, str):
        return item.strip(), ""
    if isinstance(item, dict):
        for key, value in item.items():
            return str(key).strip(), str(value or "").strip()
    return "", ""


def _label_tokens(label: str) -> set[str]:
    return set(normalize_candidate_label(label).split())


def _labels_match(a: str, b: str) -> bool:
    na = normalize_candidate_label(a)
    nb = normalize_candidate_label(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    ta = set(na.split())
    tb = set(nb.split())
    if not ta or not tb:
        return False
    overlap = len(ta & tb) / max(len(ta), len(tb))
    return overlap >= 0.75


def _snippet(text: str, label: str, max_chars: int = 180) -> str:
    cleaned = " ".join(str(text or "").split())
    if not cleaned:
        return ""
    norm_text = cleaned.lower()
    norm_label = str(label or "").lower().strip()
    pos = norm_text.find(norm_label) if norm_label else -1
    if pos < 0:
        return cleaned[:max_chars]
    start = max(0, pos - max_chars // 3)
    end = min(len(cleaned), pos + len(label) + max_chars // 2)
    return cleaned[start:end]


def _evidence_for_label(chunks: Sequence[str], label: str, max_evidence: int) -> List[Dict[str, Any]]:
    evidence: List[Dict[str, Any]] = []
    if not label:
        return evidence
    norm_label = normalize_candidate_label(label)
    label_tokens = set(norm_label.split())
    for idx, chunk in enumerate(chunks):
        norm_chunk = normalize_candidate_label(chunk)
        if norm_label and norm_label in norm_chunk:
            evidence.append(
                {
                    "doc_id": f"chunk-{idx:03d}",
                    "chunk_index": idx,
                    "match": label,
                    "snippet": _snippet(chunk, label),
                }
            )
        elif label_tokens and len(label_tokens & set(norm_chunk.split())) >= min(2, len(label_tokens)):
            evidence.append(
                {
                    "doc_id": f"chunk-{idx:03d}",
                    "chunk_index": idx,
                    "match": label,
                    "snippet": _snippet(chunk, label),
                }
            )
        if len(evidence) >= max_evidence:
            break
    return evidence


def _english_entity_terms(text: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for match in re.finditer(r"\b[A-Z][a-zA-Z0-9]+(?:\s+[A-Z][a-zA-Z0-9]+){0,3}\b", text):
        value = match.group(0).strip()
        if value.lower() not in STOPWORDS_EN and len(value) > 2:
            counter[value] += 1
    for token in re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{4,}\b", text):
        low = token.lower()
        if low not in STOPWORDS_EN:
            counter[low] += 1
    return counter


def _zh_entity_terms(text: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    for match in re.finditer(r"[\u4e00-\u9fff]{2,8}", text):
        value = match.group(0).strip()
        if value:
            counter[value] += 1
    return counter


def _relation_terms(text: str, language_code: str, mode: str) -> Counter[str]:
    counter: Counter[str] = Counter()
    if language_code == "zh":
        verbs = re.findall(r"[\u4e00-\u9fff]{1,6}(?:于|为|到|向|与|对|被|由|在|成|化|发|行|用|属|含)", text)
        for value in verbs:
            if len(value) >= 2:
                counter[value] += 1
        return counter

    for token in re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}(?:ed|ing|es|s)?\b", text):
        low = token.lower()
        if low not in STOPWORDS_EN and len(low) >= 4:
            counter[low] += 1
    if mode == "full":
        words = [w.lower() for w in re.findall(r"\b[a-zA-Z][a-zA-Z0-9]{2,}\b", text)]
        for left, mid, right in zip(words, words[1:], words[2:]):
            if mid in {"of", "for", "in", "to", "with", "from"} and left not in STOPWORDS_EN and right not in STOPWORDS_EN:
                counter[f"{left} {mid} {right}"] += 1
    return counter


def _event_terms(text: str, language_code: str, mode: str) -> Counter[str]:
    counter = _relation_terms(text, language_code, mode)
    if language_code != "zh":
        for match in re.finditer(r"\b(?:attack|meeting|transfer|movement|conflict|agreement|event|incident)\b", text, re.I):
            counter[match.group(0).lower()] += 2
    return counter


def _top_items(counter: Counter[str], limit: int) -> List[str]:
    return [label for label, _ in counter.most_common(limit) if normalize_candidate_label(label)]


def _cluster_labels(labels: Iterable[str]) -> Dict[str, str]:
    buckets: Dict[str, List[str]] = defaultdict(list)
    for label in labels:
        norm = normalize_candidate_label(label)
        tokens = norm.split()
        key = " ".join(tokens[:2]) if len(tokens) >= 2 else norm
        if key:
            buckets[key].append(label)
    cluster_ids: Dict[str, str] = {}
    for idx, key in enumerate(sorted(buckets), start=1):
        cluster_id = f"c{idx:04d}"
        for label in buckets[key]:
            cluster_ids[label] = cluster_id
    return cluster_ids


def _candidate_id(prefix: str, index: int) -> str:
    return f"{prefix}_{index:04d}"


def build_candidate_package(
    chunks: Sequence[str],
    entity_hints: Sequence[Any] | None = None,
    relationship_hints: Sequence[Dict[str, Any]] | None = None,
    event_type_hints: Sequence[Any] | None = None,
    argument_role_hints: Sequence[Any] | None = None,
    mode: str = "lite",
    language_code: str = "en",
    max_text_candidates: int = 40,
    max_evidence: int = 3,
) -> Dict[str, Any]:
    """Build a candidate package from train text plus configured seed hints."""

    normalized_mode = "full" if str(mode).lower() == "full" else "lite"
    text = "\n\n".join(chunk for chunk in chunks if str(chunk).strip())
    text_candidate_limit = max_text_candidates * (2 if normalized_mode == "full" else 1)

    entity_rows: List[Dict[str, Any]] = []
    seen_entities: set[str] = set()
    for item in entity_hints or []:
        label, description = _hint_label_and_description(item)
        norm = normalize_candidate_label(label)
        if not norm or norm in seen_entities:
            continue
        seen_entities.add(norm)
        entity_rows.append(
            {
                "label": label,
                "description": description,
                "source": "config_hint",
                "evidence": _evidence_for_label(chunks, label, max_evidence),
            }
        )

    mined_entities = _english_entity_terms(text) if language_code != "zh" else _zh_entity_terms(text)
    for label in _top_items(mined_entities, text_candidate_limit):
        norm = normalize_candidate_label(label)
        if not norm or norm in seen_entities:
            continue
        seen_entities.add(norm)
        entity_rows.append(
            {
                "label": label,
                "description": "",
                "source": "text_mined",
                "support": int(mined_entities[label]),
                "evidence": _evidence_for_label(chunks, label, max_evidence),
            }
        )

    relation_rows: List[Dict[str, Any]] = []
    seen_relations: set[Tuple[str, str, str]] = set()
    for item in relationship_hints or []:
        head = str(item.get("head_entity") or item.get("head") or "Entity").strip() or "Entity"
        tail = str(item.get("tail_entity") or item.get("tail") or "Entity").strip() or "Entity"
        rel_type = str(item.get("rel_type") or item.get("relationship") or item.get("type") or "").strip()
        if not rel_type:
            continue
        key = (normalize_candidate_label(head), normalize_candidate_label(rel_type), normalize_candidate_label(tail))
        if key in seen_relations:
            continue
        seen_relations.add(key)
        relation_rows.append(
            {
                "head_entity": head,
                "rel_type": rel_type,
                "tail_entity": tail,
                "description": str(item.get("description") or "").strip(),
                "source": "config_hint",
                "evidence": _evidence_for_label(chunks, rel_type, max_evidence),
            }
        )

    mined_relations = _relation_terms(text, language_code, normalized_mode)
    default_head = entity_rows[0]["label"] if entity_rows else "Entity"
    default_tail = entity_rows[1]["label"] if len(entity_rows) > 1 else "Entity"
    for rel_type in _top_items(mined_relations, text_candidate_limit):
        key = (normalize_candidate_label(default_head), normalize_candidate_label(rel_type), normalize_candidate_label(default_tail))
        if key in seen_relations:
            continue
        seen_relations.add(key)
        relation_rows.append(
            {
                "head_entity": default_head,
                "rel_type": rel_type,
                "tail_entity": default_tail,
                "description": "",
                "source": "text_mined",
                "support": int(mined_relations[rel_type]),
                "evidence": _evidence_for_label(chunks, rel_type, max_evidence),
            }
        )

    event_rows: List[Dict[str, Any]] = []
    seen_events: set[str] = set()
    for item in event_type_hints or []:
        label, description = _hint_label_and_description(item)
        norm = normalize_candidate_label(label)
        if not norm or norm in seen_events:
            continue
        seen_events.add(norm)
        event_rows.append(
            {
                "event_type": label,
                "description": description,
                "source": "config_hint",
                "trigger_words": [],
                "arguments": [],
                "evidence": _evidence_for_label(chunks, label, max_evidence),
            }
        )

    mined_events = _event_terms(text, language_code, normalized_mode)
    for label in _top_items(mined_events, max(10, max_text_candidates // 2)):
        norm = normalize_candidate_label(label)
        if not norm or norm in seen_events:
            continue
        seen_events.add(norm)
        event_rows.append(
            {
                "event_type": label,
                "description": "",
                "source": "text_mined",
                "support": int(mined_events[label]),
                "trigger_words": [label],
                "arguments": [],
                "evidence": _evidence_for_label(chunks, label, max_evidence),
            }
        )

    role_rows: List[Dict[str, Any]] = []
    seen_roles: set[str] = set()
    common_roles = COMMON_ROLES_ZH if language_code == "zh" else COMMON_ROLES_EN
    for item in list(argument_role_hints or []) + common_roles:
        label, description = _hint_label_and_description(item)
        norm = normalize_candidate_label(label)
        if not norm or norm in seen_roles:
            continue
        seen_roles.add(norm)
        role_rows.append(
            {
                "role": label,
                "description": description,
                "source": "config_hint" if description else "default_role",
                "evidence": _evidence_for_label(chunks, label, max_evidence),
            }
        )

    if role_rows:
        for event in event_rows:
            event["arguments"] = [
                {"role": role["role"], "description": role.get("description", ""), "required": False}
                for role in role_rows[: min(3, len(role_rows))]
            ]

    if normalized_mode == "full":
        cluster_ids = _cluster_labels(
            [row["label"] for row in entity_rows]
            + [row["rel_type"] for row in relation_rows]
            + [row["event_type"] for row in event_rows]
            + [row["role"] for row in role_rows]
        )
    else:
        cluster_ids = {}

    for idx, row in enumerate(entity_rows, start=1):
        row["id"] = _candidate_id("ent", idx)
        if row["label"] in cluster_ids:
            row["cluster_id"] = cluster_ids[row["label"]]
    for idx, row in enumerate(relation_rows, start=1):
        row["id"] = _candidate_id("rel", idx)
        if row["rel_type"] in cluster_ids:
            row["cluster_id"] = cluster_ids[row["rel_type"]]
    for idx, row in enumerate(event_rows, start=1):
        row["id"] = _candidate_id("evt", idx)
        if row["event_type"] in cluster_ids:
            row["cluster_id"] = cluster_ids[row["event_type"]]
    for idx, row in enumerate(role_rows, start=1):
        row["id"] = _candidate_id("role", idx)
        if row["role"] in cluster_ids:
            row["cluster_id"] = cluster_ids[row["role"]]

    return {
        "schema": "scion_candidate_package_v1",
        "mode": normalized_mode,
        "source": "train_text",
        "entities": entity_rows,
        "relationships": relation_rows,
        "events": event_rows,
        "roles": role_rows,
        "diagnostics": {
            "chunk_count": len(chunks),
            "entity_count": len(entity_rows),
            "relationship_count": len(relation_rows),
            "event_count": len(event_rows),
            "role_count": len(role_rows),
            "clustered": normalized_mode == "full",
        },
    }


def candidate_package_to_prompt(package: Dict[str, Any], max_chars: int = 6000) -> str:
    rows: List[str] = [
        "You must select, rename conservatively, merge, or filter only from this candidate package.",
        "Every output item must be linked to at least one candidate label or evidence pointer.",
        "Candidate package summary:",
    ]
    for section, label_key in [
        ("entities", "label"),
        ("relationships", "rel_type"),
        ("events", "event_type"),
        ("roles", "role"),
    ]:
        rows.append(f"[{section}]")
        for item in package.get(section, [])[:40]:
            if section == "relationships":
                value = f"{item.get('head_entity')} --{item.get('rel_type')}--> {item.get('tail_entity')}"
            else:
                value = str(item.get(label_key) or "")
            evidence = item.get("evidence") or []
            evidence_id = evidence[0].get("doc_id") if evidence and isinstance(evidence[0], dict) else item.get("source", "")
            rows.append(f"- {item.get('id')}: {value} (source={item.get('source')}; evidence={evidence_id})")
    text = "\n".join(rows)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...[candidate package truncated]"


def _entity_candidate_labels(package: Dict[str, Any]) -> List[str]:
    return [str(item.get("label") or "") for item in package.get("entities", []) if item.get("label")]


def _relation_candidate_rows(package: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [item for item in package.get("relationships", []) if isinstance(item, dict)]


def _event_candidate_rows(package: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [item for item in package.get("events", []) if isinstance(item, dict)]


def _role_candidate_labels(package: Dict[str, Any]) -> List[str]:
    roles = [str(item.get("role") or "") for item in package.get("roles", []) if item.get("role")]
    for event in package.get("events", []):
        for arg in event.get("arguments", []) or []:
            role = str(arg.get("role") or "")
            if role:
                roles.append(role)
    return roles


def _matches_any(label: str, candidates: Sequence[str]) -> bool:
    return any(_labels_match(label, candidate) for candidate in candidates)


def constrain_ontology_to_candidates(
    entities: Sequence[Any],
    relationships: Sequence[Dict[str, Any]],
    package: Dict[str, Any] | None,
) -> Tuple[List[Any], List[Dict[str, Any]], Dict[str, Any]]:
    if not package:
        return list(entities), list(relationships), {"enabled": False}

    candidate_entities = _entity_candidate_labels(package)
    retained_entities: List[Any] = []
    removed_entities: List[str] = []
    for item in entities:
        label, description = _hint_label_and_description(item)
        if _matches_any(label, candidate_entities):
            retained_entities.append({label: description} if description else label)
        else:
            removed_entities.append(label)

    relation_rows = _relation_candidate_rows(package)
    relation_labels = [str(item.get("rel_type") or "") for item in relation_rows]
    retained_relationships: List[Dict[str, Any]] = []
    removed_relationships: List[str] = []
    for rel in relationships:
        head = str(rel.get("head_entity") or "")
        rel_type = str(rel.get("rel_type") or "")
        tail = str(rel.get("tail_entity") or "")
        exact = any(
            _labels_match(head, str(row.get("head_entity") or ""))
            and _labels_match(rel_type, str(row.get("rel_type") or ""))
            and _labels_match(tail, str(row.get("tail_entity") or ""))
            for row in relation_rows
        )
        label_linked = _matches_any(rel_type, relation_labels)
        endpoint_linked = (
            _matches_any(head, candidate_entities)
            and _matches_any(tail, candidate_entities)
        )
        if exact or (label_linked and endpoint_linked) or (label_linked and not candidate_entities):
            retained_relationships.append(dict(rel))
        else:
            removed_relationships.append(f"{head}|{rel_type}|{tail}")

    return (
        retained_entities,
        retained_relationships,
        {
            "enabled": True,
            "removed_entities": removed_entities,
            "removed_relationships": removed_relationships,
            "retained_entities": len(retained_entities),
            "retained_relationships": len(retained_relationships),
        },
    )


def constrain_events_to_candidates(
    events: Sequence[Dict[str, Any]],
    package: Dict[str, Any] | None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if not package:
        return list(events), {"enabled": False}

    event_rows = _event_candidate_rows(package)
    event_labels = [str(item.get("event_type") or "") for item in event_rows]
    role_labels = _role_candidate_labels(package)
    retained_events: List[Dict[str, Any]] = []
    removed_events: List[str] = []
    removed_roles: List[str] = []

    for event in events:
        event_type = str(event.get("event_type") or "")
        if not _matches_any(event_type, event_labels):
            removed_events.append(event_type)
            continue
        retained_args = []
        for arg in event.get("arguments", []) or []:
            role = str(arg.get("role") or "")
            if _matches_any(role, role_labels):
                retained_args.append(dict(arg))
            else:
                removed_roles.append(f"{event_type}|{role}")
        payload = dict(event)
        payload["arguments"] = retained_args
        retained_events.append(payload)

    return (
        retained_events,
        {
            "enabled": True,
            "removed_events": removed_events,
            "removed_roles": removed_roles,
            "retained_events": len(retained_events),
        },
    )


def candidate_package_to_schema(package: Dict[str, Any], max_entities: int = 16, max_relationships: int = 24, max_events: int = 12) -> Dict[str, Any]:
    entities = []
    for item in package.get("entities", [])[:max_entities]:
        label = str(item.get("label") or "").strip()
        description = str(item.get("description") or "").strip()
        if label:
            entities.append({label: description} if description else label)

    relationships = []
    for item in package.get("relationships", [])[:max_relationships]:
        rel_type = str(item.get("rel_type") or "").strip()
        if not rel_type:
            continue
        relationships.append(
            {
                "head_entity": str(item.get("head_entity") or "Entity"),
                "tail_entity": str(item.get("tail_entity") or "Entity"),
                "rel_type": rel_type,
                "description": str(item.get("description") or ""),
            }
        )

    events = []
    for item in package.get("events", [])[:max_events]:
        event_type = str(item.get("event_type") or "").strip()
        if not event_type:
            continue
        events.append(
            {
                "event_type": event_type,
                "description": str(item.get("description") or ""),
                "trigger_words": [str(x) for x in item.get("trigger_words", []) if str(x).strip()],
                "arguments": [
                    {
                        "role": str(arg.get("role") or ""),
                        "description": str(arg.get("description") or ""),
                        "required": bool(arg.get("required", False)),
                    }
                    for arg in item.get("arguments", []) or []
                    if str(arg.get("role") or "").strip()
                ],
            }
        )

    payload: Dict[str, Any] = {"entities": entities, "relationships": relationships}
    if events:
        payload["events"] = events
    return payload

