"""数据集路径解析与加载工具。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

from .common import resolve_project_path


RELATION_ONLY_DATASET_TYPES = {"duie", "instructie", "relation_extraction"}


def _normalize_name(name: str | None) -> str:
    return str(name or "").strip().replace("-", "_").lower()


def dataset_output_dir(config: Dict[str, Any]) -> Path:
    conv_cfg = config.get("dataset_conversion") or {}
    base_dir = conv_cfg.get("output_dir", "data/input")
    return resolve_project_path(base_dir)


def _iter_dataset_entries(config: Dict[str, Any]) -> Iterable[Tuple[Dict[str, Any], str]]:
    conv_cfg = config.get("dataset_conversion") or {}
    base_output = conv_cfg.get("output_dir", "data/input")

    for ds_cfg in conv_cfg.get("datasets", []):
        yield ds_cfg, base_output

    for group_key in ("re", "ee"):
        group_cfg = conv_cfg.get(group_key) or {}
        group_output = group_cfg.get("output_dir", base_output)
        for ds_cfg in group_cfg.get("dataset_configs", []) or []:
            yield ds_cfg, group_output


def _dataset_output_dir_for_name(config: Dict[str, Any], dataset_name: str) -> Path:
    normalized_target = _normalize_name(dataset_name)
    for ds_cfg, output_dir in _iter_dataset_entries(config):
        if _normalize_name(ds_cfg.get("name")) == normalized_target:
            return resolve_project_path(output_dir)
    return dataset_output_dir(config)


def dataset_config(config: Dict[str, Any], dataset_name: str) -> Dict[str, Any] | None:
    normalized_target = _normalize_name(dataset_name)
    for ds_cfg, output_dir in _iter_dataset_entries(config):
        if _normalize_name(ds_cfg.get("name")) == normalized_target:
            merged = dict(ds_cfg)
            merged.setdefault("output_dir", output_dir)
            return merged
    return None


def dataset_is_relation_only(config: Dict[str, Any], dataset_name: str) -> bool:
    ds_cfg = dataset_config(config, dataset_name)
    if not ds_cfg:
        return False
    task = str(ds_cfg.get("task", "")).strip().lower()
    if task == "re":
        return True
    ds_type = str(ds_cfg.get("type", "")).strip().lower()
    if ds_type in RELATION_ONLY_DATASET_TYPES:
        return True
    format_key = str(ds_cfg.get("format", "")).strip().lower()
    return format_key in RELATION_ONLY_DATASET_TYPES


def dataset_data_files(config: Dict[str, Any], dataset_name: str) -> List[Path]:
    ds_cfg = dataset_config(config, dataset_name)
    if not ds_cfg:
        raise ValueError(f"dataset_conversion 中缺少名为 {dataset_name} 的配置")

    files: List[Path] = []
    for raw in ds_cfg.get("data_files", []):
        path = resolve_project_path(raw)
        if not path.exists():
            raise FileNotFoundError(f"未找到数据集文件: {path}")
        files.append(path)
    if not files:
        data_dirs = ds_cfg.get("data_dirs", []) or []
        data_glob = ds_cfg.get("data_glob") or "**/*.json"
        for raw_dir in data_dirs:
            base_dir = resolve_project_path(raw_dir)
            if not base_dir.exists():
                raise FileNotFoundError(f"未找到数据集目录: {base_dir}")
            for path in base_dir.glob(data_glob):
                if path.name == "schema.json":
                    continue
                if path.is_file():
                    files.append(path)
    if not files:
        raise FileNotFoundError(f"数据集 {dataset_name} 未配置任何 data_files")
    return files


def _iter_json_records(paths: Sequence[Path]) -> Iterable[Dict[str, Any]]:
    for path in paths:
        content = path.read_text(encoding="utf-8")
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            payload = None

        if isinstance(payload, list):
            for item in payload:
                if isinstance(item, dict):
                    yield item
            continue
        if isinstance(payload, dict):
            yield payload
            continue

        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                yield record


def _dataset_text_field(dataset_type: str, ds_cfg: Dict[str, Any]) -> str:
    if ds_cfg.get("text_field"):
        return str(ds_cfg["text_field"])
    ds_type = dataset_type.strip().lower()
    format_key = str(ds_cfg.get("format", "")).strip().lower()
    if ds_type == "instructie" or format_key == "instructie":
        return "input"
    return "text"


def load_dataset_background_text(config: Dict[str, Any], dataset_name: str) -> str:
    ds_cfg = dataset_config(config, dataset_name)
    if not ds_cfg:
        raise ValueError(f"未找到数据集 {dataset_name} 的转换配置")

    data_files = dataset_data_files(config, dataset_name)
    text_field = _dataset_text_field(str(ds_cfg.get("type", "")), ds_cfg)

    texts: List[str] = []
    for record in _iter_json_records(data_files):
        text = str(record.get(text_field, "")).strip()
        if text:
            texts.append(text)

    if not texts:
        raise ValueError(f"数据集 {dataset_name} 的文件中未找到任何文本字段 {text_field}")

    return "\n\n".join(texts)


def resolve_dataset_paths(config: Dict[str, Any], dataset_name: str) -> Tuple[Path, Path]:
    """根据 config 中的 dataset_conversion 配置推断金标准文件路径。"""

    normalized_target = _normalize_name(dataset_name)
    output_dir = _dataset_output_dir_for_name(config, dataset_name)

    for ds_cfg, _ in _iter_dataset_entries(config):
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


__all__ = [
    "dataset_config",
    "dataset_data_files",
    "dataset_is_relation_only",
    "dataset_output_dir",
    "load_dataset_background_text",
    "load_dataset_text",
    "resolve_dataset_paths",
]
