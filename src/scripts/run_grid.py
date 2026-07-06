"""
Grid runner for EXP001: 2×3 factorial design.

Features: [log_mel, log_mel_pcen]
Losses: [prototypical, ge2e, triplet]
Seeds: primary=[42,43,44], secondary=[42]

Design decisions (v2.0):
- Primary cells: ProtoNet (3 seeds) — full statistical analysis
- Secondary cells: GE2E, Triplet (1 seed) — baseline comparison

Usage:
    python src/scripts/run_grid.py                    # full grid
    python src/scripts/run_grid.py --dry-run           # show what would run
    python src/scripts/run_grid.py --resume            # skip existing results
"""

import argparse
import subprocess
import sys
from pathlib import Path


FEATURES = ["log_mel", "log_mel_pcen"]
LOSSES = ["prototypical", "ge2e", "triplet"]
SEEDS = [42, 43, 44]
PRIMARY_LOSSES = ["prototypical"]
EXPERIMENT = "exp001"


def config_dir(feature: str, loss: str, seed: int) -> str:
    """Match the output directory name in run_experiment.py."""
    feat_short = "LogMel" if feature == "log_mel" else "PCEN"
    loss_short = loss.capitalize()
    return f"experiments/{EXPERIMENT}/{feat_short}_{loss_short}_seed{seed}"


def get_cells():
    cells = []
    for feature in FEATURES:
        for loss in LOSSES:
            seeds = SEEDS if loss in PRIMARY_LOSSES else [SEEDS[0]]
            for seed in seeds:
                cells.append((feature, loss, seed))
    return cells


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would run without executing")
    parser.add_argument("--resume", action="store_true",
                        help="Skip cells with existing results")
    args = parser.parse_args()

    config_path = f"src/configs/{EXPERIMENT}.yaml"
    cells = get_cells()
    total = len(cells)
    completed = 0
    skipped = 0
    failed = 0

    print(f"{'='*60}")
    print(f"EXP001 Grid: {len(FEATURES)} features × {len(LOSSES)} losses")
    print(f"  Primary (3 seeds): {len(FEATURES)} × {len(PRIMARY_LOSSES)} × 3 = {len(FEATURES) * len(PRIMARY_LOSSES) * 3}")
    print(f"  Secondary (1 seed): {len(FEATURES)} × {len(set(LOSSES)-set(PRIMARY_LOSSES))} × 1 = {len(FEATURES) * (len(LOSSES)-len(PRIMARY_LOSSES)) * 1}")
    print(f"  Total: {total} cells")
    print(f"{'='*60}")

    for feature, loss, seed in cells:
        out_dir = config_dir(feature, loss, seed)

        if args.resume and Path(out_dir).exists():
            metrics_path = Path(out_dir) / "metrics.json"
            if metrics_path.exists():
                skipped += 1
                print(f"  [{completed+skipped+failed+1}/{total}] SKIP {out_dir}")
                continue

        if args.dry_run:
            print(f"  [{completed+skipped+failed+1}/{total}] DRY-RUN: feature={feature}, loss={loss}, seed={seed}")
            continue

        cmd = [
            sys.executable, "src/scripts/run_experiment.py",
            "--config", config_path,
            "--feature", feature,
            "--loss", loss,
            "--seed", str(seed),
        ]

        print(f"\n[{completed+skipped+failed+1}/{total}] Running: feature={feature}, loss={loss}, seed={seed}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            completed += 1
            # Print last lines of output
            for line in result.stdout.strip().split("\n")[-6:]:
                print(f"  {line}")
        else:
            failed += 1
            print(f"  ERROR (code {result.returncode})")
            print(f"  {result.stderr[-500:]}")

    print(f"\n{'='*60}")
    print(f"Grid complete: {completed} done, {skipped} skipped, {failed} failed")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
