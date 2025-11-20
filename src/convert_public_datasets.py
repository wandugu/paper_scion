"""统一转换公开数据集 schema 与样例。"""

from __future__ import annotations

from utils.common import load_yaml_config
from utils.public_dataset_conversion import convert_from_config


def main() -> None:
    config = load_yaml_config()
    results = convert_from_config(config)
    if results["schemas"] or results["samples"]:
        print("转换完成：")
        for path in results["schemas"]:
            print(f"  schema -> {path}")
        for path in results["samples"]:
            print(f"  samples -> {path}")
    else:
        print("未找到可转换的数据集配置。")


if __name__ == "__main__":
    main()
