"""统一的日志记录工具。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .common import PROJECT_ROOT, load_yaml_config, resolve_project_path


LOGGER_NAME = "ot_logger"
LOG_FILENAME = "ot.log"


def get_ot_logger(log_dir: Optional[Path] = None) -> logging.Logger:
    """返回统一的 ot_logger 实例，确保仅初始化一次。

    参数:
        log_dir: 日志目录，默认为仓库根目录下的 ``logs``。
    """

    target_dir = _resolve_log_dir(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    httpx_logger = logging.getLogger("httpx")
    httpcore_logger = logging.getLogger("httpcore")
    httpx_logger.setLevel(logging.WARNING)
    httpcore_logger.setLevel(logging.WARNING)

    if not logger.handlers:
        log_path = target_dir / LOG_FILENAME
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


def _resolve_log_dir(log_dir: Optional[Path]) -> Path:
    if log_dir is not None:
        return Path(log_dir)
    config_dir = _resolve_log_dir_from_config()
    if config_dir is not None:
        return config_dir
    return PROJECT_ROOT / "logs"


def _resolve_log_dir_from_config() -> Optional[Path]:
    try:
        config = load_yaml_config()
    except (FileNotFoundError, ValueError) as exc:
        logging.getLogger(LOGGER_NAME).debug("读取日志配置失败，使用默认 logs 目录: %s", exc)
        return None
    log_cfg = config.get("logging") or {}
    log_dir = log_cfg.get("log_dir") or log_cfg.get("dir")
    if not log_dir:
        legacy = config.get("logs") or {}
        log_dir = legacy.get("dir")
    if not log_dir:
        return None
    return resolve_project_path(log_dir)


__all__ = ["get_ot_logger", "LOGGER_NAME"]
