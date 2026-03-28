# E9 Summary

## objective
- SFT vs RL + reward ablation

## methods compared
- base,sft_only,rl_full

## dataset scope
- actual subset_8 audit

## exact files produced
- `E9_sft_vs_rl.csv`
- `E9_reward_ablation.csv`
- `E9_training_stability.csv`
- `E9_manifest.json`

## key findings
- SFT/RL 指标在 submission-aligned evaluator 下重算
- 奖励项消融按 term 差异化输出
- 训练稳定性表补齐算法 metadata

## Suggested rebuttal sentence
在 held-out subset_8 上，RL 版本在结构一致性与图指标更优。
