from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, Tuple

from tqdm import tqdm

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
        ExperimentSpec("E7", "src/rebuttal/scripts/E7_v2_prepare_annotation.py", ["data/scope/subsets"], ["rebuttal/outputs/E7_v2_annotation_packet.csv"]),
        ExperimentSpec("E7_SCORE", "src/rebuttal/scripts/E7_v2_score.py", ["rebuttal/outputs/E7_v2_template_1.csv", "rebuttal/outputs/E7_v2_template_2.csv"], ["rebuttal/outputs/E7_v2_score_bin_calibration.csv"]),
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


def _collect_protected_output_inputs(specs: List[ExperimentSpec], out_dir: Path) -> Set[Path]:
    """收集位于输出目录中的输入文件，避免被前置实验清理误删。"""
    protected: Set[Path] = set()
    for spec in specs:
        for input_path in _resolve_many(spec.inputs):
            try:
                input_path.relative_to(out_dir)
            except ValueError:
                continue
            protected.add(input_path)
    return protected


def _select_specs(specs: List[ExperimentSpec]) -> Tuple[List[ExperimentSpec], List[str]]:
    cfg = _rebuttal_run_all_cfg()
    selected_ids = cfg.get("selected_experiments")
    if selected_ids is None:
        return specs, []
    if not isinstance(selected_ids, list):
        LOGGER.warning("rebuttal.run_all.selected_experiments 不是 list，忽略该配置并执行全量实验。")
        return specs, []
    normalized = [str(x).strip() for x in selected_ids if str(x).strip()]
    if not normalized:
        return specs, []
    id_set = set(normalized)
    selected_specs = [s for s in specs if s.exp_id in id_set]
    missing = [x for x in normalized if x not in {s.exp_id for s in specs}]
    if missing:
        LOGGER.warning("selected_experiments 中存在未知实验ID，将忽略: %s", missing)
    if not selected_specs:
        raise ValueError(f"selected_experiments={normalized} 未命中任何实验，请检查配置。")
    return selected_specs, normalized


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


def _render_output_section(
    rec: dict,
    project_root: Path,
    out_dir: Path,
    output_include_suffixes: List[str],
    output_preview_char_limit: int,
) -> str:
    exp_id = rec["exp_id"]
    lines = [f"## {exp_id}", ""]
    listed_paths: List[Path] = []
    for item in rec.get("expected_outputs", []):
        p = Path(item.get("path", ""))
        if p.exists() and p.suffix.lower() in set(output_include_suffixes):
            listed_paths.append(p)
    for rel in rec.get("new_output_files", []) or []:
        p = out_dir / rel
        if p.exists() and p.suffix.lower() in set(output_include_suffixes):
            listed_paths.append(p)
    if not listed_paths:
        listed_paths = _collect_experiment_output_files(out_dir, exp_id, output_include_suffixes)
    uniq_files = sorted(set(listed_paths))
    if not uniq_files:
        lines.extend(["(no output files found)", ""])
        return "\n".join(lines).rstrip() + "\n"
    for file_path in uniq_files:
        rel = file_path.relative_to(project_root)
        lines.extend(
            [
                f"### 源文件: `{rel.name}`",
                "",
                f"- 路径: `{rel}`",
                f"- 文件大小(bytes): `{file_path.stat().st_size}`",
                "",
                "```text",
                _read_text_preview(file_path, output_preview_char_limit).rstrip("\n"),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _parse_output_md_sections(text: str) -> Tuple[str, Dict[str, str], List[str]]:
    lines = text.splitlines()
    header_lines: List[str] = []
    sections: Dict[str, str] = {}
    order: List[str] = []
    idx = 0
    while idx < len(lines) and not lines[idx].startswith("## "):
        header_lines.append(lines[idx])
        idx += 1
    while idx < len(lines):
        line = lines[idx]
        if not line.startswith("## "):
            idx += 1
            continue
        exp_id = line[3:].strip()
        start = idx
        idx += 1
        while idx < len(lines) and not lines[idx].startswith("## "):
            idx += 1
        block = "\n".join(lines[start:idx]).rstrip() + "\n"
        sections[exp_id] = block
        order.append(exp_id)
    header = "\n".join(header_lines).rstrip() + "\n\n"
    return header, sections, order


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


def _clean_experiment_output_files_safe(
    out_dir: Path,
    exp_id: str,
    include_suffixes: List[str],
    protected_paths: Set[Path],
) -> List[Path]:
    prefixes = (f"{exp_id}_", f"{exp_id}.")
    suffixes = tuple(include_suffixes)
    removed: List[Path] = []
    if not out_dir.exists():
        return removed
    for item in sorted(out_dir.iterdir()):
        if not item.is_file():
            continue
        if item in protected_paths:
            LOGGER.debug("跳过受保护输入文件: %s", item)
            continue
        if not item.name.startswith(prefixes):
            continue
        if suffixes and item.suffix.lower() not in suffixes:
            continue
        item.unlink()
        removed.append(item)
    return removed


def run_all() -> int:
    all_specs = _load_specs()
    specs, selected_ids = _select_specs(all_specs)
    is_partial_run = len(specs) < len(all_specs)
    out_dir = outputs_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    run_all_cfg = _rebuttal_run_all_cfg()
    logs_dir = resolve_project_path(run_all_cfg.get("logs_dir", "rebuttal/outputs/run_logs"))
    logs_dir.mkdir(parents=True, exist_ok=True)
    combined_log_path = resolve_project_path(run_all_cfg.get("combined_log_path", str(logs_dir / "E0_run_all.log")))

    summary_md_path = resolve_project_path(run_all_cfg.get("summary_md", "rebuttal/outputs/E0_run_all_summary.md"))
    output_md_path = resolve_project_path(run_all_cfg.get("output_md", "rebuttal/outputs/E0_run_all_output.md"))
    result_jsonl_path = resolve_project_path(run_all_cfg.get("result_jsonl", "rebuttal/outputs/E0_run_all_results.jsonl"))
    output_preview_char_limit = int(run_all_cfg.get("output_preview_char_limit", 20000))
    output_include_suffixes = run_all_cfg.get("output_include_suffixes", [".csv", ".json", ".md"])
    if not isinstance(output_include_suffixes, list):
        output_include_suffixes = [".csv", ".json", ".md"]
    output_include_suffixes = [str(x).lower() for x in output_include_suffixes]
    clean_old_outputs = bool(run_all_cfg.get("clean_old_outputs", True))
    protect_output_inputs = bool(run_all_cfg.get("protect_output_inputs", True))

    project_root = resolve_project_path(".")

    LOGGER.debug("E0 run_all 启动，实验数量=%s, logs_dir=%s", len(specs), logs_dir)
    LOGGER.debug("E0 run_all selected_experiments=%s partial_run=%s", selected_ids or "(all)", is_partial_run)
    LOGGER.debug("SCOPE 子集目录=%s，存在=%s", scope_subsets_dir(), scope_subsets_dir().exists())
    LOGGER.debug("E0 run_all 合并日志路径=%s", combined_log_path)
    protected_paths = _collect_protected_output_inputs(specs, out_dir) if protect_output_inputs else set()
    LOGGER.debug(
        "E0 run_all 清理保护开关=%s, 受保护输入文件数量=%s",
        protect_output_inputs,
        len(protected_paths),
    )
    if protected_paths:
        LOGGER.debug("E0 run_all 受保护输入文件=%s", sorted(str(p) for p in protected_paths))

    before_all = _collect_files(out_dir)
    records: List[dict] = []
    failed = False
    result_jsonl_path.write_text("", encoding="utf-8")
    combined_log_path.parent.mkdir(parents=True, exist_ok=True)
    combined_log_path.write_text("# E0 Run All Combined Log\n\n", encoding="utf-8")
    heartbeat_seconds = int(run_all_cfg.get("subprocess_heartbeat_seconds", 20))
    if heartbeat_seconds <= 0:
        heartbeat_seconds = 20

    progress = tqdm(specs, desc="E0 run_all", unit="exp")
    for idx, spec in enumerate(progress, start=1):
        script_path = resolve_project_path(spec.script)

        inputs = _resolve_many(spec.inputs)
        inputs_status = [{"path": str(p), "exists": p.exists()} for p in inputs]

        before = _collect_files(out_dir)
        cmd = [sys.executable, str(script_path)]
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root)

        LOGGER.debug("开始执行 %s: script=%s", spec.exp_id, script_path)
        LOGGER.debug("%s 输入检查: %s", spec.exp_id, inputs_status)
        if clean_old_outputs and spec.exp_id != "E0":
            removed_files = _clean_experiment_output_files_safe(
                out_dir,
                spec.exp_id,
                output_include_suffixes,
                protected_paths,
            )
            LOGGER.debug("%s 预清理旧产物数量=%s", spec.exp_id, len(removed_files))

        start_ts = time.time()
        LOGGER.info("[%s/%s] 开始执行 %s -> %s", idx, len(specs), spec.exp_id, spec.script)
        proc = subprocess.Popen(cmd, cwd=project_root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        last_heartbeat = start_ts
        while proc.poll() is None:
            now = time.time()
            elapsed = int(now - start_ts)
            progress.set_postfix({"exp": spec.exp_id, "status": "running", "elapsed_s": elapsed})
            if now - last_heartbeat >= heartbeat_seconds:
                LOGGER.debug("实验 %s 仍在运行中，elapsed=%ss", spec.exp_id, elapsed)
                last_heartbeat = now
            time.sleep(1)
        stdout_text, stderr_text = proc.communicate()
        log_text = (stdout_text or "") + "\n\n# STDERR\n" + (stderr_text or "")
        with combined_log_path.open("a", encoding="utf-8") as f:
            f.write(f"## [{idx}/{len(specs)}] {spec.exp_id}\n")
            f.write(f"- script: {spec.script}\n")
            f.write(f"- cmd: {' '.join(cmd)}\n")
            f.write(f"- return_code: {proc.returncode}\n\n")
            f.write(log_text.rstrip() + "\n\n")
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
            "stdout_lines": len((stdout_text or "").splitlines()),
            "stderr_lines": len((stderr_text or "").splitlines()),
            "duration_seconds": round(time.time() - start_ts, 2),
            "log_file": str(combined_log_path.relative_to(project_root)),
            "io_logged": bool(stdout_text or stderr_text),
            "llm_signal_detected": llm_signal["detected"],
            "llm_signal_keywords": llm_signal["keywords"],
        }
        records.append(record)

        with result_jsonl_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        LOGGER.info(
            "[%s/%s] %s 完成: rc=%s, duration=%.2fs, new_files=%s",
            idx,
            len(specs),
            spec.exp_id,
            proc.returncode,
            float(record["duration_seconds"]),
            len(created),
        )
        LOGGER.debug("%s expected=%s", spec.exp_id, expected_status)
        progress.set_postfix({"exp": spec.exp_id, "rc": proc.returncode, "new": len(created), "sec": record["duration_seconds"]})

        if proc.returncode != 0:
            failed = True
            LOGGER.error("%s 执行失败，详见日志: %s", spec.exp_id, combined_log_path)
            break
    progress.close()

    after_all = _collect_files(out_dir)
    overall_new = sorted(after_all - before_all)

    lines = [
        "# E0 Run All Summary",
        "",
        f"- total_scripts: {len(all_specs)}",
        f"- selected_scripts: {len(specs)}",
        f"- selected_experiments: `{','.join(selected_ids) if selected_ids else 'ALL'}`",
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
            f"- duration_seconds: `{rec['duration_seconds']}`",
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

    default_header = "\n".join(
        [
            "# E0 Run All Output Details",
            "",
            f"- generated_by: `src/rebuttal/scripts/E0_run_all.py`",
            f"- output_preview_char_limit: `{output_preview_char_limit}`",
            "",
        ]
    ).rstrip() + "\n\n"
    if output_md_path.exists():
        existing_header, existing_sections, existing_order = _parse_output_md_sections(output_md_path.read_text(encoding="utf-8"))
        header = existing_header or default_header
    else:
        existing_sections, existing_order = {}, []
        header = default_header
    for rec in records:
        exp_id = rec["exp_id"]
        if exp_id == "E0":
            continue
        existing_sections[exp_id] = _render_output_section(rec, project_root, out_dir, output_include_suffixes, output_preview_char_limit)
        if exp_id not in existing_order:
            existing_order.append(exp_id)
    output_parts = [header.rstrip(), ""]
    for exp_id in existing_order:
        section_text = existing_sections.get(exp_id, "").rstrip()
        if section_text:
            output_parts.append(section_text)
            output_parts.append("")
    output_md_path.write_text("\n".join(output_parts).rstrip() + "\n", encoding="utf-8")
    LOGGER.debug("详细输出汇总已写入: %s", output_md_path)

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(run_all())
