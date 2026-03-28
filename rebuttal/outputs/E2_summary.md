# E2 Summary

## objective
- normalization sensitivity and manual/official gap audit

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion,scion_full,scion_rl

## dataset scope
- all SCOPE subsets

## exact files produced
- `E2_target_variant_metrics.csv`
- `E2_rank_stability.csv`
- `E2_manual_completion_audit.csv`
- `E2_manual_stage_artifacts.csv`
- `E2_manual_audit_sanity_report.json`
- `E2_mismatch_cases.csv`
- `E2_alignment_check.json`
- `E2_manifest.json`

## key findings
- full_normalized_gold 与 E1 frozen full_gold 完全对齐
- manual completion audit 四阶段均来自 manual stage-specific artifacts（不再借用其他 method）
- 新增 accidental equality 检查，防止 stage 均值误贴其他方法
- rank stability 建立在修复后的 target_variant 指标上

## Suggested rebuttal sentence
排序稳定性在 submission 对齐 target 下依然成立。
