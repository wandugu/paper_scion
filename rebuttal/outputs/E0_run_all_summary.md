# E0 Run All Summary

- total_scripts: 14
- selected_scripts: 3
- selected_experiments: `E1,E7,E7_SCORE`
- executed_scripts: 3
- failed: False
- outputs_dir: `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs`
- result_jsonl: `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/E0_run_all_results.jsonl`
- output_md: `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/E0_run_all_output.md`
- logs_dir: `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/run_logs`

## Overall New Output Files
- `E7_v2_PENDING.md`
- `E7_v2_annotation_guidelines.md`
- `E7_v2_annotation_packet.csv`
- `E7_v2_sampling_report.json`

## E1
- script: `src/rebuttal/scripts/E1_run_reachable_eval.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `41`
- duration_seconds: `152.06`
- log_file: `rebuttal/outputs/run_logs/E0_run_all.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/home/iie4bu/hmb/code/hmb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/E1_main_metrics.csv` (exists=True)
- new_output_files:
  - (none)

## E7
- script: `src/rebuttal/scripts/E7_v2_prepare_annotation.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `3`
- duration_seconds: `26.02`
- log_file: `rebuttal/outputs/run_logs/E0_run_all.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/home/iie4bu/hmb/code/hmb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/E7_v2_annotation_packet.csv` (exists=True)
- new_output_files:
  - `rebuttal/outputs/E7_v2_PENDING.md`
  - `rebuttal/outputs/E7_v2_annotation_guidelines.md`
  - `rebuttal/outputs/E7_v2_annotation_packet.csv`
  - `rebuttal/outputs/E7_v2_sampling_report.json`

## E7_SCORE
- script: `src/rebuttal/scripts/E7_v2_score.py`
- return_code: `0`
- io_logged(stdout/stderr): `False`
- stdout_lines: `0`, stderr_lines: `0`
- duration_seconds: `1.01`
- log_file: `rebuttal/outputs/run_logs/E0_run_all.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/E7_v2_template_1.csv` (exists=True)
  - `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/E7_v2_template_2.csv` (exists=True)
- expected_outputs:
  - `/home/iie4bu/hmb/code/hmb_6_graph_maker/rebuttal/outputs/E7_v2_score_bin_calibration.csv` (exists=False)
- new_output_files:
  - (none)
