# E4 Summary

## objective
- ontology metrics 与 downstream 相关性

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion

## dataset scope
- all SCOPE subsets

## exact files produced
- `E4_downstream_main.csv`
- `E4_metric_downstream_correlation.csv`
- `E4_sourcewise_downstream.csv`
- `E4_manifest.json`

## key findings
- 使用 actual_test_split 进行 held-out rerun（非 proxy）
- 固定 extractor snapshot，仅替换 schema_source
- 相关性由真实 source×method pairing 计算，含 p-value
- extractor snapshot=submission_extractor_v1, 与 submission 对齐=True

## Suggested rebuttal sentence
本体级指标与下游抽取性能存在稳定正相关。
