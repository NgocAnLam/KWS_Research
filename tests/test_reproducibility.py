"""Tests for reproducibility: same seed → same results."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import random
import numpy as np
import torch
from kws_framework.dataset.dataset import GSCv2Dataset, EpisodeSampler
from kws_framework.models.bc_resnet import BCResNet32

# Use deterministic algorithms
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


def set_all_seeds(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed) if torch.cuda.is_available() else None
    os.environ["PYTHONHASHSEED"] = str(seed)


def test_model_init_reproducibility():
    """Same seed → same model initialization."""
    set_all_seeds(42)
    m1 = BCResNet32(embedding_dim=64)
    params1 = [p.clone().detach() for p in m1.parameters()]

    set_all_seeds(42)
    m2 = BCResNet32(embedding_dim=64)
    params2 = [p.clone().detach() for p in m2.parameters()]

    for i, (p1, p2) in enumerate(zip(params1, params2)):
        assert torch.equal(p1, p2), \
            f"Parameter {i} differs between seeds"


def test_different_seeds_different_model():
    """Different seeds → different model initialization."""
    set_all_seeds(42)
    m1 = BCResNet32(embedding_dim=64)
    p1 = next(m1.parameters()).clone().detach()

    set_all_seeds(43)
    m2 = BCResNet32(embedding_dim=64)
    p2 = next(m2.parameters()).clone().detach()

    assert not torch.equal(p1, p2), \
        "Different seeds should produce different init"


def test_forward_reproducibility():
    """Same model + same input → same output."""
    set_all_seeds(42)
    model = BCResNet32(embedding_dim=64)
    model.eval()

    dummy_input = torch.randn(1, 1, 40, 101)
    out1 = model(dummy_input)

    out2 = model(dummy_input)
    assert torch.allclose(out1, out2, atol=1e-6), \
        "Same input should produce same output"
