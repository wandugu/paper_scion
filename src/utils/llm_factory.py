"""LLM 客户端工厂与 DeepSeek Client 实现。"""

from __future__ import annotations

import os
from typing import Any, Dict, Protocol

import requests


class LLMClient(Protocol):
    def generate(self, user_message: str, system_message: str) -> str:
        """Generate a completion based on system/user prompts."""
        raise NotImplementedError


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

    if provider == "ollama":
        from knowledge_graph_maker.llm_clients.ollama_client import OllamaClient

        ollama_cfg = llm_cfg.get("ollama", {})
        return OllamaClient(
            model=ollama_cfg.get("model", "bge-m3"),
            temperature=llm_cfg["temperature"],
            top_p=llm_cfg["top_p"],
            url=ollama_cfg.get("base_url", "http://0.0.0.0:11434"),
        )

    raise ValueError("llm.provider 仅支持 'deepseek'、'openai'、'groq' 或 'ollama'")


__all__ = ["DeepSeekClient", "instantiate_llm_client"]
