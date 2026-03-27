from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from src.utils.common import load_yaml_config, resolve_project_path
from src.utils.logger import get_ot_logger
from src.utils.rebuttal_helpers import outputs_dir, scope_subsets_dir

LOGGER = get_ot_logger()
CONFIG = load_yaml_config()


@dataclass(frozen=True)
class ExperimentSpec:
    exp_id: str
    script: str
    inputs: List[str]
    expected_outputs: List[str]


def _rebuttal_run_all_cfg() -> Dict:
    rebuttal_cfg = CONFIG.get("rebuttal")
    if not isinstance(rebuttal_cfg, dict):
        return {}
    run_all_cfg = rebuttal_cfg.get("run_all")
    return run_all_cfg if isinstance(run_all_cfg, dict) else {}


def _default_specs() -> List[ExperimentSpec]:
    # E0 负责准备数据与基线元信息，E1-E12 为 12 个 rebuttal 实验。
    return [
        ExperimentSpec("E0", "src/rebuttal/scripts/E0_phase0_setup.py", ["data/scope/subsets"], ["rebuttal/outputs/E0_environment.json"]),
        ExperimentSpec("E1", "src/rebuttal/scripts/E1_run_reachable_eval.py", ["data/scope/subsets"], ["rebuttal/outputs/E1_main_metrics.csv"]),
        ExperimentSpec("E2", "src/rebuttal/scripts/E2_run_normalization_sensitivity.py", ["data/scope/subsets"], ["rebuttal/outputs/E2_target_variant_metrics.csv"]),
        ExperimentSpec("E3", "src/rebuttal/scripts/E3_run_eta_baseline.py", ["data/scope/subsets"], ["rebuttal/outputs/E3_main_baseline_comparison.csv"]),
        ExperimentSpec("E4", "src/rebuttal/scripts/E4_run_downstream_eval.py", ["data/scope/subsets"], ["rebuttal/outputs/E4_downstream_main.csv"]),
        ExperimentSpec("E5", "src/rebuttal/scripts/E5_run_contamination_probes.py", ["data/scope/subsets"], ["rebuttal/outputs/E5_probe_results.csv"]),
        ExperimentSpec("E6", "src/rebuttal/scripts/E6_run_fusion_baselines.py", ["data/scope/subsets"], ["rebuttal/outputs/E6_fusion_main.csv"]),
        ExperimentSpec("E7", "src/rebuttal/scripts/E7_prepare_metric_human_calibration.py", ["data/scope/subsets"], ["rebuttal/outputs/E7_annotation_packet.csv"]),
        ExperimentSpec("E8", "src/rebuttal/scripts/E8_run_noise_polysemy_encoder.py", ["data/scope/subsets"], ["rebuttal/outputs/E8_noise_robustness.csv"]),
        ExperimentSpec("E9", "src/rebuttal/scripts/E9_run_scion_rl_ablation.py", ["data/scope/subsets"], ["rebuttal/outputs/E9_sft_vs_rl.csv"]),
        ExperimentSpec("E10", "src/rebuttal/scripts/E10_run_lite_full_tradeoff.py", ["data/scope/subsets"], ["rebuttal/outputs/E10_lite_full_main.csv"]),
        ExperimentSpec("E11", "src/rebuttal/scripts/E11_run_domain_specific_engineer.py", ["data/scope/subsets"], ["rebuttal/outputs/E11_domain_specific_main.csv"]),
        ExperimentSpec("E12", "src/rebuttal/scripts/E12_run_inter_event_pilot.py", ["data/scope/subsets"], ["rebuttal/outputs/E12_inter_event_main.csv"]),
    ]


def _load_specs() -> List[ExperimentSpec]:
    cfg = _rebuttal_run_all_cfg()
    scripts = cfg.get("scripts")
    if not isinstance(scripts, list) or not scripts:
        return _default_specs()

    specs: List[ExperimentSpec] = []
    for item in scripts:
        if not isinstance(item, dict):
            continue
        exp_id = str(item.get("id", "")).strip()
        script = str(item.get("script", "")).strip()
        if not exp_id or not script:
            continue
        inputs = item.get("inputs") if isinstance(item.get("inputs"), list) else []
        outputs = item.get("expected_outputs") if isinstance(item.get("expected_outputs"), list) else []
        specs.append(ExperimentSpec(exp_id=exp_id, script=script, inputs=[str(x) for x in inputs], expected_outputs=[str(x) for x in outputs]))

    return specs if specs else _default_specs()


def _collect_files(base: Path) -> set[str]:
    if not base.exists():
        return set()
    return {str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()}


def _resolve_many(paths: List[str]) -> List[Path]:
    return [resolve_project_path(p) for p in paths]


def _read_text_preview(path: Path, max_chars: int) -> str:
    if not path.exists() or not path.is_file():
        return "(missing)"
    content = path.read_text(encoding="utf-8", errors="replace")
    if len(content) <= max_chars:
        return content
    truncated = content[:max_chars]
    return f"{truncated}\n\n... (truncated, total_chars={len(content)}, max_chars={max_chars})"


def _detect_llm_signal(log_text: str) -> dict:
    lowered = log_text.lower()
    keywords = [
        "openai",
        "deepseek",
        "groq",
        "chat.completions",
        "responses.create",
        "api_key",
        "http",
        "llm",
    ]
    hits = [k for k in keywords if k in lowered]
    return {"detected": bool(hits), "keywords": hits}


def _collect_experiment_output_files(out_dir: Path, exp_id: str, include_suffixes: List[str]) -> List[Path]:
    prefixes = (f"{exp_id}_", f"{exp_id}.")
    suffixes = tuple(include_suffixes)
    files: List[Path] = []
    for item in sorted(out_dir.iterdir() if out_dir.exists() else []):
        if not item.is_file():
            continue
        if not item.name.startswith(prefixes):
            continue
        if suffixes and item.suffix.lower() not in suffixes:
            continue
        files.append(item)
    return files


def _clean_experiment_output_files(out_dir: Path, exp_id: str, include_suffixes: List[str]) -> List[Path]:
    prefixes = (f"{exp_id}_", f"{exp_id}.")
    suffixes = tuple(include_suffixes)
    removed: List[Path] = []
    if not out_dir.exists():
        return removed
    for item in sorted(out_dir.iterdir()):
        if not item.is_file():
            continue
        if not item.name.startswith(prefixes):
            continue
        if suffixes and item.suffix.lower() not in suffixes:
            continue
        item.unlink()
        removed.append(item)
    return removed


def run_all() -> int:
    specs = _load_specs()
    out_dir = outputs_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    run_all_cfg = _rebuttal_run_all_cfg()
    logs_dir = resolve_project_path(run_all_cfg.get("logs_dir", "rebuttal/outputs/run_logs"))
    logs_dir.mkdir(parents=True, exist_ok=True)

    summary_md_path = resolve_project_path(run_all_cfg.get("summary_md", "rebuttal/outputs/E0_run_all_summary.md"))
    output_md_path = resolve_project_path(run_all_cfg.get("output_md", "rebuttal/outputs/E0_run_all_output.md"))
    result_jsonl_path = resolve_project_path(run_all_cfg.get("result_jsonl", "rebuttal/outputs/E0_run_all_results.jsonl"))
    output_preview_char_limit = int(run_all_cfg.get("output_preview_char_limit", 20000))
    output_include_suffixes = run_all_cfg.get("output_include_suffixes", [".csv", ".json", ".md"])
    if not isinstance(output_include_suffixes, list):
        output_include_suffixes = [".csv", ".json", ".md"]
    output_include_suffixes = [str(x).lower() for x in output_include_suffixes]
    clean_old_outputs = bool(run_all_cfg.get("clean_old_outputs", True))

    project_root = resolve_project_path(".")

    LOGGER.debug("E0 run_all 启动，实验数量=%s, logs_dir=%s", len(specs), logs_dir)
    LOGGER.debug("SCOPE 子集目录=%s，存在=%s", scope_subsets_dir(), scope_subsets_dir().exists())

    before_all = _collect_files(out_dir)
    records: List[dict] = []
    failed = False
    result_jsonl_path.write_text("", encoding="utf-8")

    for spec in specs:
        script_path = resolve_project_path(spec.script)
        log_path = logs_dir / f"{spec.exp_id}.log"

        inputs = _resolve_many(spec.inputs)
        inputs_status = [{"path": str(p), "exists": p.exists()} for p in inputs]

        before = _collect_files(out_dir)
        cmd = [sys.executable, str(script_path)]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root)

        LOGGER.debug("开始执行 %s: script=%s", spec.exp_id, script_path)
        LOGGER.debug("%s 输入检查: %s", spec.exp_id, inputs_status)
        if clean_old_outputs and spec.exp_id != "E0":
            removed_files = _clean_experiment_output_files(out_dir, spec.exp_id, output_include_suffixes)
            LOGGER.debug("%s 预清理旧产物数量=%s", spec.exp_id, len(removed_files))

        proc = subprocess.run(cmd, cwd=project_root, env=env, text=True, capture_output=True)
        log_text = (proc.stdout or "") + "\n\n# STDERR\n" + (proc.stderr or "")
        log_path.write_text(log_text, encoding="utf-8")
        llm_signal = _detect_llm_signal(log_text)

        after = _collect_files(out_dir)
        created = sorted(after - before)

        expected_paths = _resolve_many(spec.expected_outputs)
        expected_status = [{"path": str(p), "exists": p.exists()} for p in expected_paths]

        record = {
            "exp_id": spec.exp_id,
            "script": spec.script,
            "cmd": " ".join(cmd),
            "return_code": proc.returncode,
            "inputs": inputs_status,
            "expected_outputs": expected_status,
            "new_output_files": created,
            "stdout_lines": len((proc.stdout or "").splitlines()),
            "stderr_lines": len((proc.stderr or "").splitlines()),
            "log_file": str(log_path.relative_to(project_root)),
            "io_logged": bool(proc.stdout or proc.stderr),
            "llm_signal_detected": llm_signal["detected"],
            "llm_signal_keywords": llm_signal["keywords"],
        }
        records.append(record)

        with result_jsonl_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        LOGGER.debug("%s 完成: rc=%s, new_files=%s, expected=%s", spec.exp_id, proc.returncode, created, expected_status)

        if proc.returncode != 0:
            failed = True
            LOGGER.error("%s 执行失败，详见日志: %s", spec.exp_id, log_path)
            break

    after_all = _collect_files(out_dir)
    overall_new = sorted(after_all - before_all)

    lines = [
        "# E0 Run All Summary",
        "",
        f"- total_scripts: {len(specs)}",
        f"- executed_scripts: {len(records)}",
        f"- failed: {failed}",
        f"- outputs_dir: `{out_dir}`",
        f"- result_jsonl: `{result_jsonl_path}`",
        f"- output_md: `{output_md_path}`",
        f"- logs_dir: `{logs_dir}`",
        "",
        "## Overall New Output Files",
    ]
    lines.extend([f"- `{f}`" for f in overall_new] or ["- (none)"])
    lines.append("")

    for rec in records:
        lines.extend([
            f"## {rec['exp_id']}",
            f"- script: `{rec['script']}`",
            f"- return_code: `{rec['return_code']}`",
            f"- io_logged(stdout/stderr): `{rec['io_logged']}`",
            f"- stdout_lines: `{rec['stdout_lines']}`, stderr_lines: `{rec['stderr_lines']}`",
            f"- log_file: `{rec['log_file']}`",
            f"- llm_signal_detected: `{rec['llm_signal_detected']}`",
            f"- llm_signal_keywords: `{', '.join(rec['llm_signal_keywords']) if rec['llm_signal_keywords'] else "(none)"}`",
            "- inputs:",
        ])
        for item in rec["inputs"]:
            lines.append(f"  - `{item['path']}` (exists={item['exists']})")
        lines.append("- expected_outputs:")
        for item in rec["expected_outputs"]:
            lines.append(f"  - `{item['path']}` (exists={item['exists']})")
        lines.append("- new_output_files:")
        for path in rec["new_output_files"]:
            lines.append(f"  - `rebuttal/outputs/{path}`")
        if not rec["new_output_files"]:
            lines.append("  - (none)")
        lines.append("")

    summary_md_path.write_text("\n".join(lines), encoding="utf-8")
    LOGGER.debug("汇总文件已写入: %s", summary_md_path)

    output_lines = [
        "# E0 Run All Output Details",
        "",
        f"- generated_by: `src/rebuttal/scripts/E0_run_all.py`",
        f"- output_preview_char_limit: `{output_preview_char_limit}`",
        "",
    ]

    for rec in records:
        exp_id = rec["exp_id"]
        if exp_id == "E0":
            continue
        output_lines.extend([f"## {exp_id}", ""])
        exp_files = _collect_experiment_output_files(out_dir, exp_id, output_include_suffixes)
        if not exp_files:
            output_lines.append("(no output files found)")
            output_lines.append("")
            continue
        for file_path in exp_files:
            rel = file_path.relative_to(project_root)
            output_lines.extend([
                f"### 源文件: `{rel.name}`",
                "",
                f"- 路径: `{rel}`",
                f"- 文件大小(bytes): `{file_path.stat().st_size}`",
                "",
                "```text",
                _read_text_preview(file_path, output_preview_char_limit).rstrip("\n"),
                "```",
                "",
            ])

    output_md_path.write_text("\n".join(output_lines), encoding="utf-8")
    LOGGER.debug("详细输出汇总已写入: %s", output_md_path)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run_all())
