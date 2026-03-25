from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e4

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E4_downstream_eval.yaml'))
    run_e4(cfg)
