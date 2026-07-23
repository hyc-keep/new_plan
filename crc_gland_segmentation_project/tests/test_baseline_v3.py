import math

import numpy as np

from src.metrics.seg_metrics import boundary_f1_score, hd95_score, object_hausdorff_score
from scripts.summarize_stage import _evaluate_stability


def test_empty_distance_policy_uses_dmax():
    pred = np.zeros((3, 4), dtype=np.uint8)
    target = np.zeros_like(pred)
    assert hd95_score(pred, target) == 0.0
    pred[0, 0] = 1
    assert math.isclose(hd95_score(pred, target), math.hypot(2, 3), rel_tol=1e-6)
    assert object_hausdorff_score(pred, target) == math.hypot(2, 3)


def test_boundary_v3_fixed_shape_and_tolerance():
    mask = np.zeros((9, 9), dtype=np.uint8)
    mask[2:7, 2:7] = 1
    assert boundary_f1_score(mask, mask) == 1.0
    try:
        boundary_f1_score(mask, mask, width=2)
    except ValueError:
        pass
    else:
        raise AssertionError("v3 boundary width must be fixed to 3")


def test_stability_gate_uses_frozen_six_units_and_tolerance():
    rows = {}
    for split in ("testA", "testB"):
        for metric in ("F1", "Object Dice", "Object Hausdorff", "Dice", "IoU", "HD95", "Boundary F1"):
            rows[(split, metric)] = {"unet_std": "1.0", "r34unet_std": "1.0"}
    assert _evaluate_stability(rows) == (True, [])
    rows[("testB", "HD95")]["r34unet_std"] = "999.0"
    assert _evaluate_stability(rows)[0] is True
    rows[("testB", "Object Dice")]["r34unet_std"] = "1.000000000002"
    assert _evaluate_stability(rows)[0] is False
