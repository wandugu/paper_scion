# E7 Summary

## objective
- metric-human calibration scoring

## methods compared
- score threshold vs adjudicated labels

## dataset scope
- all E7 annotation pairs

## exact files produced
- `E7_annotation_template.csv`
- `E7_metric_human_agreement.csv`
- `E7_annotation_summary.csv`
- `E7_score_bin_calibration.csv`
- `E7_sampling_report.json`
- `E7_manifest.json`

## key findings
- 读取人工标注文件 rebuttal/outputs/E7_annotation_template_1.csv,rebuttal/outputs/E7_annotation_template_2.csv
- 有效 adjudicated 数量 235
- annotator agreement=0.9362, human_accept_rate=0.0468

## Suggested rebuttal sentence
我们已基于双人标注文件完成 E7 打分并产出可复核指标文件。
