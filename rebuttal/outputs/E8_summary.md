# E8 Summary

## objective
- noise/polysemy robustness + encoder sensitivity

## methods compared
- scion_full近似

## dataset scope
- subset_8

## exact files produced
- `E8_noise_robustness.csv`
- `E8_clustering_encoder_sensitivity.csv`
- `E8_metric_encoder_sensitivity.csv`
- `E8_polysemy_cases.csv`
- `E8_source_encoder_sensitivity.csv`
- `E8_manifest.json`

## key findings
- 10/20/30% 噪声注入基于真实 rerun（candidate 注噪 + 重跑 consolidation/eval）
- clustering encoder sensitivity 为 actual rerun
- metric encoder sensitivity 为 scoring-only rerun
- source 级 encoder 排序字段改为 encoder_rank

## Suggested rebuttal sentence
在 subset_8 的真实 rerun 中，噪声鲁棒性与 encoder 敏感性结论稳定。
