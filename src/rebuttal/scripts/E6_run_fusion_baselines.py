from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e6

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E6_fusion_baselines.yaml'))
    run_e6(cfg)
