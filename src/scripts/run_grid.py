"""
Grid runner for EXP001: 2×3 factorial design.

Modes:
  --smoke    6 runs (2 features × 3 losses × 1 seed, mini epochs)
  --full     18 runs (2 features × 3 losses × 3 seeds)
  --dry-run  Print plan without executing
  --resume   Skip cells with existing results

Workflow:
  python src/scripts/run_grid.py --dry-run   # preview
  python src/scripts/run_grid.py --smoke     # 6 cells validation
  python src/scripts/run_grid.py --full      # 18 cells — production
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path


FEATURES = ["log_mel", "log_mel_pcen"]
LOSSES = ["prototypical", "ge2e", "triplet"]
SEEDS = [42, 43, 44]
PRIMARY_LOSSES = ["prototypical"]
EXPERIMENT = "exp001"
CONFIG = f"src/configs/{EXPERIMENT}.yaml"


def config_dir(feature: str, loss: str, seed: int) -> str:
    feat_short = "LogMel" if feature == "log_mel" else "PCEN"
    loss_short = loss.capitalize()
    return f"experiments/{EXPERIMENT}/{feat_short}_{loss_short}_seed{seed}"


def get_cells(full: bool):
    cells = []
    for feature in FEATURES:
        for loss in LOSSES:
            seeds = SEEDS if (full and loss in PRIMARY_LOSSES) else [SEEDS[0]]
            for seed in seeds:
                cells.append((feature, loss, seed))
    return cells


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    mode = "full"
    if args.smoke:
        mode = "smoke"
    if args.dry_run:
        mode = "dry_run"

    cells = get_cells(full=(mode == "full"))
    total = len(cells)

    label = {"full": "FULL (18 cells)", "smoke": "SMOKE (6 cells)", "dry_run": "DRY RUN"}[mode]

    print(f"{'='*60}")
    print(f"EXP001 Grid — {label}")
    print(f"{'='*60}")
    if mode == "full":
        print(f"  Primary   (3 seeds): {len(FEATURES)} feats × {len(PRIMARY_LOSSES)} losses × 3 = {len(FEATURES) * len(PRIMARY_LOSSES) * 3}")
        print(f"  Secondary (1 seed):  {len(FEATURES)} feats × {len(set(LOSSES)-set(PRIMARY_LOSSES))} losses × 1 = {len(FEATURES) * (len(LOSSES)-len(PRIMARY_LOSSES))}")
    elif mode == "smoke":
        print(f"  All cells: 1 seed each = {total} cells (mini epochs)")
    print(f"  Total: {total} cells")
    print(f"{'='*60}\n")

    completed = 0
    skipped = 0
    failed = 0
    t_start = time.time()

    for i, (feature, loss, seed) in enumerate(cells, 1):
        out_dir = config_dir(feature, loss, seed)

        if args.resume and Path(out_dir / "metrics.json").exists():
            skipped += 1
            print(f"  [{i}/{total}] SKIP {out_dir}")
            continue

        if args.dry_run:
            print(f"  [{i}/{total}] feature={feature:15s} loss={loss:15s} seed={seed}")
            continue

        cmd = [
            sys.executable, "src/scripts/run_experiment.py",
            "--config", CONFIG,
            "--feature", feature, "--loss", loss, "--seed", str(seed),
        ]
        if args.smoke:
            cmd.append("--smoke")

        print(f"[{i}/{total}] feature={feature:15s} loss={loss:15s} seed={seed}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            completed += 1
            for line in result.stdout.strip().split("\n")[-6:]:
                print(f"  {line}")
        else:
            failed += 1
            print(f"  ERROR (code {result.returncode})")
            for line in result.stderr.strip().split("\n")[-5:]:
                print(f"  {line}")

    elapsed = time.time() - t_start
    print(f"\n{'='*60}")
    print(f"Grid {mode}: {completed} done, {skipped} skipped, {failed} failed")
    print(f"Elapsed: {elapsed:.0f}s")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
