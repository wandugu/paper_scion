import logging

from ollama import Client
from ..types import LLMClient


LOGGER = logging.getLogger(__name__)


class OllamaClient(LLMClient):
    _url: str
    _model: str
    _temperature: float
    _top_p: float

    def __init__(self, model: str = "llama3:8b", temperature=0.2, top_p=1, url: str = "http://localhost:11434"):
        self._model = model
        self._temperature = temperature
        self._top_p = top_p
        self._url = url
        # 关闭环境变量代理，确保调用本地 Ollama 服务不被代理配置干扰。
        self._client = Client(host=url, trust_env=False)
        LOGGER.info("使用 Ollama 服务: %s | 模型=%s", url, model)

    def generate(self, user_message: str, system_message: str) -> str:
        options = {
            "top_p": self._top_p,
            "temperature": self._temperature,
        }
        response = self._client.generate(
            model=self._model,
            system=system_message,
            prompt=user_message,
            options=options,
            keep_alive="5m",
        )
        return response["response"]
