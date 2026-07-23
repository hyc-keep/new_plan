"""Boundary supervision loss for 06_Boundary."""

from __future__ import annotations

from typing import Any

import torch
from torch import nn

from .seg_losses import BCEDiceLoss


class BoundaryBCEDiceLoss(nn.Module):
    """Combine frozen segmentation BCE+Dice with weighted boundary BCE."""

    def __init__(self, bce_weight: float, dice_weight: float, eps: float, lambda_boundary: float) -> None:
        super().__init__()
        self.seg_loss = BCEDiceLoss(bce_weight=bce_weight, dice_weight=dice_weight, eps=eps)
        self.boundary_loss = nn.BCEWithLogitsLoss()
        self.lambda_boundary = float(lambda_boundary)

    def forward(
        self,
        outputs: dict[str, torch.Tensor],
        targets: torch.Tensor,
        boundary_targets: torch.Tensor,
    ) -> dict[str, torch.Tensor]:
        seg_losses = self.seg_loss(outputs["seg_logits"], targets)
        loss_boundary = self.boundary_loss(outputs["boundary_logits"], boundary_targets.float())
        loss_total = seg_losses["loss_total"] + self.lambda_boundary * loss_boundary
        return {
            **seg_losses,
            "loss_boundary": loss_boundary,
            "loss_total": loss_total,
        }


def build_boundary_loss(train_config: dict[str, Any]) -> BoundaryBCEDiceLoss:
    return BoundaryBCEDiceLoss(
        bce_weight=float(train_config["bce_weight"]),
        dice_weight=float(train_config["dice_weight"]),
        eps=float(train_config["loss_eps"]),
        lambda_boundary=float(train_config.get("lambda_boundary", 0.3)),
    )
