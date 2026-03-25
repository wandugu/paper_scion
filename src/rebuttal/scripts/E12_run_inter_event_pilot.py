from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e12

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E12_inter_event_pilot.yaml'))
    run_e12(cfg)
