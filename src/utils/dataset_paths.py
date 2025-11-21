"""数据集路径解析与加载工具。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

from .common import resolve_project_path


def _normalize_name(name: str | None) -> str:
    return str(name or "").strip().replace("-", "_").lower()


def dataset_output_dir(config: Dict[str, Any]) -> Path:
    conv_cfg = config.get("dataset_conversion") or {}
    base_dir = conv_cfg.get("output_dir", "input")
    return resolve_project_path(base_dir)


def resolve_dataset_paths(config: Dict[str, Any], dataset_name: str) -> Tuple[Path, Path]:
    """根据 config 中的 dataset_conversion 配置推断金标准文件路径。"""

    normalized_target = _normalize_name(dataset_name)
    conv_cfg = config.get("dataset_conversion") or {}
    output_dir = dataset_output_dir(config)

    for ds_cfg in conv_cfg.get("datasets", []):
        if _normalize_name(ds_cfg.get("name")) != normalized_target:
            continue

        schema_out = ds_cfg.get("schema_output") or f"golden_schema_{dataset_name}.json"
        samples_out = ds_cfg.get("samples_output") or f"golden_input_{dataset_name}.json"

        schema_path = Path(schema_out)
        samples_path = Path(samples_out)
        if not schema_path.is_absolute():
            schema_path = output_dir / schema_path
        if not samples_path.is_absolute():
            samples_path = output_dir / samples_path

        return resolve_project_path(schema_path), resolve_project_path(samples_path)

    default_schema = output_dir / f"golden_schema_{dataset_name}.json"
    default_samples = output_dir / f"golden_input_{dataset_name}.json"
    return resolve_project_path(default_schema), resolve_project_path(default_samples)


def load_dataset_text(samples_path: Path) -> str:
    """将 golden_input JSON 中的样本文本拼接为背景字符串。"""

    if not samples_path.exists():
        raise FileNotFoundError(f"未找到 golden_input 文件: {samples_path}")

    payload = json.loads(samples_path.read_text(encoding="utf-8"))
    texts = []
    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            for sample in item.get("samples", []):
                if not isinstance(sample, dict):
                    continue
                text = str(sample.get("text", "")).strip()
                if text:
                    texts.append(text)
    return "\n\n".join(texts)


__all__ = ["dataset_output_dir", "load_dataset_text", "resolve_dataset_paths"]
