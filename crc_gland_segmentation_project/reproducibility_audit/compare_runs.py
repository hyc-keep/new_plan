"""Compare two formal runs for reproducibility audit evidence."""

from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_METADATA_DIFFERENCES = {"run_name", "timestamp", "created_at", "updated_at", "output_dir", "run_dir"}
REQUIRED_FILES = ("run_meta.yaml", "train_log.csv", "val_metrics.csv", "testA_metrics.csv", "testB_metrics.csv", "checkpoints/best.ckpt", "checkpoints/last.ckpt")
STRICT_METADATA_KEYS = {"config_version", "stage_code", "dataset_code", "model_name", "model_version", "train_proto_version", "eval_proto_version", "train_seed", "best_checkpoint_path", "best_checkpoint_sha256", "best_checkpoint_epoch", "best_metric_value", "data_config_sha256", "split_manifest_sha256", "asset_manifest_sha256", "dataset_files_sha256", "initial_model_state_sha256", "pretrained_weights_path", "pretrained_weights_sha256", "source_tree_sha256", "frozen_source_config_sha256", "reproducibility", "executable", "git_commit"}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def compare_csv(left: Path, right: Path) -> tuple[bool, str]:
    left_rows, right_rows = load_csv(left), load_csv(right)
    if len(left_rows) != len(right_rows):
        return False, f"row_count {len(left_rows)} != {len(right_rows)}"
    differences: list[str] = []
    for row_index, (left_row, right_row) in enumerate(zip(left_rows, right_rows), start=2):
        if list(left_row) != list(right_row):
            differences.append(f"row {row_index} columns differ")
            continue
        for key in left_row:
            if key in {"run_name", "seed", "checkpoint_relative_path"}:
                continue
            try:
                left_value, right_value = float(left_row[key]), float(right_row[key])
                same = math.isclose(left_value, right_value, rel_tol=0.0, abs_tol=0.0)
            except ValueError:
                same = left_row[key] == right_row[key]
            if not same:
                differences.append(f"row {row_index} {key}: {left_row[key]!r} != {right_row[key]!r}")
    return (not differences, "all compared CSV values identical" if not differences else "; ".join(differences[:20]))


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, item in value.items():
            result.update(flatten(item, f"{prefix}.{key}" if prefix else str(key)))
        return result
    return {prefix: value}


def compare_checkpoint(left: Path, right: Path) -> tuple[bool, str]:
    import torch

    left_checkpoint = torch.load(left, map_location="cpu")
    right_checkpoint = torch.load(right, map_location="cpu")
    differences: list[str] = []

    def compare_value(key: str, left_value: Any, right_value: Any) -> None:
        if key == "run_name":
            return
        if torch.is_tensor(left_value) or torch.is_tensor(right_value):
            if not (torch.is_tensor(left_value) and torch.is_tensor(right_value)):
                differences.append(f"{key}: tensor/non-tensor mismatch")
            elif left_value.dtype != right_value.dtype or left_value.shape != right_value.shape or not torch.equal(left_value, right_value):
                differences.append(f"{key}: tensor values differ")
            return
        if isinstance(left_value, dict) or isinstance(right_value, dict):
            if not (isinstance(left_value, dict) and isinstance(right_value, dict)):
                differences.append(f"{key}: mapping/non-mapping mismatch")
                return
            for child_key in sorted(set(left_value) | set(right_value)):
                if child_key not in left_value or child_key not in right_value:
                    differences.append(f"{key}.{child_key}: missing")
                else:
                    compare_value(f"{key}.{child_key}", left_value[child_key], right_value[child_key])
            return
        if isinstance(left_value, (list, tuple)) or isinstance(right_value, (list, tuple)):
            if not (isinstance(left_value, (list, tuple)) and isinstance(right_value, (list, tuple))) or len(left_value) != len(right_value):
                differences.append(f"{key}: sequence differs")
                return
            for index, (left_item, right_item) in enumerate(zip(left_value, right_value)):
                compare_value(f"{key}[{index}]", left_item, right_item)
            return
        if left_value != right_value:
            differences.append(f"{key}: {left_value!r} != {right_value!r}")

    compare_value("checkpoint", left_checkpoint, right_checkpoint)
    return (not differences, "all checkpoint states identical" if not differences else "; ".join(differences[:20]))


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_runs.py RUN_A RUN_B")
    left, right = ROOT / sys.argv[1], ROOT / sys.argv[2]
    if not left.is_dir() or not right.is_dir():
        raise SystemExit("both run directories must exist")
    failures: list[str] = []
    for relative in REQUIRED_FILES:
        if not (left / relative).is_file():
            failures.append(f"left missing: {relative}")
        if not (right / relative).is_file():
            failures.append(f"right missing: {relative}")
    if failures:
        for item in failures:
            print(f"FAIL {item}")
        return 1
    left_meta = yaml.safe_load((left / "run_meta.yaml").read_text(encoding="utf-8")) or {}
    right_meta = yaml.safe_load((right / "run_meta.yaml").read_text(encoding="utf-8")) or {}
    left_flat, right_flat = flatten(left_meta), flatten(right_meta)
    keys = set(left_flat) | set(right_flat)
    for key in sorted(keys):
        field = key.rsplit(".", 1)[-1]
        if field in ALLOWED_METADATA_DIFFERENCES:
            continue
        if left_flat.get(key) != right_flat.get(key):
            failures.append(f"metadata {key}: {left_flat.get(key)!r} != {right_flat.get(key)!r}")
    for key in sorted(STRICT_METADATA_KEYS):
        if key in {"executable", "git_commit"}:
            present = (
                "reproducibility" in left_meta
                and "reproducibility" in right_meta
                and key in left_meta["reproducibility"]
                and key in right_meta["reproducibility"]
            )
        else:
            present = key in left_meta and key in right_meta
        if not present:
            failures.append(f"required metadata missing: {key}")
    for key in ("executable", "git_commit"):
        for label, meta in (("left", left_meta), ("right", right_meta)):
            value = meta.get("reproducibility", {}).get(key)
            if not isinstance(value, str) or not value.strip() or value == "unavailable":
                failures.append(f"{label} reproducibility.{key} is missing or unavailable")
    for relative in ("train_log.csv", "val_metrics.csv", "testA_metrics.csv", "testB_metrics.csv"):
        same, detail = compare_csv(left / relative, right / relative)
        print(f"{relative}_equal={same} detail={detail}")
        if not same:
            failures.append(f"CSV {relative}: {detail}")
    for relative in ("checkpoints/best.ckpt", "checkpoints/last.ckpt"):
        same, detail = compare_checkpoint(left / relative, right / relative)
        print(f"{relative}_state_equal={same} detail={detail}")
        if not same:
            failures.append(f"checkpoint state {relative}: {detail}")
    if failures:
        print("REPRODUCIBILITY_AUDIT=FAIL")
        for item in failures:
            print(f"DIFF {item}")
        return 1
    print("REPRODUCIBILITY_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
