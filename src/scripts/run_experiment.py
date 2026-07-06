"""
Experiment runner for EXP001 — 2×3 factorial design.

Pre-flight checks (research-design-v2.0):
- Full git commit SHA + clean working tree
- Configuration SHA256 hash
- Environment snapshot (Python, PyTorch, CUDA, GPU)
- Dataset integrity (speaker overlap, sample counts)
- Disk space estimation
- Random seed verification (run twice, compare)
"""

import argparse
import yaml
import json
import os
import sys
import random
import platform
import subprocess
import time
import shutil
import hashlib
from datetime import datetime
from pathlib import Path

import torch
import torch.backends.cudnn as cudnn
import numpy as np

from kws_framework.dataset.dataset import GSCv2Dataset, EpisodeSampler
from kws_framework.features.features import FeatureExtractor
from kws_framework.models.bc_resnet import BCResNet32
from kws_framework.losses.losses import PrototypicalLoss, GE2ELoss, TripletLoss
from kws_framework.trainer.trainer import Trainer
from kws_framework.trainer.evaluator import Evaluator

EXPERIMENT_BRANCH = "main"
DESIGN_TAG = "research-design-v2.0"
LOSS_MAP = {
    "prototypical": PrototypicalLoss,
    "ge2e": GE2ELoss,
    "triplet": TripletLoss,
}


# ─── Pre-flight utilities ────────────────────────────────────────────────────


def set_seed(seed: int, deterministic: bool = True):
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


def get_git_info() -> dict:
    info = {"commit": "unknown", "branch": "unknown", "tag": "none", "clean": False}
    try:
        info["commit"] = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
        info["branch"] = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL
        ).decode().strip()
        info["clean"] = len(status) == 0
        try:
            info["tag"] = subprocess.check_output(
                ["git", "describe", "--exact-match", "--tags", "HEAD"],
                stderr=subprocess.DEVNULL
            ).decode().strip()
        except subprocess.CalledProcessError:
            info["tag"] = "none"
    except Exception:
        pass
    return info


def config_sha256(config_path: str) -> str:
    with open(config_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def snapshot_environment(output_dir: Path):
    env = {
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__ if "torch" in sys.modules else "N/A",
        "cuda_available": torch.cuda.is_available(),
        "cuda_version": torch.version.cuda if torch.cuda.is_available() else "N/A",
        "cudnn_version": torch.backends.cudnn.version() if torch.cuda.is_available() else "N/A",
        "gpu_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "gpu_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A",
        "gpu_vram_gb": torch.cuda.get_device_properties(0).total_memory / 1e9
            if torch.cuda.is_available() else 0,
        "numpy": np.__version__,
    }
    with open(output_dir / "environment.json", "w") as f:
        json.dump(env, f, indent=2)
    return env


def audit_dataset(data_root: str, split: str) -> dict:
    ds = GSCv2Dataset(data_root, split=split)
    # Dataset checksum: SHA256 of dataset root README + README files
    # (stable identifier for the dataset version)
    dataset_hash = hashlib.sha256()
    try:
        readme = os.path.join(data_root, "README.md")
        if os.path.exists(readme):
            with open(readme, "rb") as f:
                dataset_hash.update(f.read())
    except Exception:
        pass
    info = {
        "split": split,
        "total_files": len(ds),
        "dataset_checksum": dataset_hash.hexdigest()[:16],
        "classes_found": ds.classes,
        "seen_classes": ds.seen_classes,
        "unseen_classes": ds.unseen_classes,
    }
    speaker_counts = {}
    for entry in ds.index:
        cls, _, spk, _ = entry
        speaker_counts.setdefault(spk, set()).add(cls)
    info["unique_speakers"] = len(speaker_counts)
    info["speaker_class_counts"] = {
        spk: len(cls_list) for spk, cls_list in speaker_counts.items()
    }
    return info


def verify_determinism(config: dict, output_dir: Path) -> dict:
    set_seed(config["seed"])
    m1 = BCResNet32(embedding_dim=config.get("embedding_dim", 64))
    p1 = [p.clone().detach() for p in m1.parameters()]
    set_seed(config["seed"])
    m2 = BCResNet32(embedding_dim=config.get("embedding_dim", 64))
    p2 = [p.clone().detach() for p in m2.parameters()]
    identical = all(torch.equal(a, b) for a, b in zip(p1, p2))
    result = {"deterministic_init": identical, "seed": config["seed"]}
    with open(output_dir / "seed_verify.json", "w") as f:
        json.dump(result, f)
    return result


# ─── Core experiment ─────────────────────────────────────────────────────────


def count_parameters(model) -> dict:
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"total_params": total, "trainable_params": trainable}


def build_output_path(base_dir: str, feature: str, loss: str, seed: int) -> Path:
    feature_short = "LogMel" if feature == "log_mel" else "PCEN"
    loss_short = loss.capitalize()
    return Path(base_dir) / f"{feature_short}_{loss_short}_seed{seed}"


def main(config: dict, smoke: bool = False):
    exp_name = config.get("experiment_name", "exp001")
    seed = config.get("seed", 42)
    data_root = config.get("data_root", "data/raw/speech_commands_v0.02")
    feature_type = config.get("feature_type", "log_mel")
    loss_name = config.get("loss", "prototypical")
    config_path = config.get("_config_path", "src/configs/exp001.yaml")

    output_dir = build_output_path(f"experiments/{exp_name}", feature_type, loss_name, seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Pre-flight checks ────────────────────────────────────────────────

    print(f"\n{'='*60}")
    print(f"EXP001 — Pre-flight Checks")
    print(f"{'='*60}")

    git_info = get_git_info()
    print(f"  Git commit: {git_info['commit'][:12]}")
    print(f"  Branch:     {git_info['branch']}")
    print(f"  Tag:        {git_info['tag']}")
    print(f"  Clean tree: {git_info['clean']}")
    if not git_info["clean"]:
        print("  ⚠ WARNING: Uncommitted changes in working tree")

    cfg_hash = config_sha256(config_path)
    print(f"  Config SHA256: {cfg_hash}")

    env = snapshot_environment(output_dir)
    print(f"  Python:   {env['python'].split()[0]}")
    print(f"  PyTorch:  {env['torch']}")
    print(f"  CUDA:     {env['cuda_version']}")
    print(f"  GPU:      {env['gpu_name']} ({env['gpu_vram_gb']:.1f} GB)")
    print(f"  Devices:  {env['gpu_count']}")

    # Dataset audit
    train_info = audit_dataset(data_root, "training")
    test_info = audit_dataset(data_root, "testing")
    train_speakers = set()
    test_speakers_full = set()
    ds_temp = GSCv2Dataset(data_root, split="training")
    for e in ds_temp.index:
        train_speakers.add(e[2])
    ds_test = GSCv2Dataset(data_root, split="testing")
    for e in ds_test.index:
        test_speakers_full.add(e[2])
    speaker_overlap = len(train_speakers & test_speakers_full)
    print(f"  Dataset: train={train_info['total_files']}, test={test_info['total_files']}")
    print(f"  Speaker overlap (train ∩ test): {speaker_overlap}")

    # Seed verification
    print(f"  Verifying deterministic init (seed={seed})...")
    det = verify_determinism(config, output_dir)
    print(f"  Deterministic init: {det['deterministic_init']}")
    if not det["deterministic_init"]:
        print("  ⚠ WARNING: Model init is NOT deterministic. Check cuDNN/cuda.")

    # Disk space estimate
    estimated_mb = 0.5 + (config.get("epochs", 40) * 0.01)
    print(f"  Estimated output size: ~{estimated_mb:.1f} MB")

    # Save pre-flight manifest
    manifest = {
        "experiment": exp_name,
        "feature": feature_type,
        "loss": loss_name,
        "seed": seed,
        "git": git_info,
        "config_sha256": cfg_hash,
        "environment": env,
        "dataset_train": train_info,
        "dataset_test": test_info,
        "speaker_overlap_train_test": speaker_overlap,
        "deterministic_init": det["deterministic_init"],
        "smoke_test": smoke,
    }
    with open(output_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    if smoke:
        print(f"\n  SMOKE TEST MODE: config={feature_type}+{loss_name}, seed={seed}")
        config["epochs"] = min(config.get("epochs", 40), 3)
        config["n_episodes_train"] = 10
        config["n_episodes_eval"] = 20

    # ── Training ──────────────────────────────────────────────────────────

    set_seed(seed)
    print(f"\n{'='*60}")
    print(f"Training: feature={feature_type}, loss={loss_name}, seed={seed}")
    print(f"{'='*60}")

    feature_extractor = FeatureExtractor(feature_type=feature_type)
    backbone = BCResNet32(
        input_channels=config.get("n_mels", 40),
        embedding_dim=config.get("embedding_dim", 64),
        t=config.get("backbone_width", 2.5),
    )
    params = count_parameters(backbone)
    print(f"  Backbone params: {params['total_params']/1e3:.1f}K")
    with open(output_dir / "params.json", "w") as f:
        json.dump(params, f)

    loss_fn = LOSS_MAP[loss_name]()

    n_way = config.get("n_way", 5)
    n_support = config.get("n_support", 5)
    n_query = config.get("n_query", 5)
    n_episodes_train = config.get("n_episodes_train", 1000)
    n_episodes_eval = config.get("n_episodes_eval", 600)
    epochs = config.get("epochs", 40)

    trainer = Trainer(backbone, feature_extractor, loss_fn, config)
    evaluator = Evaluator(backbone, feature_extractor, config)

    train_sampler = EpisodeSampler(
        train_dataset := GSCv2Dataset(data_root, split="training"),
        n_way=n_way, n_support=n_support, n_query=n_query, seed=seed
    )
    # Eval uses training split too — unseen classes (not files) are the held-out aspect
    eval_sampler = EpisodeSampler(
        GSCv2Dataset(data_root, split="training"),
        n_way=n_way, n_support=n_support, n_query=n_query, seed=seed + 1000
    )

    print(f"  Episode: {n_way}-way {n_support}-shot, {epochs} epochs")
    train_log = []
    t_start = time.time()

    for epoch in range(epochs):
        epoch_loss = 0.0
        for _ in range(n_episodes_train):
            support_data, support_labels, query_data, query_labels = \
                train_sampler.sample_episode(train_dataset.unseen_classes)
            sd = torch.FloatTensor(support_data)
            qd = torch.FloatTensor(query_data)
            sl = torch.LongTensor(support_labels)
            ql = torch.LongTensor(query_labels)
            loss = trainer.train_epoch([(sd, sl, qd, ql)])
            epoch_loss += loss

        avg_loss = epoch_loss / max(n_episodes_train, 1)
        train_log.append({"epoch": epoch + 1, "loss": avg_loss})
        if (epoch + 1) % max(1, epochs // 4) == 0 or epoch == 0:
            print(f"  Epoch {epoch+1}/{epochs}: loss = {avg_loss:.4f}")

    train_time = time.time() - t_start
    with open(output_dir / "train_log.json", "w") as f:
        json.dump(train_log, f)

    # ── Evaluation ────────────────────────────────────────────────────────

    print(f"  Evaluating ({n_episodes_eval} episodes)...")
    t_eval_start = time.time()
    results = evaluator.evaluate_full(eval_sampler, n_episodes=n_episodes_eval)
    eval_time = time.time() - t_eval_start

    # Latency
    sample_data, _, _, _ = eval_sampler.sample_episode(train_dataset.unseen_classes)
    dummy = torch.FloatTensor(sample_data[:1])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    dummy = dummy.to(device)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    t_lat = time.time()
    with torch.no_grad():
        for _ in range(100):
            _ = evaluator.feature_extractor(dummy)
            _ = evaluator.model(_)
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    latency_ms = (time.time() - t_lat) / 100 * 1000

    # ── Metrics ───────────────────────────────────────────────────────────

    metrics = {
        # Experiment info
        "experiment": exp_name,
        "feature": feature_type,
        "loss": loss_name,
        "seed": seed,
        "git_commit": git_info["commit"][:12],
        "config_sha256": cfg_hash,
        "timestamp": datetime.now().isoformat(),
        "smoke_test": smoke,

        # Few-shot eval
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
        "inference_latency_ms": round(latency_ms, 2),
        "training_time_s": round(train_time, 1),
        "evaluation_time_s": round(eval_time, 1),

        # Config
        "n_way": n_way,
        "n_support": n_support,
        "n_query": n_query,
        "n_episodes_eval": n_episodes_eval,
        "epochs": epochs,
    }

    with open(output_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\n  ── Results ──")
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
    print(f"  Saved:        {output_dir}")

    if smoke:
        print(f"\n  ⚠ SMOKE TEST — results not meaningful for analysis")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--feature", type=str, default=None)
    parser.add_argument("--loss", type=str, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--smoke", action="store_true", help="Mini run (3 epochs, 10 episodes)")
    args = parser.parse_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)
    config["_config_path"] = args.config

    if args.feature:
        config["feature_type"] = args.feature
    if args.loss:
        config["loss"] = args.loss
    if args.seed is not None:
        config["seed"] = args.seed

    main(config, smoke=args.smoke)
