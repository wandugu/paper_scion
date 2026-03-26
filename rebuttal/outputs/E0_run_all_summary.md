# E0 Run All Summary

- total_scripts: 13
- executed_scripts: 13
- failed: False
- outputs_dir: `/workspace/gxb_6_graph_maker/rebuttal/outputs`
- result_jsonl: `/workspace/gxb_6_graph_maker/rebuttal/outputs/E0_run_all_results.jsonl`
- output_md: `/workspace/gxb_6_graph_maker/rebuttal/outputs/E0_run_all_output.md`
- logs_dir: `/workspace/gxb_6_graph_maker/rebuttal/outputs/run_logs`

## Overall New Output Files
- (none)

## E0
- script: `src/rebuttal/scripts/E0_phase0_setup.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `2`
- log_file: `rebuttal/outputs/run_logs/E0.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E0_environment.json` (exists=True)
- new_output_files:
  - (none)

## E1
- script: `src/rebuttal/scripts/E1_run_reachable_eval.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `4`
- log_file: `rebuttal/outputs/run_logs/E1.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E1_main_metrics.csv` (exists=True)
- new_output_files:
  - (none)

## E2
- script: `src/rebuttal/scripts/E2_run_normalization_sensitivity.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `4`
- log_file: `rebuttal/outputs/run_logs/E2.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E2_target_variant_metrics.csv` (exists=True)
- new_output_files:
  - (none)

## E3
- script: `src/rebuttal/scripts/E3_run_eta_baseline.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `3`
- log_file: `rebuttal/outputs/run_logs/E3.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E3_main_baseline_comparison.csv` (exists=True)
- new_output_files:
  - (none)

## E4
- script: `src/rebuttal/scripts/E4_run_downstream_eval.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `2`
- log_file: `rebuttal/outputs/run_logs/E4.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E4_downstream_main.csv` (exists=True)
- new_output_files:
  - (none)

## E5
- script: `src/rebuttal/scripts/E5_run_contamination_probes.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `2`
- log_file: `rebuttal/outputs/run_logs/E5.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E5_probe_results.csv` (exists=True)
- new_output_files:
  - (none)

## E6
- script: `src/rebuttal/scripts/E6_run_fusion_baselines.py`
- return_code: `0`
- io_logged(stdout/stderr): `False`
- stdout_lines: `0`, stderr_lines: `0`
- log_file: `rebuttal/outputs/run_logs/E6.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E6_fusion_main.csv` (exists=True)
- new_output_files:
  - (none)

## E7
- script: `src/rebuttal/scripts/E7_prepare_metric_human_calibration.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `2`
- log_file: `rebuttal/outputs/run_logs/E7.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E7_annotation_packet.csv` (exists=True)
- new_output_files:
  - (none)

## E8
- script: `src/rebuttal/scripts/E8_run_noise_polysemy_encoder.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `2`
- log_file: `rebuttal/outputs/run_logs/E8.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E8_noise_robustness.csv` (exists=True)
- new_output_files:
  - (none)

## E9
- script: `src/rebuttal/scripts/E9_run_scion_rl_ablation.py`
- return_code: `0`
- io_logged(stdout/stderr): `False`
- stdout_lines: `0`, stderr_lines: `0`
- log_file: `rebuttal/outputs/run_logs/E9.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E9_sft_vs_rl.csv` (exists=True)
- new_output_files:
  - (none)

## E10
- script: `src/rebuttal/scripts/E10_run_lite_full_tradeoff.py`
- return_code: `0`
- io_logged(stdout/stderr): `False`
- stdout_lines: `0`, stderr_lines: `0`
- log_file: `rebuttal/outputs/run_logs/E10.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E10_lite_full_main.csv` (exists=True)
- new_output_files:
  - (none)

## E11
- script: `src/rebuttal/scripts/E11_run_domain_specific_engineer.py`
- return_code: `0`
- io_logged(stdout/stderr): `True`
- stdout_lines: `0`, stderr_lines: `2`
- log_file: `rebuttal/outputs/run_logs/E11.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E11_domain_specific_main.csv` (exists=True)
- new_output_files:
  - (none)

## E12
- script: `src/rebuttal/scripts/E12_run_inter_event_pilot.py`
- return_code: `0`
- io_logged(stdout/stderr): `False`
- stdout_lines: `0`, stderr_lines: `0`
- log_file: `rebuttal/outputs/run_logs/E12.log`
- llm_signal_detected: `False`
- llm_signal_keywords: `(none)`
- inputs:
  - `/workspace/gxb_6_graph_maker/data/scope/subsets` (exists=True)
- expected_outputs:
  - `/workspace/gxb_6_graph_maker/rebuttal/outputs/E12_inter_event_main.csv` (exists=True)
- new_output_files:
  - (none)
