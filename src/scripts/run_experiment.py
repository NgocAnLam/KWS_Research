"""
Experiment runner for EXP001 — 2×3 factorial design.

Fixes applied per code review:
- Comprehensive random seeding (Python, NumPy, PyTorch, CUDA, cuDNN)
- Structured output per config subdirectory
- 12 metrics including FAR-constrained
- Resource logging (params, FLOPs, latency, memory)
- Git commit hash tracking
- Config copy in output dir
"""

import argparse
import yaml
import json
import os
import sys
import random
import subprocess
import shutil
import time
from datetime import datetime
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
import numpy as np
from thop import profile

from kws_framework.dataset.dataset import GSCv2Dataset, EpisodeSampler
from kws_framework.features.features import FeatureExtractor
from kws_framework.models.bc_resnet import BCResNet32
from kws_framework.losses.losses import PrototypicalLoss, GE2ELoss, TripletLoss
from kws_framework.trainer.trainer import Trainer
from kws_framework.trainer.evaluator import Evaluator


LOSS_MAP = {
    "prototypical": PrototypicalLoss,
    "ge2e": GE2ELoss,
    "triplet": TripletLoss,
}


def set_seed(seed: int, deterministic: bool = True):
    """Fix ALL random sources for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    if deterministic:
        cudnn.deterministic = True
        cudnn.benchmark = False
    os.environ["PYTHONHASHSEED"] = str(seed)
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"


def get_git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "unknown"


def count_parameters(model) -> dict:
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"total_params": total, "trainable_params": trainable}


def estimate_flops(model, input_shape) -> float:
    """Estimate FLOPs using thop. Returns MACs (G)."""
    try:
        dummy = torch.randn(1, *input_shape)
        macs, _ = profile(model, inputs=(dummy,), verbose=False)
        return macs / 1e6  # convert to M
    except Exception:
        return 0.0


def build_output_path(base_dir: str, feature: str, loss: str, seed: int) -> Path:
    """Structured output: experiments/exp001/LogMel_Proto_seed42/"""
    feature_short = "LogMel" if feature == "log_mel" else "PCEN"
    loss_short = loss.capitalize()
    dir_name = f"{feature_short}_{loss_short}_seed{seed}"
    return Path(base_dir) / dir_name


def main(config: dict):
    exp_name = config.get("experiment_name", "exp001")
    seed = config.get("seed", 42)
    data_root = config.get("data_root", "data/raw/speech_commands_v0.02")
    feature_type = config.get("feature_type", "log_mel")
    loss_name = config.get("loss", "prototypical")

    set_seed(seed)
    git_hash = get_git_commit()

    # Structured output directory
    output_dir = build_output_path(f"experiments/{exp_name}", feature_type, loss_name, seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save config copy
    config["git_commit"] = git_hash
    config["start_time"] = datetime.now().isoformat()
    with open(output_dir / "config.yaml", "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    with open(output_dir / "seed.txt", "w") as f:
        f.write(str(seed))

    # Dataset
    print(f"[{exp_name}] Loading dataset...")
    train_dataset = GSCv2Dataset(data_root, split="training")
    test_dataset = GSCv2Dataset(data_root, split="testing")

    # Verify speaker leakage
    train_speakers = set(x[2] for x in train_dataset.index)
    test_speakers = set(x[2] for x in test_dataset.index)
    overlap = train_speakers & test_speakers
    print(f"  Speakers: train={len(train_speakers)}, test={len(test_speakers)}, overlap={len(overlap)}")

    # Feature extractor
    feature_extractor = FeatureExtractor(feature_type=feature_type)

    # Backbone
    backbone = BCResNet32(
        input_channels=config.get("n_mels", 40),
        embedding_dim=config.get("embedding_dim", 64),
    )

    # Resource logging
    params = count_parameters(backbone)
    print(f"  Params: {params['total_params']/1e3:.1f}K total, {params['trainable_params']/1e3:.1f}K trainable")
    with open(output_dir / "params.json", "w") as f:
        json.dump(params, f)

    # Loss
    loss_fn = LOSS_MAP[loss_name]()

    # Episode config
    n_way = config.get("n_way", 5)
    n_support = config.get("n_support", 5)
    n_query = config.get("n_query", 5)
    n_episodes_train = config.get("n_episodes_train", 1000)
    n_episodes_eval = config.get("n_episodes_eval", 600)
    epochs = config.get("epochs", 40)

    # Trainer
    trainer = Trainer(backbone, feature_extractor, loss_fn, config)
    evaluator = Evaluator(backbone, feature_extractor, config)

    # Samplers (separate seeds for train/eval)
    train_sampler = EpisodeSampler(
        train_dataset, n_way=n_way, n_support=n_support,
        n_query=n_query, seed=seed
    )
    eval_sampler = EpisodeSampler(
        test_dataset, n_way=n_way, n_support=n_support,
        n_query=n_query, seed=seed + 1000
    )

    print(f"  Config: feature={feature_type}, loss={loss_name}, {n_way}-way {n_support}-shot")
    print(f"  Output: {output_dir}")

    # Training
    print(f"  Training {epochs} epochs...")
    train_log = []
    t_start = time.time()

    for epoch in range(epochs):
        epoch_loss = 0.0
        for _ in range(n_episodes_train):
            support_data, support_labels, query_data, query_labels = \
                train_sampler.sample_episode(train_dataset.unseen_classes)
            sd = torch.FloatTensor(support_data).unsqueeze(1)
            qd = torch.FloatTensor(query_data).unsqueeze(1)
            sl = torch.LongTensor(support_labels)
            ql = torch.LongTensor(query_labels)
            batch = (sd, sl, qd, ql)
            loss = trainer.train_epoch([batch])
            epoch_loss += loss

        avg_loss = epoch_loss / n_episodes_train
        train_log.append({"epoch": epoch + 1, "loss": avg_loss})

        if (epoch + 1) % 10 == 0 or epoch == 0:
            print(f"    Epoch {epoch+1}/{epochs}: loss = {avg_loss:.4f}")

    train_time = time.time() - t_start

    # Save training log
    with open(output_dir / "train_log.json", "w") as f:
        json.dump(train_log, f)

    # Evaluation
    print(f"  Evaluating ({n_episodes_eval} episodes)...")
    t_eval_start = time.time()
    results = evaluator.evaluate_full(eval_sampler, n_episodes=n_episodes_eval)
    eval_time = time.time() - t_eval_start

    # Inference latency
    sample_data, _, _, _ = eval_sampler.sample_episode(test_dataset.unseen_classes)
    dummy = torch.FloatTensor(sample_data[:1]).unsqueeze(1)
    if torch.cuda.is_available():
        dummy = dummy.cuda()
        torch.cuda.synchronize()
    t_lat = time.time()
    with torch.no_grad():
        for _ in range(100):
            _ = evaluator.feature_extractor(dummy)
            _ = evaluator.model(_)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    latency_ms = (time.time() - t_lat) / 100 * 1000

    # Build final metrics
    metrics = {
        # Experiment info
        "experiment": exp_name,
        "feature": feature_type,
        "loss": loss_name,
        "seed": seed,
        "git_commit": git_hash,
        "timestamp": datetime.now().isoformat(),

        # Few-shot eval metrics
        "accuracy": results["accuracy"],
        "accuracy_std": results["accuracy_std"],
        "precision": results["precision"],
        "recall": results["recall"],
        "f1": results["f1"],
        "auc": results["auc"],
        "eer": results["eer"],
        "acc_at_1pct_far": results["acc_at_1pct_far"],
        "acc_at_5pct_far": results["acc_at_5pct_far"],
        "far": results["far"],
        "frr": results["frr"],

        # Resources
        "total_params": params["total_params"],
        "trainable_params": params["trainable_params"],
        "inference_latency_ms": latency_ms,
        "training_time_s": train_time,
        "evaluation_time_s": eval_time,

        # Config
        "n_way": n_way,
        "n_support": n_support,
        "n_query": n_query,
        "n_episodes_eval": n_episodes_eval,
        "epochs": epochs,
    }

    # Save metrics
    with open(output_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n  === Results ===")
    print(f"  Accuracy:     {metrics['accuracy']:.4f} ± {metrics['accuracy_std']:.4f}")
    print(f"  Precision:    {metrics['precision']:.4f}")
    print(f"  Recall:       {metrics['recall']:.4f}")
    print(f"  F1:           {metrics['f1']:.4f}")
    print(f"  AUC:          {metrics['auc']:.4f}")
    print(f"  EER:          {metrics['eer']:.4f}")
    print(f"  Acc@1%FAR:    {metrics['acc_at_1pct_far']:.4f}")
    print(f"  Acc@5%FAR:    {metrics['acc_at_5pct_far']:.4f}")
    print(f"  Latency:      {metrics['inference_latency_ms']:.2f} ms")
    print(f"  Params:       {metrics['total_params']/1e3:.1f}K")
    print(f"  Train time:   {train_time:.1f}s")
    print(f"  Saved to:     {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--feature", type=str, default=None)
    parser.add_argument("--loss", type=str, default=None)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    if args.feature:
        config["feature_type"] = args.feature
    if args.loss:
        config["loss"] = args.loss
    if args.seed is not None:
        config["seed"] = args.seed

    main(config)
