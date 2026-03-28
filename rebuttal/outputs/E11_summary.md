# E11 Summary

## objective
- domain-specific schema engineer

## methods compared
- general vs domain-specific

## dataset scope
- high-value domains slice (biomedical/finance) + diagnostic source-level domains

## exact files produced
- `E11_domain_specific_main.csv`
- `E11_source_domain_specific.csv`
- `E11_domain_mapping_used.json`
- `E11_manifest.json`

## key findings
- 主表仅聚合高价值领域 biomedical/finance
- domain mapping 改为显式输出 E11_domain_mapping_used.json
- 主表新增 source_count/cost_ratio/aggregation_mode，语义与 reviewer 问题对齐

## Suggested rebuttal sentence
这是高价值领域切片补充实验，不等同于全 benchmark 主结果。
