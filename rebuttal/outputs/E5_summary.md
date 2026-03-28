# E5 Summary

## objective
- contamination/memorization probe

## methods compared
- llm_only,scion_lite

## dataset scope
- all SCOPE subsets

## exact files produced
- `E5_probe_results.csv`
- `E5_popular_vs_niche.csv`
- `E5_source_probe.csv`
- `E5_source_diagnostics.csv`
- `E5_cache_sanity_check.csv`
- `E5_manifest.json`

## key findings
- 九种输入条件输出完成
- probe cache key 显式包含 source/input_condition/corpus_hash/prompt_signature/split
- 新增 E5_cache_sanity_check.csv 检查跨条件泄漏
- popular/niche 改为 gap(real-name / real-shuffled) 统计
- 新增 source-level diagnostics（parse success/pred size/target size）

## Suggested rebuttal sentence
real_100pct 显著优于 name_only/shuffled，支持语料驱动归纳。
