# E8 Fix Report

## Root cause
- `E8_source_encoder_sensitivity.csv` 来自 post-hoc shift（按 source 加固定偏移），不是真实 per-source raw score 导出。

## Modified files
- `src/rebuttal/rebuttal_experiments.py`

## Validation
- source-level 表改为按 source+encoder 逐一重算 metrics（scoring from per-source prediction），不再使用统一平移。
- `E8_run_mode_report.json` 保留 provenance：noise/clustering/source=actual_rerun，metric=scoring_only，polysemy=curated set。