"""Distance-target helpers for the frozen data protocol."""

from __future__ import annotations

import math

import numpy as np
from scipy.ndimage import distance_transform_edt


def _edt_1d(values: np.ndarray) -> np.ndarray:
    length = len(values)
    v = np.zeros(length, dtype=np.int32)
    z = np.zeros(length + 1, dtype=np.float64)
    output = np.zeros(length, dtype=np.float64)
    k = 0
    v[0] = 0
    z[0] = -math.inf
    z[1] = math.inf
    for q in range(1, length):
        s = ((values[q] + q * q) - (values[v[k]] + v[k] * v[k])) / (2.0 * (q - v[k]))
        while s <= z[k]:
            k -= 1
            s = ((values[q] + q * q) - (values[v[k]] + v[k] * v[k])) / (2.0 * (q - v[k]))
        k += 1
        v[k] = q
        z[k] = s
        z[k + 1] = math.inf
    k = 0
    for q in range(length):
        while z[k + 1] < q:
            k += 1
        output[q] = (q - v[k]) * (q - v[k]) + values[v[k]]
    return output


def euclidean_distance_transform(binary_mask: np.ndarray) -> np.ndarray:
    return distance_transform_edt(np.asarray(binary_mask) > 0).astype(np.float64, copy=False)


def build_distance_target(binary_mask: np.ndarray) -> np.ndarray:
    mask = np.asarray(binary_mask) > 0
    if not mask.any() or mask.all():
        return np.zeros(mask.shape, dtype=np.float32)
    inside = euclidean_distance_transform(mask)
    outside = euclidean_distance_transform(~mask)
    signed = inside - outside
    minimum = float(signed.min())
    maximum = float(signed.max())
    if maximum <= minimum:
        return np.zeros(mask.shape, dtype=np.float32)
    return ((signed - minimum) / (maximum - minimum)).astype(np.float32)


def normalize_distance_map(distance_map: np.ndarray) -> np.ndarray:
    maximum = float(distance_map.max())
    if maximum <= 0.0:
        return distance_map.astype(np.float32)
    return (distance_map / maximum).astype(np.float32)
