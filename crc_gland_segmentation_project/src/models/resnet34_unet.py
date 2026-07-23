"""ResNet34 encoder with a U-Net decoder for the 04_Baseline stage.

The implementation is defined from the current 04_Baseline protocol and the
public torchvision ResNet34 API. It emits one-channel segmentation logits.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import torch
from torch import nn
from torchvision.models import resnet34

from .boundary_head import BoundaryHead
from .lkma import LKMAResidualBlock


class DoubleConv(nn.Module):
    """Two convolutional refinements used by the decoder."""

    def __init__(self, in_channels: int, out_channels: int) -> None:
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.block(x)


class DecoderBlock(nn.Module):
    """Bilinear upsampling, optional skip fusion, and convolutional refinement."""

    def __init__(self, in_channels: int, skip_channels: int, out_channels: int) -> None:
        super().__init__()
        self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False)
        self.conv = DoubleConv(in_channels + skip_channels, out_channels)

    def forward(self, x: torch.Tensor, skip: torch.Tensor | None = None) -> torch.Tensor:
        x = self.up(x)
        if skip is not None:
            diff_y = skip.size(2) - x.size(2)
            diff_x = skip.size(3) - x.size(3)
            if diff_y or diff_x:
                x = nn.functional.pad(
                    x,
                    [diff_x // 2, diff_x - diff_x // 2, diff_y // 2, diff_y - diff_y // 2],
                )
            x = torch.cat([skip, x], dim=1)
        return self.conv(x)


class ResNet34UNet(nn.Module):
    """ResNet34-U-Net with optional decoder-final boundary supervision."""

    BN_POLICY_VERSION = "bn_policy_v3_encoder_running_stats_frozen"
    BN_POLICY_SCOPE = "pretrained_encoder"

    def __init__(
        self,
        in_channels: int = 3,
        out_channels: int = 1,
        pretrained: bool = True,
        pretrained_weights_path: str | None = None,
        decoder_channels: tuple[int, int, int, int, int] = (256, 128, 64, 32, 16),
        use_lkma: bool = False,
        lkma_kernel_size: int = 15,
        lkma_use_pwconv: bool = True,
        lkma_use_residual: bool = True,
        use_boundary_head: bool = False,
        use_distance_head: bool = False,
        bn_policy_enabled: bool = False,
    ) -> None:
        super().__init__()
        self.bn_policy_enabled = bn_policy_enabled
        self.pretrained_weights_path = pretrained_weights_path
        if in_channels != 3:
            raise ValueError("ResNet34UNet requires three-channel input")

        weights = None
        encoder = resnet34(weights=None)
        if pretrained:
            weights_path = self._resolve_pretrained_weights_path(getattr(self, "pretrained_weights_path", None))
            state_dict = torch.load(weights_path, map_location="cpu")
            if not isinstance(state_dict, dict):
                raise ValueError(f"local ResNet34 weights must be a state dict: {weights_path}")
            encoder.load_state_dict(state_dict)
            self.pretrained_weights_path = str(weights_path)
            self.pretrained_weights_sha256 = hashlib.sha256(weights_path.read_bytes()).hexdigest()
        else:
            self.pretrained_weights_path = None
            self.pretrained_weights_sha256 = None
        self.stem = nn.Sequential(encoder.conv1, encoder.bn1, encoder.relu)
        self.pool = encoder.maxpool
        self.layer1 = encoder.layer1
        self.layer2 = encoder.layer2
        self.layer3 = encoder.layer3
        self.layer4 = encoder.layer4
        self.lkma = (
            LKMAResidualBlock(
                channels=512,
                kernel_size=lkma_kernel_size,
                use_pwconv=lkma_use_pwconv,
                use_residual=lkma_use_residual,
            )
            if use_lkma
            else nn.Identity()
        )

        d1, d2, d3, d4, d5 = decoder_channels
        self.up1 = DecoderBlock(512, 256, d1)
        self.up2 = DecoderBlock(d1, 128, d2)
        self.up3 = DecoderBlock(d2, 64, d3)
        self.up4 = DecoderBlock(d3, 64, d4)
        self.up5 = DecoderBlock(d4, 0, d5)
        self.head = nn.Conv2d(d5, out_channels, kernel_size=1)
        self.boundary_head = BoundaryHead(d5, out_channels) if use_boundary_head else None
        self.distance_head = nn.Conv2d(d5, out_channels, kernel_size=1) if use_distance_head else None

    @staticmethod
    def _resolve_pretrained_weights_path(value: str | None) -> Path:
        if not value or not value.strip():
            raise ValueError("pretrained_weights_path is required when encoder_pretrained=true")
        path = Path(value).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"local ResNet34 pretrained weights not found: {path}")
        return path

    def apply_encoder_bn_policy(self) -> None:
        """Keep pretrained encoder BN stats frozen while training affine weights."""
        if not self.bn_policy_enabled:
            return
        encoder_modules = (self.stem, self.layer1, self.layer2, self.layer3, self.layer4)
        for module in encoder_modules:
            for child in module.modules():
                if isinstance(child, nn.modules.batchnorm._BatchNorm):
                    child.training = False
                    if child.weight is not None:
                        child.weight.requires_grad = True
                    if child.bias is not None:
                        child.bias.requires_grad = True

    def bn_policy_metadata(self) -> dict[str, Any]:
        return {
            "bn_policy_version": self.BN_POLICY_VERSION,
            "bn_policy_scope": self.BN_POLICY_SCOPE,
            "bn_affine_trainable": True,
        }

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        skip0 = self.stem(x)
        skip1 = self.layer1(self.pool(skip0))
        skip2 = self.layer2(skip1)
        skip3 = self.layer3(skip2)
        bottleneck = self.layer4(skip3)
        bottleneck = self.lkma(bottleneck)

        x = self.up1(bottleneck, skip3)
        x = self.up2(x, skip2)
        x = self.up3(x, skip1)
        x = self.up4(x, skip0)
        x = self.up5(x)
        seg_logits = self.head(x)
        if self.boundary_head is None and self.distance_head is None:
            return seg_logits
        outputs = {"seg_logits": seg_logits}
        if self.boundary_head is not None:
            outputs["boundary_logits"] = self.boundary_head(x)
        if self.distance_head is not None:
            outputs["distance_logits"] = self.distance_head(x)
        return outputs


def build_resnet34_unet(model_config: dict[str, Any]) -> ResNet34UNet:
    """Build the current standard-name model from the frozen model config."""
    weights_path = model_config.get("pretrained_weights_path")
    if bool(model_config.get("encoder_pretrained", True)):
        resolved = ResNet34UNet._resolve_pretrained_weights_path(weights_path)
        expected_hash = str(model_config.get("pretrained_weights_sha256", "")).strip()
        actual_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()
        if expected_hash and actual_hash != expected_hash:
            raise ValueError(f"local ResNet34 pretrained weights SHA256 mismatch: {actual_hash} != {expected_hash}")
    return ResNet34UNet(
        in_channels=int(model_config.get("in_channels", 3)),
        out_channels=int(model_config.get("out_channels", 1)),
        pretrained=bool(model_config.get("encoder_pretrained", True)),
        pretrained_weights_path=model_config.get("pretrained_weights_path"),
        bn_policy_enabled=bool(model_config.get("bn_policy_enabled", False)),
        use_lkma=bool(model_config.get("use_lkma", False)),
        lkma_kernel_size=int(model_config.get("lkma_kernel_size", 15)),
        lkma_use_pwconv=bool(model_config.get("lkma_use_pwconv", True)),
        lkma_use_residual=bool(model_config.get("lkma_use_residual", True)),
        use_boundary_head=bool(model_config.get("use_boundary_head", False)),
        use_distance_head=bool(model_config.get("use_distance_head", False)),
    )
