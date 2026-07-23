"""Aggregate auditable D2 Distance evidence without modifying experiment assets."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import fmean, pstdev
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEEDS = (3407, 1234, 2025)
RUN_PREFIX = "D2_R34UNet_Distance_GlaS_seed"
METRICS = (
    ("f1", "F1"),
    ("objdice", "Object Dice"),
    ("object_hausdorff", "Object Hausdorff"),
    ("dice", "Dice"),
    ("iou", "IoU"),
    ("hd95", "HD95"),
    ("boundary_f1", "Boundary F1"),
)
PROTO_FIELDS = (
    "config_version",
    "data_proto_version",
    "train_proto_version",
    "eval_proto_version",
    "eval_cast_policy",
    "boundary_metric_width",
    "boundary_metric_impl",
    "connected_components_impl",
    "connected_components_connectivity",
    "best_selector",
    "threshold_source",
    "threshold_value",
)
LINEAGE = {
    "source_stage": "B1",
    "source_manifest": "reports/tables/baseline_stage_manifest.csv",
    "source_protocol_version": "eval_proto_v1",
    "source_run_name": "B1_ResNet34_UNet_GlaS_seed3407",
    "consumer_stage": "07_Distance",
    "consumer_file": "reports/tables/distance_per_seed_summary.csv",
    "consumption_boundary": "boundary_input_base",
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def required_run_assets(run_dir: Path) -> list[Path]:
    return [
        run_dir / "run_meta.yaml",
        run_dir / "config.yaml",
        run_dir / "checkpoints" / "best.ckpt",
        run_dir / "testA_metrics.csv",
        run_dir / "testB_metrics.csv",
    ]


def independent_check_path(seed: int) -> Path:
    return PROJECT_ROOT / "notes" / f"independent_metric_check_D2_R34UNet_Distance_GlaS_seed{seed}.json"


def validate_and_collect() -> tuple[list[dict[str, Any]], dict[int, dict[str, Any]], list[str]]:
    blockers: list[str] = []
    metas: dict[int, dict[str, Any]] = {}
    per_seed: list[dict[str, Any]] = []
    proto_reference: dict[str, str] | None = None

    source_manifest = PROJECT_ROOT / "reports/tables/baseline_stage_manifest.csv"
    baseline_table = PROJECT_ROOT / "reports/tables/baseline_mean_std.csv"
    if not source_manifest.exists():
        blockers.append(f"missing_source_manifest:{rel(source_manifest)}")
    if not baseline_table.exists():
        blockers.append(f"missing_baseline_mean_std:{rel(baseline_table)}")

    for seed in SEEDS:
        run_name = f"{RUN_PREFIX}{seed}"
        run_dir = PROJECT_ROOT / "experiments" / run_name
        missing = [rel(path) for path in required_run_assets(run_dir) if not path.exists()]
        if missing:
            blockers.append(f"seed{seed}:missing_assets={missing}")
            continue
        meta = read_yaml(run_dir / "run_meta.yaml")
        config = read_yaml(run_dir / "config.yaml")
        metas[seed] = meta
        expected_identity = {
            "run_name": run_name,
            "stage_code": "D2_Distance",
            "dataset_code": "glas",
            "model_name": "resnet34_unet_distance",
            "train_seed": seed,
            "eval_proto_version": "eval_proto_v1",
            "best_selector": "val_objdice_max",
            "threshold_source": "val17",
            "checkpoint_identity_status": "pass",
            "metric_crosscheck_result": "pass",
        }
        for field, expected in expected_identity.items():
            actual = meta.get(field)
            if (int(actual) if field == "train_seed" else str(actual)) != expected:
                blockers.append(f"seed{seed}:identity_mismatch:{field}={actual!r},expected={expected!r}")
        experiment = config.get("experiment", {})
        config_identity = {
            "run_name": run_name,
            "stage_code": "D2_Distance",
            "dataset_code": "glas",
            "model_name": "resnet34_unet_distance",
            "train_seed": seed,
            "source_stage": "B1",
            "source_manifest": LINEAGE["source_manifest"],
            "source_protocol_version": "eval_proto_v1",
            "consumer_stage": "07_Distance",
            "consumption_boundary": "boundary_input_base",
        }
        for field, expected in config_identity.items():
            actual = experiment.get(field)
            if (int(actual) if field == "train_seed" else str(actual)) != expected:
                blockers.append(f"seed{seed}:config_identity_mismatch:{field}={actual!r},expected={expected!r}")
        distance_config = experiment.get("distance", {})
        for field, expected in (("target_version", "EDT_norm01_v1"), ("loss_type", "SmoothL1"), ("lambda_dist", 0.1)):
            actual = distance_config.get(field)
            if (float(actual) if field == "lambda_dist" else str(actual)) != expected:
                blockers.append(f"seed{seed}:distance_config_mismatch:{field}={actual!r},expected={expected!r}")
        current_proto = {field: str(meta.get(field, "")) for field in PROTO_FIELDS}
        if proto_reference is None:
            proto_reference = current_proto
        elif current_proto != proto_reference:
            blockers.append(f"protocol_mismatch:seed{seed}:{current_proto}")

        check_path = independent_check_path(seed)
        if not check_path.exists():
            blockers.append(f"seed{seed}:missing_independent_check:{rel(check_path)}")
        else:
            check = json.loads(check_path.read_text(encoding="utf-8"))
            if check.get("status") != "pass":
                blockers.append(f"seed{seed}:independent_check_not_pass:{check.get('status')!r}")
            for split, expected_count in (("testA", 60), ("testB", 20)):
                split_check = check.get("splits", {}).get(split, {})
                if split_check.get("status") != "pass" or split_check.get("sample_count") != expected_count:
                    blockers.append(f"seed{seed}:{split}:independent_check_invalid")

        checkpoint = run_dir / "checkpoints" / "best.ckpt"
        declared_sha = str(meta.get("best_checkpoint_sha256", ""))
        if declared_sha and declared_sha != sha256(checkpoint):
            blockers.append(f"seed{seed}:checkpoint_sha256_mismatch")

        for split, expected_count in (("testA", 60), ("testB", 20)):
            rows = read_csv(run_dir / f"{split}_metrics.csv")
            sample_rows = [row for row in rows if row.get("row_type") == "sample"]
            if len(sample_rows) != expected_count or len({row.get("sample_id") for row in sample_rows}) != expected_count:
                blockers.append(f"seed{seed}:{split}:sample_identity_or_count_invalid")
            for key, _name in METRICS:
                values = []
                for row in sample_rows:
                    try:
                        value = float(row[key])
                    except (KeyError, TypeError, ValueError):
                        value = math.nan
                    values.append(value)
                if len(values) != expected_count or not all(math.isfinite(value) for value in values):
                    blockers.append(f"seed{seed}:{split}:{key}:nonfinite_or_missing")
                else:
                    per_seed.append({
                        **LINEAGE,
                        "run_name": run_name,
                        "stage": "D2_Distance",
                        "dataset": "GlaS",
                        "model_name": str(meta.get("model_name", "")),
                        "seed": seed,
                        "split_role": split,
                        "metric_name": _name,
                        "metric_key": key,
                        "metric_value": fmean(values),
                        "sample_count": expected_count,
                        "checkpoint_path": rel(checkpoint),
                        "checkpoint_sha256": sha256(checkpoint),
                        "independent_metric_check_path": rel(check_path),
                        "result_tag": str(meta.get("result_tag", "")),
                        "aggregation": "single_seed",
                        "evidence_status": "blocked" if blockers else "pass",
                    })
    if len(metas) != len(SEEDS):
        blockers.append(f"three_seed_identity_incomplete:found={sorted(metas)} expected={list(SEEDS)}")
    return per_seed, metas, blockers


def aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for split in ("testA", "testB"):
        for key, name in METRICS:
            selected = [row for row in rows if row["split_role"] == split and row["metric_key"] == key]
            values = [float(row["metric_value"]) for row in selected]
            complete = len(values) == len(SEEDS)
            output.append({
                **LINEAGE,
                "stage": "D2_Distance",
                "dataset": "GlaS",
                "model_name": "resnet34_unet_distance",
                "split_role": split,
                "metric_name": name,
                "metric_key": key,
                "mean": fmean(values) if complete else "BLOCKED",
                "std": pstdev(values) if complete else "BLOCKED",
                "n_runs": len(values),
                "seeds": ",".join(str(seed) for seed in SEEDS),
                "aggregation": "mean+-std_population_ddof0",
                "evidence_status": "pass" if complete else "blocked",
            })
    return output


def compare(distance_rows: list[dict[str, Any]], baseline_path: Path, status: str) -> list[dict[str, Any]]:
    baseline = {(row.get("split_role"), row.get("metric_name")): row for row in read_csv(baseline_path)}
    output = []
    for row in distance_rows:
        base = baseline.get((row["split_role"], row["metric_name"]), {})
        ready = row["evidence_status"] == "pass" and base.get("mean") not in (None, "")
        output.append({
            **LINEAGE,
            "split_role": row["split_role"],
            "metric_name": row["metric_name"],
            "metric_key": row["metric_key"],
            "baseline_mean": base.get("mean", "BLOCKED"),
            "baseline_std": base.get("std", "BLOCKED"),
            "distance_mean": row["mean"],
            "distance_std": row["std"],
            "delta_distance_minus_baseline": (
                float(row["mean"]) - float(base["mean"]) if ready else "BLOCKED"
            ),
            "n_runs": row["n_runs"],
            "seeds": row["seeds"],
            "aggregation": "mean+-std_population_ddof0",
            "evidence_status": "pass" if ready and status == "pass" else "blocked",
        })
    return output


def manifest(metas: dict[int, dict[str, Any]], status: str, blockers: list[str], paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows = []
    for seed in SEEDS:
        run_name = f"{RUN_PREFIX}{seed}"
        run_dir = PROJECT_ROOT / "experiments" / run_name
        meta = metas.get(seed, {})
        checkpoint = run_dir / "checkpoints" / "best.ckpt"
        check_path = independent_check_path(seed)
        rows.append({
            **LINEAGE,
            "stage": "D2_Distance",
            "seed": seed,
            "run_name": run_name,
            "run_dir": rel(run_dir),
            "testA_metrics_path": rel(run_dir / "testA_metrics.csv"),
            "testB_metrics_path": rel(run_dir / "testB_metrics.csv"),
            "checkpoint_path": rel(checkpoint),
            "checkpoint_sha256": sha256(checkpoint) if checkpoint.exists() else "BLOCKED",
            "checkpoint_identity_status": meta.get("checkpoint_identity_status", "BLOCKED"),
            "independent_metric_check_path": rel(check_path),
            "independent_metric_check_status": "pass" if check_path.exists() and json.loads(check_path.read_text(encoding="utf-8")).get("status") == "pass" else "BLOCKED",
            "stage_evidence_status": status,
            "blocker_count": len(blockers),
        })
    rows.append({
        **LINEAGE,
        "stage": "D2_Distance",
        "seed": "aggregate",
        "run_name": "D2_R34UNet_Distance_stage",
        "run_dir": "",
        "testA_metrics_path": rel(paths["per_seed"]),
        "testB_metrics_path": rel(paths["mean_std"]),
        "checkpoint_path": "",
        "checkpoint_sha256": "",
        "checkpoint_identity_status": "not_applicable",
        "independent_metric_check_path": "",
        "independent_metric_check_status": "not_applicable",
        "stage_evidence_status": status,
        "blocker_count": len(blockers),
    })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate D2 Distance evidence.")
    parser.add_argument("--dry-run", action="store_true", help="Validate real inputs without writing outputs.")
    args = parser.parse_args()
    per_seed, metas, blockers = validate_and_collect()
    status = "pass" if not blockers and len(per_seed) == len(SEEDS) * 2 * len(METRICS) else "blocked"
    mean_std = aggregate(per_seed)
    baseline_path = PROJECT_ROOT / "reports/tables/baseline_mean_std.csv"
    comparison = compare(mean_std, baseline_path, status)
    paths = {
        "per_seed": PROJECT_ROOT / "reports/tables/distance_per_seed_summary.csv",
        "mean_std": PROJECT_ROOT / "reports/tables/distance_mean_std.csv",
        "comparison": PROJECT_ROOT / "reports/tables/current_base_vs_distance_mean_std.csv",
        "manifest": PROJECT_ROOT / "reports/tables/distance_stage_manifest.csv",
    }
    if not args.dry_run:
        per_fields = list(per_seed[0].keys()) if per_seed else list(LINEAGE) + ["evidence_status"]
        mean_fields = list(mean_std[0].keys())
        compare_fields = list(comparison[0].keys())
        manifest_rows = manifest(metas, status, blockers, paths)
        write_csv(paths["per_seed"], per_seed, per_fields)
        write_csv(paths["mean_std"], mean_std, mean_fields)
        write_csv(paths["comparison"], comparison, compare_fields)
        write_csv(paths["manifest"], manifest_rows, list(manifest_rows[0].keys()))
    print(json.dumps({"status": status, "dry_run": args.dry_run, "per_seed_rows": len(per_seed), "mean_std_rows": len(mean_std), "comparison_rows": len(comparison), "blockers": blockers, "outputs": {key: rel(path) for key, path in paths.items()}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
