"""本体比较与评测工具。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

try:  # optional heavy deps
    import numpy as np
except Exception:  # pragma: no cover - optional dependency guard
    np = None  # type: ignore[assignment]

try:  # optional heavy deps
    from scipy.optimize import linear_sum_assignment
except Exception:  # pragma: no cover
    linear_sum_assignment = None  # type: ignore[assignment]

try:  # optional heavy deps
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover
    SentenceTransformer = None  # type: ignore[assignment]

_MODEL_CACHE: Dict[str, Any] = {}


@dataclass(frozen=True)
class Edge:
    src: str
    tgt: str


@dataclass
class OntologyGraph:
    nodes: Dict[str, str]
    edges: Set[Edge]


def normalize_label(label: str | None) -> str:
    if label is None:
        return ""
    return str(label).strip().lower()


def load_schema_file(path: str | Path) -> Dict[str, Any]:
    schema_path = Path(path)
    if not schema_path.exists():
        raise FileNotFoundError(f"未找到本体文件: {schema_path}")
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("本体文件必须是 JSON 对象。")
    return data


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
        description = str(item.get("description", "")).strip()
        normalized.append(
            {
                "head_entity": head,
                "tail_entity": tail,
                "rel_type": rel_type,
                "description": description,
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


def _ensure_numpy():  # type: ignore[return-value]
    if np is None:
        raise ImportError("运行本体评测需要 numpy，请先安装 numpy")
    return np


def _ensure_linear_sum_assignment():  # type: ignore[return-value]
    if linear_sum_assignment is None:
        raise ImportError("运行本体评测需要 scipy，请先安装 scipy")
    return linear_sum_assignment


def _load_sentence_model(model_name: str):  # type: ignore[return-value]
    if SentenceTransformer is None:
        raise ImportError("运行本体评测需要 sentence-transformers，请先安装对应依赖")
    if model_name not in _MODEL_CACHE:
        _MODEL_CACHE[model_name] = SentenceTransformer(model_name)
    return _MODEL_CACHE[model_name]


def build_embeddings(onto: OntologyGraph, model: Any) -> Dict[str, "np.ndarray"]:
    np_mod = _ensure_numpy()
    ids = list(onto.nodes.keys())
    if not ids:
        return {}
    texts = [onto.nodes[node_id] for node_id in ids]
    vectors = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True, show_progress_bar=False)
    return {node_id: vectors[idx] for idx, node_id in enumerate(ids)}


def cos_sim(x: "np.ndarray", y: "np.ndarray") -> float:
    np_mod = _ensure_numpy()
    return float(np_mod.dot(x, y))


def literal_f1(gold: OntologyGraph, pred: OntologyGraph) -> Tuple[float, float, float]:
    gold_edges = {(gold.nodes[e.src], gold.nodes[e.tgt]) for e in gold.edges}
    pred_edges = {(pred.nodes[e.src], pred.nodes[e.tgt]) for e in pred.edges}
    tp = len(gold_edges & pred_edges)
    fp = len(pred_edges - gold_edges)
    fn = len(gold_edges - pred_edges)
    prec = tp / (tp + fp + 1e-9)
    rec = tp / (tp + fn + 1e-9)
    f1 = 2 * prec * rec / (prec + rec + 1e-9)
    return prec, rec, f1


def _best_similarity_scores(
    pred_vecs: Dict[str, "np.ndarray"], gold_vecs: Dict[str, "np.ndarray"]
) -> Dict[str, float]:
    np_mod = _ensure_numpy()
    if not gold_vecs:
        return {pid: 0.0 for pid in pred_vecs}
    gold_matrix = np_mod.stack(list(gold_vecs.values()), axis=0)
    scores: Dict[str, float] = {}
    for node_id, vec in pred_vecs.items():
        sims = gold_matrix @ vec
        scores[node_id] = float(np_mod.max(sims))
    return scores


def fuzzy_f1_edges(
    gold: OntologyGraph,
    pred: OntologyGraph,
    gold_vecs: Dict[str, "np.ndarray"],
    pred_vecs: Dict[str, "np.ndarray"],
    threshold: float = 0.45,
) -> Tuple[float, float, float]:
    if not pred.edges or not gold.edges:
        return 0.0, 0.0, 0.0
    best_scores = _best_similarity_scores(pred_vecs, gold_vecs)
    tp = 0
    for edge in pred.edges:
        s1 = best_scores.get(edge.src, 0.0)
        s2 = best_scores.get(edge.tgt, 0.0)
        if min(s1, s2) >= threshold:
            tp += 1
    prec = tp / (len(pred.edges) + 1e-9)
    rec = tp / (len(gold.edges) + 1e-9)
    f1 = 2 * prec * rec / (prec + rec + 1e-9)
    return prec, rec, f1


def edge_similarity(
    e_p: Edge,
    e_g: Edge,
    pred_vecs: Dict[str, "np.ndarray"],
    gold_vecs: Dict[str, "np.ndarray"],
) -> float:
    if e_p.src not in pred_vecs or e_p.tgt not in pred_vecs:
        return 0.0
    if e_g.src not in gold_vecs or e_g.tgt not in gold_vecs:
        return 0.0
    up = pred_vecs[e_p.src]
    vp = pred_vecs[e_p.tgt]
    ug = gold_vecs[e_g.src]
    vg = gold_vecs[e_g.tgt]
    s1 = min(cos_sim(up, ug), cos_sim(vp, vg))
    s2 = min(cos_sim(up, vg), cos_sim(vp, ug))
    return max(s1, s2)


def continuous_f1_edges(
    gold: OntologyGraph,
    pred: OntologyGraph,
    gold_vecs: Dict[str, "np.ndarray"],
    pred_vecs: Dict[str, "np.ndarray"],
) -> Tuple[float, float, float]:
    np_mod = _ensure_numpy()
    lsa = _ensure_linear_sum_assignment()
    pred_edges = list(pred.edges)
    gold_edges = list(gold.edges)
    if not pred_edges or not gold_edges:
        return 0.0, 0.0, 0.0
    n_p, n_g = len(pred_edges), len(gold_edges)
    sim_matrix = np_mod.zeros((n_p, n_g), dtype=np_mod.float32)
    for i, e_p in enumerate(pred_edges):
        for j, e_g in enumerate(gold_edges):
            sim_matrix[i, j] = edge_similarity(e_p, e_g, pred_vecs, gold_vecs)
    cost = -sim_matrix
    row_ind, col_ind = lsa(cost)
    matched = np_mod.maximum(sim_matrix[row_ind, col_ind], 0.0)
    soft_tp = float(matched.sum())
    prec = soft_tp / (n_p + 1e-9)
    rec = soft_tp / (n_g + 1e-9)
    f1 = 2 * prec * rec / (prec + rec + 1e-9)
    return prec, rec, f1


def graph_smooth(
    onto: OntologyGraph,
    base_vecs: Dict[str, "np.ndarray"],
    K: int = 2,
    alpha: float = 0.5,
) -> Dict[str, "np.ndarray"]:
    np_mod = _ensure_numpy()
    if not base_vecs:
        return {}
    if K <= 0:
        return {nid: vec.copy() for nid, vec in base_vecs.items()}
    adj: Dict[str, List[str]] = {nid: [] for nid in onto.nodes}
    for edge in onto.edges:
        adj[edge.src].append(edge.tgt)
        adj[edge.tgt].append(edge.src)
    fallback_vec = next(iter(base_vecs.values()))
    h: Dict[str, "np.ndarray"] = {nid: base_vecs.get(nid, fallback_vec).copy() for nid in onto.nodes}
    for _ in range(K):
        new_h: Dict[str, "np.ndarray"] = {}
        for node_id, vec in h.items():
            neighs = adj.get(node_id, [])
            if not neighs:
                new_h[node_id] = vec
                continue
            neigh_vecs = np_mod.stack([h[n] for n in neighs], axis=0)
            mean_vec = neigh_vecs.mean(axis=0)
            updated = alpha * vec + (1.0 - alpha) * mean_vec
            norm = np_mod.linalg.norm(updated) + 1e-9
            new_h[node_id] = updated / norm
        h = new_h
    return h


def graph_f1_nodes(
    gold: OntologyGraph,
    pred: OntologyGraph,
    gold_vecs: Dict[str, "np.ndarray"],
    pred_vecs: Dict[str, "np.ndarray"],
) -> Tuple[float, float, float]:
    np_mod = _ensure_numpy()
    lsa = _ensure_linear_sum_assignment()
    gold_ids = list(gold_vecs.keys())
    pred_ids = list(pred_vecs.keys())
    if not gold_ids or not pred_ids:
        return 0.0, 0.0, 0.0
    gold_matrix = np_mod.stack([gold_vecs[nid] for nid in gold_ids], axis=0)
    pred_matrix = np_mod.stack([pred_vecs[nid] for nid in pred_ids], axis=0)
    sim_matrix = pred_matrix @ gold_matrix.T
    cost = -sim_matrix
    row_ind, col_ind = lsa(cost)
    matched = np_mod.maximum(sim_matrix[row_ind, col_ind], 0.0)
    soft_tp = float(matched.sum())
    prec = soft_tp / (len(pred_ids) + 1e-9)
    rec = soft_tp / (len(gold_ids) + 1e-9)
    f1 = 2 * prec * rec / (prec + rec + 1e-9)
    return prec, rec, f1


def compute_ontology_metrics(
    gold_graph: OntologyGraph,
    pred_graph: OntologyGraph,
    emb_model: str = "BAAI/bge-large-zh-v1.5",
    threshold: float = 0.45,
    graph_smoothing_rounds: int = 2,
    graph_smoothing_alpha: float = 0.5,
) -> Dict[str, Dict[str, float]]:
    model = _load_sentence_model(emb_model)
    gold_base_vecs = build_embeddings(gold_graph, model)
    pred_base_vecs = build_embeddings(pred_graph, model)

    literal_p, literal_r, literal_f = literal_f1(gold_graph, pred_graph)
    fuzzy_p, fuzzy_r, fuzzy_f = fuzzy_f1_edges(gold_graph, pred_graph, gold_base_vecs, pred_base_vecs, threshold)
    cont_p, cont_r, cont_f = continuous_f1_edges(gold_graph, pred_graph, gold_base_vecs, pred_base_vecs)

    gold_graph_vecs = graph_smooth(gold_graph, gold_base_vecs, K=graph_smoothing_rounds, alpha=graph_smoothing_alpha)
    pred_graph_vecs = graph_smooth(pred_graph, pred_base_vecs, K=graph_smoothing_rounds, alpha=graph_smoothing_alpha)
    graph_p, graph_r, graph_f = graph_f1_nodes(gold_graph, pred_graph, gold_graph_vecs, pred_graph_vecs)

    return {
        "literal": {"precision": literal_p, "recall": literal_r, "f1": literal_f},
        "fuzzy": {"precision": fuzzy_p, "recall": fuzzy_r, "f1": fuzzy_f, "threshold": threshold},
        "continuous": {"precision": cont_p, "recall": cont_r, "f1": cont_f},
        "graph": {"precision": graph_p, "recall": graph_r, "f1": graph_f},
    }


__all__ = [
    "Edge",
    "OntologyGraph",
    "build_embeddings",
    "compute_ontology_metrics",
    "continuous_f1_edges",
    "cos_sim",
    "fuzzy_f1_edges",
    "graph_f1_nodes",
    "graph_smooth",
    "literal_f1",
    "load_schema_file",
    "normalize_label",
    "schema_dict_to_graph",
]
