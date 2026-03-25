from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e9

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E9_scion_rl_ablation.yaml'))
    run_e9(cfg)
