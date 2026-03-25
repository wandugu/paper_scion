from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e11

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E11_domain_specific_engineer.yaml'))
    run_e11(cfg)
