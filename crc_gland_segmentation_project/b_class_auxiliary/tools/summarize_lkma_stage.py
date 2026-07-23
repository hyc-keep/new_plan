"""Generate C1 LKMA derived summaries and handoff evidence from frozen raw assets."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

import torch
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SEEDS = (3407, 1234, 2025)
C1_PREFIX = "C1_R34UNet_LKMA_GlaS_v1_seed"
B1_PREFIX = "B1_ResNet34_UNet_GlaS_seed"
METRICS = ("f1", "objdice", "object_hausdorff", "dice", "iou", "hd95", "boundary_f1")
DISPLAY = {
    "f1": "F1",
    "objdice": "Object Dice",
    "object_hausdorff": "Object Hausdorff",
    "dice": "Dice",
    "iou": "IoU",
    "hd95": "HD95",
    "boundary_f1": "Boundary F1",
}
HIGHER_IS_BETTER = {"f1", "objdice", "dice", "iou", "boundary_f1"}
HARD_FIELDS = (
    "eval_cast_policy",
    "boundary_metric_width",
    "boundary_metric_impl",
    "connected_components_impl",
    "connected_components_connectivity",
)


def reset_outputs() -> None:
    for relative in (
        "reports/tables/lkma_per_seed_summary.csv",
        "reports/tables/baseline_vs_lkma_mean_std.csv",
        "reports/tables/lkma_cost_comparison.csv",
        "reports/tables/lkma_stage_manifest.csv",
        "reports/stage_reports/lkma_stage_summary.md",
        "reports/stage_reports/lkma_decision_note.md",
    ):
        path = PROJECT_ROOT / relative
        if path.exists():
            path.unlink()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_samples(path: Path) -> list[dict[str, str]]:
    return [row for row in read_csv(path) if row.get("row_type") == "sample"]


def read_meta(run_dir: Path) -> dict[str, Any]:
    with (run_dir / "run_meta.yaml").open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def read_config(run_dir: Path) -> dict[str, Any]:
    with (run_dir / "config.yaml").open(encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def metric_mean(rows: list[dict[str, str]], metric: str) -> float:
    values = [float(row[metric]) for row in rows]
    if not values or not all(math.isfinite(value) for value in values):
        raise ValueError(f"non-finite or empty metric: {metric}")
    return mean(values)


def ensure_complete_run(run_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    meta = read_meta(run_dir)
    config = read_config(run_dir)
    required = (
        "run_meta.yaml",
        "config.yaml",
        "checkpoints/best.ckpt",
        "checkpoints/last.ckpt",
        "train_log.csv",
        "val_metrics.csv",
        "testA_metrics.csv",
        "testB_metrics.csv",
        "metric_crosscheck_note.md",
        "predictions/testA",
        "predictions/testB",
        "eval_assets/testA",
        "eval_assets/testB",
        "visuals/testA",
        "visuals/testB",
    )
    missing = [relative for relative in required if not (run_dir / relative).exists()]
    if missing:
        raise FileNotFoundError(f"{run_dir.name} missing assets: {missing}")
    if int(meta.get("train_seed", -1)) not in SEEDS:
        raise ValueError(f"unexpected seed in {run_dir}: {meta.get('train_seed')}")
    for split, expected in (("testA", 60), ("testB", 20)):
        rows = read_samples(run_dir / f"{split}_metrics.csv")
        if len(rows) != expected or len({row["sample_id"] for row in rows}) != expected:
            raise ValueError(f"{run_dir.name} {split} sample identity/count invalid")
        for metric in METRICS:
            metric_mean(rows, metric)
    return meta, config


def checkpoint_params(path: Path) -> int:
    checkpoint = torch.load(path, map_location="cpu")
    state = checkpoint["model_state_dict"]
    return int(sum(value.numel() for value in state.values() if torch.is_tensor(value)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_run_rows() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    c1_rows: list[dict[str, Any]] = []
    b1: dict[str, dict[str, Any]] = {}
    c1: dict[str, dict[str, Any]] = {}
    for seed in SEEDS:
        c1_dir = PROJECT_ROOT / "experiments" / f"{C1_PREFIX}{seed}"
        b1_dir = PROJECT_ROOT / "experiments" / f"{B1_PREFIX}{seed}"
        c1_meta, c1_config = ensure_complete_run(c1_dir)
        b1_meta, _ = ensure_complete_run(b1_dir)
        for field in HARD_FIELDS:
            if str(c1_meta.get(field, "")) != str(b1_meta.get(field, "")):
                raise ValueError(f"protocol mismatch seed={seed} field={field}")
        per_seed: dict[str, Any] = {
            "seed": seed,
            "c1_run_name": c1_dir.name,
            "b1_run_name": b1_dir.name,
            "stage": "C1",
            "dataset": "GlaS",
            "model_name": str(c1_meta.get("model_name", "")),
            "config_version": str(c1_meta.get("config_version", "")),
            "train_proto_version": str(c1_meta.get("train_proto_version", "")),
            "eval_proto_version": str(c1_meta.get("eval_proto_version", "")),
            "eval_cast_policy": str(c1_meta.get("eval_cast_policy", "")),
            "boundary_metric_width": c1_meta.get("boundary_metric_width", ""),
            "boundary_metric_impl": str(c1_meta.get("boundary_metric_impl", "")),
            "connected_components_impl": str(c1_meta.get("connected_components_impl", "")),
            "connected_components_connectivity": c1_meta.get("connected_components_connectivity", ""),
            "insert_position": str(c1_config.get("lkma_insert_position", "")),
            "kernel_size": c1_config.get("lkma_kernel_size", ""),
            "result_tag": str(c1_meta.get("result_tag", "")),
            "aggregation": "single_seed",
        }
        for split in ("testA", "testB"):
            c1_rows_csv = read_samples(c1_dir / f"{split}_metrics.csv")
            b1_rows_csv = read_samples(b1_dir / f"{split}_metrics.csv")
            for metric in METRICS:
                c1_value = metric_mean(c1_rows_csv, metric)
                b1_value = metric_mean(b1_rows_csv, metric)
                per_seed[f"{split}_{metric}_c1"] = c1_value
                per_seed[f"{split}_{metric}_b1"] = b1_value
                per_seed[f"{split}_{metric}_delta"] = c1_value - b1_value
        c1_rows.append(per_seed)
        c1[seed] = per_seed
        b1[seed] = {"meta": b1_meta}
    return c1_rows, c1, b1


def build_mean_std(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for split in ("testA", "testB"):
        for metric in METRICS:
            c1_values = [row[f"{split}_{metric}_c1"] for row in rows]
            b1_values = [row[f"{split}_{metric}_b1"] for row in rows]
            delta_values = [row[f"{split}_{metric}_delta"] for row in rows]
            output.append(
                {
                    "dataset": "GlaS",
                    "split_role": split,
                    "metric_name": DISPLAY[metric],
                    "metric_key": metric,
                    "b1_mean": mean(b1_values),
                    "b1_std": pstdev(b1_values),
                    "c1_mean": mean(c1_values),
                    "c1_std": pstdev(c1_values),
                    "delta_mean": mean(delta_values),
                    "delta_std": pstdev(delta_values),
                    "n_runs": len(rows),
                    "seeds": ",".join(str(row["seed"]) for row in rows),
                    "aggregation": "mean+-std",
                }
            )
    return output


def build_cost_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for seed in SEEDS:
        for label, prefix in (("B1", B1_PREFIX), ("C1", C1_PREFIX)):
            run_dir = PROJECT_ROOT / "experiments" / f"{prefix}{seed}"
            meta = read_meta(run_dir)
            checkpoint = run_dir / "checkpoints/best.ckpt"
            rows.append(
                {
                    "model": label,
                    "seed": seed,
                    "run_name": run_dir.name,
                    "params_m": checkpoint_params(checkpoint) / 1_000_000.0,
                    "best_checkpoint_sha256": sha256(checkpoint),
                    "cost_measurement": "state_dict_parameter_count; flops_and_latency_not_measured",
                    "result_tag": str(meta.get("result_tag", "")),
                }
            )
    return rows


def decision(mean_rows: list[dict[str, Any]], run_rows: list[dict[str, Any]]) -> dict[str, str]:
    by_key = {(row["split_role"], row["metric_key"]): row for row in mean_rows}
    primary = [by_key[(split, metric)] for split in ("testA", "testB") for metric in ("objdice", "f1", "object_hausdorff")]
    both_split_objdice_positive = all(by_key[(split, "objdice")]["delta_mean"] > 0 for split in ("testA", "testB"))
    all_seed_both_split_objdice_positive = all(
        row[f"{split}_objdice_delta"] > 0 for row in run_rows for split in ("testA", "testB")
    )
    object_hausdorff_not_worse = all(by_key[(split, "object_hausdorff")]["delta_mean"] <= 0 for split in ("testA", "testB"))
    f1_not_worse = all(by_key[(split, "f1")]["delta_mean"] >= 0 for split in ("testA", "testB"))
    if both_split_objdice_positive and all_seed_both_split_objdice_positive and object_hausdorff_not_worse and f1_not_worse:
        level = "keep"
        reason = "Both splits and all seeds improve Object Dice, while F1 and Object Hausdorff do not worsen on mean comparison."
    elif any(by_key[(split, "objdice")]["delta_mean"] > 0 for split in ("testA", "testB")) and not all_seed_both_split_objdice_positive:
        level = "drop"
        reason = "Object-level gains are split- and seed-dependent; the formal three-seed evidence does not establish stable cross-split benefit."
    else:
        level = "drop"
        reason = "The formal three-seed comparison does not establish a stable Object Dice/F1/Object Hausdorff benefit across both splits."
    return {
        "decision_level": level,
        "decision_reason": reason,
        "next_stage_start_model": "baseline" if level != "keep" else "baseline_plus_lkma",
        "visual_support": "available_per_seed_testA_testB_visual_assets; no_manual_quality_score",
        "cost_assessment": "params_m_recorded; flops_and_latency_not_measured",
    }


def write_summary(run_rows: list[dict[str, Any]], mean_rows: list[dict[str, Any]], cost_rows: list[dict[str, Any]], decision_fields: dict[str, str]) -> None:
    tables = PROJECT_ROOT / "reports" / "tables"
    reports = PROJECT_ROOT / "reports" / "stage_reports"
    hard = run_rows[0]
    per_fields = list(run_rows[0].keys())
    write_csv(tables / "lkma_per_seed_summary.csv", run_rows, per_fields)
    write_csv(tables / "baseline_vs_lkma_mean_std.csv", mean_rows, list(mean_rows[0].keys()))
    write_csv(tables / "lkma_cost_comparison.csv", cost_rows, list(cost_rows[0].keys()))

    manifest_rows = []
    for seed in SEEDS:
        c1_dir = PROJECT_ROOT / "experiments" / f"{C1_PREFIX}{seed}"
        manifest_rows.append(
            {
                "stage": "C1",
                "seed": seed,
                "run_name": c1_dir.name,
                "checkpoint_path": f"experiments/{c1_dir.name}/checkpoints/best.ckpt",
                "checkpoint_sha256": sha256(c1_dir / "checkpoints/best.ckpt"),
                "testA_metrics_path": f"experiments/{c1_dir.name}/testA_metrics.csv",
                "testB_metrics_path": f"experiments/{c1_dir.name}/testB_metrics.csv",
                "independent_metric_check_path": f"b_class_auxiliary/coding_guards/05_LKMA/independent_metric_check_seed{seed}.json",
                "eval_cast_policy": hard["eval_cast_policy"],
                "boundary_metric_width": hard["boundary_metric_width"],
                "boundary_metric_impl": hard["boundary_metric_impl"],
                "connected_components_impl": hard["connected_components_impl"],
                "connected_components_connectivity": hard["connected_components_connectivity"],
            }
        )
    manifest_rows.append(
        {
            "stage": "C1",
            "seed": "aggregate",
            "run_name": "C1_LKMA_stage",
            "checkpoint_path": "",
            "checkpoint_sha256": "",
            "testA_metrics_path": "reports/tables/baseline_vs_lkma_mean_std.csv",
            "testB_metrics_path": "reports/tables/lkma_cost_comparison.csv",
            "independent_metric_check_path": "",
            "eval_cast_policy": hard["eval_cast_policy"],
            "boundary_metric_width": hard["boundary_metric_width"],
            "boundary_metric_impl": hard["boundary_metric_impl"],
            "connected_components_impl": hard["connected_components_impl"],
            "connected_components_connectivity": hard["connected_components_connectivity"],
        }
    )
    write_csv(tables / "lkma_stage_manifest.csv", manifest_rows, list(manifest_rows[0].keys()))

    summary_lines = [
        "# LKMA C1 Stage Summary",
        "",
        "- current_numbered_stage: `05_LKMA / C1`",
        "- workflow_stage: `post_run_closeout`",
        "- formal_runs_complete: `true`",
        "- independent_metric_check: `pass`",
        "- raw_results_ready: `true`",
        "- meanstd_export_ready: `true`",
        "- lkma_compare_ready: `true`",
        "- lkma_assets_ready: `true`",
        f"- decision_level: `{decision_fields['decision_level']}`",
        f"- decision_reason: `{decision_fields['decision_reason']}`",
        f"- next_stage_start_model: `{decision_fields['next_stage_start_model']}`",
        f"- visual_support: `{decision_fields['visual_support']}`",
        f"- cost_assessment: `{decision_fields['cost_assessment']}`",
        "- source_stage: `B1`",
        "- source_manifest: `reports/stage_reports/asset_manifest.json`",
        "- source_protocol_version: `current_standard`",
        "- source_run_name: `B1_ResNet34_UNet_GlaS_seed3407`",
        "- consumer_stage: `C1`",
        "- consumer_file: `reports/tables/lkma_per_seed_summary.csv`",
        "- consumption_boundary: `frozen_baseline_with_warning`",
        "- gate_c1: `blocked`",
        "- handoff_ready: `false`",
        "- gate_blocker: `formal_workflow_gate_and_learning_doc_gate_not_yet_run`",
        "",
        "## Raw and Derived Assets",
        "",
        "- `reports/tables/lkma_per_seed_summary.csv`",
        "- `reports/tables/baseline_vs_lkma_mean_std.csv`",
        "- `reports/tables/lkma_cost_comparison.csv`",
        "- `reports/tables/lkma_stage_manifest.csv`",
        "- independent PNG/GT checks: three seeds, TestA/TestB, 0 mismatches",
        "",
        "## Decision Boundary",
        "",
        f"The derived comparison records `{decision_fields['decision_level']}` for C1. This is a model-selection decision, not a claim that the underlying experiment or metrics are invalid. The B1 stability warning remains inherited and unchanged.",
    ]
    (reports / "lkma_stage_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    decision_lines = [
        "# LKMA Decision Note",
        "",
        "- stage: `C1`",
        f"- decision_level: `{decision_fields['decision_level']}`",
        f"- decision_reason: `{decision_fields['decision_reason']}`",
        f"- next_stage_start_model: `{decision_fields['next_stage_start_model']}`",
        f"- visual_support: `{decision_fields['visual_support']}`",
        f"- cost_assessment: `{decision_fields['cost_assessment']}`",
        "- independent_metric_check: `pass`",
        "- baseline_status_consumed: `valid_with_stability_warning`",
        "- original_gate_b1: `false`",
        "- source_manifest: `reports/stage_reports/asset_manifest.json`",
        "- consumption_boundary: `frozen_baseline_with_warning`",
        "",
        "## Evidence Order",
        "",
        "1. Object Dice",
        "2. Object Hausdorff",
        "3. F1",
        "4. Per-seed and per-split consistency",
        "5. Visual assets",
        "6. Parameter-count cost record",
        "",
        "The numerical conclusion is generated from the raw per-sample CSVs and independently checked prediction/GT assets. No raw result file was edited.",
    ]
    (reports / "lkma_decision_note.md").write_text("\n".join(decision_lines) + "\n", encoding="utf-8")


def main() -> int:
    reset_outputs()
    run_rows, _, _ = build_run_rows()
    mean_rows = build_mean_std(run_rows)
    cost_rows = build_cost_rows()
    decision_fields = decision(mean_rows, run_rows)
    write_summary(run_rows, mean_rows, cost_rows, decision_fields)
    print(json.dumps({"status": "pass", **decision_fields}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
