"""
BC-ResNet backbone for keyword spotting.
Reference: Kim et al. 2021, "Broadcasted Residual Learning for Efficient Keyword Spotting"
EdgeSpot variant: Buyuksolak et al. 2026

Design (v2.0): BC-ResNet-32 is the primary backbone.
Output: 64-dimensional L2-normalized embedding.
"""

import torch
import torch.nn as nn


class SubSpectralNorm(nn.Module):
    def __init__(self, num_channels):
        super().__init__()
        self.bn = nn.BatchNorm2d(num_channels)

    def forward(self, x):
        return self.bn(x)


class BCResBlock(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3,
                 stride=1, dilation=1):
        super().__init__()
        self.freq_dw = nn.Conv2d(
            in_channels, in_channels, kernel_size=(kernel_size, 1),
            padding=(kernel_size // 2, 0), groups=in_channels, bias=False
        )
        self.subspec_norm = SubSpectralNorm(in_channels)
        self.temporal_dw = nn.Conv2d(
            in_channels, in_channels, kernel_size=(1, kernel_size),
            padding=(0, kernel_size // 2 * dilation),
            dilation=(1, dilation), groups=in_channels, bias=False
        )
        self.pointwise = nn.Conv2d(
            in_channels, out_channels, kernel_size=1, bias=False
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)
        self.skip = nn.Conv2d(in_channels, out_channels, kernel_size=1, bias=False) \
            if in_channels != out_channels else nn.Identity()

    def forward(self, x):
        residual = self.skip(x)
        out = self.freq_dw(x)
        out = self.subspec_norm(out)
        out = self.temporal_dw(out)
        out = self.pointwise(out)
        out = self.bn(out)
        out = self.relu(out + residual)
        return out


class BCResNet32(nn.Module):
    """BC-ResNet-32 backbone.

    Width multiplier t controls channel width (t=1.0 → ~25K, t=2.0 → ~110K).
    Default t=2.0 matches BC-ResNet-32 capacity per original paper.

    Args:
        input_channels: Number of input feature channels (default: 40)
        embedding_dim: Output embedding dimension (default: 64)
        t: Channel width multiplier (default: 2.0)
    """

    def __init__(self, input_channels=40, embedding_dim=64, t=2.5):
        super().__init__()
        c = lambda ch: max(8, int(ch * t // 8) * 8)  # round to nearest 8

        self.conv1 = nn.Sequential(
            nn.Conv2d(1, c(16), kernel_size=(5, 5), stride=(2, 1), padding=(2, 2)),
            nn.BatchNorm2d(c(16)),
            nn.ReLU(inplace=True),
        )

        # Initial conv
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(5, 5), stride=(2, 1), padding=(2, 2)),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
        )

        # Stage 1: 2 blocks, 16→16 ch
        self.stage1 = nn.Sequential(
            BCResBlock(c(16), c(16), stride=1, dilation=1),
            BCResBlock(c(16), c(16), stride=1, dilation=1),
        )
        # Stage 2: 2 blocks, 16→24 ch (stride 2 downsamples freq)
        self.stage2 = nn.Sequential(
            BCResBlock(c(16), c(24), stride=2, dilation=1),
            BCResBlock(c(24), c(24), stride=1, dilation=1),
        )
        # Stage 3: 4 blocks, 24→32 ch (stride 2)
        self.stage3 = nn.Sequential(
            BCResBlock(c(24), c(32), stride=2, dilation=1),
            BCResBlock(c(32), c(32), stride=1, dilation=1),
            BCResBlock(c(32), c(32), stride=1, dilation=2),
            BCResBlock(c(32), c(32), stride=1, dilation=4),
        )
        # Stage 4: 4 blocks, 32→40 ch
        self.stage4 = nn.Sequential(
            BCResBlock(c(32), c(40), stride=1, dilation=8),
            BCResBlock(c(40), c(40), stride=1, dilation=1),
            BCResBlock(c(40), c(40), stride=1, dilation=2),
            BCResBlock(c(40), c(40), stride=1, dilation=4),
        )

        self.temporal_pool = nn.AdaptiveAvgPool2d((1, None))

        self.embedding = nn.Sequential(
            nn.Conv2d(c(40), c(64), kernel_size=1),
            nn.BatchNorm2d(c(64)),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(64, embedding_dim),
        )

        self._initialize_weights()

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = self.stage1(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)
        x = self.temporal_pool(x)
        x = self.embedding(x)
        return torch.nn.functional.normalize(x, p=2, dim=1)
