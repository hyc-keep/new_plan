"""Minimal LKMA v1 block for the C1 stage."""

from __future__ import annotations

import torch
from torch import nn


class LKMAResidualBlock(nn.Module):
    """Single-branch depth-wise large-kernel spatial mixing block."""

    def __init__(
        self,
        channels: int,
        kernel_size: int = 15,
        use_pwconv: bool = True,
        use_residual: bool = True,
    ) -> None:
        super().__init__()
        if kernel_size not in (15, 21) or kernel_size % 2 == 0:
            raise ValueError("C1 LKMA kernel_size must be odd and one of {15, 21}")
        self.channels = channels
        self.kernel_size = kernel_size
        self.use_pwconv = use_pwconv
        self.use_residual = use_residual
        self.spatial = nn.Conv2d(
            channels,
            channels,
            kernel_size=kernel_size,
            stride=1,
            padding=kernel_size // 2,
            groups=channels,
            bias=False,
        )
        self.channel_mix = nn.Conv2d(channels, channels, kernel_size=1, bias=False) if use_pwconv else nn.Identity()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mixed = self.channel_mix(self.spatial(x))
        if self.use_residual:
            if mixed.shape != x.shape:
                raise RuntimeError("LKMA residual path requires identical input/output shapes")
            return x + mixed
        return mixed


def build_lkma_block(config: dict[str, object]) -> LKMAResidualBlock:
    return LKMAResidualBlock(
        channels=int(config.get("channels", 512)),
        kernel_size=int(config.get("kernel_size", 15)),
        use_pwconv=bool(config.get("use_pwconv", True)),
        use_residual=bool(config.get("use_residual", True)),
    )


__all__ = ["LKMAResidualBlock", "build_lkma_block"]
