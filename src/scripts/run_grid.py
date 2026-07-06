"""
Grid runner for EXP001: 2×3 factorial design.

Features: [log_mel, log_mel_pcen]
Losses: [prototypical, ge2e, triplet]
Seeds: [42, 43, 44]

Usage:
    python src/scripts/run_grid.py --experiment exp001
"""

import subprocess
import sys
from pathlib import Path


FEATURES = ["log_mel", "log_mel_pcen"]
LOSSES = ["prototypical", "ge2e", "triplet"]
SEEDS = [42, 43, 44]

# Primary cells: ProtoNet (3 seeds)
# Secondary cells: GE2E, Triplet (1 seed)
PRIMARY_LOSSES = ["prototypical"]
SECONDARY_LOSSES = ["ge2e", "triplet"]


def main():
    experiment = "exp001"
    config_path = f"src/configs/{experiment}.yaml"
    total_cells = 0

    for feature in FEATURES:
        for loss in LOSSES:
            seeds = SEEDS if loss in PRIMARY_LOSSES else [SEEDS[0]]
            for seed in seeds:
                total_cells += 1
                cmd = [
                    sys.executable, "src/scripts/run_experiment.py",
                    "--config", config_path,
                    "--feature", feature,
                    "--loss", loss,
                    "--seed", str(seed),
                ]
                print(f"\n{'='*60}")
                print(f"Running: feature={feature}, loss={loss}, seed={seed}")
                print(f"{'='*60}")
                result = subprocess.run(cmd)
                if result.returncode != 0:
                    print(f"ERROR: Failed for {feature}/{loss}/seed={seed}")

    print(f"\n{'='*60}")
    print(f"Grid complete: {total_cells} experiments")
    print(f"Results saved to experiments/{experiment}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
