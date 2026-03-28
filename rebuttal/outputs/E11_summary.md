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
- `E11_manifest.json`

## key findings
- 主表仅聚合高价值领域 biomedical/finance；cybersecurity/general 仅保留 source-level diagnostics
- 主表新增 slice_only_flag/not_full_benchmark/benchmark_scope/source_list/source_count_checked guardrail 字段
- 新增 E11_scope_note.json 明确这是 hoTR Q3 的 slice-only 补充，不等同 full-suite 结论

## Suggested rebuttal sentence
这是高价值领域切片补充实验（hoTR Q3），不等同于全 benchmark 主结果。
