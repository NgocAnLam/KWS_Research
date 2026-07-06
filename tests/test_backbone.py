"""Tests for BC-ResNet-32 backbone."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import torch
from kws_framework.models.bc_resnet import BCResNet32


def test_backbone_output_shape():
    model = BCResNet32(embedding_dim=64)
    dummy_input = torch.randn(1, 1, 40, 101)  # (B, C, F, T)
    output = model(dummy_input)
    assert output.shape == (1, 64), \
        f"Expected (1, 64), got {output.shape}"


def test_backbone_l2_normalized():
    model = BCResNet32(embedding_dim=64)
    model.eval()
    dummy_input = torch.randn(4, 1, 40, 101)
    output = model(dummy_input)
    norms = torch.norm(output, p=2, dim=1)
    assert torch.allclose(norms, torch.ones_like(norms), atol=1e-5), \
        f"Embeddings not L2-normalized: norms = {norms}"


def test_backbone_different_inputs_different_embeddings():
    model = BCResNet32(embedding_dim=64)
    model.eval()
    input1 = torch.randn(1, 1, 40, 101)
    input2 = torch.randn(1, 1, 40, 101) * 10
    emb1 = model(input1)
    emb2 = model(input2)
    cos_sim = torch.nn.functional.cosine_similarity(emb1, emb2)
    assert cos_sim < 0.99, \
        "Different inputs should produce different embeddings"


def test_backbone_forward_backward():
    model = BCResNet32(embedding_dim=64)
    dummy_input = torch.randn(2, 1, 40, 101, requires_grad=True)
    output = model(dummy_input)
    loss = output.sum()
    loss.backward()
    assert dummy_input.grad is not None, "Gradients should flow"
    assert not torch.isnan(dummy_input.grad).any(), "NaN in gradients"


def test_backbone_param_count():
    model = BCResNet32(embedding_dim=64)
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    assert 80_000 < total < 150_000, \
        f"Unexpected param count: {total} (expected ~110K)"
    assert total == trainable, "All params should be trainable"
