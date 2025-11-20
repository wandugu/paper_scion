"""本体生成-评估流程控制脚本。

根据 `config/config.yaml` 中的 `process.mode` 配置，可选择：
- all：先生成 schema，再与金标准进行评估；
- generate_only：仅生成 schema；
- evaluate_only：仅执行评估（要求已存在预测本体文件）。
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import ontology_eval
import ontology_generate
from ontology_eval import resolve_golden_schema_path, resolve_pred_schema_path
from utils.common import load_yaml_config
from utils.logger import get_ot_logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"
CONFIG: Dict = load_yaml_config(CONFIG_PATH)
LOGGER = get_ot_logger()

_VALID_MODES = {"all", "generate_only", "evaluate_only", "generate", "evaluate"}


def _process_mode() -> str:
    process_cfg = CONFIG.get("process") or {}
    raw_mode = str(process_cfg.get("mode", "all")).lower()
    if raw_mode not in _VALID_MODES:
        LOGGER.warning("检测到未知的 process.mode=%s，回退为 all。", raw_mode)
        return "all"
    if raw_mode == "generate":
        return "generate_only"
    if raw_mode == "evaluate":
        return "evaluate_only"
    return raw_mode


def _should_run_generation(mode: str) -> bool:
    return mode in {"all", "generate_only"}


def _should_run_evaluation(mode: str) -> bool:
    return mode in {"all", "evaluate_only"}


def _ensure_pred_schema() -> Path:
    pred_path = resolve_pred_schema_path()
    if pred_path.exists():
        return pred_path
    raise FileNotFoundError(
        f"预测本体文件不存在: {pred_path}，请先运行 ontology_generate.py 或调整配置。"
    )


def _log_eval_targets() -> None:
    gold_path = resolve_golden_schema_path()
    pred_path = resolve_pred_schema_path()
    LOGGER.info("评估目标 | 预测: %s | 金标准: %s", pred_path, gold_path)


def run_generation() -> None:
    LOGGER.info("开始执行本体生成流程……")
    ontology_generate.main()


def run_evaluation(force: bool = False) -> None:
    eval_enabled = bool(CONFIG.get("evaluation", {}).get("enabled", False))
    if not eval_enabled and not force:
        LOGGER.info("evaluation.enabled=false，按配置跳过评估阶段。")
        return

    _ensure_pred_schema()
    _log_eval_targets()
    LOGGER.info("开始执行本体评估流程……")
    ontology_eval.main()


def main() -> None:
    mode = _process_mode()
    LOGGER.info("流程模式=%s", mode)

    if _should_run_generation(mode):
        run_generation()

    if _should_run_evaluation(mode):
        run_evaluation(force=mode == "evaluate_only")

    if not _should_run_generation(mode) and not _should_run_evaluation(mode):
        LOGGER.warning("未匹配到可执行的流程，请检查 process.mode 配置。")


if __name__ == "__main__":
    main()
