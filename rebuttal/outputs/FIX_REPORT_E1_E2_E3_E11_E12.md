# FIX REPORT: E1 / E2 / E3 / E11 / E12

## Scope & constraints
- 仅修改并重跑 E1、E2、E3、E11、E12。
- 未修改 E4–E10 及论文正文。
- shared util 未做结构性改动；仅在 `src/rebuttal/rebuttal_experiments.py` 内新增最小闭包 sanity/assert/trace 字段逻辑。

---

## E1 reachable target + recall decomposition
### 改动
- 新增 `result_mode`（`submission_replay` / `rerun_only`）与 `E1_submission_replay_comparison.csv`。
- 新增 `E1_consistency_report.json`（alignment、placeholder matching、full/reachable delta、mode）。
- 主表增加 `evaluator_hash` 与 `result_mode` 字段。
- 新增 sourcewise->macro 自动断言（full/reachable continuous_f1）。

### 发现的风险/bug
- 仓库内未检测到可用 submission-time prediction artifacts，无法完整 replay。

### 安全降级
- 当前明确标记 `result_mode=rerun_only`；full_gold 作为 rerun diagnostics，不伪装为 submission replay。

### 本次重跑输出
- `E1_main_metrics.csv`
- `E1_recall_breakdown.csv`
- `E1_source_reachable_ratio.csv`
- `E1_reachability_mode_sensitivity.csv`
- `E1_reachability_debug_samples.csv`
- `E1_alignment_check.json`
- `E1_consistency_report.json`
- `E1_submission_replay_comparison.csv`
- `E1_summary.md`

### Sanity checks
- alignment_check 通过（submission frozen gold 对齐）。
- sourcewise->macro 一致性断言通过。

---

## E2 normalization sensitivity + manual/official gap audit
### 改动
- 重写 `E2_manual_completion_audit.csv` 生成路径：四阶段均从 manual 的 stage-specific target/pred 计算，不再混入 method 行。
- 新增 `E2_manual_stage_artifacts.csv`（source/stage/artifact_hash/protocol/frozen_hash）。
- 新增 `E2_manual_audit_sanity_report.json`（stage 来源、统计、 accidental equality 检查）。
- 主表增加 `evaluator_hash` 字段。

### 发现的风险/bug
- 旧逻辑存在“manual stage 分数借用其他方法输出”的数据流风险（merge/pivot 维度串位风险）。

### 本次重跑输出
- `E2_target_variant_metrics.csv`
- `E2_rank_stability.csv`
- `E2_manual_completion_audit.csv`
- `E2_manual_stage_artifacts.csv`
- `E2_manual_audit_sanity_report.json`
- `E2_mismatch_cases.csv`
- `E2_alignment_check.json`
- `E2_summary.md`

### Sanity checks
- accidental equality 检查通过（stage 均值未与 text2onto/llm_only/scion_lite 宏均值异常重合）。
- 每个 source 四个 stage artifact 完整存在。

---

## E3 ETA baseline
### 改动
- 主表补齐 `evaluator_signature/evaluator_hash/evaluation_protocol/frozen_gold_artifact_hash/graph_result_mode`。
- `E3_error_profile.csv` 改为 method-specific 统计；新增 `E3_error_profile_counts.csv`（numerator/denominator）。
- 新增 `E3_metric_consistency_check.json`，对比 E3 与 E2 共享方法/target 的 literal/continuous/graph。
- 新增 sourcewise->main 聚合断言（eta/scion_lite literal/graph）。

### 发现的风险/bug
- 旧 error profile 可能出现 method 维度丢失导致多个方法 rate 异常接近。

### 本次重跑输出
- `E3_main_baseline_comparison.csv`
- `E3_error_profile.csv`
- `E3_error_profile_counts.csv`
- `E3_sourcewise_comparison.csv`
- `E3_cache_diagnostics.csv`
- `E3_metric_consistency_check.json`
- `E3_summary.md`

### Sanity checks
- sourcewise->macro 聚合断言通过。
- E3 与 E2 跨实验一致性检查已输出并可追踪。

---

## E11 domain-specific schema engineer
### 改动
- 新增 `E11_domain_mapping_used.json`（source->domain、主表聚合 domain、diagnostic-only domain）。
- 主表仅聚合 `biomedical/finance`，并增加 `source_count`。
- 主表补齐字段：`domain,source_count,general_graph_f1,domain_specific_graph_f1,delta_graph_f1,general_downstream_f1,domain_specific_downstream_f1,cost_ratio,aggregation_mode` + evaluator trace。
- summary 明确这是 high-value domain slice 补充实验。

### 本次重跑输出
- `E11_domain_specific_main.csv`
- `E11_source_domain_specific.csv`
- `E11_domain_mapping_used.json`
- `E11_summary.md`

### Sanity checks
- 主表 domain 与 mapping 配置一致。
- diagnostic-only domain（general/cybersecurity）未混入主表聚合。

---

## E12 inter-event relation pilot
### 改动
- 新增 `E12_inter_event_diagnostics.csv`（gold/reachable/pred/correct counts + link inventory + mode + pilot flag）。
- 主表新增 `pilot_only_flag/evaluation_scope/result_interpretation` 与 evaluator trace。
- 案例表新增 `error_category/ambiguity_type`。
- 新增 `E12_PILOT_CAVEAT.md` 明确 pilot 边界。

### 本次重跑输出
- `E12_inter_event_main.csv`
- `E12_inter_event_diagnostics.csv`
- `E12_inter_event_cases.csv`
- `E12_PILOT_CAVEAT.md`
- `E12_summary.md`

### Sanity checks
- pilot-only 字段已在主表/诊断表统一标注。
- caveat 文件已生成，避免误读为核心 benchmark 结论。

---

## Completion checklist
- E1 区分 submission replay vs rerun：**是**（当前为 `rerun_only`）。
- E2 manual audit 修复：**是**。
- E3 graph 与 error profile 修复：**是（含一致性检查与计数级审计）**。
- E11 domain aggregation 统一：**是**。
- E12 pilot caveat 增加：**是**。
