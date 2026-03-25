#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=. python src/rebuttal/scripts/E0_phase0_setup.py
PYTHONPATH=. python src/rebuttal/scripts/E1_run_reachable_eval.py
PYTHONPATH=. python src/rebuttal/scripts/E2_run_normalization_sensitivity.py
PYTHONPATH=. python src/rebuttal/scripts/E3_run_eta_baseline.py
PYTHONPATH=. python src/rebuttal/scripts/E4_run_downstream_eval.py
PYTHONPATH=. python src/rebuttal/scripts/E5_run_contamination_probes.py
PYTHONPATH=. python src/rebuttal/scripts/E6_run_fusion_baselines.py
PYTHONPATH=. python src/rebuttal/scripts/E7_prepare_metric_human_calibration.py
PYTHONPATH=. python src/rebuttal/scripts/E9_run_scion_rl_ablation.py
PYTHONPATH=. python src/rebuttal/scripts/E10_run_lite_full_tradeoff.py
PYTHONPATH=. python src/rebuttal/scripts/E8_run_noise_polysemy_encoder.py
PYTHONPATH=. python src/rebuttal/scripts/E11_run_domain_specific_engineer.py
PYTHONPATH=. python src/rebuttal/scripts/E12_run_inter_event_pilot.py
