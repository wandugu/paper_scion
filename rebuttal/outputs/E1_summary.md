# E1 Summary

## objective
- reachable target + recall decomposition

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion,scion_full,scion_rl

## dataset scope
- all SCOPE subsets

## exact files produced
- `E1_main_metrics.csv`
- `E1_recall_breakdown.csv`
- `E1_source_reachable_ratio.csv`
- `E1_reachability_debug_samples.csv`
- `E1_alignment_check.json`
- `E1_manifest.json`

## key findings
- full_gold 使用 submission frozen artifact，并通过 1597/558/1039 对齐断言
- reachable_gold 仅在 frozen full_gold 上做可达性过滤，不重新构图
- placeholder/label-only/undirected 仅保留在 debug 字段

## Suggested rebuttal sentence
在 submission 对齐口径下，可达 target 的影响被透明量化。
