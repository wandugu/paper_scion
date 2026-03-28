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
- `E3_sourcewise_comparison.csv`
- `E3_cache_diagnostics.csv`
- `E3_manifest.json`

## key findings
- E3 主表固定使用 full_normalized_gold（submission frozen target）
- cache key 显式包含 source/method/target_variant/evaluation_protocol/frozen_hash
- sourcewise comparison 来自 E3 本次 rerun（不复用 E1/E2 输出）

## Suggested rebuttal sentence
在 submission 对齐口径下，SCION-lite 相对 ETA 仍保持稳定优势。
