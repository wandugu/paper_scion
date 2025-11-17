"""Graph Maker 演示脚本
=========================

此脚本展示如何使用 ``knowledge-graph-maker`` 包从任意文本生成知识图谱，并把
结果保存到 ``output/`` 目录下的多种文件格式中。所有运行配置均集中在
``config/config.yaml`` 中，可直接根据自身场景进行修改。

运行前准备
----------
1. 安装依赖：``pip install knowledge-graph-maker``（仓库自带 ``poetry`` 环境亦可）。
2. 配置 LLM 服务：
   - DeepSeek: 设置 ``DEEPSEEK_API_KEY`` 环境变量（示例脚本默认使用
     ``provider='deepseek'``，API Key 也可通过 ``config/config.yaml`` 中的
     ``llm.default_api_key`` 字段临时填写）。
   - OpenAI: 设置 ``OPENAI_API_KEY`` 环境变量。
   - Groq: 设置 ``GROQ_API_KEY`` 环境变量（脚本已提供占位符，只有当你选择
     ``provider='groq'`` 时才会真正使用）。
3. 如需自动写入 Neo4j，请确保本地或远端 Neo4j 实例已启动，且账号、密码、URI
   与 ``config/config.yaml`` 的 ``neo4j`` 配置保持一致。

执行：``python src/demo.py`` 或 ``python -m src.demo``
"""



from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
LOG_DIR = PROJECT_ROOT / "logs"
BACKGROUND_SNIPPET_MAX_CHARS = 4000


def resolve_project_path(path_str: str | Path) -> Path:
    """将相对路径解析为相对于项目根目录的绝对路径。"""

    path = Path(path_str).expanduser()
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def load_config(path: Path = CONFIG_PATH) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"未找到配置文件: {path}")
    with path.open("r", encoding="utf-8") as fp:
        data = yaml.safe_load(fp) or {}
    if not isinstance(data, dict):
        raise ValueError("配置文件格式必须为字典")
    return data


def setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("graph_maker")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_DIR / "ot.log", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


CONFIG: Dict = load_config()
LOGGER = setup_logger()

# ---------------------------------------------------
# 0) 记录当前进程的代理环境变量，稍后再恢复
# ---------------------------------------------------
_PROXY_ENV_VARS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
)
_SAVED_PROXIES: Dict[str, str | None] = {k: os.environ.get(k) for k in _PROXY_ENV_VARS}

# 临时把代理从环境里移除，避免 Groq + httpx 在 import 阶段读到 socks5h 就炸
for k in _PROXY_ENV_VARS:
    os.environ.pop(k, None)

# ---------------------------------------------------
# 1) 给 Groq 一个占位 API Key，避免它在 import 阶段因为缺 key 报错
# ---------------------------------------------------
if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = "placeholder-key"

# 这里 import 时会顺带实例化 GroqClient，但不会真正发网络请求
from knowledge_graph_maker.graph_maker import GraphMaker
from knowledge_graph_maker.neo4j_graph_model import Neo4jGraphModel
from knowledge_graph_maker.types import Document, Edge, LLMClient, Node, Ontology

# ---------------------------------------------------
# 2) import 完之后，把代理环境变量恢复回来，给 DeepSeek 用
# ---------------------------------------------------
for k, v in _SAVED_PROXIES.items():
    if v is not None:
        os.environ[k] = v



import requests  # 放在文件头部 import 区域也可以

class DeepSeekClient(LLMClient):
    """DeepSeek LLM Client：直接调用 DeepSeek /chat/completions API，可显式设置代理。"""

    _model: str
    _temperature: float
    _top_p: float
    _max_tokens: int

    def __init__(
        self,
        model: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
        api_key: str,
        proxy: str | None = None,
    ):
        if not api_key or api_key == "123":
            raise EnvironmentError(
                "请设置有效的 DeepSeek API Key（DEEPSEEK_API_KEY 或 config/config.yaml 中的 llm.default_api_key)"
            )

        self._model = model
        self._temperature = float(temperature)
        self._top_p = float(top_p)
        self._max_tokens = int(max_tokens)
        self._api_key = api_key

        # 自己管理一个 Session，显式挂代理
        self._session = requests.Session()
        if proxy:
            # 这里 proxy 可以是 http://... 或 socks5h://...
            self._session.proxies.update(
                {
                    "http": proxy,
                    "https": proxy,
                }
            )

        # DeepSeek 官方推荐 base_url = https://api.deepseek.com
        self._base_url = "https://api.deepseek.com"

    def generate(self, user_message: str, system_message: str) -> str:
        """按照 knowledge_graph_maker 的预期返回一个纯文本字符串。"""
        url = f"{self._base_url}/chat/completions"
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            "temperature": self._temperature,
            "top_p": self._top_p,
            "max_tokens": self._max_tokens,
            "stream": False,
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        resp = self._session.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # DeepSeek 兼容 OpenAI ChatCompletion 格式
        return data["choices"][0]["message"]["content"]


# NOTE: 只有在真正需要各自的 LLM 客户端时才做延迟导入，避免因为未设置相关环境
# 变量而在脚本启动阶段失败。


@dataclass
class OutputPaths:
    base_dir: Path
    schema: Path
    nodes: Path
    edges: Path
    neo4j_nodes_csv: Path
    neo4j_edges_csv: Path


# ----------------------------------------------------------------------------
# 工具函数
# ----------------------------------------------------------------------------


def ensure_output_paths() -> OutputPaths:
    base_dir = resolve_project_path(CONFIG["output"]["dir"])
    base_dir.mkdir(parents=True, exist_ok=True)
    return OutputPaths(
        base_dir=base_dir,
        schema=base_dir / CONFIG["output"]["schema_filename"],
        nodes=base_dir / CONFIG["output"]["nodes_filename"],
        edges=base_dir / CONFIG["output"]["edges_filename"],
        neo4j_nodes_csv=base_dir / CONFIG["output"]["neo4j_nodes_csv"],
        neo4j_edges_csv=base_dir / CONFIG["output"]["neo4j_edges_csv"],
    )


def load_text_chunks() -> Sequence[str]:
    cfg = CONFIG["input"]
    if cfg["type"] == "sample":
        from lotr_wikipedia_summary import lord_of_the_rings_wikipedia_summary

        return [chunk.strip() for chunk in lord_of_the_rings_wikipedia_summary if chunk.strip()]
    if cfg["type"] == "text":
        return chunk_text(cfg["text"], cfg["chunk_size"])
    if cfg["type"] == "file":
        text_path = resolve_project_path(cfg["file_path"])
        if not text_path.exists():
            raise FileNotFoundError(f"未找到输入文件: {text_path}")
        return chunk_text(text_path.read_text(encoding="utf-8"), cfg["chunk_size"])
    raise ValueError("input.type 仅支持 'sample'、'text' 或 'file'")


def chunk_text(text: str, chunk_size: int) -> List[str]:
    text = text.strip()
    if not text:
        return []
    words = text.split()
    chunks: List[str] = []
    current: List[str] = []
    length = 0
    for word in words:
        current.append(word)
        length += len(word) + 1
        if length >= chunk_size:
            chunks.append(" ".join(current))
            current = []
            length = 0
    if current:
        chunks.append(" ".join(current))
    return chunks


def build_background_excerpt(chunks: Sequence[str], limit: int = BACKGROUND_SNIPPET_MAX_CHARS) -> str:
    """将所有文本块拼成给 LLM 使用的背景摘要，并裁剪长度。"""

    combined = "\n\n".join(chunk.strip() for chunk in chunks if chunk.strip()).strip()
    if not combined:
        return ""
    if len(combined) <= limit:
        return combined
    return combined[:limit]


def build_documents(chunks: Sequence[str]) -> List[Document]:
    metadata_base = {
        "source": CONFIG["input"]["source_label"],
        "total_chunks": len(chunks),
    }
    documents: List[Document] = []
    for idx, chunk in enumerate(chunks):
        documents.append(
            Document(
                text=chunk,
                metadata={**metadata_base, "chunk_index": idx, "chunk_id": f"chunk-{idx:03d}"},
            )
        )
    return documents


def load_existing_ontology_schema() -> Tuple[Dict[str, Any] | None, Path | None]:
    """尝试加载已有本体定义，返回 (payload, path)。"""

    cfg = CONFIG.get("input", {})
    raw_path = cfg.get("existing_ontology_path")
    if not raw_path:
        return None, None
    path = resolve_project_path(raw_path)
    if not path.exists():
        LOGGER.info("配置了 existing_ontology_path，但文件不存在: %s", path)
        return None, path
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("读取输入本体失败 (%s): %s", path, exc)
        return None, path
    if not isinstance(data, dict):
        LOGGER.warning("输入本体文件内容必须是 JSON 对象: %s", path)
        return None, path
    LOGGER.info("检测到已有本体文件: %s", path)
    return data, path


def _format_label_hints() -> str:
    hints: List[str] = []
    for item in CONFIG["ontology"]["labels"]:
        if isinstance(item, str):
            hints.append(f"- {item}")
        elif isinstance(item, dict):
            for key, value in item.items():
                hints.append(f"- {key}: {value}")
    return "\n".join(hints)


def _format_relationship_hints() -> str:
    return "\n".join(f"- {relation}" for relation in CONFIG["ontology"]["relationships"])


def _event_cfg() -> Dict[str, Any]:
    return CONFIG.get("event_extraction") or {}


def _format_event_type_hints() -> str:
    cfg = _event_cfg()
    hints = cfg.get("event_type_hints", [])
    lines: List[str] = []
    for item in hints:
        if isinstance(item, str):
            lines.append(f"- {item}")
        elif isinstance(item, dict):
            for key, value in item.items():
                lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def _format_argument_role_hints() -> str:
    cfg = _event_cfg()
    hints = cfg.get("argument_role_hints", [])
    lines: List[str] = []
    for item in hints:
        if isinstance(item, str):
            lines.append(f"- {item}")
        elif isinstance(item, dict):
            for key, value in item.items():
                lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def _format_trigger_guidelines() -> str:
    cfg = _event_cfg()
    guidelines = cfg.get("trigger_word_guidelines", [])
    return "\n".join(f"- {item}" for item in guidelines if isinstance(item, str))


def _extract_json_payload(response: str) -> Dict[str, Any]:
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", response, re.S)
        if match:
            return json.loads(match.group(0))
    raise ValueError("LLM 响应未包含合法的 JSON")


def _normalize_labels(raw_labels: Any) -> List[Any]:
    if not isinstance(raw_labels, list):
        return []
    normalized: List[Any] = []
    for item in raw_labels:
        if isinstance(item, str):
            stripped = item.strip()
            if stripped:
                normalized.append(stripped)
        elif isinstance(item, dict):
            cleaned = {str(k).strip(): str(v).strip() for k, v in item.items() if str(k).strip()}
            if cleaned:
                normalized.append(cleaned)
    return normalized


def _normalize_relationships(raw_relationships: Any) -> List[str]:
    if not isinstance(raw_relationships, list):
        return []
    relationships: List[str] = []
    for rel in raw_relationships:
        if isinstance(rel, str):
            stripped = rel.strip()
            if stripped:
                relationships.append(stripped)
    return relationships


def _fallback_ontology() -> Ontology:
    return Ontology(
        labels=CONFIG["ontology"]["labels"],
        relationships=CONFIG["ontology"]["relationships"],
    )


def _fallback_events() -> List[Dict[str, Any]]:
    cfg = _event_cfg()
    fallback = cfg.get("fallback_events")
    if isinstance(fallback, list):
        normalized = _normalize_event_schema(fallback)
        if normalized:
            return normalized
    return []


def build_ontology(llm_client: LLMClient, background_text: str) -> Ontology:
    """根据背景语料动态生成本体。"""

    if not background_text.strip():
        LOGGER.warning("背景文本为空，退回使用配置中的本体。")
        return _fallback_ontology()

    system_message = (
        "你是一名资深本体工程师，负责根据输入背景语料设计知识图谱本体。"
        "输出需聚焦核心实体，标签数量建议 6-10 个，并结合语料给出关键关系类型。"
        "最终只返回 JSON。"
    )

    label_hint = _format_label_hints()
    relation_hint = _format_relationship_hints()
    user_message = (
        "请参考以下背景语料，并以上述提示为灵感，生成最贴近内容的知识图谱本体。\n"
        "- 允许微调标签或新增更贴近场景的标签描述。\n"
        "- 关系需覆盖主要角色/事件之间的因果、隶属或互动。\n"
        "- 输出 JSON，字段只包含 labels 与 relationships。\n\n"
        "【背景摘录】\n"
        f"{background_text}\n\n"
        "【可参考的标签提示】\n"
        f"{label_hint}\n\n"
        "【可参考的关系提示】\n"
        f"{relation_hint}\n\n"
        "示例输出格式：\n"
        "{\n  \"labels\": [\"概念A\", {\"概念B\": \"描述\"}],\n"
        "  \"relationships\": [\"关系1\", \"关系2\"]\n}"
    )

    try:
        response = llm_client.generate(user_message=user_message, system_message=system_message)
        payload = _extract_json_payload(response)
        labels = _normalize_labels(payload.get("labels"))
        relationships = _normalize_relationships(payload.get("relationships"))
        if not labels or not relationships:
            raise ValueError("LLM 响应缺少标签或关系")
        return Ontology(labels=labels, relationships=relationships)
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("根据背景生成动态本体失败，改用配置本体。原因: %s", exc)
        return _fallback_ontology()


def _normalize_event_schema(raw_events: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw_events, list):
        return []
    normalized: List[Dict[str, Any]] = []
    for item in raw_events:
        if not isinstance(item, dict):
            continue
        event_type = str(item.get("event_type", "")).strip()
        if not event_type:
            continue
        description = str(item.get("description", "")).strip()
        trigger_words: List[str] = []
        raw_triggers = item.get("trigger_words", [])
        if isinstance(raw_triggers, list):
            for trig in raw_triggers:
                if isinstance(trig, str):
                    stripped = trig.strip()
                    if stripped:
                        trigger_words.append(stripped)
        arguments: List[Dict[str, Any]] = []
        raw_arguments = item.get("arguments", [])
        if isinstance(raw_arguments, list):
            for arg in raw_arguments:
                if not isinstance(arg, dict):
                    continue
                role = str(arg.get("role", "")).strip()
                if not role:
                    continue
                description_text = str(arg.get("description", "")).strip()
                required = bool(arg.get("required", False))
                arguments.append(
                    {
                        "role": role,
                        "description": description_text,
                        "required": required,
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


def _iter_label_entries(item: Any) -> Iterable[Tuple[str, str | None]]:
    if isinstance(item, str):
        stripped = item.strip()
        if stripped:
            yield stripped, None
    elif isinstance(item, dict):
        for key, value in item.items():
            label = str(key).strip()
            if not label:
                continue
            description = str(value).strip() if value is not None else ""
            yield label, description or None


def _merge_label_items(existing: List[Any], new_items: List[Any]) -> List[Any]:
    merged: List[Any] = []
    index: Dict[str, int] = {}

    def _add(label: str, description: str | None):
        label = label.strip()
        if not label:
            return
        if label not in index:
            idx = len(merged)
            index[label] = idx
            if description:
                merged.append({label: description})
            else:
                merged.append(label)
            return
        if not description:
            return
        current_idx = index[label]
        current = merged[current_idx]
        if isinstance(current, str):
            merged[current_idx] = {label: description}
        elif isinstance(current, dict):
            existing_desc = next(iter(current.values()))
            if not existing_desc:
                merged[current_idx] = {label: description}

    for candidate in existing:
        for label, description in _iter_label_entries(candidate):
            _add(label, description)
    for candidate in new_items:
        for label, description in _iter_label_entries(candidate):
            _add(label, description)
    return merged


def _merge_string_list(primary: Sequence[str], secondary: Sequence[str]) -> List[str]:
    seen: set[str] = set()
    merged: List[str] = []
    for value in list(primary) + list(secondary):
        if not isinstance(value, str):
            continue
        stripped = value.strip()
        if stripped and stripped not in seen:
            seen.add(stripped)
            merged.append(stripped)
    return merged


def _merge_event_arguments(existing: Sequence[Dict[str, Any]], new_items: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: List[Dict[str, Any]] = []
    index: Dict[str, int] = {}

    def _add(arg: Dict[str, Any]):
        role = str(arg.get("role", "")).strip()
        if not role:
            return
        description = str(arg.get("description", "")).strip()
        required = bool(arg.get("required", False))
        payload = {"role": role, "description": description, "required": required}
        if role not in index:
            index[role] = len(merged)
            merged.append(payload)
            return
        existing_payload = merged[index[role]]
        if description and not existing_payload.get("description"):
            existing_payload["description"] = description
        if required:
            existing_payload["required"] = True

    for item in existing:
        if isinstance(item, dict):
            _add(item)
    for item in new_items:
        if isinstance(item, dict):
            _add(item)
    return merged


def _merge_event_schema(existing: Sequence[Dict[str, Any]], new_items: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    merged: List[Dict[str, Any]] = []
    index: Dict[str, int] = {}

    def _add(event: Dict[str, Any]):
        event_type = str(event.get("event_type", "")).strip()
        if not event_type:
            return
        description = str(event.get("description", "")).strip()
        trigger_words = _merge_string_list(event.get("trigger_words", []), [])
        arguments = _merge_event_arguments([], event.get("arguments", []))
        if event_type not in index:
            merged.append(
                {
                    "event_type": event_type,
                    "description": description,
                    "trigger_words": trigger_words,
                    "arguments": arguments,
                }
            )
            index[event_type] = len(merged) - 1
            return
        current = merged[index[event_type]]
        if description and not current.get("description"):
            current["description"] = description
        current["trigger_words"] = _merge_string_list(current.get("trigger_words", []), trigger_words)
        current["arguments"] = _merge_event_arguments(current.get("arguments", []), arguments)

    for event in existing:
        if isinstance(event, dict):
            _add(event)
    for event in new_items:
        if isinstance(event, dict):
            _add(event)
    return merged


def merge_schema_payload(
    existing_schema: Dict[str, Any] | None,
    new_ontology: Ontology,
    new_events: Sequence[Dict[str, Any]],
) -> Tuple[Ontology, Dict[str, Any]]:
    existing_labels = _normalize_labels(existing_schema.get("labels")) if existing_schema else []
    existing_relationships = _normalize_relationships(existing_schema.get("relationships")) if existing_schema else []
    existing_events = _normalize_event_schema(existing_schema.get("events")) if existing_schema else []

    normalized_labels = _normalize_labels(new_ontology.labels)
    normalized_relationships = _normalize_relationships(new_ontology.relationships)

    merged_labels = _merge_label_items(existing_labels, normalized_labels)
    merged_relationships = _merge_string_list(existing_relationships, normalized_relationships)
    merged_events = _merge_event_schema(existing_events, new_events)

    merged_ontology = Ontology(labels=merged_labels, relationships=merged_relationships)
    payload = merged_ontology.model_dump()
    if merged_events:
        payload["events"] = merged_events
    return merged_ontology, payload


def build_event_schema(llm_client: LLMClient, background_text: str) -> List[Dict[str, Any]]:
    cfg = _event_cfg()
    if not cfg.get("enabled", False):
        return []

    if not background_text.strip():
        LOGGER.warning("背景文本为空，事件抽取提示退回使用 fallback 配置。")
        return _fallback_events()

    system_message = (
        "你是事件抽取专家，需为知识图谱设计事件类型与论元。"
        "输出包含可复用的 event_type、触发词和论元。"
        "最终只返回 JSON，结构为 {\"events\": [...]}。"
    )

    event_hint = _format_event_type_hints()
    argument_hint = _format_argument_role_hints()
    trigger_guidelines = _format_trigger_guidelines()

    max_events = cfg.get("max_event_types", 6)
    user_message = (
        "请基于以下背景语料，总结最重要的事件类型。\n"
        f"- 事件数量不超过 {max_events} 个，可根据内容增删。\n"
        "- 每个事件需包含触发词 trigger_words（数组）与 arguments（论元列表）。\n"
        "- 论元至少覆盖发起方、受影响方或其它关键角色。\n"
        "- arguments 中的每一项需包含 role、description、required 字段。\n"
        "- JSON 结构示例：{\"events\": [{\"event_type\": \"行动\", \"trigger_words\": [..], \"arguments\": [{...}]}]}。\n\n"
        "【背景摘录】\n"
        f"{background_text}\n\n"
        "【可参考的事件类型提示】\n"
        f"{event_hint}\n\n"
        "【论元角色提示】\n"
        f"{argument_hint}\n\n"
        "【触发词撰写建议】\n"
        f"{trigger_guidelines}\n"
    )

    try:
        response = llm_client.generate(user_message=user_message, system_message=system_message)
        payload = _extract_json_payload(response)
        events = _normalize_event_schema(payload.get("events"))
        if not events:
            raise ValueError("LLM 响应缺少 events 字段或内容为空")
        return events
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("生成事件抽取配置失败，改用 fallback。原因: %s", exc)
        return _fallback_events()


def instantiate_llm_client():
    llm_cfg = CONFIG["llm"]
    provider = llm_cfg["provider"].lower()

    if provider == "deepseek":
        # 1) 优先用环境变量，其次用 CONFIG 里的 default_api_key
        api_key = os.environ.get("DEEPSEEK_API_KEY") or llm_cfg.get("default_api_key")
        if not api_key:
            raise EnvironmentError(
                "请先设置 DEEPSEEK_API_KEY 或在 config/config.yaml 的 llm.default_api_key 中提供 Key"
            )

        proxy = llm_cfg.get("proxy")  # 例如 socks5h://192.168.134.165:1010

        return DeepSeekClient(
            model=llm_cfg["deepseek"]["model"],
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
            max_tokens=llm_cfg["deepseek"]["max_tokens"],
            api_key=api_key,
            proxy=proxy,
        )

    if provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("请先设置 OPENAI_API_KEY 环境变量")
        from knowledge_graph_maker.llm_clients.openai_client import OpenAIClient

        return OpenAIClient(
            model=llm_cfg["openai"]["model"],
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
            max_tokens=llm_cfg["openai"]["max_tokens"],
        )

    if provider == "groq":
        if not os.environ.get("GROQ_API_KEY") or os.environ["GROQ_API_KEY"] == "placeholder-key":
            raise EnvironmentError("请先设置有效的 GROQ_API_KEY 环境变量")
        from knowledge_graph_maker.llm_clients.groq_client import GroqClient

        return GroqClient(
            model=llm_cfg["groq"]["model"],
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
        )

    raise ValueError("llm.provider 仅支持 'deepseek'、'openai' 或 'groq'")



def save_json(path: Path, payload: Dict | List):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_nodes(edges: Iterable[Edge]) -> List[Node]:
    unique: Dict[Tuple[str, str], Node] = {}
    for edge in edges:
        unique[(edge.node_1.label, edge.node_1.name)] = edge.node_1
        unique[(edge.node_2.label, edge.node_2.name)] = edge.node_2
    return list(unique.values())


def write_nodes_json(path: Path, nodes: Sequence[Node]):
    save_json(path, [node.model_dump() for node in nodes])


def write_edges_json(path: Path, edges: Sequence[Edge]):
    save_json(path, [edge.model_dump() for edge in edges])


def write_csv(path: Path, headers: Sequence[str], rows: Iterable[Sequence[str]]):
    import csv

    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)


def export_neo4j_csv(paths: OutputPaths, edges: Sequence[Edge]):
    nodes = collect_nodes(edges)
    node_rows = [
        [f"{node.label}:{node.name}", node.label, node.name]
        for node in nodes
    ]
    write_csv(
        paths.neo4j_nodes_csv,
        headers=["node_id", "label", "name"],
        rows=node_rows,
    )
    edge_rows = []
    for edge in edges:
        start_id = f"{edge.node_1.label}:{edge.node_1.name}"
        end_id = f"{edge.node_2.label}:{edge.node_2.name}"
        edge_rows.append(
            [
                start_id,
                end_id,
                edge.relationship,
                json.dumps(edge.metadata, ensure_ascii=False),
                edge.order,
            ]
        )
    write_csv(
        paths.neo4j_edges_csv,
        headers=["start_id", "end_id", "relationship", "metadata", "order"],
        rows=edge_rows,
    )


def sync_neo4j_config():
    import knowledge_graph_maker.neo4j_graph_model as neo_module

    neo_cfg = CONFIG["neo4j"]
    neo_module.config.update(
        {
            "NEO4J_URI": neo_cfg["uri"],
            "NEO4J_USERNAME": neo_cfg["username"],
            "NEO4J_PASSWORD": neo_cfg["password"],
        }
    )


def maybe_save_to_neo4j(edges: Sequence[Edge]):
    if not CONFIG["neo4j"]["enabled"]:
        return
    sync_neo4j_config()
    neo_model = Neo4jGraphModel(edges=list(edges), create_indices=CONFIG["neo4j"]["create_indices"])
    inserted = neo_model.save()
    LOGGER.info("已写入 Neo4j 关系数: %s", inserted)


def main():
    output_paths = ensure_output_paths()
    existing_schema, _ = load_existing_ontology_schema()
    chunks = load_text_chunks()
    if not chunks:
        raise RuntimeError("未获取到任何文本块，请检查 input 配置")
    documents = build_documents(chunks)
    llm_client = instantiate_llm_client()
    background_excerpt = build_background_excerpt(chunks)
    ontology = build_ontology(llm_client=llm_client, background_text=background_excerpt)
    log_label = "新构建出的本体" if existing_schema else "构建出的本体"
    LOGGER.info("%s: %s", log_label, json.dumps(ontology.model_dump(), ensure_ascii=False, indent=2))
    event_schema = build_event_schema(llm_client=llm_client, background_text=background_excerpt)
    merged_ontology, schema_payload = merge_schema_payload(existing_schema, ontology, event_schema)
    graph_maker = GraphMaker(ontology=merged_ontology, llm_client=llm_client, verbose=CONFIG["runtime"]["verbose"])
    edges = graph_maker.from_documents(
        docs=documents,
        delay_s_between=CONFIG["runtime"]["delay_between_requests"],
    )

    nodes = collect_nodes(edges)

    save_json(output_paths.schema, schema_payload)
    write_nodes_json(output_paths.nodes, nodes)
    write_edges_json(output_paths.edges, edges)
    export_neo4j_csv(output_paths, edges)
    maybe_save_to_neo4j(edges)

    LOGGER.info("已生成 %s 个节点、%s 条边。输出目录: %s", len(nodes), len(edges), output_paths.base_dir)


if __name__ == "__main__":
    main()
