"""Minimal decoder-final boundary supervision head for 06_Boundary."""

from __future__ import annotations

import torch
from torch import nn


class BoundaryHead(nn.Module):
    """Predict a single boundary logit map from the final decoder feature."""

    def __init__(self, channels: int, out_channels: int = 1) -> None:
        super().__init__()
        self.refine = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.activation = nn.ReLU(inplace=True)
        self.predict = nn.Conv2d(channels, out_channels, kernel_size=1)

    def forward(self, features: torch.Tensor) -> torch.Tensor:
        return self.predict(self.activation(self.refine(features)))
