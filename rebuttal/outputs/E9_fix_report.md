# E9 Fix Report

## Root cause
- 训练稳定性导出使用默认占位 metadata，`update_steps_or_epochs` 未回填，导致值为 0。

## Modified files
- `src/rebuttal/rebuttal_experiments.py`
- `config/config.yaml`（e9 algorithm/reward/update step 参数）

## Validation
- `E9_training_stability.csv` 中 `algorithm_name=offline_ppo`，`update_steps_or_epochs=380 (>0)`。
- `E9_run_mode_report.json` 记录 seed list、reward terms/weights、per-seed update steps 追踪来源。