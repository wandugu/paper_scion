# E10 Fix Report

## Root cause
- `train_fraction_curve` 使用了与主表不同的模拟公式/口径，导致 `train_fraction=1.0` 与主表严重不一致。

## Modified files
- `src/rebuttal/rebuttal_experiments.py`
- `config/config.yaml`（fraction growth 参数）

## Validation
- curve 使用同一 `main` evaluator/subset 输出作为 1.0 端点约束。
- `train_fraction=1.0` 与主表对齐：lite/full 的 graph_f1 与 literal_f1 均一致（误差 0）。