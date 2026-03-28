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
- `E3_manifest.json`

## key findings
- E3 与 E1/E2 复用 submission-aligned frozen gold + evaluator
- 新增 delta_vs_eta 直接反映相对提升
- 成本列显式标注为 suite_total_*

## Suggested rebuttal sentence
在 submission 对齐口径下，SCION-lite 相对 ETA 仍保持稳定优势。
