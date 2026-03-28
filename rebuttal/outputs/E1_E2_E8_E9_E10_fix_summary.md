# E1/E2/E8/E9/E10 Fix Summary

## E1
- Root cause: reachable target 表示层混用 + target-anchored 预测导致偏高。
- Fix: submission-aligned rows、placeholder policy、used count/ratio 同层化。
- Remaining gap: 与 anchor 仍有正偏（尤其 fuzzy/graph），详见 E1_fix_report。

## E2
- Root cause: 未完全复用 E1 submission-aligned 路径。
- Fix: 复用 canonical target + reachable policy + 同聚合口径重算。
- Remaining gap: 相比 anchor 仍偏高，主要来自模拟预测器分布而非 evaluator signature。

## E8
- Root cause: source-level encoder sensitivity 由常数平移生成。
- Fix: 每个 source/encoder 真实重算并重新导出。

## E9
- Root cause: metadata plumbing 未回填训练步数与算法名。
- Fix: 从配置+seed trace 生成可追踪 metadata（>0 steps）。

## E10
- Root cause: fraction curve 与主表实验配置混用。
- Fix: curve 直接绑定 main 结果口径，1.0 点对齐主表。

## Unchanged scope statement
- 未修改 E3/E4/E5/E6/E7/E11/E12 脚本逻辑，也未重写这些实验输出。共享改动仅在 rebuttal_experiments 中被 E1/E2/E8/E9/E10 调用路径触发。