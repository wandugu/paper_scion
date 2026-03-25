from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e1

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E1_reachable_eval.yaml'))
    run_e1(cfg)
