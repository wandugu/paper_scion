#!/usr/bin/env bash
set -euo pipefail
PYTHONPATH=. python src/rebuttal/scripts/E0_phase0_setup.py
PYTHONPATH=. python src/rebuttal/scripts/E1_run_reachable_eval.py
PYTHONPATH=. python src/rebuttal/scripts/E3_run_eta_baseline.py
PYTHONPATH=. python src/rebuttal/scripts/E4_run_downstream_eval.py
