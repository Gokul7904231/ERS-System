"""
CBAM: Convolutional Block Attention Module
Ref: https://arxiv.org/abs/1807.06521

Combines channel attention and spatial attention to help the
emotion model focus on the most informative facial regions
(eyes, mouth, eyebrows).
"""

import torch
import torch.nn as nn


class ChannelAttention(nn.Module):
    """Channel attention: learns WHICH feature maps are important."""

    def __init__(self, in_channels, reduction=16):
        super().__init__()
        mid = max(in_channels // reduction, 1)
        self.shared_mlp = nn.Sequential(
            nn.Linear(in_channels, mid, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(mid, in_channels, bias=False),
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        # Global average pool → (B, C)
        avg_out = x.mean(dim=[2, 3])
        # Global max pool → (B, C)
        max_out = x.amax(dim=[2, 3])
        # Shared MLP
        att = torch.sigmoid(self.shared_mlp(avg_out) + self.shared_mlp(max_out))
        return x * att.view(b, c, 1, 1)


class SpatialAttention(nn.Module):
    """Spatial attention: learns WHERE to look in the feature map."""

    def __init__(self, kernel_size=7):
        super().__init__()
        pad = kernel_size // 2
        self.conv = nn.Conv2d(2, 1, kernel_size=kernel_size, padding=pad, bias=False)

    def forward(self, x):
        avg_out = x.mean(dim=1, keepdim=True)
        max_out = x.amax(dim=1, keepdim=True)
        combined = torch.cat([avg_out, max_out], dim=1)
        att = torch.sigmoid(self.conv(combined))
        return x * att


class CBAM(nn.Module):
    """CBAM = Channel Attention → Spatial Attention (sequential)."""

    def __init__(self, in_channels, reduction=16, spatial_kernel=7):
        super().__init__()
        self.channel_att = ChannelAttention(in_channels, reduction)
        self.spatial_att = SpatialAttention(spatial_kernel)

    def forward(self, x):
        x = self.channel_att(x)
        x = self.spatial_att(x)
        return x
