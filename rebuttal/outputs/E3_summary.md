# E3 Summary

## objective
- ETA baseline

## methods compared
- llm_only,eta,scion_lite

## dataset scope
- all SCOPE subsets

## exact files produced
- `E3_main_baseline_comparison.csv`
- `E3_error_profile.csv`
- `E3_error_profile_counts.csv`
- `E3_sourcewise_comparison.csv`
- `E3_cache_diagnostics.csv`
- `E3_metric_consistency_check.json`
- `E3_manifest.json`

## key findings
- E3 主表固定使用 full_normalized_gold（submission frozen target）
- cache key 显式包含 source/method/target_variant/evaluation_protocol/frozen_hash
- error profile 改为 method-specific counts+rate，不再共享聚合结果
- 新增 sourcewise->macro 自动断言

## Suggested rebuttal sentence
在 submission 对齐口径下，SCION-lite 相对 ETA 仍保持稳定优势。
