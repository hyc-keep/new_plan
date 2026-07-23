"""Boundary-target helpers for the frozen 06_Boundary protocol."""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def extract_binary_contour(binary_mask: np.ndarray) -> np.ndarray:
    mask = np.asarray(binary_mask).astype(bool)
    structure = np.ones((3, 3), dtype=bool)
    return np.logical_xor(mask, ndimage.binary_erosion(mask, structure=structure, border_value=0))


def dilate_boundary_band(contour: np.ndarray, width: int = 3) -> np.ndarray:
    if width not in {3, 5}:
        raise ValueError(f"Unsupported boundary width: {width}")
    structure = np.ones((3, 3), dtype=bool)
    return ndimage.binary_dilation(
        np.asarray(contour).astype(bool), structure=structure, iterations=width
    ).astype(np.uint8)


def build_boundary_target(binary_mask: np.ndarray, width: int = 3) -> np.ndarray:
    return dilate_boundary_band(extract_binary_contour(binary_mask), width=width)


def build_boundary_band(binary_mask: np.ndarray, width: int = 3) -> np.ndarray:
    """Backward-compatible name for the frozen contour-band target."""
    return build_boundary_target(binary_mask, width=width)
