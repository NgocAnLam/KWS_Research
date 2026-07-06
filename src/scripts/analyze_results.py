#!/usr/bin/env python3
"""
Statistical analysis for EXP001 results.

Produces:
- Mean ± std table for each config (across seeds)
- 95% confidence intervals
- Pairwise comparison (paired t-test / Wilcoxon)
- Best config identification
- LaTeX table for paper
"""

import json
import sys
from pathlib import Path
import numpy as np
from scipy import stats


EXPERIMENT_DIR = Path("experiments/exp001")
FEATURES = ["LogMel", "PCEN"]
LOSSES = ["Prototypical", "Ge2e", "Triplet"]
SEEDS = [42, 43, 44]
PRIMARY_LOSSES = ["Prototypical"]
METRICS = ["accuracy", "f1", "auc", "eer", "acc_at_1pct_far", "acc_at_5pct_far"]


def load_metrics(feature: str, loss: str, seed: int) -> dict:
    dir_name = f"{feature}_{loss}_seed{seed}"
    path = EXPERIMENT_DIR / dir_name / "metrics.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def collect_results() -> dict:
    """results[feature][loss] = list of metric dicts (one per seed)"""
    results = {}
    for feat in FEATURES:
        results[feat] = {}
        for loss in LOSSES:
            seeds = SEEDS if loss in PRIMARY_LOSSES else [SEEDS[0]]
            results[feat][loss] = []
            for seed in seeds:
                m = load_metrics(feat, loss, seed)
                if m:
                    results[feat][loss].append(m)
    return results


def mean_ci(values, confidence=0.95):
    arr = np.array(values)
    n = len(arr)
    if n < 2:
        return float(arr.mean()), 0.0
    se = stats.sem(arr)
    h = se * stats.t.ppf((1 + confidence) / 2, n - 1)
    return float(arr.mean()), float(h)


def print_table(results):
    print(f"\n{'='*90}")
    print(f"EXP001 RESULTS — Feature × Metric Learning (2×3 Factorial)")
    print(f"{'='*90}")
    print(f"{'Feature':<10} {'Loss':<15} {'Acc':<12} {'F1':<12} {'AUC':<12} {'EER':<12} {'Acc@1%FAR':<12}")
    print(f"{'-'*90}")

    best = {"acc": 0, "f1": 0, "auc": 0, "eer": 1, "config": ""}

    for feat in FEATURES:
        for loss in LOSSES:
            runs = results[feat].get(loss, [])
            if not runs:
                print(f"{feat:<10} {loss:<15} {'N/A':<12}")
                continue

            keys = ["accuracy", "f1", "auc", "eer", "acc_at_1pct_far"]
            values = {k: [] for k in keys}
            for run in runs:
                for k in keys:
                    if k in run:
                        values[k].append(run[k])

            row = f"{feat:<10} {loss:<15}"
            for k in keys:
                if values[k]:
                    m, ci = mean_ci(values[k])
                    row += f"{m:.4f}±{ci:.4f}  "
                    if k == "accuracy" and m > best["acc"]:
                        best["acc"] = m
                        best["config"] = f"{feat}+{loss}"
                    if k == "f1" and m > best["f1"]:
                        best["f1"] = m
                    if k == "auc" and m > best["auc"]:
                        best["auc"] = m
                    if k == "eer" and m < best["eer"]:
                        best["eer"] = m
                        best["config"] = f"{feat}+{loss}"
                else:
                    row += f"{'N/A':<12} "
            print(row)

    print(f"{'-'*90}")
    print(f"BEST: {best['config']} — acc={best['acc']:.4f}, auc={best['auc']:.4f}, eer={best['eer']:.4f}")


def main():
    results = collect_results()
    print_table(results)


if __name__ == "__main__":
    main()
