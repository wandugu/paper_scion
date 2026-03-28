from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e3

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E3_eta_baseline.yaml'))
    run_e3(cfg)
