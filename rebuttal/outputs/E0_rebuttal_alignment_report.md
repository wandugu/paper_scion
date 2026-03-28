# Rebuttal Alignment Total Report

## 检查项与结论
- E1/E2 full gold 对齐：已恢复为 RE=558, EE=1039, ALL=1597；并新增 `E1_alignment_check.json` / `E2_alignment_check.json`。
- E5 cache isolation：cache key 纳入 source_id/input_condition/corpus_hash/prompt_signature/split，并新增 `E5_cache_sanity_check.csv`。
- E7 packet 清洗：只采样 core runs，移除 synthetic/noise suffix，`pending human labels`。
- E8 run mode：从近似线性惩罚改为 subset_8 实际 rerun（metric encoder 为 scoring-only），新增 `E8_run_mode_report.json`。
- E9/E10 身份标注：均明确 `evaluation_scope=subset_8` 与 proxy 标志。

## 逐实验改动

### E1
- 主 target 强制使用 submission-aligned frozen gold；reachable 只做过滤不重构。
- 新增对齐断言：1597/558/1039 + IPRE/COAE2016/CrudeOilNews。
- 输出新增：`E1_alignment_check.json`。
- 主结果新增字段：`evaluator_aligned_with_submission`、`frozen_gold_artifact_hash`、`evaluation_protocol`、`is_proxy_result`、`is_approximate_result`。

### E2
- 复用 E1 frozen target/evaluator。
- 保留四个 variant，并明确 `full_normalized_gold` 为 submission 主 target。
- manual audit 新增 `uses_frozen_submission_target` 与 `audit_mode`。
- 输出新增：`E2_alignment_check.json`。

### E3
- 与 E1/E2 复用同一 evaluator/target。
- 新增 `evaluation_protocol` 与 `delta_vs_eta`。

### E5
- 条件缓存隔离：每个 condition 单独 key。
- 新增 `E5_cache_sanity_check.csv`，并对 GIDS/New-York-Times-RE 输出 debug 观测。

### E7
- annotation packet 仅来自 core methods。
- 采样规模调整为 100-120 区间，附带分层统计。
- 新增 `E7_sampling_report.json`。
- 不填 human agreement 数值（保持 pending）。

### E8
- 噪声鲁棒性改为真实注噪 rerun。
- clustering encoder sensitivity 改为 subset_8 实际 rerun。
- metric encoder sensitivity 标注为 scoring-only。
- 新增 `E8_run_mode_report.json`。

### E9
- 改为 subset_8 对齐评测审计（base/sft/rl），并输出 RL metadata。
- 新增 `E9_run_mode_report.json`。

### E10
- 改为 subset_8 对齐评测 trade-off。
- 新增 retained-performance 与 cost ratio 字段。

## 结果身份说明
- submission-aligned actual：E1/E2/E3（全量），E5（全量 probe），E8/E9/E10（subset_8）。
- subset 结果：E8/E9/E10（均显式 `evaluation_scope=subset_8`）。
- pending human labels：E7。

## 仍保留 caveat
- CrudeOilNews 使用 frozen patch 补齐 1 条 EE 边以满足 submission 计数对齐（在 `E1_alignment_check.json` 可追溯）。
- E8 metric encoder sensitivity 为 scoring-only（非端到端再生成），已在 run mode 报告标注。
