"""命令行工具：对比预测与金标准本体，输出多种评测指标。

参数全部来自 ``config/config.yaml``，无需再传入命令行参数。
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, Set, Tuple

from utils.common import load_yaml_config, resolve_project_path, save_json
from utils.dataset_paths import resolve_dataset_paths
from utils.logger import get_ot_logger
from utils.ontology_graph import Edge, OntologyGraph, load_schema_file, schema_dict_to_graph

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

try:  # optional heavy deps
    import torch
except Exception:  # pragma: no cover - optional dependency guard
    torch = None  # type: ignore[assignment]


CONFIG = load_yaml_config()
LOGGER = get_ot_logger()
_MODEL_CACHE: Dict[Tuple[str, str], Any] = {}


# 禁止联网加载 Hugging Face 资源，强制使用本地缓存
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")


SUPPORTED_LANG_CODES = {"zh", "en"}


def _language_code() -> str:
    lang_cfg = CONFIG.get("language")
    if isinstance(lang_cfg, dict):
        raw_code = lang_cfg.get("code")
    else:
        raw_code = lang_cfg
    code = str(raw_code or "zh").lower()
    return code if code in SUPPORTED_LANG_CODES else "zh"


LANGUAGE_CODE = _language_code()
LANGUAGE_SUFFIX = f"_{LANGUAGE_CODE}"


def _apply_language_suffix(path: Path) -> Path:
    suffix = LANGUAGE_SUFFIX
    ext = path.suffix
    target_suffix = f"{suffix}{ext}" if ext else suffix
    if path.name.endswith(target_suffix):
        return path
    if ext:
        return path.with_name(f"{path.stem}{suffix}{ext}")
    return path.with_name(f"{path.name}{suffix}")


def _normalize_dataset_name(dataset_name: str) -> str:
    cleaned = dataset_name.strip()
    normalized = re.sub(r"[^\w.-]+", "_", cleaned)
    return normalized or "dataset"


def _schema_filename(output_cfg: Dict[str, Any], dataset_name: str) -> str:
    if dataset_name:
        normalized = _normalize_dataset_name(dataset_name)
        return f"ontology_schema_{normalized}{LANGUAGE_SUFFIX}.json"
    schema_name = output_cfg.get("schema_filename", "ontology_schema.json")
    return _apply_language_suffix(Path(schema_name)).name


def evaluation_config() -> Dict:
    cfg = CONFIG.get("evaluation")
    return cfg if isinstance(cfg, dict) else {}


def _selected_dataset_name() -> str:
    cfg = evaluation_config()
    dataset = cfg.get("dataset_name") or cfg.get("dataset")
    if dataset:
        return str(dataset).strip()
    input_cfg = CONFIG.get("input") or {}
    dataset = input_cfg.get("dataset_name")
    return str(dataset).strip() if dataset else ""


def _resolve_pred_schema_path() -> Path:
    eval_cfg = evaluation_config()
    raw_pred = eval_cfg.get("pred_schema_path")
    if raw_pred:
        return resolve_project_path(raw_pred)

    output_cfg = CONFIG.get("output", {})
    base_dir = resolve_project_path(output_cfg.get("dir", "output"))
    dataset_name = _selected_dataset_name()
    schema_name = _schema_filename(output_cfg, dataset_name)
    return base_dir / schema_name


def _eval_device(eval_cfg: Dict) -> str:
    raw_device = eval_cfg.get("device")
    if isinstance(raw_device, str) and raw_device.strip():
        return raw_device.strip()
    return "cuda:1"


def _ensure_numpy():  # type: ignore[return-value]
    if np is None:
        raise ImportError("运行本体评测需要 numpy，请先安装 numpy")
    return np


def _ensure_linear_sum_assignment():  # type: ignore[return-value]
    if linear_sum_assignment is None:
        raise ImportError("运行本体评测需要 scipy，请先安装 scipy")
    return linear_sum_assignment


def _auto_select_device() -> str:
    """自动选空闲显存最多的 CUDA 设备，失败则回退到 CPU。"""

    if torch is None or not torch.cuda.is_available():
        return "cpu"

    try:
        device_count = torch.cuda.device_count()
    except Exception:  # pragma: no cover - defensive
        return "cpu"

    best_device = "cpu"
    best_free_mem = -1

    for idx in range(device_count):
        try:
            free_mem, _ = torch.cuda.mem_get_info(idx)
        except Exception:  # pragma: no cover - mem query may fail
            continue
        if free_mem > best_free_mem:
            best_free_mem = free_mem
            best_device = f"cuda:{idx}"

    return best_device if best_free_mem >= 0 else "cpu"


def _select_device(requested: str | None) -> str:
    """解析并验证 device 字符串，支持 auto / cuda / cpu。"""

    if torch is None:
        return "cpu"

    if requested:
        normalized = requested.strip().lower()
        if normalized == "auto":
            selected = _auto_select_device()
            LOGGER.info("自动选择评估设备: %s", selected)
            return selected
        if normalized == "cpu":
            return "cpu"
        if normalized.startswith("cuda"):
            if torch.cuda.is_available():
                try:
                    device_idx = int(normalized.split(":", 1)[1]) if ":" in normalized else 0
                    if 0 <= device_idx < torch.cuda.device_count():
                        return f"cuda:{device_idx}"
                    LOGGER.warning(
                        "请求的 CUDA 设备 %s 超出范围，当前共 %d 张卡，回退到 auto。",
                        normalized,
                        torch.cuda.device_count(),
                    )
                    return _auto_select_device()
                except Exception:  # pragma: no cover - 防御
                    LOGGER.warning("CUDA 设备解析失败 (%s)，回退到 auto。", normalized)
                    return _auto_select_device()
            LOGGER.warning("CUDA 不可用，回退到 CPU。")
            return "cpu"

    return _auto_select_device()


def _load_sentence_model(model_name: str, device: str | None = None):  # type: ignore[return-value]
    if SentenceTransformer is None:
        raise ImportError("运行本体评测需要 sentence-transformers，请先安装对应依赖")

    resolved_device = _select_device(device)
    model_path = _resolve_local_model(model_name)
    cache_key = (str(model_path), resolved_device)
    if cache_key not in _MODEL_CACHE:
        LOGGER.info("加载向量模型 %s 到设备 %s (仅使用本地文件)", model_path, resolved_device)
        _MODEL_CACHE[cache_key] = SentenceTransformer(str(model_path), device=resolved_device)
    return _MODEL_CACHE[cache_key]


def _resolve_golden_schema_path(dataset_name: str) -> Path:
    eval_cfg = evaluation_config()
    raw_gold = eval_cfg.get("golden_schema_path")
    if raw_gold:
        return resolve_project_path(raw_gold)
    if not dataset_name:
        raise ValueError("未配置 dataset_name，无法推断金标准本体路径。")
    schema_path, _ = resolve_dataset_paths(CONFIG, dataset_name)
    return schema_path


def evaluation_output_path(base_dir: Path) -> Path:
    cfg = evaluation_config()
    raw_path = cfg.get("output_json")
    if isinstance(raw_path, str) and raw_path.strip():
        return resolve_project_path(raw_path)
    filename = f"ontology_eval_metrics{LANGUAGE_SUFFIX}.json"
    return base_dir / filename


def _coerce_float(value, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _coerce_int(value, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _resolve_local_model(model_name: str) -> Path:
    """确保使用本地向量模型，缺失时直接报错避免联网。"""

    candidate = resolve_project_path(model_name)
    if candidate.exists():
        return candidate

    fallback = Path(model_name)
    if fallback.exists():
        return fallback

    raise FileNotFoundError(
        f"未找到本地向量模型: {model_name}，请将模型放在本地后再运行（例如 models/bge-m3）。"
    )


def _embedding_model_path(eval_cfg: Dict) -> Path:
    raw_model = eval_cfg.get("emb_model") or "models/bge-m3"
    model_path = _resolve_local_model(str(raw_model))
    LOGGER.info("将使用本地向量模型: %s", model_path)
    return model_path


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


def literal_f1(gold: OntologyGraph, pred: OntologyGraph):
    gold_edges = {(gold.nodes[e.src], gold.nodes[e.tgt]) for e in gold.edges}
    pred_edges = {(pred.nodes[e.src], pred.nodes[e.tgt]) for e in pred.edges}
    tp = len(gold_edges & pred_edges)
    fp = len(pred_edges - gold_edges)
    fn = len(gold_edges - pred_edges)
    prec = tp / (tp + fp + 1e-9)
    rec = tp / (tp + fn + 1e-9)
    f1 = 2 * prec * rec / (prec + rec + 1e-9)
    return prec, rec, f1


def _best_similarity_scores(pred_vecs: Dict[str, "np.ndarray"], gold_vecs: Dict[str, "np.ndarray"]):
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
):
    """计算基于节点相似度的模糊匹配 F1。

    之前的实现按预测边逐条累计命中，可能出现命中次数大于金标准边数量，
    导致 Recall/F1 > 1。这里改为双向一一匹配，命中数最多为 min(len(gold), len(pred))。
    """

    if not pred.edges or not gold.edges:
        return 0.0, 0.0, 0.0

    matched_pred_edges: Set[int] = set()
    tp = 0
    for g_edge in gold.edges:
        for idx, p_edge in enumerate(pred.edges):
            if idx in matched_pred_edges:
                continue
            sim = edge_similarity(p_edge, g_edge, pred_vecs, gold_vecs)
            if sim >= threshold:
                matched_pred_edges.add(idx)
                tp += 1
                break

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
):
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
):
    np_mod = _ensure_numpy()
    if not base_vecs:
        return {}
    if K <= 0:
        return {nid: vec.copy() for nid, vec in base_vecs.items()}
    adj: Dict[str, list[str]] = {nid: [] for nid in onto.nodes}
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
):
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
    device: str | None = None,
) -> Dict[str, Dict[str, float]]:
    model = _load_sentence_model(emb_model, device=device)
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


def main() -> None:
    eval_cfg = evaluation_config()
    dataset_name = _selected_dataset_name()
    LOGGER.info("开始本体评估，语言=%s，数据集=%s", LANGUAGE_CODE, dataset_name or "未指定")
    gold_schema_path = _resolve_golden_schema_path(dataset_name)
    pred_schema_path = _resolve_pred_schema_path()

    LOGGER.info("加载金标准本体文件: %s", gold_schema_path)
    gold_schema = load_schema_file(gold_schema_path)
    LOGGER.info(
        "金标准本体加载完成，实体=%d，关系=%d",
        len(gold_schema.get("entities", [])),
        len(gold_schema.get("relationships", [])),
    )

    LOGGER.info("加载预测本体文件: %s", pred_schema_path)
    pred_schema = load_schema_file(pred_schema_path)
    LOGGER.info(
        "预测本体加载完成，实体=%d，关系=%d",
        len(pred_schema.get("entities", [])),
        len(pred_schema.get("relationships", [])),
    )

    gold_graph = schema_dict_to_graph(gold_schema)
    pred_graph = schema_dict_to_graph(pred_schema)

    emb_model_path = _embedding_model_path(eval_cfg)
    device = _eval_device(eval_cfg)
    threshold = _coerce_float(eval_cfg.get("threshold"), 0.45)
    smoothing_rounds = _coerce_int(eval_cfg.get("graph_smoothing_rounds"), 2)
    smoothing_alpha = _coerce_float(eval_cfg.get("graph_smoothing_alpha"), 0.5)

    LOGGER.info(
        "开始计算本体评估指标 | 向量模型=%s | 设备=%s | 阈值=%.2f | 平滑轮数=%d | 平滑因子=%.2f",
        emb_model_path,
        device,
        threshold,
        smoothing_rounds,
        smoothing_alpha,
    )

    metrics = compute_ontology_metrics(
        gold_graph=gold_graph,
        pred_graph=pred_graph,
        emb_model=str(emb_model_path),
        threshold=threshold,
        graph_smoothing_rounds=smoothing_rounds,
        graph_smoothing_alpha=smoothing_alpha,
        device=device,
    )

    for name, result in metrics.items():
        LOGGER.info(
            "[%s] Precision=%.4f Recall=%.4f F1=%.4f",
            name,
            result["precision"],
            result["recall"],
            result["f1"],
        )

    output_dir = resolve_project_path(CONFIG.get("output", {}).get("dir", "output"))
    output_path = evaluation_output_path(output_dir)
    save_json(output_path, metrics)
    LOGGER.info("评测指标已写入: %s", output_path)


if __name__ == "__main__":
    main()
