# E1 Fix Report

## Root cause
- `full_gold` 指标使用了过于乐观的 target-anchored 预测路径，且 reachable target 在 strict/placeholder 表示层混用，导致分数偏高、ratio 与 count 不自洽。
- `reachable_ratio_used_for_target` 之前与 used count/full count 不同层。
- placeholder-typed RE source 未执行分流 policy。

## Modified files
- `src/rebuttal/rebuttal_experiments.py`
- `config/config.yaml` (新增 `e1e2_anchor_from_target`)

## Validation
- ratio 自洽检查：`0 / 24` 行异常（期望 0）。
- placeholder source policy: `GIDS` / `New-York-Times-RE` 使用 `placeholder_collapsed_typed` 作为 used target。
- `full_gold` 与 submission anchor 对比（值 / Δanchor）：
  - manual: literal=0.5455 (-0.0492), fuzzy=0.8242 (-0.0232), continuous=0.7679 (+0.0168), graph=0.7308 (+0.0725)
  - text2onto: literal=0.6004 (-0.0221), fuzzy=0.8424 (-0.0264), continuous=0.7906 (+0.0186), graph=0.7582 (+0.0346)
  - llm_only: literal=0.6511 (-0.0083), fuzzy=0.8426 (-0.0826), continuous=0.8080 (-0.0212), graph=0.7848 (+0.0517)
  - scion_lite: literal=0.7162 (-0.0008), fuzzy=0.8910 (-0.0722), continuous=0.8520 (-0.0369), graph=0.8278 (+0.0390)

## Notes
- evaluator signature 保持 `cabc45613b834dee`，frozen hash 保持 `26bad3bb3f37a484`。