"""
BC-ResNet-32 backbone for keyword spotting.

Reference: Kim et al. 2021, "Broadcasted Residual Learning for Efficient Keyword Spotting"
EdgeSpot variant: Buyuksolak et al. 2026 (uses Fused BC-ResBlocks + SDPA)

Design decision (v2.0): BC-ResNet-32 is the primary backbone.
Output: 64-dimensional embedding (matching EdgeSpot and DMA-KWS).
"""

import torch
import torch.nn as nn


class SubSpectralNorm(nn.Module):
    """SubSpectral Normalization: average activation along frequency dim."""

    def __init__(self, num_channels):
        super().__init__()
        self.bn = nn.BatchNorm2d(num_channels)

    def forward(self, x):
        return self.bn(x)


class BCResBlock(nn.Module):
    """BC-ResBlock: frequency-depthwise conv + temporal depthwise conv + pointwise conv."""

    def __init__(self, in_channels, out_channels, kernel_size=3,
                 stride=1, dilation=1):
        super().__init__()
        self.freq_dw = nn.Conv2d(
            in_channels, in_channels, kernel_size=(kernel_size, 1),
            padding=(kernel_size // 2, 0),
            groups=in_channels, bias=False
        )
        self.subspec_norm = SubSpectralNorm(in_channels)
        self.temporal_dw = nn.Conv2d(
            in_channels, in_channels, kernel_size=(1, kernel_size),
            padding=(0, kernel_size // 2 * dilation),
            dilation=(1, dilation),
            groups=in_channels, bias=False
        )
        self.pointwise = nn.Conv2d(
            in_channels, out_channels, kernel_size=1, bias=False
        )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU(inplace=True)

        # Residual connection
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

    Output: 64-dimensional embedding vector.

    Args:
        input_channels: Number of input feature channels (default: 40 for mel bands)
        embedding_dim: Output embedding dimension (default: 64)
    """

    def __init__(self, input_channels=40, embedding_dim=64):
        super().__init__()

        # Initial conv: 5x5
        self.conv1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(5, 5), stride=(2, 1), padding=(2, 2)),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
        )

        # BC-ResBlocks with increasing channels
        self.block1 = BCResBlock(16, 8, stride=1, dilation=1)
        self.block2 = BCResBlock(8, 12, stride=2, dilation=1)
        self.block3 = BCResBlock(12, 16, stride=2, dilation=1)
        self.block4 = BCResBlock(16, 20, stride=1, dilation=1)

        # Temporal pooling
        self.temporal_pool = nn.AdaptiveAvgPool2d((1, None))

        # Final projection to embedding
        self.embedding = nn.Sequential(
            nn.Conv2d(20, 32, kernel_size=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(32, embedding_dim),
        )

        self._initialize_weights()

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out",
                                        nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, 1, F, T) where F=mel bands, T=time frames
        x = self.conv1(x)
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)
        x = self.temporal_pool(x)
        x = self.embedding(x)
        # L2-normalize
        x = torch.nn.functional.normalize(x, p=2, dim=1)
        return x
