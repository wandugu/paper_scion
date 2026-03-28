# E6 Summary

## objective
- fusion baseline comparison

## methods compared
- agreementmakerlight_oaei,logmap_oaei,llm_pairwise_matcher,scion_fusion

## dataset scope
- fixed candidate budget

## exact files produced
- `E6_fusion_main.csv`
- `E6_mapping_type_distribution.csv`
- `E6_mapping_audit.csv`
- `E6_manifest.json`

## key findings
- 新增具名 OAEI matcher（AML/LogMap）对照
- 所有方法统一 5k candidate-pair 预算
- mapping type distribution 按方法独立统计

## Suggested rebuttal sentence
在同预算下，SCION fusion 具备更好的精度-冲突率折中，并优于具名 OAEI 匹配器回放基线。
