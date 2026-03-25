from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e10

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E10_lite_full_tradeoff.yaml'))
    run_e10(cfg)
