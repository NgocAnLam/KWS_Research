"""
Feature extraction: Log-Mel Spectrogram and PCEN.

Design decisions (v2.0):
- Primary: Log-Mel (40 bands)
- Ablation: Log-Mel + PCEN
- Historical baseline: MFCC (13 coeffs)
- Parameters from EdgeSpot 2026: 40 mel bands, 25ms window, 10ms hop
"""

import torch
import torch.nn as nn
import torchaudio


class MelSpectrogram(nn.Module):
    """Log-Mel spectrogram extraction.

    Args:
        sample_rate: Audio sample rate (Hz)
        n_fft: FFT size
        hop_length: Hop length (samples)
        win_length: Window length (samples)
        n_mels: Number of mel bands
        f_min: Minimum frequency (Hz)
        f_max: Maximum frequency (Hz)
    """

    def __init__(self, sample_rate=16000, n_fft=512, hop_length=160,
                 win_length=400, n_mels=40, f_min=0, f_max=8000):
        super().__init__()
        self.mel_spec = torchaudio.transforms.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=n_fft,
            hop_length=hop_length,
            win_length=win_length,
            n_mels=n_mels,
            f_min=f_min,
            f_max=f_max,
            power=2.0,
            normalized=True,
        )
        self.eps = 1e-6

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        spec = self.mel_spec(waveform)
        log_spec = torch.log(spec + self.eps)
        return log_spec


class PCEN(nn.Module):
    """Per-Channel Energy Normalization.

    Replaces static log compression with per-channel automatic gain control.
    All parameters are trainable. Zero additional inference cost.

    Args:
        n_mels: Number of mel bands
        s: Smoothing coefficient (IIR smoother)
        alpha: AGC strength
        delta: Bias
        r: Root compression exponent
        eps: Small constant for numerical stability

    Reference: Wang et al. 2017, EdgeSpot (Buyuksolak et al. 2026)
    """

    def __init__(self, n_mels=40, s=0.025, alpha=0.98, delta=2.0, r=0.5, eps=1e-6):
        super().__init__()
        self.n_mels = n_mels
        self.eps = eps

        # Trainable parameters (channel-shared per EdgeSpot)
        self.s = nn.Parameter(torch.tensor(s))
        self.alpha = nn.Parameter(torch.tensor(alpha))
        self.delta = nn.Parameter(torch.tensor(delta))
        self.r = nn.Parameter(torch.tensor(r))

    def forward(self, mel_energy: torch.Tensor) -> torch.Tensor:
        B, C, T = mel_energy.shape
        device = mel_energy.device

        s = torch.sigmoid(self.s)
        alpha = torch.sigmoid(self.alpha)
        delta = torch.nn.functional.softplus(self.delta)
        r = torch.sigmoid(self.r)

        # Causal IIR smoother
        M = torch.zeros(B, C, device=device)
        out = torch.zeros_like(mel_energy)

        for t in range(T):
            M = (1 - s) * M + s * mel_energy[:, :, t]
            smoothed = mel_energy[:, :, t] / (self.eps + M) ** alpha + delta
            out[:, :, t] = smoothed ** r - delta ** r

        return out


class FeatureExtractor(nn.Module):
    """Combined feature extractor: Mel + optional PCEN.

    Args:
        feature_type: "log_mel" or "log_mel_pcen"
        n_mels: Number of mel bands
    """

    def __init__(self, feature_type: str = "log_mel", n_mels: int = 40):
        super().__init__()
        self.feature_type = feature_type
        self.mel = MelSpectrogram(n_mels=n_mels)

        if feature_type == "log_mel_pcen":
            self.pcen = PCEN(n_mels=n_mels)
        elif feature_type == "log_mel":
            self.pcen = None
        else:
            raise ValueError(f"Unknown feature type: {feature_type}")

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        mel_energy = self.mel(waveform)
        if self.pcen is not None:
            return self.pcen(mel_energy)
        return mel_energy
