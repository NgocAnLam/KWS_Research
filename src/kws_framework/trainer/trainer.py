"""
Trainer and Evaluator for few-shot KWS experiments.

Design:
- Config-driven: all parameters from YAML
- Experiment logging to experiments/EXP00N/
- Supports ProtoNet/GE2E/Triplet with unified interface
"""

import os
import json
import time
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader


class Trainer:
    """Trainer for few-shot KWS models."""

    def __init__(self, model: nn.Module, feature_extractor: nn.Module,
                 loss_fn: nn.Module, config: Dict[str, Any],
                 device: torch.device = None):
        self.model = model
        self.feature_extractor = feature_extractor
        self.loss_fn = loss_fn
        self.config = config
        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")

        self.model.to(self.device)
        self.feature_extractor.to(self.device)

        self.optimizer = optim.Adam(
            list(self.model.parameters()) + list(self.feature_extractor.parameters()),
            lr=config.get("learning_rate", 1e-3),
            weight_decay=config.get("weight_decay", 4e-5),
        )

        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=config.get("epochs", 40)
        )

    def train_epoch(self, episode_loader) -> float:
        self.model.train()
        self.feature_extractor.train()
        total_loss = 0.0
        n_batches = 0

        for batch in episode_loader:
            support_data, support_labels, query_data, query_labels = batch
            support_data = support_data.to(self.device)
            query_data = query_data.to(self.device)
            support_labels = support_labels.to(self.device)
            query_labels = query_labels.to(self.device)

            # Feature extraction
            support_feat = self.feature_extractor(support_data)
            query_feat = self.feature_extractor(query_data)

            # Embedding
            support_emb = self.model(support_feat)
            query_emb = self.model(query_feat)

            # Loss
            loss = self.loss_fn(support_emb, support_labels,
                                query_emb, query_labels)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()
            n_batches += 1

        return total_loss / max(n_batches, 1)


class Evaluator:
    """Evaluator for few-shot KWS."""

    def __init__(self, model: nn.Module, feature_extractor: nn.Module,
                 config: Dict[str, Any], device: torch.device = None):
        self.model = model
        self.feature_extractor = feature_extractor
        self.config = config
        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.feature_extractor.to(self.device)

    @torch.no_grad()
    def evaluate(self, episode_loader, n_episodes: int = 600) -> Dict[str, float]:
        self.model.eval()
        self.feature_extractor.eval()

        accuracies = []
        losses = []

        for _ in range(n_episodes):
            batch = next(iter(episode_loader))
            support_data, support_labels, query_data, query_labels = batch
            support_data = support_data.to(self.device)
            query_data = query_data.to(self.device)
            support_labels = support_labels.to(self.device)
            query_labels = query_labels.to(self.device)

            support_feat = self.feature_extractor(support_data)
            query_feat = self.feature_extractor(query_data)

            support_emb = self.model(support_feat)
            query_emb = self.model(query_feat)

            # Compute prototypes
            n_classes = len(torch.unique(support_labels))
            prototypes = torch.zeros(n_classes, support_emb.size(-1),
                                     device=self.device)
            for c in range(n_classes):
                mask = support_labels == c
                prototypes[c] = support_emb[mask].mean(0)

            # Cosine similarity
            prototypes = torch.nn.functional.normalize(prototypes, p=2, dim=1)
            query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)
            sim = torch.mm(query_emb, prototypes.t())
            preds = sim.argmax(dim=1)

            acc = (preds == query_labels).float().mean().item()
            accuracies.append(acc)

        return {
            "accuracy": float(np.mean(accuracies)),
            "accuracy_std": float(np.std(accuracies)),
            "n_episodes": n_episodes,
        }

    @torch.no_grad()
    def compute_prototypes(self, support_data, support_labels):
        self.model.eval()
        self.feature_extractor.eval()
        support_data = support_data.to(self.device)
        support_labels = support_labels.to(self.device)

        support_feat = self.feature_extractor(support_data)
        support_emb = self.model(support_feat)

        n_classes = len(torch.unique(support_labels))
        prototypes = torch.zeros(n_classes, support_emb.size(-1),
                                 device=self.device)
        for c in range(n_classes):
            mask = support_labels == c
            prototypes[c] = support_emb[mask].mean(0)

        return torch.nn.functional.normalize(prototypes, p=2, dim=1)
