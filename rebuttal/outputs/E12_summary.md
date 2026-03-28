# E12 Summary

## objective
- inter-event relation pilot

## methods compared
- pilot schema extension

## dataset scope
- 1-2 EE datasets

## exact files produced
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_PILOT_CAVEAT.md`
- `E12_manifest.json`

## key findings
- 新增 pilot 诊断表（count + inventory + mode）避免误读
- 主表新增 pilot_only_flag/evaluation_scope/result_interpretation
- 案例表新增 error_category/ambiguity_type

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
