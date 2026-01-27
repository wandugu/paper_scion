"""LLM 客户端工厂与 DeepSeek/OpenRouter Client 实现。"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Protocol

import requests
from openai import OpenAI

from .llm_stats import get_llm_run_stats, llm_stats_enabled
from .logger import get_ot_logger


class LLMClient(Protocol):
    def generate(self, user_message: str, system_message: str) -> str:
        """Generate a completion based on system/user prompts."""
        raise NotImplementedError


class TrackedLLMClient(LLMClient):
    def __init__(self, client: LLMClient, config: Dict[str, Any], provider: str, model: str):
        self._client = client
        self._provider = provider
        self._model = model
        self._config = config

    def generate(self, user_message: str, system_message: str) -> str:
        start = time.perf_counter()
        response = self._client.generate(user_message=user_message, system_message=system_message)
        elapsed_s = time.perf_counter() - start
        stats = get_llm_run_stats(self._config, run_id="ontology")
        stats.record_call(
            provider=self._provider,
            model=self._model,
            prompt_text=f"{system_message}\n{user_message}",
            completion_text=response,
            elapsed_s=elapsed_s,
        )
        return response


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

        self._session = requests.Session()
        if proxy:
            self._session.proxies.update({"http": proxy, "https": proxy})

        self._base_url = "https://api.deepseek.com"

    def generate(self, user_message: str, system_message: str) -> str:
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
        headers = {"Authorization": f"Bearer {self._api_key}", "Content-Type": "application/json"}

        resp = self._session.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


class OpenRouterClient(LLMClient):
    """OpenRouter LLM Client：使用 OpenAI SDK 适配 OpenRouter /chat/completions。"""

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
        cfg: Dict[str, Any],
    ):
        base_url = cfg.get("base_url", "https://openrouter.ai/api/v1")
        key_env = cfg.get("api_key_env", "OPENROUTER_API_KEY")
        api_key = cfg.get("api_key") or os.environ.get(key_env, "")
        if not api_key:
            raise RuntimeError(
                "OpenRouter API key 未提供，请在 config.openrouter.api_key 或环境变量中设置 api_key_env"
            )

        extra_headers_cfg = cfg.get("extra_headers", {}) or {}
        default_headers: Dict[str, str] = {}
        referer = extra_headers_cfg.get("referer")
        title = extra_headers_cfg.get("title")
        if referer:
            default_headers["HTTP-Referer"] = referer
        if title:
            default_headers["X-Title"] = title

        client_kwargs: Dict[str, Any] = {
            "base_url": base_url,
            "api_key": api_key,
            "default_headers": default_headers or None,
        }
        timeout = cfg.get("timeout")
        if timeout is not None:
            client_kwargs["timeout"] = timeout

        self._client = OpenAI(**client_kwargs)
        self._model = model
        self._temperature = float(temperature)
        self._top_p = float(top_p)
        self._max_tokens = int(max_tokens)
        self._extra_body = cfg.get("extra_body") or {}
        self._plugins = cfg.get("plugins") or []
        self._logger = get_ot_logger()
        self._logger.debug(
            "OpenRouterClient 初始化完成: base_url=%s model=%s headers=%s timeout=%s",
            base_url,
            model,
            list(default_headers.keys()),
            timeout,
        )

    def generate(self, user_message: str, system_message: str) -> str:
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]
        body: Dict[str, Any] = dict(self._extra_body) if self._extra_body else {}
        if self._plugins:
            body["plugins"] = self._plugins

        self._logger.debug(
            "OpenRouter 请求: model=%s messages=%s temperature=%s top_p=%s max_tokens=%s extra_body_keys=%s",
            self._model,
            len(messages),
            self._temperature,
            self._top_p,
            self._max_tokens,
            list(body.keys()),
        )

        resp = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,
            top_p=self._top_p,
            max_tokens=self._max_tokens,
            extra_body=body,
        )
        content = resp.choices[0].message.content
        self._logger.debug("OpenRouter 响应完成: content_len=%s", len(content or ""))
        return content


def _maybe_wrap_client(config: Dict[str, Any], client: LLMClient, provider: str, model: str) -> LLMClient:
    if not llm_stats_enabled(config):
        return client
    return TrackedLLMClient(client=client, config=config, provider=provider, model=model)


def instantiate_llm_client(config: Dict[str, Any]) -> LLMClient:
    llm_cfg = config.get("llm") or {}
    provider = str(llm_cfg.get("provider", "")).lower()
    logger = get_ot_logger()
    logger.debug("LLM provider 初始化: %s", provider)

    if provider == "deepseek":
        api_key = os.environ.get("DEEPSEEK_API_KEY") or llm_cfg.get("default_api_key")
        if not api_key:
            raise EnvironmentError(
                "请先设置 DEEPSEEK_API_KEY 或在 config/config.yaml 的 llm.default_api_key 中提供 Key"
            )

        proxy = llm_cfg.get("proxy")

        client = DeepSeekClient(
            model=llm_cfg["deepseek"]["model"],
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
            max_tokens=llm_cfg["deepseek"]["max_tokens"],
            api_key=api_key,
            proxy=proxy,
        )
        return _maybe_wrap_client(config, client, "deepseek", llm_cfg["deepseek"]["model"])

    if provider == "openrouter":
        openrouter_cfg = config.get("openrouter") or llm_cfg.get("openrouter") or {}
        if not isinstance(openrouter_cfg, dict):
            openrouter_cfg = {}
        model = llm_cfg.get("openrouter", {}).get("model")
        if not model:
            model = openrouter_cfg.get("model")
        if not model:
            raise EnvironmentError("请在 llm.openrouter.model 或 openrouter.model 中设置模型名称")
        client = OpenRouterClient(
            model=model,
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
            max_tokens=llm_cfg.get("openrouter", {}).get("max_tokens", llm_cfg.get("openai", {}).get("max_tokens", 2048)),
            cfg=openrouter_cfg,
        )
        return _maybe_wrap_client(config, client, "openrouter", model)

    if provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            raise EnvironmentError("请先设置 OPENAI_API_KEY 环境变量")
        from knowledge_graph_maker.llm_clients.openai_client import OpenAIClient

        client = OpenAIClient(
            model=llm_cfg["openai"]["model"],
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
            max_tokens=llm_cfg["openai"]["max_tokens"],
        )
        return _maybe_wrap_client(config, client, "openai", llm_cfg["openai"]["model"])

    if provider == "groq":
        if not os.environ.get("GROQ_API_KEY") or os.environ["GROQ_API_KEY"] == "placeholder-key":
            raise EnvironmentError("请先设置有效的 GROQ_API_KEY 环境变量")
        from knowledge_graph_maker.llm_clients.groq_client import GroqClient

        client = GroqClient(
            model=llm_cfg["groq"]["model"],
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
        )
        return _maybe_wrap_client(config, client, "groq", llm_cfg["groq"]["model"])

    if provider == "ollama":
        from knowledge_graph_maker.llm_clients.ollama_client import OllamaClient

        ollama_cfg = llm_cfg.get("ollama", {})
        client = OllamaClient(
            model=ollama_cfg.get("model", "bge-m3"),
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
            url=ollama_cfg.get("base_url", "http://0.0.0.0:11434"),
        )
        return _maybe_wrap_client(config, client, "ollama", ollama_cfg.get("model", "bge-m3"))

    raise ValueError("llm.provider 仅支持 'deepseek'、'openrouter'、'openai'、'groq' 或 'ollama'")


__all__ = ["DeepSeekClient", "OpenRouterClient", "instantiate_llm_client"]
