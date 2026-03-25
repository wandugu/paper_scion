from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e5

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E5_contamination_probes.yaml'))
    run_e5(cfg)
