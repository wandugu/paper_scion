from pathlib import Path
from src.rebuttal.rebuttal_experiments import run_e8

if __name__ == '__main__':
    cfg = str(Path('src/rebuttal/configs/E8_noise_polysemy_encoder.yaml'))
    run_e8(cfg)
