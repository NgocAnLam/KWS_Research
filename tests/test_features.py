"""Tests for feature extraction: MelSpectrogram and PCEN."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import torch
import numpy as np

from kws_framework.features.features import MelSpectrogram, PCEN, FeatureExtractor


def test_mel_spectrogram_shape():
    mel = MelSpectrogram(n_mels=40)
    waveform = torch.randn(1, 16000)  # 1 second at 16kHz
    spec = mel(waveform)
    # Shape: (1, 40, T) where T ≈ 101 for hop_length=160
    assert spec.dim() == 3, f"Expected 3D, got {spec.dim()}"
    assert spec.shape[1] == 40, f"Expected 40 mel bands, got {spec.shape[1]}"
    assert abs(spec.shape[2] - 101) <= 2, \
        f"Expected ~101 time frames, got {spec.shape[2]}"


def test_mel_no_nan():
    mel = MelSpectrogram(n_mels=40)
    waveform = torch.randn(1, 16000)
    spec = mel(waveform)
    assert not torch.isnan(spec).any(), "NaN in Mel spectrogram"
    assert not torch.isinf(spec).any(), "Inf in Mel spectrogram"


def test_mel_zero_input():
    mel = MelSpectrogram(n_mels=40)
    waveform = torch.zeros(1, 16000)
    spec = mel(waveform)
    assert not torch.isnan(spec).any(), "NaN with zero input"
    assert torch.isfinite(spec).all(), "Inf with zero input"


def test_pcen_shape():
    pcen = PCEN(n_mels=40)
    mel_energy = torch.rand(1, 40, 101) * 100
    out = pcen(torch.log(mel_energy + 1e-6))
    assert out.shape == mel_energy.shape, \
        f"PCEN output shape mismatch: {out.shape} vs {mel_energy.shape}"


def test_pcen_no_nan():
    pcen = PCEN(n_mels=40)
    mel_energy = torch.rand(1, 40, 101) * 100
    out = pcen(torch.log(mel_energy + 1e-6))
    assert not torch.isnan(out).any(), "NaN in PCEN output"
    assert not torch.isinf(out).any(), "Inf in PCEN output"


def test_pcen_trainable_params():
    pcen = PCEN(n_mels=40)
    params = list(pcen.parameters())
    assert len(params) == 4, f"Expected 4 trainable params, got {len(params)}"
    for p in params:
        assert p.requires_grad, "All PCEN params should be trainable"


def test_feature_extractor_log_mel():
    fe = FeatureExtractor(feature_type="log_mel")
    waveform = torch.randn(1, 16000)
    feat = fe(waveform)
    assert feat.shape[1] == 40  # 40 mel bands
    assert feat.dim() == 3


def test_feature_extractor_log_mel_pcen():
    fe = FeatureExtractor(feature_type="log_mel_pcen")
    waveform = torch.randn(1, 16000)
    feat = fe(waveform)
    assert feat.shape[1] == 40
    assert feat.dim() == 3  # (B, C, T)


def test_feature_extractor_backward():
    """Verify gradients flow through feature extractor."""
    fe = FeatureExtractor(feature_type="log_mel_pcen")
    waveform = torch.randn(1, 16000, requires_grad=True)
    feat = fe(waveform)
    loss = feat.sum()
    loss.backward()
    assert waveform.grad is not None, "Gradients should flow to input"
    assert not torch.isnan(waveform.grad).any(), "NaN in gradients"
