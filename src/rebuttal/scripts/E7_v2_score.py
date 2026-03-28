from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e7_v2_score

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E7_metric_human_calibration.yaml'))
    run_e7_v2_score(cfg)
