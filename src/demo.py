"""Graph Maker 演示脚本
=========================

此脚本展示如何使用仓库内置的 ``knowledge_graph_maker`` 包从任意文本生成知识图谱，
并把结果保存到 ``output/`` 目录下的多种文件格式中。所有运行配置均集中在
``config/config.yaml`` 中，可直接根据自身场景进行修改。

运行前准备
----------
1. 安装依赖：确保 ``requirements.txt``（或 ``poetry`` 环境）已安装好即可，
   无需额外 ``pip install knowledge-graph-maker``。
2. 配置 LLM 服务：
   - DeepSeek: 设置 ``DEEPSEEK_API_KEY`` 环境变量（示例脚本默认使用
     ``provider='deepseek'``，API Key 也可通过 ``config/config.yaml`` 中的
     ``llm.default_api_key`` 字段临时填写）。
   - OpenAI: 设置 ``OPENAI_API_KEY`` 环境变量。
   - Groq: 设置 ``GROQ_API_KEY`` 环境变量。
3. 如需自动写入 Neo4j，请确保本地或远端 Neo4j 实例已启动，且账号、密码、URI
   与 ``config/config.yaml`` 的 ``neo4j`` 配置保持一致。

执行：``python src/demo.py``
"""



from __future__ import annotations

import json
import logging
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Collection, Dict, Iterable, List, Sequence, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
LOG_DIR = PROJECT_ROOT / "logs"
BACKGROUND_SNIPPET_MAX_CHARS = 4000

from utils.common import load_yaml_config, resolve_project_path, save_json


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


CONFIG: Dict = load_yaml_config(CONFIG_PATH)
LOGGER = setup_logger()

SUPPORTED_LANG_CODES: Dict[str, str] = {"zh": "中文", "en": "English"}


def _configured_language_code() -> str:
    lang_cfg = CONFIG.get("language")
    if isinstance(lang_cfg, dict):
        raw_code = lang_cfg.get("code")
    else:
        raw_code = lang_cfg
    code = str(raw_code or "zh").lower()
    if code not in SUPPORTED_LANG_CODES:
        return "zh"
    return code


LANGUAGE_CODE: str = _configured_language_code()
LANGUAGE_SUFFIX: str = f"_{LANGUAGE_CODE}"

ONTOLOGY_SAMPLE_JSON_ZH = (
    '{\n'
    '  "entities": ["概念A", {"概念B": "描述"}],\n'
    '  "relationships": [\n'
    '    {"head_entity": "Person", "tail_entity": "Organisation", "rel_type": "隶属于", "description": "可选说明"}\n'
    '  ]\n'
    '}'
)

ONTOLOGY_SAMPLE_JSON_EN = (
    '{\n'
    '  "entities": ["Concept A", {"Concept B": "description"}],\n'
    '  "relationships": [\n'
    '    {"head_entity": "Person", "tail_entity": "Organisation", "rel_type": "member_of", "description": "optional note"}\n'
    '  ]\n'
    '}'
)

EVENT_SAMPLE_JSON_ZH = (
    '{"events": [{"event_type": "行动", "trigger_words": ["发起", "部署"], '
    '"arguments": [{"role": "发起方", "description": "主动推动事件的一方", "required": true}]}]}'
)

EVENT_SAMPLE_JSON_EN = (
    '{"events": [{"event_type": "Action", "trigger_words": ["initiate", "deploy"], '
    '"arguments": [{"role": "Initiator", "description": "Side that drives the event", "required": true}]}]}'
)

DEFAULT_PROMPT_TEMPLATES: Dict[str, Dict[str, Dict[str, str]]] = {
    "ontology": {
        "zh": {
            "system": (
                "你是一名资深本体工程师，负责根据输入背景语料设计知识图谱本体。"
                "{entity_range_sentence}{relationship_range_sentence}最终只返回 JSON。"
                "{language_instruction}"
            ),
            "user": (
                "请参考以下背景语料，并以上述提示为灵感，生成最贴近内容的知识图谱本体。\n"
                "- 允许微调实体类型或新增更贴近场景的实体描述。\n"
                "- 关系需覆盖主要角色/事件之间的因果、隶属或互动。\n"
                "- 严禁输出具体角色/组织名称，只描述抽象的实体类型（可附简短解释）。\n"
                "- relationships 数组中的每一项必须包含 head_entity、tail_entity、rel_type 字段，可选填 description。\n"
                "- 输出 JSON，字段只包含 entities 与 relationships。\n\n"
                "【背景摘录】\n"
                "{background_text}\n\n"
                "【可参考的实体提示】\n"
                "{entity_hint}\n\n"
                "【可参考的关系提示】\n"
                "{relation_hint}\n\n"
                "示例输出格式：\n"
                "{ontology_sample_json}\n"
                "{language_instruction}"
            ),
        },
        "en": {
            "system": (
                "You are a senior ontology engineer who must design a schema from the provided background text. "
                "{entity_range_sentence}{relationship_range_sentence}Respond with JSON only. {language_instruction}"
            ),
            "user": (
                "Use the following background excerpt and hints to craft an ontology.\n"
                "- You may tweak entity types or add better aligned descriptions.\n"
                "- Relationships should cover causality, affiliation or interaction between major roles/events.\n"
                "- NEVER output concrete names of roles/organisations; only abstract entity types with short notes.\n"
                "- Each item in the relationships array must include head_entity, tail_entity and rel_type, with optional description.\n"
                "- Output JSON with only 'entities' and 'relationships'.\n\n"
                "[Background Excerpt]\n"
                "{background_text}\n\n"
                "[Entity Hints]\n"
                "{entity_hint}\n\n"
                "[Relationship Hints]\n"
                "{relation_hint}\n\n"
                "Sample output:\n"
                "{ontology_sample_json}\n"
                "{language_instruction}"
            ),
        },
    },
    "events": {
        "zh": {
            "system": (
                "你是事件抽取专家，需为知识图谱设计事件类型与论元。{event_range_sentence}输出包含可复用的 "
                "event_type、触发词和论元。最终只返回 JSON，仅保留 events 数组。{language_instruction}"
            ),
            "user": (
                "请基于以下背景语料，总结最重要的事件类型。\n"
                "{event_limit_instruction}\n"
                "- 每个事件需包含触发词 trigger_words（数组）与 arguments（论元列表）。\n"
                "- 论元至少覆盖发起方、受影响方或其它关键角色。\n"
                "- arguments 中的每一项需包含 role、description、required 字段。\n"
                "- JSON 结构示例：{event_sample_json}\n\n"
                "【背景摘录】\n"
                "{background_text}\n\n"
                "【可参考的事件类型提示】\n"
                "{event_hint}\n\n"
                "【论元角色提示】\n"
                "{argument_hint}\n\n"
                "【触发词撰写建议】\n"
                "{trigger_guidelines}\n"
                "{language_instruction}"
            ),
        },
        "en": {
            "system": (
                "You are an event extraction expert who must design reusable event types and arguments for a knowledge graph. "
                "{event_range_sentence}Provide event_type, trigger_words and arguments. Respond with JSON shaped as an 'events' "
                "array only. {language_instruction}"
            ),
            "user": (
                "Summarize the most important event types from the background excerpt.\n"
                "{event_limit_instruction}\n"
                "- Each event must include trigger_words (array) and arguments (list of roles).\n"
                "- Arguments should at least cover initiators, impacted parties or other key roles.\n"
                "- Every argument entry must contain role, description and required fields.\n"
                "- JSON example: {event_sample_json}\n\n"
                "[Background Excerpt]\n"
                "{background_text}\n\n"
                "[Event Type Hints]\n"
                "{event_hint}\n\n"
                "[Argument Role Hints]\n"
                "{argument_hint}\n\n"
                "[Trigger Word Guidelines]\n"
                "{trigger_guidelines}\n"
                "{language_instruction}"
            ),
        },
    },
}


def _prompts_cfg() -> Dict[str, Any]:
    prompts = CONFIG.get("prompts")
    if isinstance(prompts, dict):
        return prompts
    return {}


def _prompt_limits_cfg() -> Dict[str, Any]:
    limits = _prompts_cfg().get("limits")
    if isinstance(limits, dict):
        return limits
    return {}


def _prompt_templates_cfg() -> Dict[str, Any]:
    templates = _prompts_cfg().get("templates")
    if isinstance(templates, dict):
        return templates
    return {}


def _get_prompt_template(section: str, message_type: str) -> str | None:
    templates = _prompt_templates_cfg().get(section)
    if not isinstance(templates, dict):
        return None
    lang_templates = templates.get(LANGUAGE_CODE)
    if not isinstance(lang_templates, dict):
        return None
    value = lang_templates.get(message_type)
    if isinstance(value, str):
        return value
    return None


def _default_prompt_template(section: str, message_type: str) -> str:
    return (
        DEFAULT_PROMPT_TEMPLATES.get(section, {})
        .get(LANGUAGE_CODE, {})
        .get(message_type, "")
    )


def _render_prompt(section: str, message_type: str, context: Dict[str, Any]) -> str:
    template = _get_prompt_template(section, message_type) or _default_prompt_template(section, message_type)
    if not template:
        raise ValueError(f"缺少 {section}-{message_type} 的提示词模板")
    try:
        return template.format(**context)
    except KeyError as exc:  # noqa: PERF203
        raise KeyError(f"提示词模板缺少变量 {exc}") from exc


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _count_range_tuple(limit_key: str) -> Tuple[int | None, int | None]:
    cfg = _prompt_limits_cfg().get(limit_key)
    if isinstance(cfg, dict):
        min_val = _coerce_int(cfg.get("min"))
        max_val = _coerce_int(cfg.get("max"))
        return min_val, max_val
    return None, None


def _format_range_text(limit_key: str) -> str:
    min_val, max_val = _count_range_tuple(limit_key)
    lang_is_zh = LANGUAGE_CODE == "zh"
    unit = "个" if lang_is_zh else " types"

    if min_val is None and (max_val is None or max_val < 0):
        return ""

    if max_val is None or max_val < 0:
        if min_val is None:
            return ""
        return (f"不少于 {min_val}{unit}" if lang_is_zh else f"at least {min_val}{unit}")

    if min_val is None:
        return (f"不超过 {max_val}{unit}" if lang_is_zh else f"up to {max_val}{unit}")

    if min_val == max_val:
        return f"{min_val}{unit}"

    return f"{min_val}-{max_val}{unit}"


def _count_range_sentence(limit_key: str, label_zh: str, label_en: str) -> str:
    range_text = _format_range_text(limit_key)
    if not range_text:
        return ""
    if LANGUAGE_CODE == "zh":
        return f"{label_zh}{range_text}。"
    return f"{label_en}{range_text}."


def _ontology_sample_json_text() -> str:
    return ONTOLOGY_SAMPLE_JSON_ZH if LANGUAGE_CODE == "zh" else ONTOLOGY_SAMPLE_JSON_EN


def _event_sample_json_text() -> str:
    return EVENT_SAMPLE_JSON_ZH if LANGUAGE_CODE == "zh" else EVENT_SAMPLE_JSON_EN


def _event_limit_instruction_text(max_events: int | None) -> str:
    if LANGUAGE_CODE == "zh":
        if max_events is not None and max_events > 0:
            return f"- 事件数量不超过 {max_events} 个，可根据内容增删。"
        return "- 事件数量不设硬性上限，可结合语料自由确定。"

    if max_events is not None and max_events > 0:
        return f"- Limit the number of event types to {max_events}, adjusting as needed."
    return "- There is no hard cap on event types; adjust freely based on the excerpt."


def _language_label() -> str:
    return SUPPORTED_LANG_CODES.get(LANGUAGE_CODE, "English")


def _language_instruction_text() -> str:
    if LANGUAGE_CODE == "zh":
        return "请确保所有输出字段均使用简体中文。"
    return "Please ensure every output field is in English."


def _ontology_language_cfg() -> Dict[str, Any]:
    ontology_cfg = CONFIG.get("ontology") or {}
    languages = ontology_cfg.get("languages")
    if isinstance(languages, dict):
        lang_cfg = languages.get(LANGUAGE_CODE)
        if isinstance(lang_cfg, dict):
            return lang_cfg
    return ontology_cfg


def _localized_entities_config() -> List[Any]:
    ontology_cfg = CONFIG.get("ontology") or {}
    entities = _ontology_language_cfg().get("entities")
    if isinstance(entities, list):
        return entities
    fallback = ontology_cfg.get("entities")
    if isinstance(fallback, list):
        return fallback
    return []


def _localized_relationships_config() -> List[Dict[str, Any]]:
    ontology_cfg = CONFIG.get("ontology") or {}
    relationships = _ontology_language_cfg().get("relationships")
    if isinstance(relationships, list):
        return relationships
    fallback = ontology_cfg.get("relationships")
    if isinstance(fallback, list):
        return fallback
    return []


def _apply_language_suffix(path: Path) -> Path:
    suffix = LANGUAGE_SUFFIX
    name = path.name
    ext = path.suffix
    target_suffix = f"{suffix}{ext}" if ext else suffix
    if name.endswith(target_suffix):
        return path
    if ext:
        new_name = f"{path.stem}{suffix}{ext}"
    else:
        new_name = f"{name}{suffix}"
    return path.with_name(new_name)


def _input_path_with_language(raw_path: str | Path) -> Path:
    resolved = resolve_project_path(raw_path)
    return _apply_language_suffix(resolved)

from knowledge_graph_maker.graph_maker import GraphMaker
from knowledge_graph_maker.neo4j_graph_model import Neo4jGraphModel
from knowledge_graph_maker.types import (
    Document,
    Edge,
    LLMClient,
    Node,
    Ontology,
    RelationshipSchema,
)



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
        schema=_apply_language_suffix(base_dir / CONFIG["output"]["schema_filename"]),
        nodes=_apply_language_suffix(base_dir / CONFIG["output"]["nodes_filename"]),
        edges=_apply_language_suffix(base_dir / CONFIG["output"]["edges_filename"]),
        neo4j_nodes_csv=_apply_language_suffix(base_dir / CONFIG["output"]["neo4j_nodes_csv"]),
        neo4j_edges_csv=_apply_language_suffix(base_dir / CONFIG["output"]["neo4j_edges_csv"]),
    )


def graph_extraction_enabled() -> bool:
    runtime_cfg = CONFIG.get("runtime", {})
    return bool(runtime_cfg.get("graph_extraction_enabled", True))


def evaluation_config() -> Dict[str, Any]:
    cfg = CONFIG.get("evaluation")
    return cfg if isinstance(cfg, dict) else {}


def evaluation_enabled() -> bool:
    cfg = evaluation_config()
    return bool(cfg.get("enabled"))


def evaluation_output_path(base_dir: Path) -> Path:
    cfg = evaluation_config()
    raw_path = cfg.get("output_json")
    if isinstance(raw_path, str) and raw_path.strip():
        return resolve_project_path(raw_path)
    filename = f"ontology_eval_metrics{LANGUAGE_SUFFIX}.json"
    return base_dir / filename


def maybe_run_schema_evaluation(
    pred_schema: Dict[str, Any], existing_schema: Dict[str, Any] | None, output_paths: OutputPaths
) -> None:
    if not evaluation_enabled():
        return
    if not existing_schema:
        LOGGER.warning("已启用本体评估，但缺少 existing_ontology_path，跳过比较。")
        return
    try:
        from utils.ontology_eval import compute_ontology_metrics, schema_dict_to_graph
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("导入本体评估模块失败: %s", exc)
        return

    cfg = evaluation_config()
    try:
        threshold = float(cfg.get("threshold", 0.45))
    except (TypeError, ValueError):
        threshold = 0.45
    try:
        smoothing_rounds = int(cfg.get("graph_smoothing_rounds", 2))
    except (TypeError, ValueError):
        smoothing_rounds = 2
    try:
        smoothing_alpha = float(cfg.get("graph_smoothing_alpha", 0.5))
    except (TypeError, ValueError):
        smoothing_alpha = 0.5

    try:
        gold_graph = schema_dict_to_graph(existing_schema)
        pred_graph = schema_dict_to_graph(pred_schema)
        metrics = compute_ontology_metrics(
            gold_graph=gold_graph,
            pred_graph=pred_graph,
            emb_model=str(cfg.get("emb_model") or "BAAI/bge-large-zh-v1.5"),
            threshold=threshold,
            graph_smoothing_rounds=smoothing_rounds,
            graph_smoothing_alpha=smoothing_alpha,
        )
    except ImportError as exc:
        LOGGER.warning("运行本体评测缺少依赖 (numpy/scipy/sentence-transformers): %s", exc)
        return
    except Exception as exc:  # noqa: BLE001
        LOGGER.warning("运行本体评测失败: %s", exc)
        return

    for name, metric in metrics.items():
        LOGGER.info(
            "[ontology_eval][%s] P=%.4f R=%.4f F1=%.4f",
            name,
            metric.get("precision", 0.0),
            metric.get("recall", 0.0),
            metric.get("f1", 0.0),
        )

    metrics_path = evaluation_output_path(output_paths.base_dir)
    save_json(metrics_path, metrics)
    LOGGER.info("本体评测指标已写入: %s", metrics_path)


SCHEMA_SECTION_ALIASES = {
    "entity": "entities",
    "entities": "entities",
    "label": "entities",
    "labels": "entities",
    "节点": "entities",
    "实体": "entities",
    "relationship": "relationships",
    "relationships": "relationships",
    "edge": "relationships",
    "edges": "relationships",
    "边": "relationships",
    "关系": "relationships",
    "event": "events",
    "events": "events",
    "事件": "events",
}
DEFAULT_SCHEMA_SECTIONS: Set[str] = {"entities", "relationships", "events"}


def schema_output_sections() -> Set[str]:
    """基于 config 决定本体 JSON 中需要保留的板块。"""

    ontology_cfg = CONFIG.get("ontology", {})
    raw_sections = ontology_cfg.get("output_sections")
    if not isinstance(raw_sections, list):
        raw_sections = []

    normalized: Set[str] = set()
    for section in raw_sections:
        if not isinstance(section, str):
            continue
        key = section.strip().lower()
        if not key:
            continue
        if key in {"all", "全部", "全量"}:
            return set(DEFAULT_SCHEMA_SECTIONS)
        alias = SCHEMA_SECTION_ALIASES.get(key)
        if alias:
            normalized.add(alias)

    if not raw_sections or not normalized:
        return set(DEFAULT_SCHEMA_SECTIONS)
    return normalized


def _section_enabled(section: str, enabled_sections: Collection[str] | None) -> bool:
    if not enabled_sections:
        return True
    return section in enabled_sections


def load_text_chunks() -> Sequence[str]:
    cfg = CONFIG["input"]
    if cfg["type"] == "sample":
        from lotr_wikipedia_summary import lord_of_the_rings_wikipedia_summary

        return [chunk.strip() for chunk in lord_of_the_rings_wikipedia_summary if chunk.strip()]
    if cfg["type"] == "text":
        return chunk_text(cfg["text"], cfg["chunk_size"])
    if cfg["type"] == "file":
        text_path = _input_path_with_language(cfg["file_path"])
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
        "language": LANGUAGE_CODE,
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
    path = _input_path_with_language(raw_path)
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


def _format_entity_hints() -> str:
    hints: List[str] = []
    for item in _localized_entities_config():
        if isinstance(item, str):
            hints.append(f"- {item}")
        elif isinstance(item, dict):
            for key, value in item.items():
                hints.append(f"- {key}: {value}")
    return "\n".join(hints)


def _format_relationship_hints() -> str:
    hints: List[str] = []
    for relation in _localized_relationships_config():
        normalized = _normalize_relationship_entry(relation)
        if not normalized:
            continue
        desc = normalized.get("description")
        suffix = f"（{desc}）" if desc else ""
        hints.append(
            f"- {normalized['head_entity']} -> {normalized['tail_entity']}: {normalized['rel_type']}{suffix}"
        )
    return "\n".join(hints)


def _event_cfg() -> Dict[str, Any]:
    base_cfg = CONFIG.get("event_extraction") or {}
    languages = base_cfg.get("languages")
    lang_cfg: Dict[str, Any] = {}
    if isinstance(languages, dict):
        candidate = languages.get(LANGUAGE_CODE)
        if isinstance(candidate, dict):
            lang_cfg = candidate
    merged = {k: v for k, v in base_cfg.items() if k != "languages"}
    merged.update(lang_cfg)
    return merged


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


def _normalize_entities(raw_entities: Any) -> List[Any]:
    if not isinstance(raw_entities, list):
        return []
    normalized: List[Any] = []
    for item in raw_entities:
        if isinstance(item, str):
            stripped = item.strip()
            if stripped:
                normalized.append(stripped)
        elif isinstance(item, dict):
            cleaned = {str(k).strip(): str(v).strip() for k, v in item.items() if str(k).strip()}
            if cleaned:
                normalized.append(cleaned)
    return normalized


def _extract_relation_type(text: str) -> str:
    """从 "实体A-关系-实体B" 这样的描述中抽取中间的关系类型。"""

    stripped = text.strip()
    if stripped.count("-") < 2:
        return stripped

    indices: List[int] = []
    for idx in range(1, len(stripped) - 1):
        if stripped[idx] != "-":
            continue
        prev_char = stripped[idx - 1]
        next_char = stripped[idx + 1]
        if prev_char.isdigit() or next_char.isdigit():
            continue
        indices.append(idx)

    if len(indices) < 2:
        return stripped

    candidate = stripped[indices[0] + 1 : indices[-1]].strip(" -")
    return candidate or stripped


def _normalize_relationship_entry(item: Any) -> Dict[str, Any] | None:
    if isinstance(item, RelationshipSchema):
        payload = item.model_dump()
    elif isinstance(item, dict):
        payload = item
    else:
        return None

    head_entity = str(
        payload.get("head_entity")
        or payload.get("head")
        or payload.get("source_entity")
        or payload.get("source")
        or ""
    ).strip()
    tail_entity = str(
        payload.get("tail_entity")
        or payload.get("tail")
        or payload.get("target_entity")
        or payload.get("target")
        or payload.get("object")
        or ""
    ).strip()
    rel_type = str(
        payload.get("rel_type")
        or payload.get("relationship")
        or payload.get("type")
        or payload.get("name")
        or ""
    ).strip()
    description_val = payload.get("description")
    if isinstance(description_val, str):
        description = description_val.strip() or None
    elif description_val is None:
        description = None
    else:
        description = str(description_val).strip() or None

    if not (head_entity and tail_entity and rel_type):
        return None

    return {
        "head_entity": head_entity,
        "tail_entity": tail_entity,
        "rel_type": rel_type,
        "description": description,
    }


def _normalize_relationships(raw_relationships: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw_relationships, list):
        return []
    relationships: List[Dict[str, Any]] = []
    for rel in raw_relationships:
        normalized = _normalize_relationship_entry(rel)
        if normalized:
            relationships.append(normalized)
    return relationships


def _fallback_ontology() -> Ontology:
    return Ontology(
        entities=_localized_entities_config(),
        relationships=_normalize_relationships(_localized_relationships_config()),
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

    language_instruction = _language_instruction_text()

    entity_hint = _format_entity_hints()
    relation_hint = _format_relationship_hints()

    context = {
        "language_instruction": language_instruction,
        "background_text": background_text,
        "entity_hint": entity_hint,
        "relation_hint": relation_hint,
        "entity_range_sentence": _count_range_sentence("entity_types", "实体类型数量建议 ", "Recommended entity types: "),
        "relationship_range_sentence": _count_range_sentence(
            "relationship_types", "关系类型数量建议 ", "Recommended relationship types: "
        ),
        "entity_range_text": _format_range_text("entity_types"),
        "relationship_range_text": _format_range_text("relationship_types"),
        "ontology_sample_json": _ontology_sample_json_text(),
    }

    system_message = _render_prompt("ontology", "system", context)
    user_message = _render_prompt("ontology", "user", context)

    try:
        response = llm_client.generate(user_message=user_message, system_message=system_message)
        payload = _extract_json_payload(response)
        entities = _normalize_entities(payload.get("entities"))
        relationships = _normalize_relationships(payload.get("relationships"))
        if not entities or not relationships:
            raise ValueError("LLM 响应缺少实体或关系")
        return Ontology(entities=entities, relationships=relationships)
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


def _iter_entity_entries(item: Any) -> Iterable[Tuple[str, str | None]]:
    if isinstance(item, str):
        stripped = item.strip()
        if stripped:
            yield stripped, None
    elif isinstance(item, dict):
        for key, value in item.items():
            entity_name = str(key).strip()
            if not entity_name:
                continue
            description = str(value).strip() if value is not None else ""
            yield entity_name, description or None


def _merge_entity_items(existing: List[Any], new_items: List[Any]) -> List[Any]:
    merged: List[Any] = []
    index: Dict[str, int] = {}

    def _add(entity_name: str, description: str | None):
        entity_name = entity_name.strip()
        if not entity_name:
            return
        if entity_name not in index:
            idx = len(merged)
            index[entity_name] = idx
            if description:
                merged.append({entity_name: description})
            else:
                merged.append(entity_name)
            return
        if not description:
            return
        current_idx = index[entity_name]
        current = merged[current_idx]
        if isinstance(current, str):
            merged[current_idx] = {entity_name: description}
        elif isinstance(current, dict):
            existing_desc = next(iter(current.values()))
            if not existing_desc:
                merged[current_idx] = {entity_name: description}

    for candidate in existing:
        for entity_name, description in _iter_entity_entries(candidate):
            _add(entity_name, description)
    for candidate in new_items:
        for entity_name, description in _iter_entity_entries(candidate):
            _add(entity_name, description)
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


def _merge_relationship_items(
    existing: Sequence[Dict[str, Any]], new_items: Sequence[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    merged: List[Dict[str, Any]] = []
    index: Dict[Tuple[str, str, str], int] = {}

    def _add(item: Dict[str, Any] | RelationshipSchema | None):
        if item is None:
            return
        normalized = _normalize_relationship_entry(item)
        if not normalized:
            return
        key = (
            normalized["head_entity"],
            normalized["tail_entity"],
            normalized["rel_type"],
        )
        if key not in index:
            index[key] = len(merged)
            merged.append(normalized)
            return
        current = merged[index[key]]
        if not current.get("description") and normalized.get("description"):
            current["description"] = normalized["description"]

    for relation in existing:
        _add(relation)
    for relation in new_items:
        _add(relation)
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


def _preferred_schema_entities(
    existing_schema: Dict[str, Any] | None, merged_entities: Sequence[Any]
) -> List[Any]:
    """返回最终写入 schema 文件的实体类型列表，包含新抽取的类型。"""

    existing_entities = _normalize_entities(existing_schema.get("entities")) if existing_schema else []
    if existing_entities:
        return _merge_entity_items(existing_entities, merged_entities)
    config_entities = _normalize_entities(_localized_entities_config())
    if config_entities:
        return _merge_entity_items(config_entities, merged_entities)
    return list(merged_entities)


def _preferred_schema_relationships(
    existing_schema: Dict[str, Any] | None, merged_relationships: Sequence[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """返回最终写入 schema 文件的关系类型列表，包含新抽取的类型。"""

    existing_relationships = (
        _normalize_relationships(existing_schema.get("relationships")) if existing_schema else []
    )
    if existing_relationships:
        return _merge_relationship_items(existing_relationships, merged_relationships)
    config_relationships = _normalize_relationships(_localized_relationships_config())
    if config_relationships:
        return _merge_relationship_items(config_relationships, merged_relationships)
    return list(merged_relationships)


def merge_schema_payload(
    existing_schema: Dict[str, Any] | None,
    new_ontology: Ontology,
    new_events: Sequence[Dict[str, Any]],
    enabled_sections: Collection[str] | None = None,
) -> Tuple[Ontology, Dict[str, Any]]:
    existing_entities = _normalize_entities(existing_schema.get("entities")) if existing_schema else []
    existing_relationships = (
        _normalize_relationships(existing_schema.get("relationships")) if existing_schema else []
    )
    existing_events = _normalize_event_schema(existing_schema.get("events")) if existing_schema else []

    normalized_entities = _normalize_entities(new_ontology.entities)
    normalized_relationships = _normalize_relationships(new_ontology.relationships)

    merged_entities = _merge_entity_items(existing_entities, normalized_entities)
    merged_relationships = _merge_relationship_items(existing_relationships, normalized_relationships)
    merged_events = _merge_event_schema(existing_events, new_events)

    merged_ontology = Ontology(entities=merged_entities, relationships=merged_relationships)

    payload: Dict[str, Any] = {}
    preferred_entities = _preferred_schema_entities(existing_schema, merged_entities) or merged_entities
    preferred_relationships = (
        _preferred_schema_relationships(existing_schema, merged_relationships) or merged_relationships
    )
    if _section_enabled("entities", enabled_sections):
        payload["entities"] = preferred_entities
    if _section_enabled("relationships", enabled_sections):
        payload["relationships"] = preferred_relationships
    if merged_events and _section_enabled("events", enabled_sections):
        payload["events"] = merged_events
    return merged_ontology, payload


def build_event_schema(llm_client: LLMClient, background_text: str) -> List[Dict[str, Any]]:
    cfg = _event_cfg()
    if not cfg.get("enabled", False):
        return []

    if not background_text.strip():
        LOGGER.warning("背景文本为空，事件抽取提示退回使用 fallback 配置。")
        return _fallback_events()

    language_instruction = _language_instruction_text()

    event_hint = _format_event_type_hints()
    argument_hint = _format_argument_role_hints()
    trigger_guidelines = _format_trigger_guidelines()

    max_events_val = _coerce_int(cfg.get("max_event_types"))
    if max_events_val is not None and max_events_val < 0:
        max_events_val = None

    context = {
        "language_instruction": language_instruction,
        "background_text": background_text,
        "event_hint": event_hint,
        "argument_hint": argument_hint,
        "trigger_guidelines": trigger_guidelines,
        "event_range_sentence": _count_range_sentence("event_types", "事件类型数量建议 ", "Recommended event types: "),
        "event_range_text": _format_range_text("event_types"),
        "event_limit_instruction": _event_limit_instruction_text(max_events_val),
        "event_sample_json": _event_sample_json_text(),
        "max_events": str(max_events_val) if max_events_val is not None else "",
    }

    system_message = _render_prompt("events", "system", context)
    user_message = _render_prompt("events", "user", context)

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

def collect_nodes(edges: Iterable[Edge]) -> List[Node]:
    unique: Dict[Tuple[str, str], Node] = {}
    for edge in edges:
        unique[(edge.node_1.entity, edge.node_1.name)] = edge.node_1
        unique[(edge.node_2.entity, edge.node_2.name)] = edge.node_2
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
        [f"{node.entity}:{node.name}", node.entity, node.name]
        for node in nodes
    ]
    write_csv(
        paths.neo4j_nodes_csv,
        headers=["node_id", "entity", "name"],
        rows=node_rows,
    )
    edge_rows = []
    for edge in edges:
        start_id = f"{edge.node_1.entity}:{edge.node_1.name}"
        end_id = f"{edge.node_2.entity}:{edge.node_2.name}"
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
    schema_for_eval: Dict[str, Any] = {
        "entities": _normalize_entities(ontology.entities),
        "relationships": _normalize_relationships(ontology.relationships),
    }
    if event_schema:
        schema_for_eval["events"] = event_schema
    merged_ontology, schema_payload = merge_schema_payload(
        existing_schema,
        ontology,
        event_schema,
        enabled_sections=schema_output_sections(),
    )

    save_json(output_paths.schema, schema_payload)
    maybe_run_schema_evaluation(schema_for_eval, existing_schema, output_paths)

    if not graph_extraction_enabled():
        LOGGER.info("已根据配置仅输出本体文件，跳过图谱抽取及 Neo4j 导出。输出目录: %s", output_paths.base_dir)
        return

    graph_maker = GraphMaker(
        ontology=merged_ontology,
        llm_client=llm_client,
        verbose=CONFIG["runtime"]["verbose"],
        language=LANGUAGE_CODE,
    )
    edges = graph_maker.from_documents(
        docs=documents,
        delay_s_between=CONFIG["runtime"]["delay_between_requests"],
    )

    nodes = collect_nodes(edges)

    write_nodes_json(output_paths.nodes, nodes)
    write_edges_json(output_paths.edges, edges)
    export_neo4j_csv(output_paths, edges)
    maybe_save_to_neo4j(edges)

    LOGGER.info("已生成 %s 个节点、%s 条边。输出目录: %s", len(nodes), len(edges), output_paths.base_dir)


if __name__ == "__main__":
    main()
