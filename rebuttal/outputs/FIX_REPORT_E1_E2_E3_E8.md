# FIX_REPORT_E1_E2_E3_E8

## 1) Root cause by experiment

### E1
- 根因 1：`reachable` 评测路径里把 prediction 又按 `tgt_edges` 做了二次过滤，导致 precision 侧几乎被“裁剪到 target 内”，出现 `literal_p/fuzzy_p/continuous_p` 异常接近或等于 1.0。
- 根因 2：summary 里写了 placeholder 仅 debug，但主输出 `reachable_mode_used_for_target` 仍可能是 placeholder mode，信息口径冲突。
- 修复：reachable 仅过滤 gold，不再裁剪 prediction；新增 strict vs placeholder-collapsed 敏感性输出，明确 placeholder 仅用于 reachability matching 判定。

### E2
- 根因：`typed_unnormalized` 与 `full_normalized_gold` 都来自同一套 canonicalized source cache，导致 target variant 没真正分离。
- 修复：E2 cache 分离 `gold_raw/pred_raw` 与 `gold/pred`；`typed_unnormalized`/`label_only_projection` 基于 raw artifact，`full_normalized_gold`/`reachable_normalized_gold` 基于 frozen canonical target。

### E3
- 根因：E3 主评测未显式锁定 target variant，也缺少可审计的 cache key 维度；sourcewise/result 复核不充分。
- 修复：E3 强制 `full_normalized_gold`；主表、sourcewise 都基于 E3 rerun 的 submission-aligned rows；新增 `E3_cache_diagnostics.csv`，cache key 显式包含 `target_variant/evaluation_protocol/frozen_hash/method/source`。

### E8
- 根因 1：原表诊断字段不足（缺 continuous_f1、pred_item_count、P/R 分解），无法解释 soft metric 行为。
- 根因 2：缺少 noise/encoder cache key 显式隔离审计。
- 根因 3：zero-noise 与 base 对齐逻辑依赖外部覆盖写值，存在可解释性风险。
- 修复：
  - 扩展 `E8_noise_robustness.csv` 诊断列。
  - 新增 `E8_cache_sanity.csv`，覆盖 noise/encoder 维度。
  - zero-noise 改为真实重算一致性校验（不手工改数值），并在运行时做严格断言。

## 2) Files changed

### Code / Config
- `src/rebuttal/rebuttal_experiments.py`
- `src/rebuttal/configs/E1_reachable_eval.yaml`
- `src/rebuttal/configs/E2_normalization_sensitivity.yaml`
- `src/rebuttal/configs/E3_eta_baseline.yaml`
- `src/rebuttal/configs/E8_noise_polysemy_encoder.yaml`
- `src/rebuttal/scripts/E3_run.py` (新增)
- `src/rebuttal/scripts/E8_run.py` (新增)

### Tests
- `tests/rebuttal/test_rebuttal_e1_e2_e3_e8.py` (新增)

### Outputs regenerated
- `rebuttal/outputs/E1_*`
- `rebuttal/outputs/E2_*`
- `rebuttal/outputs/E3_*`
- `rebuttal/outputs/E8_*`
- 本报告：`rebuttal/outputs/FIX_REPORT_E1_E2_E3_E8.md`

## 3) Before/after sanity checks

- E1：reachable precision 不再全 1.0（见 Key numerical checks）。
- E2：`typed_unnormalized` 与 `full_normalized_gold` 已出现可见差异。
- E3：主表固定 `full_normalized_gold`，不再镜像 reachable 量级。
- E8：zero-noise 与 base 对齐；noise 表新增 continuous/pred size/P-R 诊断列。

## 4) Key numerical checks

- E1 full_gold totals 仍为 submission frozen artifact：`ALL=1597, RE=558, EE=1039`（来自 `E1_alignment_check.json`）。
- E1 reachable precision 已脱离全 1.0：
  - `literal_p` 范围 `[0.7391, 0.8698]`
  - `fuzzy_p` 范围 `[0.9645, 0.9817]`
  - `continuous_p` 范围 `[0.9343, 0.9522]`
- E2 full_normalized_gold vs E1 full_gold：
  - 重叠方法 (`llm_only/eta/scion_lite`) 的连续指标与 E1 full_gold 对齐；
  - 且 `typed_unnormalized` 相对 `full_normalized_gold` 出现非零差异（例如 `llm_only +0.0071`, `eta +0.0072`）。
- E3 overlap methods vs E1/E2 full_gold：
  - `continuous_f1` 差值为 0（到打印精度）；
  - `graph_f1` 仅在浮点微差量级（约 `1e-4`）。
- E8 zero-noise consistency：运行时一致性断言通过（`literal/fuzzy/continuous/graph` diff 全为 0 within tol）。

## 5) Remaining caveats

- E8 轻度 noise 下若仍出现 soft metric 局部上升，当前版本保留该真实 rerun 结果，不做手工“压回”；请结合新增诊断列（`pred_item_count`, `literal_p/r`, `graph_p/r`, `continuous_f1`）解释是否为 recall 增益与预测规模变化共同作用。
- E1 某些 placeholder-only source 仍可能在 reachable 判定上触发 `placeholder_collapsed_typed`；该模式仅用于 reachability matching 判定，不用于重构主 target 图，且已在 `E1_reachability_mode_sensitivity.csv` 明示。

## 6) Acceptance checklist (self-check)

### [E1]
- [x] reachable_gold 下 precision 不再全部等于 1.0
- [x] full_gold totals 仍对齐 frozen artifact (1597/558/1039)
- [x] summary 与实际 target mode 不再矛盾（主表 + sensitivity 明示）

### [E2]
- [x] typed_unnormalized 与 full_normalized_gold 出现可见差异
- [x] full_normalized_gold 与 E1 full_gold 对齐
- [x] manual completion audit 保留且标注为 representation gap analysis

### [E3]
- [x] E3 主表确认使用 full_normalized_gold
- [x] llm_only / eta / scion_lite 不再异常贴近 reachable
- [x] cache key 已包含 target_variant / evaluation_protocol / frozen hash（并含 method/source）

### [E8]
- [x] zero-noise 行与 base subset_8 对齐
- [x] noise 表新增 continuous_f1、pred_item_count、precision/recall 诊断
- [x] encoder sensitivity cache key 隔离（见 cache sanity 文件）
- [x] 对 soft metric 变化给出诊断口径，不做强行改数值

## 7) Canonical files to use

本次修复后请以以下文件为准：
- E1: `E1_main_metrics.csv`, `E1_recall_breakdown.csv`, `E1_source_reachable_ratio.csv`, `E1_reachability_mode_sensitivity.csv`
- E2: `E2_target_variant_metrics.csv`, `E2_rank_stability.csv`, `E2_manual_completion_audit.csv`
- E3: `E3_main_baseline_comparison.csv`, `E3_sourcewise_comparison.csv`, `E3_cache_diagnostics.csv`
- E8: `E8_noise_robustness.csv`, `E8_clustering_encoder_sensitivity.csv`, `E8_metric_encoder_sensitivity.csv`, `E8_source_encoder_sensitivity.csv`, `E8_cache_sanity.csv`
