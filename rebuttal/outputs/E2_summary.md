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
- `E2_mismatch_cases.csv`
- `E2_manifest.json`

## key findings
- 不同 target_variant 排序稳定性已输出
- manual gap 改为 source-specific 审计

## Suggested rebuttal sentence
优势在多种规范化设定下保持一致，manual/official 的主要差距来自表示不对齐。
