"""
Experiment runner for EXP001.

Usage:
    python src/scripts/run_experiment.py --config src/configs/exp001.yaml
"""

import argparse
import yaml
import json
import os
from datetime import datetime
from pathlib import Path

import torch
import numpy as np

from kws_framework.dataset.dataset import GSCv2Dataset, EpisodeSampler
from kws_framework.features.features import FeatureExtractor
from kws_framework.models.bc_resnet import BCResNet32
from kws_framework.losses.losses import PrototypicalLoss, GE2ELoss, TripletLoss
from kws_framework.trainer.trainer import Trainer, Evaluator


LOSS_MAP = {
    "prototypical": PrototypicalLoss,
    "ge2e": GE2ELoss,
    "triplet": TripletLoss,
}


def set_seed(seed: int):
    torch.manual_seed(seed)
    np.random.seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def main(config: dict):
    exp_name = config.get("experiment_name", "exp001")
    seed = config.get("seed", 42)
    data_root = config.get("data_root", "data/raw/speech_commands_v0.02")
    output_dir = Path(f"experiments/{exp_name}")

    set_seed(seed)

    # Dataset
    train_dataset = GSCv2Dataset(data_root, split="training")
    test_dataset = GSCv2Dataset(data_root, split="testing")

    # Feature extractor
    feature_type = config.get("feature_type", "log_mel")
    feature_extractor = FeatureExtractor(feature_type=feature_type)

    # Backbone
    backbone = BCResNet32(
        input_channels=config.get("n_mels", 40),
        embedding_dim=config.get("embedding_dim", 64),
    )

    # Loss
    loss_name = config.get("loss", "prototypical")
    loss_fn = LOSS_MAP[loss_name]()

    # Episode sampler
    n_way = config.get("n_way", 5)
    n_support = config.get("n_support", 5)
    n_query = config.get("n_query", 5)
    n_episodes_train = config.get("n_episodes_train", 1000)
    n_episodes_eval = config.get("n_episodes_eval", 600)
    epochs = config.get("epochs", 40)

    # Trainer
    trainer = Trainer(backbone, feature_extractor, loss_fn, config)
    evaluator = Evaluator(backbone, feature_extractor, config)

    # Training loop
    train_sampler = EpisodeSampler(
        train_dataset, n_way=n_way, n_support=n_support,
        n_query=n_query, seed=seed
    )
    eval_sampler = EpisodeSampler(
        test_dataset, n_way=n_way, n_support=n_support,
        n_query=n_query, seed=seed + 1
    )

    print(f"Running {exp_name}: feature={feature_type}, loss={loss_name}, seed={seed}")

    for epoch in range(epochs):
        train_loss = 0.0
        for _ in range(n_episodes_train):
            support_data, support_labels, query_data, query_labels = \
                train_sampler.sample_episode(train_dataset.unseen_classes)
            # Convert to tensors
            sd = torch.FloatTensor(support_data).unsqueeze(1)
            qd = torch.FloatTensor(query_data).unsqueeze(1)
            sl = torch.LongTensor(support_labels)
            ql = torch.LongTensor(query_labels)

            batch = (sd, sl, qd, ql)
            loss = trainer.train_epoch([batch])
            train_loss += loss

        if (epoch + 1) % 10 == 0:
            print(f"  Epoch {epoch+1}/{epochs}: loss = {train_loss/n_episodes_train:.4f}")

    # Evaluation
    print("  Evaluating...")
    results = evaluator.evaluate(eval_sampler, n_episodes=n_episodes_eval)
    results.update({
        "experiment": exp_name,
        "feature": feature_type,
        "loss": loss_name,
        "seed": seed,
        "n_support": n_support,
    })

    # Save results
    output_dir.mkdir(parents=True, exist_ok=True)
    result_path = output_dir / f"results_{loss_name}_{feature_type}_seed{seed}.json"
    with open(result_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"  Results: acc={results['accuracy']:.4f} ± {results['accuracy_std']:.4f}")
    print(f"  Saved to {result_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=True,
                        help="Path to YAML config file")
    parser.add_argument("--feature", type=str, default=None,
                        help="Override feature type")
    parser.add_argument("--loss", type=str, default=None,
                        help="Override loss type")
    parser.add_argument("--seed", type=int, default=None,
                        help="Override random seed")
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
