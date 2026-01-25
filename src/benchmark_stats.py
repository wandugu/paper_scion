"""生成公开数据集 benchmark 统计信息。"""

from __future__ import annotations

import logging

from .utils.benchmark_stats import run_benchmark_stats
from .utils.common import load_yaml_config
from .utils.logger import get_ot_logger


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


def main() -> None:
    config = load_yaml_config()
    run_benchmark_stats(config)


if __name__ == "__main__":
    main()
