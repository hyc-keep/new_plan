"""Independently recompute saved segmentation metrics from GT and prediction PNGs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]

import sys

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data import load_mask_array
from src.metrics.seg_metrics import compute_sample_segmentation_metrics

METRIC_NAMES = (
    "dice",
    "iou",
    "objdice",
    "f1",
    "boundary_f1",
    "hd95",
    "object_hausdorff",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read formal metric CSVs and independently recompute metrics from PNG assets."
    )
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument("--run-name", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--atol", type=float, default=1.0e-6)
    return parser.parse_args()


def _resolve_project_path(project_root: Path, raw_path: str) -> Path:
    candidate = Path(raw_path)
    return candidate if candidate.is_absolute() else project_root / candidate


def _finite_close(expected: float, actual: float, atol: float) -> bool:
    if math.isnan(expected) and math.isnan(actual):
        return True
    if not math.isfinite(expected) or not math.isfinite(actual):
        return False
    return abs(expected - actual) <= atol


def _check_split(project_root: Path, csv_path: Path, atol: float) -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row.get("row_type") == "sample"]

    mismatches: list[dict[str, Any]] = []
    missing_assets: list[dict[str, str]] = []
    max_abs_error = {metric: 0.0 for metric in METRIC_NAMES}
    for row in rows:
        gt_path = _resolve_project_path(project_root, row["eval_gt_path"])
        pred_path = _resolve_project_path(project_root, row["pred_path"])
        if not gt_path.exists() or not pred_path.exists():
            missing_assets.append(
                {
                    "sample_id": row.get("sample_id", ""),
                    "mask_path": gt_path.as_posix(),
                    "pred_path": pred_path.as_posix(),
                }
            )
            continue

        target = load_mask_array(gt_path) > 0
        prediction = load_mask_array(pred_path) > 0
        if target.shape != prediction.shape:
            raise ValueError(
                f"evaluation asset shape mismatch for {row.get('sample_id', '')}: "
                f"gt={target.shape}, prediction={prediction.shape}"
            )
        recomputed = compute_sample_segmentation_metrics(
            prediction,
            target,
            boundary_width=int(row.get("boundary_metric_width") or 3),
            connectivity=int(row.get("boundary_metric_connectivity") or 8),
            include_distance_metrics=True,
        )
        row_mismatches: dict[str, Any] = {}
        for metric in METRIC_NAMES:
            recorded = float(row[metric])
            actual = float(recomputed[metric])
            if math.isfinite(recorded) and math.isfinite(actual):
                max_abs_error[metric] = max(max_abs_error[metric], abs(recorded - actual))
            if not _finite_close(recorded, actual, atol):
                row_mismatches[metric] = {"recorded": recorded, "recomputed": actual}
        if row_mismatches:
            mismatches.append(
                {"sample_id": row.get("sample_id", ""), "metrics": row_mismatches}
            )

    return {
        "csv_path": csv_path.relative_to(project_root).as_posix(),
        "sample_count": len(rows),
        "missing_assets": missing_assets,
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "max_abs_error": max_abs_error,
        "status": "pass" if not missing_assets and not mismatches else "fail",
    }


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    run_dir = project_root / "experiments" / args.run_name
    split_reports = {}
    for split in ("testA", "testB"):
        csv_path = run_dir / f"{split}_metrics.csv"
        if not csv_path.exists():
            raise FileNotFoundError(csv_path)
        split_reports[split] = _check_split(project_root, csv_path, args.atol)

    report = {
        "run_name": args.run_name,
        "check_type": "independent_png_gt_metric_recomputation",
        "metric_implementation": "src.metrics.seg_metrics.compute_sample_segmentation_metrics",
        "target_resize_policy": "forbidden_shape_mismatch_fails",
        "atol": args.atol,
        "splits": split_reports,
        "status": "pass" if all(item["status"] == "pass" for item in split_reports.values()) else "fail",
    }
    output_path = (
        Path(args.output).resolve()
        if args.output
        else project_root / "notes" / f"independent_metric_check_{args.run_name}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
