"""统一的本体生成与评测流程入口。

根据 ``config/config.yaml`` 中的 pipeline 配置，可选择：
- 全流程（生成 -> 评测），
- 仅生成，
- 仅评测。
"""

from __future__ import annotations

from typing import Literal

from .utils.common import load_yaml_config
from .utils.logger import get_ot_logger

CONFIG = load_yaml_config()
LOGGER = get_ot_logger()


PipelineMode = Literal["all", "generate", "evaluate"]


def _pipeline_config() -> dict:
    cfg = CONFIG.get("pipeline")
    return cfg if isinstance(cfg, dict) else {}


def pipeline_mode() -> PipelineMode:
    cfg = _pipeline_config()
    raw_mode = str(cfg.get("mode", "all")).strip().lower()
    if raw_mode in {"all", "generate", "generate_only"}:
        return "generate" if raw_mode.startswith("generate") else "all"
    if raw_mode in {"eval", "evaluate", "evaluate_only"}:
        return "evaluate"
    return "all"


def _bool_from_cfg(cfg: dict, key: str, default: bool) -> bool:
    value = cfg.get(key, default)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "on"}
    return bool(value)


def generation_enabled() -> bool:
    cfg = _pipeline_config()
    mode = pipeline_mode()
    if mode == "generate":
        return True
    if mode == "evaluate":
        return False
    return _bool_from_cfg(cfg, "generation_enabled", True)


def evaluation_enabled() -> bool:
    cfg = _pipeline_config()
    mode = pipeline_mode()
    base_flag = _bool_from_cfg(cfg, "evaluation_enabled", mode in {"all", "evaluate"})
    eval_cfg = CONFIG.get("evaluation") or {}
    if "enabled" not in eval_cfg:
        return base_flag
    return base_flag and _bool_from_cfg(eval_cfg, "enabled", True)


def run_generation() -> None:
    from .ontology_generate import main as generate_main

    LOGGER.info("[pipeline] 启动本体生成阶段…")
    generate_main()


def run_evaluation() -> None:
    from .ontology_eval import main as eval_main

    LOGGER.info("[pipeline] 启动本体评测阶段…")
    eval_main()


def main() -> None:
    if generation_enabled():
        run_generation()
    else:
        LOGGER.info("[pipeline] 跳过本体生成阶段。")

    if evaluation_enabled():
        run_evaluation()
    else:
        LOGGER.info("[pipeline] 跳过本体评测阶段（未开启或未满足启用条件）。")


if __name__ == "__main__":
    main()
