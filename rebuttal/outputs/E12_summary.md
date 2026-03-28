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
- `E12_manifest.json`

## key findings
- 所有主输出维持 pilot_only_flag，并新增 not_comparable_to_core_benchmark/scope_note
- diagnostics 新增 reachable_link_ratio，显式区分可达覆盖与预测质量
- 新增 E12_scope_note.json 与 caveat，强调仅回答 representational feasibility

## Suggested rebuttal sentence
该实验仅为 representational feasibility pilot，不构成主benchmark扩展结论。
