from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e2

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E2_normalization_sensitivity.yaml'))
    run_e2(cfg)
