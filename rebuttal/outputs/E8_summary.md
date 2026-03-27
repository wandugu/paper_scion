# E8 Summary

## objective
- noise/polysemy robustness + encoder sensitivity

## methods compared
- scion_full近似

## dataset scope
- all SCOPE subsets

## exact files produced
- `E8_noise_robustness.csv`
- `E8_clustering_encoder_sensitivity.csv`
- `E8_metric_encoder_sensitivity.csv`
- `E8_polysemy_cases.csv`
- `E8_source_encoder_sensitivity.csv`
- `E8_manifest.json`

## key findings
- 10/20/30% 噪声注入结果已导出
- noise=0 基线与 E1_main 对齐校验通过
- encoder sensitivity 拆分为 clustering 与 metric 两张表
- source 级 encoder 排序字段改为 encoder_rank

## Suggested rebuttal sentence
10%-30% 噪声下性能呈平稳下降，未出现崩溃。
