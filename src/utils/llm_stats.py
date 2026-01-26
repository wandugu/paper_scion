"""LLM 运行统计与简单 Token 估算。"""

from __future__ import annotations

import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .common import resolve_project_path
from .logger import get_ot_logger


LOGGER = get_ot_logger()


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return max(1, math.ceil(len(text) / 4))


@dataclass
class LLMCallStats:
    provider: str
    model: str
    prompt_chars: int
    completion_chars: int
    prompt_tokens: int
    completion_tokens: int
    elapsed_s: float


@dataclass
class LLMRunStats:
    run_id: str
    start_time: float = field(default_factory=time.time)
    calls: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    prompt_chars: int = 0
    completion_chars: int = 0
    elapsed_total_s: float = 0.0
    min_elapsed_s: Optional[float] = None
    max_elapsed_s: Optional[float] = None
    keep_details: bool = False
    call_details: List[LLMCallStats] = field(default_factory=list)
    dumped: bool = False

    def record_call(
        self,
        provider: str,
        model: str,
        prompt_text: str,
        completion_text: str,
        elapsed_s: float,
    ) -> None:
        prompt_chars = len(prompt_text)
        completion_chars = len(completion_text)
        prompt_tokens = estimate_tokens(prompt_text)
        completion_tokens = estimate_tokens(completion_text)

        self.calls += 1
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.prompt_chars += prompt_chars
        self.completion_chars += completion_chars
        self.elapsed_total_s += elapsed_s
        self.min_elapsed_s = elapsed_s if self.min_elapsed_s is None else min(self.min_elapsed_s, elapsed_s)
        self.max_elapsed_s = elapsed_s if self.max_elapsed_s is None else max(self.max_elapsed_s, elapsed_s)

        if self.keep_details:
            self.call_details.append(
                LLMCallStats(
                    provider=provider,
                    model=model,
                    prompt_chars=prompt_chars,
                    completion_chars=completion_chars,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    elapsed_s=elapsed_s,
                )
            )

        LOGGER.debug(
            "LLM 调用统计: provider=%s model=%s prompt_tokens=%s completion_tokens=%s elapsed_s=%.3f",
            provider,
            model,
            prompt_tokens,
            completion_tokens,
            elapsed_s,
        )

    def to_payload(self) -> Dict[str, Any]:
        elapsed_wall = time.time() - self.start_time
        payload: Dict[str, Any] = {
            "run_id": self.run_id,
            "calls": self.calls,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "prompt_chars": self.prompt_chars,
            "completion_chars": self.completion_chars,
            "elapsed_total_s": round(self.elapsed_total_s, 3),
            "elapsed_wall_s": round(elapsed_wall, 3),
            "min_elapsed_s": None if self.min_elapsed_s is None else round(self.min_elapsed_s, 3),
            "max_elapsed_s": None if self.max_elapsed_s is None else round(self.max_elapsed_s, 3),
        }
        if self.keep_details:
            payload["call_details"] = [
                {
                    "provider": item.provider,
                    "model": item.model,
                    "prompt_chars": item.prompt_chars,
                    "completion_chars": item.completion_chars,
                    "prompt_tokens": item.prompt_tokens,
                    "completion_tokens": item.completion_tokens,
                    "elapsed_s": round(item.elapsed_s, 3),
                }
                for item in self.call_details
            ]
        return payload

    def dump(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_payload(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        self.dumped = True
        LOGGER.info("LLM 运行统计已写入: %s", path)


_GLOBAL_LLM_STATS: Optional[LLMRunStats] = None


def _stats_cfg(config: Dict[str, Any]) -> Dict[str, Any]:
    stats_cfg = config.get("stats") or {}
    return stats_cfg if isinstance(stats_cfg, dict) else {}


def llm_stats_enabled(config: Dict[str, Any]) -> bool:
    stats_cfg = _stats_cfg(config)
    if stats_cfg.get("enabled", True) is False:
        return False
    llm_cfg = stats_cfg.get("llm_run") or {}
    enabled = llm_cfg.get("enabled", True)
    return bool(enabled)


def resolve_llm_stats_path(config: Dict[str, Any]) -> Path:
    stats_cfg = _stats_cfg(config)
    llm_cfg = stats_cfg.get("llm_run") or {}
    output_dir = resolve_project_path(stats_cfg.get("output_dir", "data/output/stats"))
    filename = llm_cfg.get("filename", "llm_run_stats.json")
    return output_dir / filename


def start_llm_run_stats(config: Dict[str, Any], run_id: str) -> LLMRunStats:
    global _GLOBAL_LLM_STATS
    stats_cfg = _stats_cfg(config)
    llm_cfg = stats_cfg.get("llm_run") or {}
    keep_details = bool(llm_cfg.get("keep_call_details", False))
    _GLOBAL_LLM_STATS = LLMRunStats(run_id=run_id, keep_details=keep_details)
    LOGGER.debug("初始化 LLM 统计追踪: run_id=%s keep_details=%s", run_id, keep_details)
    return _GLOBAL_LLM_STATS


def ensure_llm_run_stats(config: Dict[str, Any], run_id: str) -> LLMRunStats:
    global _GLOBAL_LLM_STATS
    if _GLOBAL_LLM_STATS is not None:
        LOGGER.debug("LLM 统计已初始化，沿用现有 run_id=%s", _GLOBAL_LLM_STATS.run_id)
        return _GLOBAL_LLM_STATS
    return start_llm_run_stats(config, run_id=run_id)


def get_llm_run_stats(config: Dict[str, Any], run_id: str = "default") -> LLMRunStats:
    global _GLOBAL_LLM_STATS
    if _GLOBAL_LLM_STATS is None:
        return start_llm_run_stats(config, run_id=run_id)
    return _GLOBAL_LLM_STATS


def dump_llm_run_stats(config: Dict[str, Any]) -> Optional[Path]:
    stats = _GLOBAL_LLM_STATS
    if stats is None:
        LOGGER.debug("未初始化 LLM 统计，无需写入。")
        return None
    if stats.dumped:
        LOGGER.debug("LLM 统计已写入，跳过重复输出。")
        return None
    if not llm_stats_enabled(config):
        LOGGER.debug("LLM 统计未启用，跳过写入。")
        return None
    path = resolve_llm_stats_path(config)
    stats.dump(path)
    return path


__all__ = [
    "LLMRunStats",
    "estimate_tokens",
    "ensure_llm_run_stats",
    "get_llm_run_stats",
    "llm_stats_enabled",
    "resolve_llm_stats_path",
    "dump_llm_run_stats",
]
