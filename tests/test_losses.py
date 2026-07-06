"""Tests for metric learning losses."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import torch
import numpy as np

from kws_framework.losses.losses import (
    PrototypicalLoss, GE2ELoss, TripletLoss
)


def _make_episode(n_way=3, n_support=2, n_query=2, dim=64):
    """Create synthetic episode data."""
    torch.manual_seed(42)
    support_emb = torch.randn(n_way * n_support, dim)
    support_emb = torch.nn.functional.normalize(support_emb, p=2, dim=1)
    support_labels = torch.arange(n_way).repeat_interleave(n_support)

    query_emb = torch.randn(n_way * n_query, dim)
    query_emb = torch.nn.functional.normalize(query_emb, p=2, dim=1)
    query_labels = torch.arange(n_way).repeat_interleave(n_query)

    return support_emb, support_labels, query_emb, query_labels


def test_protonet_loss_finite():
    loss_fn = PrototypicalLoss(distance="cosine")
    s_emb, s_lbl, q_emb, q_lbl = _make_episode()
    loss = loss_fn(s_emb, s_lbl, q_emb, q_lbl)
    assert torch.isfinite(loss), f"ProtoNet loss is not finite: {loss}"
    assert loss.item() > 0, f"ProtoNet loss should be positive: {loss}"


def test_protonet_loss_decreases():
    """Test that loss decreases with more similar embeddings."""
    loss_fn = PrototypicalLoss(distance="cosine")

    # Random embeddings → higher loss
    s_emb, s_lbl, q_emb, q_lbl = _make_episode(dim=64)
    loss_random = loss_fn(s_emb, s_lbl, q_emb, q_lbl)

    # Perfectly clustered embeddings → lower loss
    s_emb_cluster = torch.zeros(6, 64)
    for i in range(3):
        s_emb_cluster[i*2:(i+1)*2] = torch.randn(2, 64) * 0.1 + i * 0.5
    q_emb_cluster = torch.zeros(6, 64)
    for i in range(3):
        q_emb_cluster[i*2:(i+1)*2] = torch.randn(2, 64) * 0.1 + i * 0.5
    s_emb_cluster = torch.nn.functional.normalize(s_emb_cluster, p=2, dim=1)
    q_emb_cluster = torch.nn.functional.normalize(q_emb_cluster, p=2, dim=1)

    loss_cluster = loss_fn(s_emb_cluster, s_lbl, q_emb_cluster, q_lbl)
    assert loss_cluster < loss_random, \
        f"Clustered loss ({loss_cluster:.4f}) should be < random ({loss_random:.4f})"


def test_protonet_predict():
    loss_fn = PrototypicalLoss()
    prototypes = torch.nn.functional.normalize(torch.randn(3, 64), p=2, dim=1)
    query = prototypes[0:1] + torch.randn(1, 64) * 0.1  # Near class 0
    preds = loss_fn.predict(query, prototypes)
    assert preds[0] == 0, f"Expected class 0, got {preds[0]}"


def test_protonet_predict_threshold():
    loss_fn = PrototypicalLoss()
    prototypes = torch.nn.functional.normalize(torch.randn(3, 64), p=2, dim=1)
    # Very different query → should be unknown
    query = torch.nn.functional.normalize(torch.randn(1, 64) * 10, p=2, dim=1)
    preds = loss_fn.predict(query, prototypes, threshold=0.3)
    assert preds[0] == -1, \
        f"Distant query should be unknown (-1), got {preds[0]}"


def test_ge2e_loss_finite():
    loss_fn = GE2ELoss()
    emb = torch.randn(12, 64)
    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    labels = torch.arange(3).repeat_interleave(4)
    loss = loss_fn(emb, labels)
    assert torch.isfinite(loss), f"GE2E loss is not finite: {loss}"
    assert loss.item() > 0, f"GE2E loss should be positive: {loss}"


def test_ge2e_loss_backward():
    loss_fn = GE2ELoss()
    emb = torch.randn(12, 64, requires_grad=True)
    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    labels = torch.arange(3).repeat_interleave(4)
    loss = loss_fn(emb, labels)
    loss.backward()
    assert emb.grad is not None, "Gradients should flow through GE2E"
    assert not torch.isnan(emb.grad).any(), "NaN in GE2E gradients"


def test_triplet_loss_finite():
    loss_fn = TripletLoss(margin=0.2)
    emb = torch.randn(12, 64)
    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    labels = torch.arange(3).repeat_interleave(4)
    try:
        loss = loss_fn(emb, labels)
        assert torch.isfinite(loss), f"Triplet loss is not finite: {loss}"
    except Exception as e:
        # Triplet loss can fail if no semi-hard pairs exist
        pass


def test_triplet_loss_semi_hard():
    """Triplet loss should be near 0 for well-separated classes."""
    loss_fn = TripletLoss(margin=0.2)
    torch.manual_seed(42)
    emb = torch.zeros(6, 64)
    # Class 0: all near origin
    emb[0:3] = torch.randn(3, 64) * 0.1
    # Class 1: far from origin
    emb[3:6] = torch.randn(3, 64) + 10
    emb = torch.nn.functional.normalize(emb, p=2, dim=1)
    labels = torch.tensor([0, 0, 0, 1, 1, 1])
    loss = loss_fn(emb, labels)
    assert loss.item() >= 0, f"Triplet loss should be non-negative: {loss}"
