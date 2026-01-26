"""LLM 客户端工厂与 DeepSeek Client 实现。"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Protocol

import requests

from .llm_stats import get_llm_run_stats, llm_stats_enabled


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


def _maybe_wrap_client(config: Dict[str, Any], client: LLMClient, provider: str, model: str) -> LLMClient:
    if not llm_stats_enabled(config):
        return client
    return TrackedLLMClient(client=client, config=config, provider=provider, model=model)


def instantiate_llm_client(config: Dict[str, Any]) -> LLMClient:
    llm_cfg = config.get("llm") or {}
    provider = str(llm_cfg.get("provider", "")).lower()

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

    raise ValueError("llm.provider 仅支持 'deepseek'、'openai'、'groq' 或 'ollama'")


__all__ = ["DeepSeekClient", "instantiate_llm_client"]
