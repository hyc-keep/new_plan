"""Public model builders for the current project stages."""

from __future__ import annotations

from typing import Any

import torch

from .boundary_head import BoundaryHead
from .lkma import LKMAResidualBlock, build_lkma_block
from .resnet34_unet import ResNet34UNet, build_resnet34_unet
from .unet import UNet, build_unet_model as build_standard_unet


def build_unet_model(model_config: dict[str, Any]) -> torch.nn.Module:
    """Route the frozen model configuration to the requested model builder."""
    name = str(model_config.get("name", "UNet"))
    if name == "ResNet34UNet":
        return build_resnet34_unet(model_config)
    return build_standard_unet(model_config)


__all__ = [
    "UNet",
    "ResNet34UNet",
    "BoundaryHead",
    "LKMAResidualBlock",
    "build_lkma_block",
    "build_unet_model",
    "build_resnet34_unet",
]
