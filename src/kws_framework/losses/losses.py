"""
Unified loss interface for metric learning.

All losses inherit from BaseLoss and implement:
- forward(embeddings, labels) -> loss tensor

Design decision (v2.0):
- Primary: Prototypical Networks (cross-entropy on distances)
- Secondary: GE2E loss (generalized end-to-end)
- Secondary: Triplet loss (semi-hard mining)
"""

from abc import ABC, abstractmethod
import torch
import torch.nn as nn
import torch.nn.functional as F


class BaseLoss(ABC, nn.Module):
    """Base class for all metric learning losses."""

    @abstractmethod
    def forward(self, embeddings: torch.Tensor,
                labels: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError


class PrototypicalLoss(BaseLoss):
    """Prototypical Networks loss.

    Computes cross-entropy over distances from query embeddings to class prototypes.

    Args:
        distance: Distance metric ("cosine" or "euclidean")
    """

    def __init__(self, distance: str = "cosine"):
        super().__init__()
        self.distance = distance

    def forward(self, support_emb: torch.Tensor, support_labels: torch.Tensor,
                query_emb: torch.Tensor, query_labels: torch.Tensor) -> torch.Tensor:
        # Compute prototypes: mean of support embeddings per class
        n_classes = len(torch.unique(support_labels))
        prototypes = torch.zeros(n_classes, support_emb.size(-1),
                                 device=support_emb.device)
        for c in range(n_classes):
            mask = support_labels == c
            prototypes[c] = support_emb[mask].mean(0)

        # Compute distances: query → prototypes
        if self.distance == "cosine":
            # Normalize prototypes
            prototypes = F.normalize(prototypes, p=2, dim=1)
            # Cosine similarity → distance
            sim = torch.mm(query_emb, prototypes.t())
            distances = -sim
        else:
            distances = torch.cdist(query_emb, prototypes, p=2)

        # Cross-entropy loss over distances
        loss = F.cross_entropy(-distances, query_labels)
        return loss

    def predict(self, query_emb: torch.Tensor,
                prototypes: torch.Tensor,
                threshold: float = None) -> torch.Tensor:
        """Predict class labels given prototypes.

        Args:
            query_emb: (N, D) query embeddings
            prototypes: (C, D) class prototypes
            threshold: If set, return -1 for unknown (distance > threshold)
        Returns:
            (N,) predicted class indices
        """
        prototypes = F.normalize(prototypes, p=2, dim=1)
        sim = torch.mm(query_emb, prototypes.t())
        preds = sim.argmax(dim=1)

        if threshold is not None:
            max_sim = sim.max(dim=1).values
            preds[max_sim < threshold] = -1

        return preds


class GE2ELoss(BaseLoss):
    """Generalized End-to-End loss for zero-shot/few-shot KWS.

    Reference: Zhu et al. 2024 (GE2E-KWS), Wan et al. 2018

    Args:
        init_w: Initial scale parameter
        init_b: Initial bias parameter
    """

    def __init__(self, init_w: float = 10.0, init_b: float = -5.0):
        super().__init__()
        self.w = nn.Parameter(torch.tensor(init_w))
        self.b = nn.Parameter(torch.tensor(init_b))

    def forward(self, embeddings: torch.Tensor,
                labels: torch.Tensor) -> torch.Tensor:
        # Group embeddings by label
        unique_labels = torch.unique(labels)
        centroids = torch.zeros(len(unique_labels), embeddings.size(-1),
                                device=embeddings.device)

        for i, label in enumerate(unique_labels):
            mask = labels == label
            centroids[i] = embeddings[mask].mean(0)

        # Compute similarity matrix (N x C)
        sim_matrix = torch.mm(embeddings, centroids.t())
        sim_matrix = self.w * sim_matrix + self.b

        # Target: for each embedding, similarity to its own centroid
        target = torch.zeros_like(sim_matrix)
        for i, emb_label in enumerate(labels):
            class_idx = torch.where(unique_labels == emb_label)[0].item()
            target[i, class_idx] = 1.0

        loss = F.cross_entropy(sim_matrix, target.argmax(dim=1))
        return loss


class TripletLoss(BaseLoss):
    """Triplet loss with semi-hard online mining.

    Reference: FaceNet (Schroff et al. 2015), Rusci & Tuytelaars 2023

    Args:
        margin: Margin for triplet loss
    """

    def __init__(self, margin: float = 0.2):
        super().__init__()
        self.margin = margin

    def forward(self, embeddings: torch.Tensor,
                labels: torch.Tensor) -> torch.Tensor:
        distances = torch.cdist(embeddings, embeddings, p=2)

        # Use a loss that always has a grad_fn: weighted sum over all valid triplets
        loss_terms = []
        for i in range(len(embeddings)):
            pos_mask = (labels == labels[i]) & (torch.arange(
                len(embeddings), device=embeddings.device) != i)
            if pos_mask.sum() == 0:
                continue
            neg_mask = labels != labels[i]
            if neg_mask.sum() == 0:
                continue
            pos_dist = distances[i, pos_mask].max()
            neg_dists = distances[i, neg_mask]
            semi_hard = (neg_dists > pos_dist) & (neg_dists < pos_dist + self.margin)
            if semi_hard.sum() > 0:
                neg_dist = neg_dists[semi_hard].min()
            else:
                neg_dist = neg_dists.min()
            triplet_loss = pos_dist - neg_dist + self.margin
            loss_terms.append(torch.nn.functional.relu(triplet_loss))

        if loss_terms:
            return torch.stack(loss_terms).mean()
        else:
            # Create a dummy loss that still flows gradients
            return (embeddings * 0).sum()
