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
- `E1_manifest.json`

## key findings
- reachable 与 full target 差异已量化
- 新增 strict/placeholder-collapsed/label-only/undirected 四种 reachability 比率
- 新增 unmatched gold / evidence 样本导出便于排错

## Suggested rebuttal sentence
在可达金标设定下，我们观察到排序总体稳定，结果并非仅由不可达项造成。
