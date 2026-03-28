# E7 Summary

## objective
- human calibration package

## methods compared
- manual,text2onto,llm_only,eta,scion_lite,scion_fusion,scion_full,scion_rl

## dataset scope
- all SCOPE subsets sampled (core runs only)

## exact files produced
- `E7_annotation_packet.csv`
- `E7_annotation_guidelines.md`
- `E7_annotation_template.csv`
- `E7_metric_human_agreement.csv`
- `E7_annotation_summary.csv`
- `E7_score_bin_calibration.csv`
- `E7_sampling_report.json`
- `E7_STATUS_NOT_RUN.md`
- `E7_manifest.json`

## key findings
- 生成 120 条待标注样本
- 标注包仅来自 core runs，不含 noise/synthetic suffix
- pending human labels，未伪造人工标签

## Suggested rebuttal sentence
我们公开了可复现的人类校准包，当前版本仍 pending human labels。
