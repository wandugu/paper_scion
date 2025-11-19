"""通用工具函数，供仓库内多个脚本复用。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import yaml

SRC_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SRC_DIR.parent


def resolve_project_path(path_str: str | Path) -> Path:
    """将任意路径解析为相对于仓库根目录的绝对路径。"""

    path = Path(path_str).expanduser()
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def load_yaml_config(path: Path | None = None) -> Dict[str, Any]:
    """加载 YAML 配置文件并返回字典。"""

    config_path = Path(path) if path else PROJECT_ROOT / "config" / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"未找到配置文件: {config_path}")
    with config_path.open("r", encoding="utf-8") as fp:
        data = yaml.safe_load(fp) or {}
    if not isinstance(data, dict):
        raise ValueError("配置文件内容必须是 JSON/YAML 字典结构。")
    return data


def save_json(path: Path, payload: Any) -> None:
    """以 UTF-8 编码写入 JSON，并自动创建父目录。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


__all__ = [
    "PROJECT_ROOT",
    "SRC_DIR",
    "load_yaml_config",
    "resolve_project_path",
    "save_json",
]
