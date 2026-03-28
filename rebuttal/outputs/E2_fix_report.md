# E2 Fix Report

## Root cause
- `full_normalized_gold` 未复用 E1 的 submission-aligned target/prediction 路径，导致指标整体偏高。
- rank stability 依赖旧分数，需要随修复后重算。

## Modified files
- `src/rebuttal/rebuttal_experiments.py`
- `config/config.yaml` (复用 `e1e2_anchor_from_target`)

## Validation
- `manual_completion_audit` 继续标注 `representation_gap_analysis_only`，未作为 official baseline。
- `full_normalized_gold` 与 submission anchor 对比（值 / Δanchor）：
  - manual: literal=0.5456 (-0.0491), fuzzy=0.8336 (-0.0138), continuous=0.7697 (+0.0186), graph=0.7325 (+0.0742)
  - text2onto: literal=0.6003 (-0.0222), fuzzy=0.8383 (-0.0305), continuous=0.7893 (+0.0173), graph=0.7608 (+0.0372)
  - llm_only: literal=0.6514 (-0.0080), fuzzy=0.8446 (-0.0806), continuous=0.8083 (-0.0209), graph=0.7850 (+0.0519)
  - scion_lite: literal=0.7162 (-0.0008), fuzzy=0.8785 (-0.0847), continuous=0.8517 (-0.0372), graph=0.8307 (+0.0419)

## Notes
- 排名稳定性文件已基于修复后的 `E2_target_variant_metrics.csv` 重新生成。