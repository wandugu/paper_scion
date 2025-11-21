"""统一的日志记录工具。"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from utils.common import PROJECT_ROOT


LOGGER_NAME = "ot_logger"
LOG_FILENAME = "ot.log"


def get_ot_logger(log_dir: Optional[Path] = None) -> logging.Logger:
    """返回统一的 ot_logger 实例，确保仅初始化一次。

    参数:
        log_dir: 日志目录，默认为仓库根目录下的 ``logs``。
    """

    target_dir = Path(log_dir) if log_dir is not None else PROJECT_ROOT / "logs"
    target_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        log_path = target_dir / LOG_FILENAME
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


__all__ = ["get_ot_logger", "LOGGER_NAME"]
