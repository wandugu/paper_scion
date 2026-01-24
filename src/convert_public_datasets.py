"""统一转换公开数据集 schema 与样例。"""

from __future__ import annotations

import logging

from .utils.common import load_yaml_config
from .utils.logger import get_ot_logger
from .utils.public_dataset_conversion import convert_from_config


LOGGER = get_ot_logger()
LOGGER.setLevel(logging.DEBUG)


def main() -> None:
    config = load_yaml_config()
    results = convert_from_config(config)
    if results["schemas"] or results["samples"]:
        LOGGER.info("转换完成：")
        for path in results["schemas"]:
            LOGGER.info("  schema -> %s", path)
        for path in results["samples"]:
            LOGGER.info("  samples -> %s", path)
    else:
        LOGGER.info("未找到可转换的数据集配置。")


if __name__ == "__main__":
    main()
