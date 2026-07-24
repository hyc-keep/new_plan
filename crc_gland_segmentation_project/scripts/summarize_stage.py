"""
对应阶段: 03_UNet稳定性
理论依据:
  - 本脚本为项目自研聚合逻辑，无直接外部论文对应
  - 公式/定义: mean = Σx_i/n, std = √(Σ(x_i-μ)²/n) (population std, n=3)
  - 多 seed 聚合: 阶段实现卡要求 3-seed 独立训练后做 mean±std 汇总 (seeds=3407,1234,2025)
  - 协议一致性校验: 所有 run_meta.yaml 的 eval_cast_policy/boundary_metric_*/connected_components_* 必须完全一致
  - A2 验收门: gate_a2 = complete_runs ∧ proto_consistent ∧ raw_results_ready ∧ failure_summary_ready
  - 协议字段: _PROTO_CONSISTENCY_FIELDS 定义了跨 run 必须一致的 10 个字段
代码参考:
  - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
  - 文件: scripts/summarize_stage.py
  - commit: project_internal
  - 许可证: project_internal
  - 本项目调整: 专为三段式实验链 A2 验收设计，从 train.py/test.py 的产物中聚合跨 seed 结果
冻结回链: 结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md
  - FORMAL_CONNECTIVITY=8, FORMAL_BOUNDARY_WIDTH=3, FORMAL_CAST_POLICY=float32_before_threshold, FORMAL_BEST_SELECTOR=val_objdice_max, FORMAL_THRESHOLD_SOURCE=val17
跨阶段说明: 本文件最初在 03_UNet稳定性 阶段落地 A2 聚合逻辑，并在 04_Baseline 阶段扩展了
  对称的 B1 (ResNet34-U-Net) 聚合与验收分支（见文件下半部分 B1 区块）；A2 函数保持只读，
  B1 产物路径与 A2 完全隔离。
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from pathlib import Path
import sys
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

FORMAL_CONNECTIVITY = 8
FORMAL_BOUNDARY_WIDTH = 3
FORMAL_CAST_POLICY = "float32_before_threshold"
FORMAL_BEST_SELECTOR = "val_objdice_max"
FORMAL_THRESHOLD_SOURCE = "val17"

# A2 阶段常量（03_UNet稳定性）
A2_SEEDS = [3407, 1234, 2025]
A2_N_RUNS = 3
A2_RUN_PREFIX = "A2_UNet_GlaS_seed"
A2_V3_RUN_PREFIX = "A2_UNet_GlaS_seed"

# B1 阶段常量（04_Baseline ResNet34-U-Net）
# 对应阶段: 04_Baseline
# 理论依据: 计划 04_阶段验收.md §5.3 要求三个固定 seed 完整存在
# 代码参考: 本项目自建，与 A2 对称
B1_SEEDS = [3407, 1234, 2025]
B1_N_RUNS = 3
B1_RUN_PREFIX = "B1_ResNet34_UNet_GlaS_seed"

_METRIC_COL_TO_NAME = {
    "f1": "F1",
    "objdice": "Object Dice",
    "object_hausdorff": "Object Hausdorff",
    "dice": "Dice",
    "iou": "IoU",
    "hd95": "HD95",
    "boundary_f1": "Boundary F1",
}

_MIN_METRIC_COLS = ["f1", "objdice", "object_hausdorff", "dice", "iou", "hd95", "boundary_f1"]
_REQUIRED_COMPARE_METRICS = [
    "F1",
    "Object Dice",
    "Object Hausdorff",
    "Dice",
    "IoU",
    "HD95",
    "Boundary F1",
]
_MAIN_COMPARE_METRICS = ["F1", "Object Dice", "Object Hausdorff"]
_LOWER_IS_BETTER_METRICS = {"Object Hausdorff", "HD95"}
_COMPARE_PROTO_FIELDS = [
    "data_proto_version",
    "train_proto_version",
    "eval_proto_version",
    "best_selector",
    "threshold_source",
    "threshold_value",
    "eval_cast_policy",
    "boundary_metric_width",
    "boundary_metric_impl",
    "connected_components_impl",
    "connected_components_connectivity",
    "batch_size",
]
_REQUIRED_MANIFEST_KEYS = [
    "B1_run_3407_dir",
    "B1_run_1234_dir",
    "B1_run_2025_dir",
    "baseline_per_seed_summary",
    "baseline_mean_std",
    "unet_vs_r34unet_comparison",
    "baseline_stage_summary",
    "freeze_best_selector",
    "freeze_threshold_source",
    "freeze_threshold_value",
    "freeze_eval_proto_version",
    "freeze_eval_cast_policy",
    "freeze_boundary_metric_width",
    "freeze_boundary_metric_impl",
    "freeze_connected_components_impl",
    "freeze_connected_components_connectivity",
    "freeze_result_tag",
    "freeze_aggregation",
    "handoff_ready_for_c1",
]

_PROTO_CONSISTENCY_FIELDS = [
    "config_version",
    "data_proto_version",
    "train_proto_version",
    "eval_proto_version",
    "eval_cast_policy",
    "threshold_value",
    "boundary_metric_width",
    "boundary_metric_impl",
    "connected_components_impl",
    "connected_components_connectivity",
    "best_selector",
    "threshold_source",
]
_CURRENT_IDENTITY_FIELDS = (
    "config_version",
    "train_proto_version",
    "eval_proto_version",
    "bn_policy_version",
)
_CURRENT_MANIFEST_CANDIDATES = (
    PROJECT_ROOT / "reports" / "tables" / "current_baseline_manifest.csv",
    PROJECT_ROOT / "reports" / "tables" / "baseline_v3_stage_manifest.csv",
    PROJECT_ROOT / "reports" / "tables" / "current_stage_manifest.csv",
)


def _current_a2_aggregate_path(run_specs: dict[str, dict[str, Any]]) -> Path:
    for manifest_path in _CURRENT_MANIFEST_CANDIDATES:
        rows = _load_csv_rows(manifest_path)
        for row in rows:
            key = str(row.get("asset_key", "")).strip().lower()
            path = str(row.get("relative_path", "")).strip()
            if key in {"a2_mean_std_summary", "a2_aggregate", "mean_std_summary"} and path:
                return PROJECT_ROOT / path
    a2_names = sorted(spec["run_name"] for spec in run_specs.values() if spec["stage_code"] == "A2")
    if len(a2_names) == 3:
        prefix = re.sub(r"(?:3407|1234|2025)$", "", a2_names[0])
        expected_names = {f"{prefix}{seed}" for seed in A2_SEEDS}
        if set(a2_names) == expected_names:
            return PROJECT_ROOT / "reports" / "tables" / "unet_v3_mean_std_summary.csv"
    raise RuntimeError("current manifest/contract does not identify an A2 aggregate; refusing legacy aggregate fallback")
_CURRENT_STAGE_CONTRACT = (
    PROJECT_ROOT / "b_class_auxiliary" / "coding_guards" / "04_Baseline" / "stage_contract.yaml"
)


def _load_current_run_specs() -> dict[str, dict[str, Any]]:
    """Load the current six-run identity from a manifest, or the current contract."""
    for manifest_path in _CURRENT_MANIFEST_CANDIDATES:
        rows = _load_csv_rows(manifest_path)
        specs = {}
        for row in rows:
            run_name = str(row.get("run_name", "")).strip()
            if not run_name:
                continue
            specs[run_name] = {
                "run_name": run_name,
                "seed": _parse_int(row.get("seed"), default=0),
                "stage_code": str(row.get("stage_code", "")).strip(),
                "output_dir": str(row.get("output_dir", row.get("run_dir", ""))).strip(),
            }
        if len(specs) == 6:
            return specs
    if not _CURRENT_STAGE_CONTRACT.exists():
        raise RuntimeError("current-round manifest/contract missing; refusing legacy run discovery")
    contract = yaml.safe_load(_CURRENT_STAGE_CONTRACT.read_text(encoding="utf-8"))
    specs = {}
    for item in contract.get("runs", []):
        if not isinstance(item, dict) or not str(item.get("run_name", "")).strip():
            continue
        run_name = str(item["run_name"]).strip()
        specs[run_name] = {
            "run_name": run_name,
            "seed": _parse_int(item.get("seed"), default=0),
            "stage_code": run_name.split("_", 1)[0],
            "output_dir": str(item.get("output_dir", f"experiments/{run_name}")),
        }
    if len(specs) != 6:
        raise RuntimeError(f"current-round contract must define exactly six runs, got {len(specs)}")
    return specs


def _validate_current_run_identity(run_dir: Path, meta: dict[str, Any], spec: dict[str, Any]) -> list[str]:
    errors = []
    expected = {
        "run_name": spec["run_name"],
        "train_seed": spec["seed"],
        "stage_code": spec["stage_code"],
    }
    for field, expected_value in expected.items():
        actual = meta.get(field)
        try:
            matches = int(actual) == int(expected_value) if field == "train_seed" else str(actual) == str(expected_value)
        except (TypeError, ValueError):
            matches = False
        if not matches:
            errors.append(f"{run_dir.name}:{field} expected={expected_value!r} actual={actual!r}")
    expected_dir = (PROJECT_ROOT / spec["output_dir"]).resolve()
    if run_dir.resolve() != expected_dir:
        errors.append(f"{run_dir.name}:output_dir expected={expected_dir} actual={run_dir.resolve()}")
    for field in _CURRENT_IDENTITY_FIELDS:
        if str(meta.get(field, "")).strip() == "":
            errors.append(f"{run_dir.name}:{field} missing_or_empty")
    return errors


def _validate_aggregate_identity(agg_csv: Path, run_metas: dict[int, dict[str, Any]], label: str) -> None:
    rows = _load_csv_rows(agg_csv)
    if not rows:
        raise RuntimeError(f"{label} aggregate missing_or_empty: {agg_csv}")
    expected_values = {
        field: {str(meta.get(field, "")).strip() for meta in run_metas.values()}
        for field in _CURRENT_IDENTITY_FIELDS
    }
    mismatches = []
    for field, values in expected_values.items():
        if len(values) != 1 or "" in values:
            mismatches.append(f"{field}:run_meta_values={sorted(values)}")
            continue
        expected = next(iter(values))
        actual_values = {str(row.get(field, "")).strip() for row in rows}
        if actual_values != {expected}:
            mismatches.append(f"{field}:aggregate_values={sorted(actual_values)} expected={expected!r}")
    if mismatches:
        raise RuntimeError(f"{label} aggregate identity mismatch: {'; '.join(mismatches)}")



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize formal stage02 acceptance state.")
    parser.add_argument("--config", required=True, help="Relative path to the experiment config.")
    parser.add_argument("--run-name", default=None, help="Optional run name override.")
    parser.add_argument(
        "--debug-note",
        default="notes/debug_note.md",
        help="Relative path to the structured debug note.",
    )
    parser.add_argument(
        "--stage-summary-output",
        default="reports/stage_reports/unet_flow_stage_summary.md",
        help="Relative path for the stage summary markdown.",
    )
    parser.add_argument(
        "--manifest-output",
        default="reports/tables/unet_flow_stage_manifest.csv",
        help="Relative path for the stage manifest csv.",
    )
    return parser.parse_args()


def _relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1"}:
            return True
        if lowered in {"false", "no", "0"}:
            return False
    return bool(value)


def _parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _parse_markdown_fields(path: Path) -> dict[str, str]:
    pattern = re.compile(r"^- ([a-zA-Z0-9_]+): `?(.*?)`?$")
    fields: dict[str, str] = {}
    if not path.exists():
        return fields
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw_line.strip())
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def _load_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _load_csv_aggregate_row(path: Path) -> dict[str, str]:
    rows = [row for row in _load_csv_rows(path) if row.get("row_type") == "sample"]
    if not rows:
        return {}
    aggregate = {"sample_count": str(len(rows))}
    for metric_col in _MIN_METRIC_COLS:
        values = [float(row[metric_col]) for row in rows]
        aggregate[metric_col] = str(sum(values) / len(values))
    return aggregate


def _parse_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _rows_by_split_metric(rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        split_role = str(row.get("split_role", "")).strip()
        metric_name = str(row.get("metric_name", "")).strip()
        if split_role and metric_name:
            index[(split_role, metric_name)] = row
    return index


def _load_stage_run_metas(run_prefix: str, seeds: list[int]) -> dict[int, dict[str, Any]]:
    experiments_root = PROJECT_ROOT / "experiments"
    run_metas: dict[int, dict[str, Any]] = {}
    for seed in seeds:
        run_dir = experiments_root / f"{run_prefix}{seed}"
        meta = _read_run_meta(run_dir)
        if meta is not None:
            run_metas[seed] = meta
    return run_metas


def _expected_compare_pairs() -> list[tuple[str, str]]:
    return [
        (split_role, metric_name)
        for split_role in ("testA", "testB")
        for metric_name in _REQUIRED_COMPARE_METRICS
    ]


def _collect_missing_compare_pairs(rows_by_key: dict[tuple[str, str], dict[str, Any]]) -> list[str]:
    missing = []
    for split_role, metric_name in _expected_compare_pairs():
        if (split_role, metric_name) not in rows_by_key:
            missing.append(f"{split_role}:{metric_name}")
    return missing


def _collect_missing_raw_pairs(raw_rows: list[dict[str, Any]], seeds: list[int]) -> list[str]:
    present = {
        (
            str(row.get("seed", "")).strip(),
            str(row.get("split_role", "")).strip(),
            str(row.get("metric_name", "")).strip(),
        )
        for row in raw_rows
    }
    missing = []
    for seed in seeds:
        for split_role, metric_name in _expected_compare_pairs():
            key = (str(seed), split_role, metric_name)
            if key not in present:
                missing.append(f"seed{seed}:{split_role}:{metric_name}")
    return missing


def _collect_compare_proto_mismatches(
    a2_meta: dict[str, Any],
    b1_meta: dict[str, Any],
) -> list[str]:
    mismatches = []
    for field in _COMPARE_PROTO_FIELDS:
        a2_value = str(a2_meta.get(field, "")).strip()
        b1_value = str(b1_meta.get(field, "")).strip()
        if a2_value != b1_value:
            mismatches.append(f"{field}:{b1_value}!={a2_value}")
    return mismatches


def _evaluate_main_metric_direction(
    compare_rows_by_key: dict[tuple[str, str], dict[str, Any]],
) -> tuple[bool, list[str]]:
    failures = []
    for split_role in ("testA", "testB"):
        for metric_name in _MAIN_COMPARE_METRICS:
            row = compare_rows_by_key.get((split_role, metric_name), {})
            a2_mean = _parse_float(row.get("unet_mean"))
            b1_mean = _parse_float(row.get("r34unet_mean"))
            if a2_mean is None or b1_mean is None:
                failures.append(f"{split_role}:{metric_name}:missing_mean")
                continue
            is_not_worse = b1_mean <= a2_mean if metric_name in _LOWER_IS_BETTER_METRICS else b1_mean >= a2_mean
            if not is_not_worse:
                failures.append(f"{split_role}:{metric_name}:{b1_mean:.6f} vs {a2_mean:.6f}")
    return len(failures) == 0, failures


def _evaluate_stability(
    compare_rows_by_key: dict[tuple[str, str], dict[str, Any]],
) -> tuple[bool, list[str]]:
    """裁决冻结三主指标×TestA/TestB 六个稳定性单元。"""
    failures = []
    for split_role in ("testA", "testB"):
        for metric_name in _MAIN_COMPARE_METRICS:
            row = compare_rows_by_key.get((split_role, metric_name), {})
            a2_std = _parse_float(row.get("unet_std"))
            b1_std = _parse_float(row.get("r34unet_std"))
            if a2_std is None or b1_std is None:
                failures.append(f"{split_role}:{metric_name}:missing_std:fail")
                continue
            tolerance = 1.0e-12 * max(1.0, a2_std)
            if b1_std > a2_std + tolerance:
                failures.append(f"{split_role}:{metric_name}:{b1_std:.6f}>{a2_std:.6f}+{tolerance:.3e}:fail")
    return len(failures) == 0, failures


def _collect_missing_qualitative_assets(run_dirs: dict[int, Path]) -> list[str]:
    missing = []
    for seed in B1_SEEDS:
        run_dir = run_dirs.get(seed)
        if run_dir is None:
            missing.append(f"seed{seed}:run_dir_missing")
            continue
        required_paths = [
            run_dir / "summaries" / "error_cases.md",
            run_dir / "visuals" / "testA",
            run_dir / "visuals" / "testB",
        ]
        for path in required_paths:
            if not path.exists():
                missing.append(_relative_path(path))
    return missing


def _manifest_rows_by_key(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row.get("asset_key", "")).strip(): row
        for row in _load_csv_rows(path)
        if str(row.get("asset_key", "")).strip()
    }


def _manifest_value(manifest_rows: dict[str, dict[str, Any]], asset_key: str) -> str:
    row = manifest_rows.get(asset_key, {})
    return str(row.get("relative_path", "")).strip()


def _manifest_exists_flag(manifest_rows: dict[str, dict[str, Any]], asset_key: str) -> bool:
    row = manifest_rows.get(asset_key, {})
    return _parse_bool(row.get("exists", False))


def _find_expected_split_count(asset_manifest: dict[str, Any], dataset_code: str, split_name: str) -> int:
    split_assets = asset_manifest.get("split_assets", [])
    if not isinstance(split_assets, list):
        return 0
    for item in split_assets:
        if not isinstance(item, dict):
            continue
        if item.get("dataset") == dataset_code and item.get("split_name") == split_name:
            return _parse_int(item.get("row_count"), default=0)
    return 0


def _collect_major_failure_modes(error_cases_path: Path) -> str:
    modes: list[str] = []
    if not error_cases_path.exists():
        return "not_exported"
    for raw_line in error_cases_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("- ") or ":" not in line:
            continue
        label, value = line[2:].split(":", 1)
        label = label.strip()
        if label in {"adhesion_merge", "boundary_over_smooth", "small_gland_miss", "fragmented_complex_region", "all_background"}:
            modes.append(label)
    return ", ".join(sorted(set(modes))) if modes else "not_exported"


def _write_stage_manifest(
    manifest_output_path: Path,
    asset_rows: list[dict[str, Any]],
) -> None:
    manifest_output_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["asset_key", "relative_path", "exists", "required_for_a2"],
        )
        writer.writeheader()
        for row in asset_rows:
            writer.writerow(row)


def _write_run_summary(
    run_summary_path: Path,
    run_meta: dict[str, Any],
    gate_status: dict[str, Any],
    split_status: dict[str, Any],
    major_failure_modes: str,
    blocking_reasons: list[str],
) -> None:
    if gate_status["stage_pass"]:
        truthful_interpretation = (
            "Current assets complete the formal stage02 closure: non-smoke A1 training ended normally, "
            "full TestA60/TestB20 were exported, evaluation and visual assets are aligned, "
            "and handoff is ready for stage03."
        )
    else:
        truthful_interpretation = (
            "Current assets only support local smoke connectivity and partial stage02 closure; "
            "formal A1 acceptance remains blocked until a non-smoke full run, full TestA60/TestB20, "
            "and frozen evaluation fields are re-exported."
        )
    lines = [
        "# Run Summary",
        "",
        "## Inputs",
        "",
        f"- run_name: `{run_meta.get('run_name', 'unknown')}`",
        f"- stop_reason: `{run_meta.get('stop_reason', 'unknown')}`",
        f"- smoke_check: `{str(_parse_bool(run_meta.get('smoke_check', False))).lower()}`",
        f"- device: `{run_meta.get('device', 'unknown')}`",
        f"- best_epoch: `{run_meta.get('best_epoch', 'unknown')}`",
        f"- best_metric_name: `val_objdice`",
        f"- best_metric_value: `{run_meta.get('best_metric_value', 'unknown')}`",
        "",
        "## Gate Status",
        "",
        f"- pass_train: `{str(gate_status['pass_train']).lower()}`",
        f"- pass_val: `{str(gate_status['pass_val']).lower()}`",
        f"- pass_test: `{str(gate_status['pass_test']).lower()}`",
        f"- pass_eval: `{str(gate_status['pass_eval']).lower()}`",
        f"- pass_visual: `{str(gate_status['pass_visual']).lower()}`",
        f"- pass_record: `{str(gate_status['pass_record']).lower()}`",
        f"- stage_pass: `{str(gate_status['stage_pass']).lower()}`",
        f"- protocol_error: `{str(gate_status['protocol_error']).lower()}`",
        f"- freeze_status: `{str(gate_status['freeze_status']).lower()}`",
        f"- handoff_ready_for_a2: `{str(gate_status['handoff_ready_for_a2']).lower()}`",
        f"- next_action: `{gate_status['next_action']}`",
        "",
        "## Test Splits",
        "",
        f"- testA_expected_count: `{split_status['testA_expected_count']}`",
        f"- testA_actual_count: `{split_status['testA_actual_count']}`",
        f"- testA_objdice: `{split_status['testA_objdice']}`",
        f"- testB_expected_count: `{split_status['testB_expected_count']}`",
        f"- testB_actual_count: `{split_status['testB_actual_count']}`",
        f"- testB_objdice: `{split_status['testB_objdice']}`",
        "",
        "## Findings",
        "",
        f"- metric_crosscheck_result: `{run_meta.get('metric_crosscheck_result', 'unknown')}`",
        f"- major_failure_modes: `{major_failure_modes}`",
        (
            "- protocol_abnormal_signs: `"
            + ("; ".join(blocking_reasons) if blocking_reasons else "none")
            + "`"
        ),
        (
            "- truthful_interpretation: `"
            + truthful_interpretation
            + "`"
        ),
    ]
    run_summary_path.parent.mkdir(parents=True, exist_ok=True)
    run_summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_stage_summary(
    stage_summary_path: Path,
    run_dir: Path,
    debug_note_path: Path,
    gate_status: dict[str, Any],
    split_status: dict[str, Any],
    blocking_reasons: list[str],
) -> None:
    lines = [
        "# UNet Flow Stage Summary",
        "",
        "## 1. Inputs",
        f"- run_dir: `{_relative_path(run_dir)}`",
        f"- run_meta: `{_relative_path(run_dir / 'run_meta.yaml')}`",
        f"- run_summary: `{_relative_path(run_dir / 'summaries' / 'run_summary.md')}`",
        f"- debug_note: `{_relative_path(debug_note_path)}`",
        "",
        "## 2. Gate Status",
        f"- pass_train: `{str(gate_status['pass_train']).lower()}`",
        f"- pass_val: `{str(gate_status['pass_val']).lower()}`",
        f"- pass_test: `{str(gate_status['pass_test']).lower()}`",
        f"- pass_eval: `{str(gate_status['pass_eval']).lower()}`",
        f"- pass_visual: `{str(gate_status['pass_visual']).lower()}`",
        f"- pass_record: `{str(gate_status['pass_record']).lower()}`",
        f"- stage_pass: `{str(gate_status['stage_pass']).lower()}`",
        f"- protocol_error: `{str(gate_status['protocol_error']).lower()}`",
        f"- freeze_status: `{str(gate_status['freeze_status']).lower()}`",
        f"- handoff_ready_for_a2: `{str(gate_status['handoff_ready_for_a2']).lower()}`",
        f"- next_action: `{gate_status['next_action']}`",
        "",
        "## 3. Split Counts",
        f"- testA_expected_count: `{split_status['testA_expected_count']}`",
        f"- testA_actual_count: `{split_status['testA_actual_count']}`",
        f"- testB_expected_count: `{split_status['testB_expected_count']}`",
        f"- testB_actual_count: `{split_status['testB_actual_count']}`",
        "",
        "## 4. Blocking Reasons",
    ]
    if blocking_reasons:
        lines.extend(f"- {item}" for item in blocking_reasons)
    else:
        lines.append("- none")
    if gate_status["stage_pass"]:
        stage_truthful_interpretation = (
            "current stage summary confirms formal stage02 closure: non-smoke A1 training ended normally, "
            "full TestA60/TestB20 are present, evaluation and visual assets are aligned, "
            "and handoff is ready for stage03."
        )
    else:
        stage_truthful_interpretation = (
            "current stage summary does not grant formal stage02 closure yet; "
            "a non-smoke full run, full TestA60/TestB20, aligned evaluation fields, "
            "and closed protocol blockers are still required before handoff."
        )
    lines.extend(
        [
            "",
            "## 5. Conclusion",
            f"- truthful_interpretation: {stage_truthful_interpretation}",
        ]
    )
    stage_summary_path.parent.mkdir(parents=True, exist_ok=True)
    stage_summary_path.write_text("\n".join(lines) + "\n", encoding="utf-8")



# ============================================================
# A2 三 seed 统计与验收函数
# ============================================================

def _read_run_meta(run_dir):
    """Read run_meta.yaml, returns None if missing."""
    meta_path = run_dir / "run_meta.yaml"
    if not meta_path.exists():
        return None
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def _validate_a2_run_identity(run_dir, meta, expected_run_name, expected_seed):
    """Reject directory-only matches before a run can enter A2 aggregation."""
    errors = []
    identity_checks = {
        "run_name": expected_run_name,
        "stage_code": "A2",
        "dataset_code": "glas",
        "model_name": "unet",
        "train_seed": expected_seed,
    }
    for field, expected in identity_checks.items():
        actual = meta.get(field)
        if field == "train_seed":
            try:
                matches = int(actual) == int(expected)
            except (TypeError, ValueError):
                matches = False
        else:
            matches = str(actual) == str(expected)
        if not matches:
            errors.append(f"{run_dir.name}:{field} expected={expected!r} actual={actual!r}")

    required_assets = {
        "best.ckpt": run_dir / "checkpoints" / "best.ckpt",
        "testA_metrics.csv": run_dir / "testA_metrics.csv",
        "testB_metrics.csv": run_dir / "testB_metrics.csv",
    }
    for asset_name, asset_path in required_assets.items():
        if not asset_path.exists():
            errors.append(f"{run_dir.name}:missing_required_asset={asset_name}")
    return errors


def _check_proto_consistency(run_metas):
    """Check protocol field consistency across runs.

    Returns:
        (consistent: bool, mismatches: list[str])
    """
    if len(run_metas) < 2:
        return True, []
    seed_names = list(run_metas.keys())
    metas = list(run_metas.values())
    base = metas[0]
    mismatches = []
    for field in _PROTO_CONSISTENCY_FIELDS:
        # Protocol §8.1: field must be present AND non-empty in every run_meta,
        # otherwise proto_consistent must not be declared true (block, never pass).
        missing_seeds = [
            seed_names[i]
            for i, meta in enumerate(metas)
            if str(meta.get(field, "")).strip() == ""
        ]
        if missing_seeds:
            mismatches.append(
                f"{field}: missing_or_empty in run_meta seeds={missing_seeds}"
            )
            continue
        base_val = str(base.get(field, ""))
        for _i, meta in enumerate(metas[1:], start=1):
            cur_val = str(meta.get(field, ""))
            if base_val != cur_val:
                mismatches.append(
                    f"{field}: differs from base ('{cur_val}' vs '{base_val}')"
                )
    return len(mismatches) == 0, mismatches


def collect_unet_seed_results(run_dirs, proto_ref, *, protocol_v3: bool = False):
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 函数被 04_Baseline 复用为对照数据源）
    理论依据: 本脚本为项目自研的多 seed 统计聚合逻辑，无直接外部论文对应；
      统计口径见模块级 docstring 章节与计划 02_mean_std汇总规则.md
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: current_standard_name_clean_restart_20260715
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    proto_fields = {
        k: str(proto_ref.get(k, ""))
        for k in [
            "config_version", "bn_policy_version", "data_proto_version", "train_proto_version",
            "eval_proto_version", "eval_cast_policy", "threshold_value", "boundary_metric_width",
            "boundary_metric_impl", "connected_components_impl",
            "connected_components_connectivity", "best_selector", "threshold_source",
        ]
    }

    raw_rows = []
    a2_v3 = "--protocol-v3" in sys.argv
    a2_run_prefix = A2_V3_RUN_PREFIX if a2_v3 else A2_RUN_PREFIX
    for seed in A2_SEEDS:
        run_name = f"{a2_run_prefix}{seed}"
        run_dir = run_dirs.get(seed)
        missing = run_dir is None or not run_dir.exists()

        for split_role in ("testA", "testB"):
            csv_key = split_role  # match test.py naming: testA_metrics.csv, testB_metrics.csv
            if missing:
                for metric_col in _MIN_METRIC_COLS:
                    raw_rows.append(dict(
                        run_name=run_name, stage="A2", dataset="GlaS",
                        model_name=str(proto_ref.get("model_name", "unet")),
                        **proto_fields,
                        seed=seed, split_role=split_role,
                        metric_name=_METRIC_COL_TO_NAME.get(metric_col, metric_col),
                        metric_value="MISSING",
                        checkpoint_path="",
                        result_tag="reproduced", aggregation="single_seed",
                        note=f"run_dir_missing:{run_name}",
                    ))
            else:
                metrics_path = run_dir / f"{csv_key}_metrics.csv"
                agg_row = _load_csv_aggregate_row(metrics_path)
                run_meta = _read_run_meta(run_dir) or {}
                run_proto_fields = {
                    key: str(run_meta.get(key, ""))
                    for key in proto_fields
                }
                threshold_value = str(run_meta.get("threshold_value", ""))
                best_ckpt = run_dir / "checkpoints" / "best.ckpt"
                checkpoint_path = _relative_path(best_ckpt) if best_ckpt.exists() else ""
                for metric_col in _MIN_METRIC_COLS:
                    raw_value = str(agg_row.get(metric_col, "MISSING")) if agg_row else "MISSING"
                    raw_rows.append(dict(
                        run_name=run_name, stage="A2", dataset="GlaS",
                        model_name=str(run_meta.get("model_name", "unet")),
                        **run_proto_fields,
                        seed=seed, split_role=split_role,
                        metric_name=_METRIC_COL_TO_NAME.get(metric_col, metric_col),
                        metric_value=str(raw_value),
                        checkpoint_path=checkpoint_path,
                        result_tag="reproduced", aggregation="single_seed",
                        note="",
                    ))

    # Write protocol-specific CSV without touching the legacy asset.
    output_name = "unet_v3_seed_results.csv" if protocol_v3 else "unet_seed_results.csv"
    output_path = PROJECT_ROOT / "reports" / "tables" / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_name", "stage", "dataset", "model_name",
        "config_version", "bn_policy_version", "data_proto_version", "train_proto_version",
        "eval_proto_version", "eval_cast_policy", "boundary_metric_width",
        "boundary_metric_impl", "connected_components_impl",
        "connected_components_connectivity",
        "seed", "split_role", "metric_name", "metric_value",
        "best_selector", "threshold_source", "threshold_value",
        "checkpoint_path", "result_tag", "aggregation", "note",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in raw_rows:
            writer.writerow(row)

    print(f"raw_table={_relative_path(output_path)} rows={len(raw_rows)}")
    return raw_rows


def aggregate_seed_metrics(raw_rows):
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 聚合函数被 04_Baseline 的 build_baseline_mean_std 直接复用）
    理论依据: 公式 mean = Σx_i/n，std = √(Σ(x_i-μ)²/n) (population std, n=3)；
      章节依据见计划 02_mean_std汇总规则.md §2.1 聚合口径规范
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: current_standard_clean_restart_20260715
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    import math

    groups: dict = {}
    for row in raw_rows:
        key = (row["split_role"], row["metric_name"])
        if key not in groups:
            groups[key] = []
        val = row["metric_value"]
        if val == "MISSING":
            groups[key].append(None)
        else:
            try:
                groups[key].append(float(val))
            except (ValueError, TypeError):
                groups[key].append(None)

    agg_rows = []
    for (split_role, metric_name), values in groups.items():
        if any(v is None for v in values):
            agg_rows.append(dict(
                split_role=split_role, metric_name=metric_name,
                mean="MISSING", std="MISSING",
                n_runs=3, seeds="3407,1234,2025",
            ))
        else:
            n = len(values)
            mean_val = sum(values) / n
            variance = sum((x - mean_val) ** 2 for x in values) / n
            std_val = math.sqrt(variance)
            agg_rows.append(dict(
                split_role=split_role, metric_name=metric_name,
                mean=mean_val, std=std_val,
                n_runs=n, seeds="3407,1234,2025",
            ))

    return agg_rows


def build_mean_std_summary(raw_rows, proto_ref, *, protocol_v3: bool = False):
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 函数与 04_Baseline 的 build_baseline_mean_std 对称）
    理论依据: 公式 mean = Σx_i/n，std = √(Σ(x_i-μ)²/n) (population std, n=3)；
      章节依据见计划 02_mean_std汇总规则.md §2.1 聚合口径规范
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: current_standard_clean_restart_20260715
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    # Population standard deviation is frozen as ddof=0 for the three-seed aggregate.
    agg_rows = aggregate_seed_metrics(raw_rows)

    proto_base = {
        "model_name": str(proto_ref.get("model_name", "unet")),
        "dataset": "GlaS",
        "config_version": str(proto_ref.get("config_version", "")),
        "bn_policy_version": str(proto_ref.get("bn_policy_version", "")),
        "train_proto_version": str(proto_ref.get("train_proto_version", "")),
        "eval_proto_version": str(proto_ref.get("eval_proto_version", "")),
        "eval_cast_policy": str(proto_ref.get("eval_cast_policy", "")),
        "boundary_metric_width": str(proto_ref.get("boundary_metric_width", "")),
        "boundary_metric_impl": str(proto_ref.get("boundary_metric_impl", "")),
        "connected_components_impl": str(proto_ref.get("connected_components_impl", "")),
        "connected_components_connectivity": str(proto_ref.get("connected_components_connectivity", "")),
        "result_tag": str(proto_ref.get("result_tag", "reproduced")),
        "aggregation": "mean+-std",
    }

    output_rows = []
    for agg in agg_rows:
        output_rows.append({**proto_base, **agg})

    output_name = "unet_v3_mean_std_summary.csv" if protocol_v3 else "unet_mean_std_summary.csv"
    output_path = PROJECT_ROOT / "reports" / "tables" / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "model_name", "dataset", "split_role", "metric_name", "mean", "std",
        "n_runs", "seeds",
        "config_version", "bn_policy_version", "train_proto_version", "eval_proto_version",
        "eval_cast_policy", "boundary_metric_width", "boundary_metric_impl",
        "connected_components_impl", "connected_components_connectivity",
        "result_tag", "aggregation",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow(row)

    print(f"agg_table={_relative_path(output_path)} rows={len(output_rows)}")
    return output_rows


def _parse_error_cases_split_summary(error_cases_path):
    """
    对应阶段: 03_UNet稳定性
    理论依据: 本函数为项目自研的错误案例解析逻辑，无直接外部论文或外部代码对应
    代码参考: 本项目自建 scripts/summarize_stage.py，无外部代码来源
    本项目调整: 解析逐 seed summaries/error_cases.md 的 split 级失败模式计数
    """
    result: dict[str, dict[str, int]] = {}
    if not error_cases_path.exists():
        return result
    current_split = None
    for raw_line in error_cases_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        header = re.match(r"^#{2,3}\s+(testA|testB)\s*$", line)
        if header:
            current_split = header.group(1)
            result.setdefault(current_split, {})
            continue
        if current_split is None or not line.startswith("- ") or ":" not in line:
            continue
        label, value = line[2:].split(":", 1)
        label = label.strip()
        value = value.strip().strip("`")
        if label == "sample_count":
            continue
        try:
            result[current_split][label] = int(value)
        except ValueError:
            continue
    return result


# 计划 §8.6 规定的跨 seed 必检失败模式；alias 把工程 taxonomy 映射到计划口径
_CANONICAL_FAILURE_MODES = [
    ("adhesion_split_fail", ["adhesion_merge", "adhesion_split_fail"]),
    ("small_gland_miss", ["small_gland_miss"]),
    ("boundary_blur", ["boundary_over_smooth", "boundary_blur"]),
]


def build_cross_seed_failure_analysis(run_dirs, agg_rows):
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 失败模式分析函数被 04_Baseline 阶段沿用）
    理论依据: 计划 02_mean_std汇总规则.md §8.6 与 03_阶段验收.md §4.5 章节
      要求波动解释绑定跨 seed 失败模式与 testB_harder 判断；
      错误模式背景见 03_文献证据/05/04_MILD-Net.md
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 聚合三次正式 run 的 error_cases.md，输出跨 seed 一致性结论
    """
    seeds_present = [s for s in A2_SEEDS if s in run_dirs]
    per_seed = {
        seed: _parse_error_cases_split_summary(
            run_dirs[seed] / "summaries" / "error_cases.md"
        )
        for seed in seeds_present
    }

    lines = ["## Cross-Seed Failure Pattern Analysis", ""]
    lines.append(f"- seeds_analyzed: {seeds_present}")
    lines.append("")

    for split_role in ("testA", "testB"):
        lines.append(f"### {split_role}")
        for canon, aliases in _CANONICAL_FAILURE_MODES:
            counts = [
                sum(per_seed[seed].get(split_role, {}).get(a, 0) for a in aliases)
                for seed in seeds_present
            ]
            consistent = len(counts) == A2_N_RUNS and all(c > 0 for c in counts)
            per_seed_str = ", ".join(
                f"seed{seed}={c}" for seed, c in zip(seeds_present, counts)
            )
            status = "cross_seed_consistent" if consistent else "not_consistent"
            lines.append(f"- {canon}: {status} ({per_seed_str})")
        lines.append("")

    lines.append("### testB_harder")

    def _mean_for(split, metric):
        for row in agg_rows:
            if row.get("split_role") == split and row.get("metric_name") == metric:
                try:
                    return float(row.get("mean"))
                except (TypeError, ValueError):
                    return None
        return None

    for metric in ("F1", "Object Dice", "Object Hausdorff"):
        a = _mean_for("testA", metric)
        b = _mean_for("testB", metric)
        if a is None or b is None:
            continue
        # Object Hausdorff 越大越差；其余指标越小越差
        testb_worse = b > a if metric == "Object Hausdorff" else b < a
        verdict = "testB_worse" if testb_worse else "testB_not_worse"
        lines.append(
            f"- {metric}: testA_mean={a:.4f}, testB_mean={b:.4f} -> {verdict}"
        )
    lines.append("")

    patterns_ready = len(seeds_present) == A2_N_RUNS and all(
        per_seed[s].get("testA") and per_seed[s].get("testB") for s in seeds_present
    )
    return lines, patterns_ready


def _build_abnormal_run_lines(run_metas):
    """
    对应阶段: 03_UNet稳定性
    理论依据: 计划 03_阶段验收.md §4.5 要求把异常 run 裁决绑定到阶段结论
    代码参考: 本项目自建 scripts/summarize_stage.py，无外部代码来源
    本项目调整: 逐 seed 记录 stop_reason/best_epoch/epoch_count 作为裁决留痕
    """
    lines = ["## Abnormal Run Adjudication", ""]
    for seed in A2_SEEDS:
        meta = run_metas.get(seed)
        if meta is None:
            lines.append(f"- seed{seed}: MISSING")
            continue
        stop_reason = str(meta.get("stop_reason", "")).strip() or "unknown"
        best_epoch = meta.get("best_epoch", "unknown")
        epoch_count = meta.get("epoch_count", "unknown")
        lines.append(
            f"- seed{seed}: stop_reason={stop_reason}, "
            f"best_epoch={best_epoch}, epoch_count={epoch_count}"
        )
    lines.append("")
    return lines


_GOOD_STOP_REASONS = {"early_stopping", "max_epoch", "max_epoch_reached", "completed"}


def _check_abnormal_runs_resolved(run_metas):
    reasons = []
    for seed in A2_SEEDS:
        meta = run_metas.get(seed)
        if meta is None:
            reasons.append(f"seed{seed}_missing")
            continue
        stop_reason = str(meta.get("stop_reason", "")).strip()
        if not stop_reason:
            reasons.append(f"seed{seed}_no_stop_reason")
        elif stop_reason not in _GOOD_STOP_REASONS:
            reasons.append(f"seed{seed}_unexpected_stop_reason={stop_reason}")
    return len(reasons) == 0, reasons


_FAILURE_PATTERN_TOKENS = (
    "Cross-Seed Failure Pattern Analysis",
    "adhesion_split_fail",
    "small_gland_miss",
    "boundary_blur",
    "testB_harder",
)


def _note_has_failure_patterns(note_path):
    if not note_path.exists():
        return False
    text = note_path.read_text(encoding="utf-8")
    return all(token in text for token in _FAILURE_PATTERN_TOKENS)


def write_unet_stability_note(agg_rows, run_metas, run_dirs, *, protocol_v3: bool = False):
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 稳定性总结函数被 04_Baseline 阶段沿用）
    理论依据: 计划 02_mean_std汇总规则.md §8.4/§8.6 与 03_阶段验收.md §4.5 章节
      要求稳定性文字总结同时给出均值水平、波动解释、跨 seed 失败模式与异常 run 裁决
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    note_name = "unet_v3_stability_note.md" if protocol_v3 else "unet_stability_note.md"
    output_path = PROJECT_ROOT / "reports" / "stage_reports" / note_name
    output_path.parent.mkdir(parents=True, exist_ok=True)

    missing_seeds = [s for s in A2_SEEDS if s not in run_metas]

    lines = ["# UNet Stability Note (A2)", ""]

    if missing_seeds:
        lines.append("## Status: blocked (missing runs)")
        lines.append(f"- missing_seeds: {missing_seeds}")
        lines.append("")
        lines.append("Three formal runs have not all been trained. Real mean+-std results are not yet available.")
        output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"stability_note={_relative_path(output_path)}")
        return output_path

    lines.append("## Mean+-Std Summary")
    lines.append("")
    for split_role in ("testA", "testB"):
        lines.append(f"### {split_role}")
        rows_for_split = [r for r in agg_rows if r.get("split_role") == split_role]
        for row in rows_for_split:
            m = row.get("mean", "MISSING")
            s = row.get("std", "MISSING")
            if m == "MISSING":
                lines.append(f"- {row['metric_name']}: MISSING")
            else:
                lines.append(f"- {row['metric_name']}: {float(m):.4f} +/- {float(s):.4f}")
        lines.append("")

    failure_lines, _ = build_cross_seed_failure_analysis(run_dirs, agg_rows)
    lines.extend(failure_lines)
    lines.extend(_build_abnormal_run_lines(run_metas))

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"stability_note={_relative_path(output_path)}")
    return output_path


def _validate_a2_result_assets(raw_csv: Path, agg_csv: Path) -> tuple[bool, bool, list[str]]:
    """Validate A2 raw and mean+-std CSV completeness without changing either asset."""
    blockers: list[str] = []
    expected_metrics = {_METRIC_COL_TO_NAME[col] for col in _MIN_METRIC_COLS}
    expected_raw_keys = {
        (str(seed), split_role, metric_name)
        for seed in A2_SEEDS
        for split_role, metric_name in _expected_compare_pairs()
    }
    raw_rows = _load_csv_rows(raw_csv)
    raw_ready = raw_csv.exists() and len(raw_rows) == A2_N_RUNS * len(expected_metrics) * 2
    raw_counts: dict[tuple[str, str, str], int] = {}
    raw_protocol_fields_ok = True
    for row in raw_rows:
        key = (
            str(row.get("seed", "")).strip(),
            str(row.get("split_role", "")).strip(),
            str(row.get("metric_name", "")).strip(),
        )
        raw_counts[key] = raw_counts.get(key, 0) + 1
        if any(str(row.get(field, "")).strip() == "" for field in _PROTO_CONSISTENCY_FIELDS):
            raw_protocol_fields_ok = False
        metric_value = str(row.get("metric_value", "")).strip()
        if not metric_value or metric_value == "MISSING" or _parse_float(metric_value) is None:
            raw_protocol_fields_ok = False
    raw_keys_ok = (
        set(raw_counts) == expected_raw_keys
        and all(count == 1 for count in raw_counts.values())
    )
    raw_ready = raw_ready and raw_keys_ok and raw_protocol_fields_ok
    if not raw_ready:
        blockers.append(
            "raw_results_ready_failed "
            f"exists={raw_csv.exists()} rows={len(raw_rows)} expected={A2_N_RUNS * len(expected_metrics) * 2}"
        )

    agg_rows = _load_csv_rows(agg_csv)
    expected_agg_keys = set(_expected_compare_pairs())
    agg_counts: dict[tuple[str, str], int] = {}
    agg_values_ok = True
    for row in agg_rows:
        key = (str(row.get("split_role", "")).strip(), str(row.get("metric_name", "")).strip())
        agg_counts[key] = agg_counts.get(key, 0) + 1
        for field in ("mean", "std"):
            value = str(row.get(field, "")).strip()
            if not value or value == "MISSING" or _parse_float(value) is None:
                agg_values_ok = False
        if _parse_int(row.get("n_runs"), default=0) != A2_N_RUNS:
            agg_values_ok = False
        if str(row.get("seeds", "")).strip() != ",".join(str(seed) for seed in A2_SEEDS):
            agg_values_ok = False
        if str(row.get("aggregation", "")).strip() != "mean+-std":
            agg_values_ok = False
    agg_ready = (
        agg_csv.exists()
        and len(agg_rows) == len(expected_agg_keys)
        and set(agg_counts) == expected_agg_keys
        and all(count == 1 for count in agg_counts.values())
        and agg_values_ok
    )
    if not agg_ready:
        blockers.append(
            "aggregated_results_ready_failed "
            f"exists={agg_csv.exists()} rows={len(agg_rows)} expected={len(expected_agg_keys)}"
        )
        blockers.append("meanstd_export_ready_failed")
    return raw_ready, agg_ready, blockers


def validate_unet_stability_stage(run_metas, raw_csv, agg_csv, note_path):
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 验收函数与 04_Baseline 的 validate_baseline_stage 对称）
    理论依据: 计划 03_阶段验收.md §3.2/§4.5 章节
      定义 Gate_A2 与 failure_summary_ready = note_ready and failure_patterns_ready and abnormal_runs_resolved
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: project_internal
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    blockers = []

    complete_runs = all(s in run_metas for s in A2_SEEDS)
    missing_seeds = [s for s in A2_SEEDS if s not in run_metas]
    if not complete_runs:
        blockers.append(f"complete_runs_failed missing_seeds={missing_seeds}")

    proto_ok, proto_mismatches = _check_proto_consistency(run_metas)
    if not proto_ok:
        blockers.append(f"proto_consistent_failed mismatches={proto_mismatches}")

    raw_ready, aggregate_ready, asset_blockers = _validate_a2_result_assets(raw_csv, agg_csv)
    blockers.extend(asset_blockers)
    meanstd_export_ready = aggregate_ready

    # failure_summary_ready = note_ready and failure_patterns_ready and abnormal_runs_resolved (计划 §4.5)
    note_ready = note_path.exists()
    if not note_ready:
        blockers.append("failure_summary_note_missing")

    patterns_ready = _note_has_failure_patterns(note_path)
    if note_ready and not patterns_ready:
        blockers.append("failure_patterns_not_documented")

    abnormal_resolved, abnormal_reasons = _check_abnormal_runs_resolved(run_metas)
    if not abnormal_resolved:
        blockers.append(f"abnormal_runs_unresolved reasons={abnormal_reasons}")

    failure_ready = note_ready and patterns_ready and abnormal_resolved

    gate_a2 = complete_runs and proto_ok and raw_ready and aggregate_ready and meanstd_export_ready and failure_ready

    protocol_blockers = [b for b in blockers if not b.startswith("complete_runs_failed")]
    blockers_resolved = len(protocol_blockers) == 0

    stage_pass_a2 = gate_a2 and blockers_resolved

    gate_status = {
        "complete_runs": complete_runs,
        "proto_consistent": proto_ok,
        "raw_results_ready": raw_ready,
        "aggregated_results_ready": aggregate_ready,
        "meanstd_export_ready": meanstd_export_ready,
        "evidence_mode": "sample_only",
        "per_run_aggregate_rows": False,
        "raw_count": len(_load_csv_rows(raw_csv)),
        "meanstd_target_count": len(_load_csv_rows(agg_csv)),
        "failure_summary_ready": failure_ready,
        "blockers_resolved": blockers_resolved,
        "gate_a2": gate_a2,
        "stage_pass_a2": stage_pass_a2,
        "handoff_ready_for_b1": stage_pass_a2,
        "missing_seeds": missing_seeds,
    }

    return gate_status, blockers


def write_stage_blockers(blockers, *, protocol_v3: bool = False):
    """Write blocker log to the protocol-specific A2 note."""
    blocker_name = "a2_v3_blockers.md" if protocol_v3 else "a2_blockers.md"
    output_path = PROJECT_ROOT / "notes" / blocker_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# A2 Stage Blockers", ""]
    if blockers:
        for b in blockers:
            lines.append(f"- {b}")
    else:
        lines.append("- none")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def mark_runs_invalid_for_aggregation(run_metas, blocker):
    """Mark runs contaminated by protocol drift.

    Current stage: fields are fixed via eval_proto_v1, no drift possible.
    Returns empty list. Future stages may extend this.
    """
    return []


def build_stage_handoff_manifest(run_dirs, raw_csv, agg_csv, note_path, *, protocol_v3: bool = False):
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 交接清单直接供 04_Baseline 消费）
    理论依据: 计划 02_mean_std汇总规则.md 章节与 03_阶段验收.md §5 要求
      handoff manifest 覆盖所有 A2 产物供下游 B1 直接消费
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    output_name = "unet_v3_stage_manifest.csv" if protocol_v3 else "unet_stage_manifest.csv"
    output_path = PROJECT_ROOT / "reports" / "tables" / output_name
    output_path.parent.mkdir(parents=True, exist_ok=True)

    asset_rows = []
    for seed in A2_SEEDS:
        run_dir = run_dirs.get(seed)
        run_prefix = A2_V3_RUN_PREFIX if protocol_v3 else A2_RUN_PREFIX
        rel = f"experiments/{run_prefix}{seed}"
        exists = run_dir is not None and run_dir.exists()
        asset_rows.append(dict(
            asset_key=f"A2_run_{seed}_dir",
            relative_path=rel,
            exists=exists,
            required_for_b1=True,
            source_stage="03_UNet稳定性",
            source_manifest="reports/tables/unet_stage_manifest.csv",
            source_protocol_version="eval_proto_v1",
            source_run_name=f"{run_prefix}{seed}",
            consumer_stage="04_Baseline",
            consumer_file="结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md",
            consumption_boundary="A2 handoff baseline input; no re-evaluation or protocol reopening",
        ))

    for key, path in [
        ("raw_seed_results", raw_csv),
        ("mean_std_summary", agg_csv),
        ("stability_note", note_path),
    ]:
        asset_rows.append(dict(
            asset_key=key,
            relative_path=_relative_path(path),
            exists=path.exists(),
            required_for_b1=True,
            source_stage="03_UNet稳定性",
            source_manifest="reports/tables/unet_stage_manifest.csv",
            source_protocol_version="eval_proto_v1",
            source_run_name="A2_UNet_GlaS_seed3407,A2_UNet_GlaS_seed1234,A2_UNet_GlaS_seed2025",
            consumer_stage="04_Baseline",
            consumer_file="结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md",
            consumption_boundary="A2 aggregate handoff baseline input; no re-evaluation or protocol reopening",
        ))

    asset_rows.append(dict(
        asset_key="restriction_baseline_no_reeval",
        relative_path="(protocol)",
        exists=True,
        required_for_b1=True,
        source_stage="03_UNet稳定性",
        source_manifest="reports/tables/unet_stage_manifest.csv",
        source_protocol_version="eval_proto_v1",
        source_run_name="A2_UNet_GlaS_seed3407,A2_UNet_GlaS_seed1234,A2_UNet_GlaS_seed2025",
        consumer_stage="04_Baseline",
        consumer_file="结直肠腺体分割_plan_优化版/01_实验执行/04_Baseline/04_阶段验收.md",
        consumption_boundary="Do not re-evaluate or reopen the A2 baseline protocol during B1 consumption",
    ))

    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "asset_key", "relative_path", "exists", "required_for_b1",
            "source_stage", "source_manifest", "source_protocol_version",
            "source_run_name", "consumer_stage", "consumer_file",
            "consumption_boundary",
        ])
        writer.writeheader()
        for row in asset_rows:
            writer.writerow(row)

    print(f"handoff_manifest={_relative_path(output_path)}")
    return output_path


def finalize_stage_a2_handoff(gate_status, blockers, *, protocol_v3: bool = False):
    """
    对应阶段: 03_UNet稳定性
    理论依据: 计划 03_阶段验收.md §5 章节要求阶段总结文件
      为下游 04_Baseline 提供完整的 A2 gate pass 证据链
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    output_path = (
        PROJECT_ROOT / "reports" / "stage_reports" / (
            "unet_v3_stability_stage_summary.md" if protocol_v3 else "unet_stability_stage_summary.md"
        )
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# UNet Stability Stage Summary (A2)",
        "",
        "## Gate Status",
        f"- complete_runs: `{str(gate_status['complete_runs']).lower()}`",
        f"- proto_consistent: `{str(gate_status['proto_consistent']).lower()}`",
        f"- raw_results_ready: `{str(gate_status['raw_results_ready']).lower()}`",
        f"- aggregated_results_ready: `{str(gate_status['aggregated_results_ready']).lower()}`  # compatibility alias: statistical table ready; not per-run aggregate rows",
        f"- evidence_mode: `{gate_status['evidence_mode']}`",
        f"- per_run_aggregate_rows: `{str(gate_status['per_run_aggregate_rows']).lower()}`",
        f"- raw_count: `{gate_status['raw_count']}`",
        f"- meanstd_target_count: `{gate_status['meanstd_target_count']}`",
        f"- failure_summary_ready: `{str(gate_status['failure_summary_ready']).lower()}`",
        f"- blockers_resolved: `{str(gate_status['blockers_resolved']).lower()}`",
        f"- gate_a2: `{str(gate_status['gate_a2']).lower()}`",
        f"- stage_pass_a2: `{str(gate_status['stage_pass_a2']).lower()}`",
        f"- handoff_ready_for_b1: `{str(gate_status['handoff_ready_for_b1']).lower()}`",
    ]

    missing = gate_status.get("missing_seeds", [])
    if missing:
        lines.append(f"- missing_seeds: `{missing}`")

    lines.extend(["", "## Blocking Reasons", ""])
    if blockers:
        for b in blockers:
            lines.append(f"- {b}")
    else:
        lines.append("- none")

    if gate_status["stage_pass_a2"]:
        lines.extend([
            "",
            "## Conclusion",
            "",
            "A2 stage passed: three formal runs are protocol-consistent; sample-only evidence covers seven metrics with raw=42, mean±std target=14, and error patterns explainable. Aggregate values are derived statistics, not per-run CSV rows.",
        ])
    else:
        lines.extend([
            "",
            "## Conclusion",
            "",
            "A2 stage blocked: prerequisites for 04_Baseline are not yet met. "
            "Complete missing formal runs or resolve blockers first.",
        ])

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"stage_summary={_relative_path(output_path)}")
    return output_path


def main_a2():
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本 A2 主流程与 04_Baseline 的 main_b1 对称）
    理论依据: 计划 03_阶段验收.md 章节定义的 A2 验收完整流程
      顺序执行：collect → aggregate → stability_note → validate → manifest → finalize
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    protocol_v3 = "--protocol-v3" in sys.argv
    experiments_root = PROJECT_ROOT / "experiments"
    run_dirs = {}
    run_metas = {}
    missing_seeds = []
    run_prefix = A2_V3_RUN_PREFIX if protocol_v3 else A2_RUN_PREFIX

    for seed in A2_SEEDS:
        run_name = f"{run_prefix}{seed}"
        run_dir = experiments_root / run_name
        meta = _read_run_meta(run_dir)
        if meta is None:
            missing_seeds.append(seed)
        else:
            identity_errors = _validate_a2_run_identity(run_dir, meta, run_name, seed)
            if identity_errors:
                missing_seeds.append(seed)
                print(f"invalid_run_identity seed={seed}: {identity_errors}")
            else:
                run_dirs[seed] = run_dir
                run_metas[seed] = meta

    print("=== A2 Stage Summary ===")
    print(f"seeds_total={len(A2_SEEDS)} seeds_found={len(run_metas)} missing={missing_seeds}")

    # Default proto_ref when all runs missing (eval_proto_v1 protocol defaults)
    if run_metas:
        proto_ref = dict(run_metas[next(iter(run_metas))])
    else:
        proto_ref = {
            "model_name": "unet", "config_version": "v1",
            "data_proto_version": "data_proto_v1", "train_proto_version": "train_proto_v1",
            "eval_proto_version": "eval_proto_v1", "eval_cast_policy": "float32_before_threshold",
            "boundary_metric_width": "3", "boundary_metric_impl": "binary_erosion_xor_plus_binary_dilation",
            "connected_components_impl": "scipy.ndimage.label", "connected_components_connectivity": "8",
            "best_selector": "val_objdice_max", "threshold_source": "val17", "threshold_value": "0.5",
        }

    # 1. Collect raw per-seed results
    raw_rows = collect_unet_seed_results(run_dirs, proto_ref, protocol_v3=protocol_v3)

    # 2. Build mean+-std summary
    agg_rows = build_mean_std_summary(raw_rows, proto_ref, protocol_v3=protocol_v3)

    # 3. Resolve protocol-specific result table paths
    raw_name = "unet_v3_seed_results.csv" if protocol_v3 else "unet_seed_results.csv"
    agg_name = "unet_v3_mean_std_summary.csv" if protocol_v3 else "unet_mean_std_summary.csv"
    raw_csv = PROJECT_ROOT / "reports" / "tables" / raw_name
    agg_csv = PROJECT_ROOT / "reports" / "tables" / agg_name

    # 4. Write stability note (含跨 seed 失败模式与异常 run 裁决)
    note_path = write_unet_stability_note(agg_rows, run_metas, run_dirs, protocol_v3=protocol_v3)

    # 5. Full validation (校验 note 内容而非仅存在性)
    gate_status, blockers = validate_unet_stability_stage(
        run_metas, raw_csv, agg_csv, note_path
    )

    # 6. Write blockers
    write_stage_blockers(blockers, protocol_v3=protocol_v3)

    # 7. Build handoff manifest
    build_stage_handoff_manifest(run_dirs, raw_csv, agg_csv, note_path, protocol_v3=protocol_v3)

    # 8. Finalize stage handoff
    finalize_stage_a2_handoff(gate_status, blockers, protocol_v3=protocol_v3)

    # Summary
    print(f"stage_pass_a2={str(gate_status['stage_pass_a2']).lower()}")
    if missing_seeds:
        print(f"missing_runs={missing_seeds}")
    if blockers:
        for b in blockers:
            print(f"blocker: {b}")

    return 0

def main() -> int:
    """
    对应阶段: 03_UNet稳定性（本文件在 04_Baseline 阶段扩展 B1 分支，本入口通过 --stage b1 路由到 04_Baseline 的 main_b1）
    理论依据: 计划 03_阶段验收.md 章节定义的单 run 验收流程（legacy 模式，A1 阶段遗留）；
      --stage a2/b1 参数路由到各自独立的验收函数
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 适配 03 阶段，固化协议
    """
    if '--stage' in sys.argv and 'a2' in sys.argv:
        return main_a2()
    if '--stage' in sys.argv and 'b1' in sys.argv:
        return main_b1()
    args = parse_args()
    _, experiment_config = train_entry.load_experiment_config(PROJECT_ROOT, args.config)
    run_name = args.run_name or str(experiment_config.get("run_name", "manual_run"))
    run_dir = train_entry.build_output_dir(PROJECT_ROOT, run_name)
    if not run_dir.exists():
        raise FileNotFoundError(f"run directory not found: {run_dir}")

    debug_note_path = (PROJECT_ROOT / train_entry.normalize_relpath(args.debug_note)).resolve()
    stage_summary_path = (PROJECT_ROOT / train_entry.normalize_relpath(args.stage_summary_output)).resolve()
    manifest_output_path = (PROJECT_ROOT / train_entry.normalize_relpath(args.manifest_output)).resolve()

    eval_config_path = train_entry.resolve_config_ref(PROJECT_ROOT, experiment_config, "eval")
    eval_config = train_entry.simple_yaml_load(eval_config_path.read_text(encoding="utf-8"))

    asset_manifest_path = (PROJECT_ROOT / "reports" / "stage_reports" / "asset_manifest.json").resolve()
    asset_manifest = train_entry.load_json_mapping(asset_manifest_path)
    data_acceptance_path = (PROJECT_ROOT / "reports" / "stage_reports" / "data_stage_acceptance.md").resolve()
    data_acceptance_fields = _parse_markdown_fields(data_acceptance_path)

    run_meta_path = run_dir / "run_meta.yaml"
    run_meta = train_entry.simple_yaml_load(run_meta_path.read_text(encoding="utf-8"))

    debug_fields = _parse_markdown_fields(debug_note_path)
    metric_note_fields = _parse_markdown_fields(run_dir / "metric_crosscheck_note.md")
    testa_aggregate = _load_csv_aggregate_row(run_dir / "testA_metrics.csv")
    testb_aggregate = _load_csv_aggregate_row(run_dir / "testB_metrics.csv")

    testA_expected_count = _find_expected_split_count(asset_manifest, str(run_meta.get("dataset_code", "")), "testA")
    testB_expected_count = _find_expected_split_count(asset_manifest, str(run_meta.get("dataset_code", "")), "testB")
    testA_actual_count = _parse_int(testa_aggregate.get("sample_count"), default=_parse_int(run_meta.get("testA_sample_count")))
    testB_actual_count = _parse_int(testb_aggregate.get("sample_count"), default=_parse_int(run_meta.get("testB_sample_count")))

    actual_connectivity = _parse_int(
        metric_note_fields.get("connected_components_connectivity", eval_config.get("connected_components_connectivity")),
        default=0,
    )
    actual_boundary_width = _parse_int(
        metric_note_fields.get("boundary_metric_width", run_meta.get("boundary_metric_width", eval_config.get("boundary_metric_width"))),
        default=0,
    )
    actual_eval_cast_policy = str(eval_config.get("eval_cast_policy", "missing"))

    data_stage_pass = data_acceptance_fields.get("data_stage_pass", "false") == "True"
    handoff_ready = data_acceptance_fields.get("handoff_ready", "false") == "True"
    preflight_pass = data_acceptance_fields.get("preflight_pass", "false") == "True"

    best_ckpt_exists = (run_dir / "checkpoints" / "best.ckpt").exists()
    last_ckpt_exists = (run_dir / "checkpoints" / "last.ckpt").exists()
    train_log_exists = (run_dir / "train_log.csv").exists()
    val_metrics_exists = (run_dir / "val_metrics.csv").exists()
    testA_metrics_exists = (run_dir / "testA_metrics.csv").exists()
    testB_metrics_exists = (run_dir / "testB_metrics.csv").exists()
    metric_note_exists = (run_dir / "metric_crosscheck_note.md").exists()
    error_cases_exists = (run_dir / "summaries" / "error_cases.md").exists()
    visuals_testA_exists = (run_dir / "visuals" / "testA").exists()
    visuals_testB_exists = (run_dir / "visuals" / "testB").exists()
    run_summary_exists = (run_dir / "summaries" / "run_summary.md").exists()

    formal_run_done = not _parse_bool(run_meta.get("smoke_check", False)) and str(run_meta.get("stop_reason", "")) != "smoke_check_complete"
    best_selector_ok = str(run_meta.get("best_selector", "")) == FORMAL_BEST_SELECTOR
    threshold_source_ok = str(run_meta.get("threshold_source", "")) == FORMAL_THRESHOLD_SOURCE
    pass_train = formal_run_done and best_ckpt_exists and last_ckpt_exists and train_log_exists
    pass_val = formal_run_done and val_metrics_exists and best_selector_ok and threshold_source_ok
    pass_test = (
        testA_metrics_exists
        and testB_metrics_exists
        and testA_expected_count > 0
        and testB_expected_count > 0
        and testA_actual_count == testA_expected_count
        and testB_actual_count == testB_expected_count
    )
    pass_eval = (
        pass_test
        and metric_note_exists
        and str(run_meta.get("metric_crosscheck_result", "")) == "pass"
        and actual_boundary_width == FORMAL_BOUNDARY_WIDTH
        and actual_eval_cast_policy == FORMAL_CAST_POLICY
        and actual_connectivity == FORMAL_CONNECTIVITY
    )
    pass_visual = error_cases_exists and visuals_testA_exists and visuals_testB_exists
    debug_note_exists = debug_note_path.exists()
    pass_record = (
        data_stage_pass
        and handoff_ready
        and preflight_pass
        and (run_dir / "config.yaml").exists()
        and run_meta_path.exists()
        and run_summary_exists
        and debug_note_exists
        and asset_manifest_path.exists()
    )

    blocking_reasons: list[str] = []
    if not formal_run_done:
        blocking_reasons.append("formal_run_missing_or_still_smoke")
    if testA_actual_count != testA_expected_count:
        blocking_reasons.append(f"testA_sample_count_mismatch:{testA_actual_count}!={testA_expected_count}")
    if testB_actual_count != testB_expected_count:
        blocking_reasons.append(f"testB_sample_count_mismatch:{testB_actual_count}!={testB_expected_count}")
    if actual_eval_cast_policy != FORMAL_CAST_POLICY:
        blocking_reasons.append(f"eval_cast_policy_mismatch:{actual_eval_cast_policy}!={FORMAL_CAST_POLICY}")
    if actual_boundary_width != FORMAL_BOUNDARY_WIDTH:
        blocking_reasons.append(f"boundary_metric_width_mismatch:{actual_boundary_width}!={FORMAL_BOUNDARY_WIDTH}")
    if actual_connectivity != FORMAL_CONNECTIVITY:
        blocking_reasons.append(f"connected_components_connectivity_mismatch:{actual_connectivity}!={FORMAL_CONNECTIVITY}")
    if debug_fields.get("close_status", "missing") != "closed":
        blocking_reasons.append(f"debug_close_status_not_closed:{debug_fields.get('close_status', 'missing')}")

    protocol_error = bool(blocking_reasons)
    stage_pass = pass_train and pass_val and pass_test and pass_eval and pass_visual and pass_record and not protocol_error
    freeze_status = stage_pass
    handoff_ready_for_a2 = stage_pass
    next_action = "enter_03_unet_stability" if handoff_ready_for_a2 else "stay_in_02_complete_formal_a1"
    rollback_reason = "; ".join(blocking_reasons) if blocking_reasons else "none"

    stage_asset_manifest_relpath = _relative_path(manifest_output_path)
    run_meta.update(
        {
            "asset_manifest": stage_asset_manifest_relpath,
            "data_stage_pass": data_stage_pass,
            "handoff_ready": handoff_ready,
            "preflight_pass": preflight_pass,
            "eval_cast_policy": actual_eval_cast_policy,
            "connected_components_connectivity": actual_connectivity,
            "pass_train": pass_train,
            "pass_val": pass_val,
            "pass_test": pass_test,
            "pass_eval": pass_eval,
            "pass_visual": pass_visual,
            "pass_record": pass_record,
            "stage_pass": stage_pass,
            "protocol_error": protocol_error,
            "rollback_reason": rollback_reason,
            "freeze_status": freeze_status,
            "handoff_ready_for_a2": handoff_ready_for_a2,
            "next_action": next_action,
        }
    )
    run_meta_path.write_text(train_entry.dump_simple_yaml(run_meta) + "\n", encoding="utf-8")

    split_status = {
        "testA_expected_count": testA_expected_count,
        "testA_actual_count": testA_actual_count,
        "testA_objdice": testa_aggregate.get("objdice", run_meta.get("testA_objdice", "unknown")),
        "testB_expected_count": testB_expected_count,
        "testB_actual_count": testB_actual_count,
        "testB_objdice": testb_aggregate.get("objdice", run_meta.get("testB_objdice", "unknown")),
    }
    gate_status = {
        "pass_train": pass_train,
        "pass_val": pass_val,
        "pass_test": pass_test,
        "pass_eval": pass_eval,
        "pass_visual": pass_visual,
        "pass_record": pass_record,
        "stage_pass": stage_pass,
        "protocol_error": protocol_error,
        "freeze_status": freeze_status,
        "handoff_ready_for_a2": handoff_ready_for_a2,
        "next_action": next_action,
    }
    major_failure_modes = _collect_major_failure_modes(run_dir / "summaries" / "error_cases.md")

    _write_run_summary(
        run_summary_path=run_dir / "summaries" / "run_summary.md",
        run_meta=run_meta,
        gate_status=gate_status,
        split_status=split_status,
        major_failure_modes=major_failure_modes,
        blocking_reasons=blocking_reasons,
    )

    asset_rows = [
        {"asset_key": "config_yaml", "relative_path": _relative_path(run_dir / "config.yaml"), "exists": (run_dir / "config.yaml").exists(), "required_for_a2": True},
        {"asset_key": "run_meta_yaml", "relative_path": _relative_path(run_meta_path), "exists": run_meta_path.exists(), "required_for_a2": True},
        {"asset_key": "train_log_csv", "relative_path": _relative_path(run_dir / "train_log.csv"), "exists": train_log_exists, "required_for_a2": True},
        {"asset_key": "val_metrics_csv", "relative_path": _relative_path(run_dir / "val_metrics.csv"), "exists": val_metrics_exists, "required_for_a2": True},
        {"asset_key": "testA_metrics_csv", "relative_path": _relative_path(run_dir / "testA_metrics.csv"), "exists": testA_metrics_exists, "required_for_a2": True},
        {"asset_key": "testB_metrics_csv", "relative_path": _relative_path(run_dir / "testB_metrics.csv"), "exists": testB_metrics_exists, "required_for_a2": True},
        {"asset_key": "metric_crosscheck_note", "relative_path": _relative_path(run_dir / "metric_crosscheck_note.md"), "exists": metric_note_exists, "required_for_a2": True},
        {"asset_key": "best_ckpt", "relative_path": _relative_path(run_dir / "checkpoints" / "best.ckpt"), "exists": best_ckpt_exists, "required_for_a2": True},
        {"asset_key": "last_ckpt", "relative_path": _relative_path(run_dir / "checkpoints" / "last.ckpt"), "exists": last_ckpt_exists, "required_for_a2": True},
        {"asset_key": "train_curve_csv", "relative_path": _relative_path(run_dir / "curves" / "train_curve.csv"), "exists": (run_dir / "curves" / "train_curve.csv").exists(), "required_for_a2": True},
        {"asset_key": "val_curve_csv", "relative_path": _relative_path(run_dir / "curves" / "val_curve.csv"), "exists": (run_dir / "curves" / "val_curve.csv").exists(), "required_for_a2": True},
        {"asset_key": "visuals_testA_dir", "relative_path": _relative_path(run_dir / "visuals" / "testA"), "exists": visuals_testA_exists, "required_for_a2": True},
        {"asset_key": "visuals_testB_dir", "relative_path": _relative_path(run_dir / "visuals" / "testB"), "exists": visuals_testB_exists, "required_for_a2": True},
        {"asset_key": "error_cases_md", "relative_path": _relative_path(run_dir / "summaries" / "error_cases.md"), "exists": error_cases_exists, "required_for_a2": True},
        {"asset_key": "run_summary_md", "relative_path": _relative_path(run_dir / "summaries" / "run_summary.md"), "exists": True, "required_for_a2": True},
        {"asset_key": "debug_note_md", "relative_path": _relative_path(debug_note_path), "exists": debug_note_exists, "required_for_a2": True},
        {"asset_key": "stage_summary_md", "relative_path": _relative_path(stage_summary_path), "exists": True, "required_for_a2": False},
        {"asset_key": "stage_manifest_csv", "relative_path": _relative_path(manifest_output_path), "exists": True, "required_for_a2": False},
    ]
    _write_stage_manifest(manifest_output_path, asset_rows)
    _write_stage_summary(stage_summary_path, run_dir, debug_note_path, gate_status, split_status, blocking_reasons)

    print(f"run_name={run_name}")
    print(f"stage_pass={str(stage_pass).lower()}")
    print(f"protocol_error={str(protocol_error).lower()}")
    print(f"next_action={next_action}")
    print(f"stage_summary={_relative_path(stage_summary_path)}")
    print(f"manifest={_relative_path(manifest_output_path)}")
    return 0


# ============================================================
# B1 阶段（04_Baseline ResNet34-U-Net）聚合与验收
# 对应阶段: 04_Baseline
# 理论依据: 计划 04_阶段验收.md Gate_B1 五子门定义
#   Gate_B1 = Gate_B1_compare AND complete_runs AND baseline_assets_ready
#             AND freeze_ready AND handoff_ready
# 代码参考: 本项目自建 scripts/summarize_stage.py，与 A2 分支对称实现
# 本项目调整: B1 专属产物路径与 A2 隔离，绝不覆盖 A2 产物
# ============================================================

def collect_baseline_seed_results(run_dirs: dict, proto_ref: dict) -> list[dict]:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md §5.4 章节要求 raw per-seed 表与聚合表分别落盘
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 产物路径为 reports/tables/baseline_per_seed_summary.csv
    """
    rows = []
    for seed in B1_SEEDS:
        run_dir = run_dirs.get(seed)
        if run_dir is None:
            continue
        meta = _read_run_meta(run_dir)
        if meta is None:
            continue
        for split_role in ("testA", "testB"):
            metrics_path = run_dir / f"{split_role}_metrics.csv"
            agg_row = _load_csv_aggregate_row(metrics_path)
            for col in _MIN_METRIC_COLS:
                val = agg_row.get(col)
                if val is None:
                    continue
                try:
                    float(val)
                except (TypeError, ValueError):
                    continue
                rows.append({
                    "run_name": str(meta.get("run_name", f"{B1_RUN_PREFIX}{seed}")),
                    "stage": "B1",
                    "dataset": "GlaS",
                    "model_name": str(meta.get("model_name", "resnet34_unet")),
                    "config_version": str(proto_ref.get("config_version", "v1")),
                    "bn_policy_version": str(proto_ref.get("bn_policy_version", "")),
                    "data_proto_version": str(proto_ref.get("data_proto_version", "")),
                    "train_proto_version": str(proto_ref.get("train_proto_version", "")),
                    "eval_proto_version": str(proto_ref.get("eval_proto_version", "")),
                    "eval_cast_policy": str(proto_ref.get("eval_cast_policy", "")),
                    "boundary_metric_width": str(proto_ref.get("boundary_metric_width", "")),
                    "boundary_metric_impl": str(proto_ref.get("boundary_metric_impl", "")),
                    "connected_components_impl": str(proto_ref.get("connected_components_impl", "")),
                    "connected_components_connectivity": str(proto_ref.get("connected_components_connectivity", "")),
                    "seed": seed,
                    "split_role": split_role,
                    "metric_name": _METRIC_COL_TO_NAME.get(col, col),
                    "metric_value": float(val),
                    "best_selector": str(proto_ref.get("best_selector", "")),
                    "threshold_source": str(proto_ref.get("threshold_source", "")),
                    "threshold_value": str(proto_ref.get("threshold_value", "0.5")),
                    "checkpoint_path": str(meta.get("best_checkpoint_path", "")),
                    "result_tag": str(meta.get("result_tag", "reproduced")),
                    "aggregation": "single_seed",
                    "note": "",
                })
    output_path = PROJECT_ROOT / "reports" / "tables" / "baseline_per_seed_summary.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_name", "stage", "dataset", "model_name",
        "config_version", "bn_policy_version", "data_proto_version", "train_proto_version", "eval_proto_version",
        "eval_cast_policy", "boundary_metric_width", "boundary_metric_impl",
        "connected_components_impl", "connected_components_connectivity",
        "seed", "split_role", "metric_name", "metric_value",
        "best_selector", "threshold_source", "threshold_value",
        "checkpoint_path", "result_tag", "aggregation", "note",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"raw_table={_relative_path(output_path)} rows={len(rows)}")
    return rows


def build_baseline_mean_std(raw_rows: list[dict], proto_ref: dict) -> list[dict]:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md §5.4 章节要求 mean+-std 聚合表；
      公式同 A2：mean = Σx_i/n，std = √(Σ(x_i-μ)²/n) (population std, n=3)
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 产物路径为 reports/tables/baseline_mean_std.csv
    """
    agg_rows = aggregate_seed_metrics(raw_rows)
    proto_base = {
        "model_name": str(proto_ref.get("model_name", "resnet34_unet")),
        "dataset": "GlaS",
        "config_version": str(proto_ref.get("config_version", "")),
        "bn_policy_version": str(proto_ref.get("bn_policy_version", "")),
        "train_proto_version": str(proto_ref.get("train_proto_version", "")),
        "eval_proto_version": str(proto_ref.get("eval_proto_version", "")),
        "eval_cast_policy": str(proto_ref.get("eval_cast_policy", "")),
        "boundary_metric_width": str(proto_ref.get("boundary_metric_width", "")),
        "boundary_metric_impl": str(proto_ref.get("boundary_metric_impl", "")),
        "connected_components_impl": str(proto_ref.get("connected_components_impl", "")),
        "connected_components_connectivity": str(proto_ref.get("connected_components_connectivity", "")),
        "result_tag": str(proto_ref.get("result_tag", "reproduced")),
        "aggregation": "mean+-std",
    }
    output_rows = []
    for agg in agg_rows:
        output_rows.append({**proto_base, **agg})
    output_path = PROJECT_ROOT / "reports" / "tables" / "baseline_mean_std.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "model_name", "dataset", "split_role", "metric_name", "mean", "std",
        "n_runs", "seeds",
        "config_version", "bn_policy_version", "train_proto_version", "eval_proto_version",
        "eval_cast_policy", "boundary_metric_width", "boundary_metric_impl",
        "connected_components_impl", "connected_components_connectivity",
        "result_tag", "aggregation",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow(row)
    print(f"agg_table={_relative_path(output_path)} rows={len(output_rows)}")
    return output_rows


def build_unet_vs_r34unet_comparison(
    b1_agg_rows: list[dict],
    a2_agg_csv: Path,
    a2_run_metas: dict[int, dict[str, Any]] | None = None,
) -> Path:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md §5.2/§5.4 章节
      要求 UNet vs R34UNet 公平比较表（Gate_B1_compare 前置）；
      delta_mean = B1_mean - A2_mean（正值对非HD指标代表 R34UNet 更好）
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: current_standard_clean_restart_20260715
      - 许可证: project_internal
    本项目调整: 从当前 A2 mean_std CSV 读 UNet 结果，与 B1 聚合行对照，输出比较表
    """
    output_path = PROJECT_ROOT / "reports" / "tables" / "unet_vs_r34unet_comparison.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 只消费当前轮 manifest/contract 指定的 A2 聚合表；旧表不得静默混入。
    if a2_run_metas is None:
        raise RuntimeError("A2 run_meta identity is required for aggregate comparison")
    _validate_aggregate_identity(a2_agg_csv, a2_run_metas, "A2")
    a2_rows = _load_csv_rows(a2_agg_csv)

    def _lookup(rows, split_role, metric_name):
        for r in rows:
            if r.get("split_role") == split_role and r.get("metric_name") == metric_name:
                return r
        return {}

    compare_rows = []
    for split_role in ("testA", "testB"):
        for metric_name in _REQUIRED_COMPARE_METRICS:
            a2_r = _lookup(a2_rows, split_role, metric_name)
            b1_r = _lookup(b1_agg_rows, split_role, metric_name)
            a2_mean = a2_r.get("mean", "")
            b1_mean = b1_r.get("mean", "")
            a2_std = a2_r.get("std", "")
            b1_std = b1_r.get("std", "")
            # delta_mean: B1 - A2 (正值代表 R34UNet 更好，对于 HD/Hausdorff 越小越好)
            try:
                delta = float(b1_mean) - float(a2_mean)
                delta_str = f"{delta:.6f}"
            except (TypeError, ValueError):
                delta_str = ""
            compare_rows.append({
                "split_role": split_role,
                "metric_name": metric_name,
                "unet_mean": a2_mean,
                "unet_std": a2_std,
                "r34unet_mean": b1_mean,
                "r34unet_std": b1_std,
                "delta_mean_r34unet_minus_unet": delta_str,
                "a2_result_tag": a2_r.get("result_tag", "reproduced"),
                "b1_result_tag": b1_r.get("result_tag", "reproduced"),
                "a2_aggregation": a2_r.get("aggregation", ""),
                "b1_aggregation": b1_r.get("aggregation", ""),
                "config_version": b1_r.get("config_version", a2_r.get("config_version", "")),
                "train_proto_version": b1_r.get("train_proto_version", a2_r.get("train_proto_version", "")),
                "eval_proto_version": b1_r.get("eval_proto_version", ""),
                "eval_cast_policy": b1_r.get("eval_cast_policy", ""),
                "boundary_metric_width": b1_r.get("boundary_metric_width", ""),
                "boundary_metric_impl": b1_r.get("boundary_metric_impl", ""),
                "connected_components_impl": b1_r.get("connected_components_impl", ""),
                "connected_components_connectivity": b1_r.get("connected_components_connectivity", ""),
                "seeds": b1_r.get("seeds", a2_r.get("seeds", "")),
                "n_runs": b1_r.get("n_runs", a2_r.get("n_runs", "")),
            })

    fieldnames = [
        "split_role", "metric_name",
        "unet_mean", "unet_std", "r34unet_mean", "r34unet_std",
        "delta_mean_r34unet_minus_unet",
        "a2_result_tag", "b1_result_tag", "a2_aggregation", "b1_aggregation",
        "config_version", "train_proto_version", "eval_proto_version", "eval_cast_policy",
        "boundary_metric_width", "boundary_metric_impl",
        "connected_components_impl", "connected_components_connectivity",
        "seeds", "n_runs",
    ]
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in compare_rows:
            writer.writerow(row)
    print(f"comparison_table={_relative_path(output_path)} rows={len(compare_rows)}")
    return output_path


def validate_baseline_stage(run_metas: dict, a2_run_metas: dict,
                             run_dirs: dict[int, Path], raw_csv: Path, agg_csv: Path,
                             compare_csv: Path, summary_path: Path,
                             manifest_csv: Path, a2_agg_csv: Path) -> tuple[dict, list[str]]:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md Gate_B1 五子门定义章节
      Gate_B1 = Gate_B1_compare AND complete_runs AND baseline_assets_ready
                AND freeze_ready AND handoff_ready
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: current_standard_clean_restart_20260715
      - 许可证: project_internal
    本项目调整: 五子门 + 当前标准身份一致性校验
    """
    blockers = []

    # 子门1: complete_runs
    complete_runs = all(s in run_metas for s in B1_SEEDS)
    missing_seeds = [s for s in B1_SEEDS if s not in run_metas]
    if not complete_runs:
        blockers.append(f"complete_runs_failed missing_seeds={missing_seeds}")

    # 协议一致性（复用 A2 的校验逻辑，但从 B1 run_metas 读）
    proto_ok, proto_mismatches = _check_proto_consistency(run_metas)
    if not proto_ok:
        blockers.append(f"proto_consistent_failed mismatches={proto_mismatches}")

    a2_complete_runs = all(s in a2_run_metas for s in A2_SEEDS)
    if not a2_complete_runs:
        missing_a2 = [s for s in A2_SEEDS if s not in a2_run_metas]
        blockers.append(f"a2_complete_runs_failed missing_seeds={missing_a2}")
    a2_proto_ok, a2_proto_mismatches = _check_proto_consistency(a2_run_metas)
    if not a2_proto_ok:
        blockers.append(f"a2_proto_consistent_failed mismatches={a2_proto_mismatches}")

    raw_rows = _load_csv_rows(raw_csv)
    b1_agg_rows = _load_csv_rows(agg_csv)
    _validate_aggregate_identity(a2_agg_csv, a2_run_metas, "A2")
    a2_agg_rows = _load_csv_rows(a2_agg_csv)
    compare_rows = _load_csv_rows(compare_csv)

    raw_missing = _collect_missing_raw_pairs(raw_rows, B1_SEEDS)
    b1_agg_missing = _collect_missing_compare_pairs(_rows_by_split_metric(b1_agg_rows))
    a2_agg_missing = _collect_missing_compare_pairs(_rows_by_split_metric(a2_agg_rows))
    compare_missing = _collect_missing_compare_pairs(_rows_by_split_metric(compare_rows))
    qualitative_missing = _collect_missing_qualitative_assets(run_dirs)

    b1_reference = run_metas.get(B1_SEEDS[0], {})
    a2_reference = a2_run_metas.get(A2_SEEDS[0], {})
    compare_proto_mismatches = []
    if a2_reference and b1_reference:
        compare_proto_mismatches = _collect_compare_proto_mismatches(a2_reference, b1_reference)
    same_repeat_set = complete_runs and a2_complete_runs
    same_stat_identity = (
        all(str(row.get("aggregation", "")).strip() == "mean+-std" for row in b1_agg_rows + a2_agg_rows)
        and all(str(row.get("seeds", "")).strip() == "3407,1234,2025" for row in b1_agg_rows + a2_agg_rows)
        and all(_parse_int(row.get("n_runs"), default=0) == 3 for row in b1_agg_rows + a2_agg_rows)
    )
    fair_compare = (
        proto_ok
        and a2_proto_ok
        and same_repeat_set
        and same_stat_identity
        and len(compare_proto_mismatches) == 0
    )
    protocol_versions = {
        str(meta.get("eval_proto_version", ""))
        for meta in list(run_metas.values()) + list(a2_run_metas.values())
    }
    config_families = {
        str(meta.get("config_version", ""))
        for meta in list(run_metas.values()) + list(a2_run_metas.values())
    }
    identity_fields_ok = all(
        len({str(meta.get(field, "")).strip() for meta in list(run_metas.values()) + list(a2_run_metas.values())}) == 1
        and all(str(meta.get(field, "")).strip() for meta in list(run_metas.values()) + list(a2_run_metas.values()))
        for field in _CURRENT_IDENTITY_FIELDS
    )
    standard_identity_ok = identity_fields_ok and complete_runs and a2_complete_runs
    if not standard_identity_ok:
        blockers.append(
            "current_identity_failed "
            f"fields={{{', '.join(field + '=' + str(sorted({str(meta.get(field, '')).strip() for meta in list(run_metas.values()) + list(a2_run_metas.values())})) for field in _CURRENT_IDENTITY_FIELDS)}}}"
        )
    if not fair_compare:
        reasons = []
        if compare_proto_mismatches:
            reasons.append(f"proto_mismatch={compare_proto_mismatches}")
        if not same_repeat_set:
            reasons.append("repeat_set_incomplete")
        if not same_stat_identity:
            reasons.append("stat_identity_mismatch")
        blockers.append(f"fair_compare_failed reasons={reasons or ['unknown']}")

    aggregate_ready = (
        agg_csv.exists()
        and a2_agg_csv.exists()
        and compare_csv.exists()
        and not b1_agg_missing
        and not a2_agg_missing
        and not compare_missing
    )
    if not aggregate_ready:
        blockers.append(
            "aggregate_ready_failed "
            f"b1_missing={b1_agg_missing} a2_missing={a2_agg_missing} compare_missing={compare_missing}"
        )

    compare_rows_by_key = _rows_by_split_metric(compare_rows)
    main_metrics_not_worse, main_metric_failures = _evaluate_main_metric_direction(compare_rows_by_key)
    if not main_metrics_not_worse:
        blockers.append(f"main_metrics_not_worse_failed reasons={main_metric_failures}")

    stability_not_weaker, stability_failures = _evaluate_stability(compare_rows_by_key)
    if not stability_not_weaker:
        blockers.append(f"stability_not_weaker_failed reasons={stability_failures}")

    qualitative_support_ready = len(qualitative_missing) == 0
    if not qualitative_support_ready:
        blockers.append(f"qualitative_support_ready_failed missing={qualitative_missing}")

    gate_b1_compare = (
        fair_compare
        and standard_identity_ok
        and aggregate_ready
        and main_metrics_not_worse
        and stability_not_weaker
        and qualitative_support_ready
    )

    manifest_rows = _manifest_rows_by_key(manifest_csv) if manifest_csv.exists() else {}
    missing_manifest_keys = [key for key in _REQUIRED_MANIFEST_KEYS if key not in manifest_rows]
    manifest_assets_ready = (
        manifest_csv.exists()
        and not missing_manifest_keys
        and all(
            _manifest_exists_flag(manifest_rows, asset_key)
            for asset_key in [
                "B1_run_3407_dir",
                "B1_run_1234_dir",
                "B1_run_2025_dir",
                "baseline_per_seed_summary",
                "baseline_mean_std",
                "unet_vs_r34unet_comparison",
                "baseline_stage_summary",
            ]
        )
    )
    summary_ready = summary_path.exists()
    compare_ready = compare_csv.exists() and not compare_missing
    cases_ready = qualitative_support_ready
    raw_ready = raw_csv.exists() and not raw_missing
    b1_aggregate_ready = agg_csv.exists() and not b1_agg_missing
    assets_ready = (
        raw_ready
        and b1_aggregate_ready
        and compare_ready
        and summary_ready
        and cases_ready
        and manifest_assets_ready
    )
    if not assets_ready:
        blockers.append(
            "baseline_assets_ready_failed "
            f"raw_missing={raw_missing} b1_agg_missing={b1_agg_missing} compare_missing={compare_missing} "
            f"summary_ready={summary_ready} cases_ready={cases_ready} missing_manifest_keys={missing_manifest_keys}"
        )

    expected_manifest_values = {
        "freeze_best_selector": FORMAL_BEST_SELECTOR,
        "freeze_threshold_source": FORMAL_THRESHOLD_SOURCE,
        "freeze_threshold_value": str(b1_reference.get("threshold_value", "")),
        "freeze_eval_proto_version": str(b1_reference.get("eval_proto_version", "")),
        "freeze_eval_cast_policy": FORMAL_CAST_POLICY,
        "freeze_boundary_metric_width": str(FORMAL_BOUNDARY_WIDTH),
        "freeze_boundary_metric_impl": str(b1_reference.get("boundary_metric_impl", "")),
        "freeze_connected_components_impl": str(b1_reference.get("connected_components_impl", "")),
        "freeze_connected_components_connectivity": str(FORMAL_CONNECTIVITY),
        "freeze_result_tag": str(b1_reference.get("result_tag", "reproduced")),
        "freeze_aggregation": "mean+-std",
    }
    freeze_value_mismatches = []
    for asset_key, expected_value in expected_manifest_values.items():
        actual_value = _manifest_value(manifest_rows, asset_key)
        if actual_value != expected_value:
            freeze_value_mismatches.append(f"{asset_key}:{actual_value}!={expected_value}")
    freeze_ready = (
        complete_runs
        and proto_ok
        and fair_compare
        and manifest_csv.exists()
        and not freeze_value_mismatches
    )
    if not freeze_ready:
        blockers.append(f"freeze_ready_failed mismatches={freeze_value_mismatches}")

    handoff_ready = (
        manifest_assets_ready
        and summary_ready
        and raw_ready
        and b1_aggregate_ready
        and compare_ready
        and cases_ready
    )
    if not handoff_ready:
        blockers.append(
            "handoff_ready_failed "
            f"manifest_assets_ready={manifest_assets_ready} summary_ready={summary_ready} "
            f"raw_ready={raw_ready} b1_aggregate_ready={b1_aggregate_ready} "
            f"compare_ready={compare_ready} cases_ready={cases_ready}"
        )

    # 异常 run 裁决
    abnormal_resolved, abnormal_reasons = _check_abnormal_runs_resolved(run_metas)
    if not abnormal_resolved:
        blockers.append(f"abnormal_runs_unresolved reasons={abnormal_reasons}")

    gate_b1 = (complete_runs and proto_ok and assets_ready
               and freeze_ready and gate_b1_compare
               and handoff_ready and abnormal_resolved)

    gate_status = {
        "complete_runs": complete_runs,
        "proto_consistent": proto_ok,
        "fair_compare": fair_compare,
        "standard_identity_ok": standard_identity_ok,
        "aggregate_ready": aggregate_ready,
        "main_metrics_not_worse": main_metrics_not_worse,
        "stability_not_weaker": stability_not_weaker,
        "qualitative_support_ready": qualitative_support_ready,
        "baseline_assets_ready": assets_ready,
        "freeze_ready": freeze_ready,
        "gate_b1_compare": gate_b1_compare,
        "handoff_ready": handoff_ready,
        "abnormal_runs_resolved": abnormal_resolved,
        "gate_b1": gate_b1,
        "stage_pass_b1": gate_b1,
        "handoff_ready_for_c1": gate_b1,
        "missing_seeds": missing_seeds,
    }
    return gate_status, blockers


def build_baseline_stage_manifest(run_dirs: dict, raw_csv: Path, agg_csv: Path,
                                   compare_csv: Path, summary_path: Path,
                                   proto_ref: dict, b1_reference: dict,
                                   handoff_ready_for_c1: bool) -> Path:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md §6.3 章节
      要求 baseline_stage_manifest.csv 可被 05_LKMA 直接消费；
      字段 required_for_c1 标记下游依赖
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: current_standard_clean_restart_20260715
      - 许可证: project_internal
    本项目调整: B1 专属字段 required_for_c1（下游 05_LKMA 消费标记）
    """
    output_path = PROJECT_ROOT / "reports" / "tables" / "baseline_stage_manifest.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    asset_rows = []
    for seed in B1_SEEDS:
        run_dir = run_dirs.get(seed)
        rel = f"experiments/{B1_RUN_PREFIX}{seed}"
        exists = run_dir is not None and run_dir.exists()
        asset_rows.append(dict(
            asset_key=f"B1_run_{seed}_dir",
            relative_path=rel,
            exists=exists,
            required_for_c1=True,
        ))
    for key, path in [
        ("baseline_per_seed_summary", raw_csv),
        ("baseline_mean_std", agg_csv),
        ("unet_vs_r34unet_comparison", compare_csv),
        ("baseline_stage_summary", summary_path),
    ]:
        asset_rows.append(dict(
            asset_key=key,
            relative_path=_relative_path(path),
            exists=path.exists(),
            required_for_c1=True,
        ))
    for asset_key, value in [
        ("freeze_best_selector", str(proto_ref.get("best_selector", ""))),
        ("freeze_threshold_source", str(proto_ref.get("threshold_source", ""))),
        ("freeze_threshold_value", str(proto_ref.get("threshold_value", ""))),
        ("freeze_eval_proto_version", str(proto_ref.get("eval_proto_version", ""))),
        ("freeze_eval_cast_policy", str(proto_ref.get("eval_cast_policy", ""))),
        ("freeze_boundary_metric_width", str(proto_ref.get("boundary_metric_width", ""))),
        ("freeze_boundary_metric_impl", str(proto_ref.get("boundary_metric_impl", ""))),
        ("freeze_connected_components_impl", str(proto_ref.get("connected_components_impl", ""))),
        ("freeze_connected_components_connectivity", str(proto_ref.get("connected_components_connectivity", ""))),
        ("freeze_result_tag", str(b1_reference.get("result_tag", "reproduced"))),
        ("freeze_aggregation", "mean+-std"),
        ("handoff_ready_for_c1", str(handoff_ready_for_c1).lower()),
    ]:
        asset_rows.append(dict(
            asset_key=asset_key,
            relative_path=value,
            exists=True,
            required_for_c1=True,
        ))
    asset_rows.append(dict(
        asset_key="restriction_no_reopen_baseline",
        relative_path="(protocol)",
        exists=True,
        required_for_c1=True,
    ))

    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["asset_key", "relative_path", "exists", "required_for_c1"])
        writer.writeheader()
        for row in asset_rows:
            writer.writerow(row)
    print(f"baseline_manifest={_relative_path(output_path)}")
    return output_path


def mark_baseline_runs_invalid_for_aggregation(run_metas: dict, blocker: str) -> list[int]:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md §8.3 要求异常 run 必须标记 invalid_for_aggregation
    代码参考: 本项目自建，与 A2 同名函数对称
    本项目调整: 当前协议冻结，无漂移情况下返回空列表
    """
    return []


def finalize_stage_b1_handoff(gate_status: dict, blockers: list[str],
                               b1_agg_rows: list[dict], a2_agg_csv: Path) -> Path:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md §5.1-§5.9 全部规则卡片章节；
      stage_pass_b1 = Gate_B1 五子门全部 true
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: workspace_local_20260711
      - 许可证: project_internal
    本项目调整: 输出 reports/stage_reports/baseline_stage_summary.md
    """
    output_path = PROJECT_ROOT / "reports" / "stage_reports" / "baseline_stage_summary.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Baseline Stage Summary (B1 ResNet34-U-Net)",
        "",
        "## Gate Status",
        f"- complete_runs: `{str(gate_status['complete_runs']).lower()}`",
        f"- proto_consistent: `{str(gate_status['proto_consistent']).lower()}`",
        f"- fair_compare: `{str(gate_status.get('fair_compare', False)).lower()}`",
        f"- standard_identity_ok: `{str(gate_status.get('standard_identity_ok', False)).lower()}`",
        f"- aggregate_ready: `{str(gate_status.get('aggregate_ready', False)).lower()}`",
        f"- main_metrics_not_worse: `{str(gate_status.get('main_metrics_not_worse', False)).lower()}`",
        f"- stability_not_weaker: `{str(gate_status.get('stability_not_weaker', False)).lower()}`",
        f"- qualitative_support_ready: `{str(gate_status.get('qualitative_support_ready', False)).lower()}`",
        f"- baseline_assets_ready: `{str(gate_status['baseline_assets_ready']).lower()}`",
        f"- freeze_ready: `{str(gate_status['freeze_ready']).lower()}`",
        f"- gate_b1_compare: `{str(gate_status['gate_b1_compare']).lower()}`",
        f"- handoff_ready: `{str(gate_status['handoff_ready']).lower()}`",
        f"- abnormal_runs_resolved: `{str(gate_status['abnormal_runs_resolved']).lower()}`",
        f"- gate_b1: `{str(gate_status['gate_b1']).lower()}`",
        f"- stage_pass_b1: `{str(gate_status['stage_pass_b1']).lower()}`",
        f"- handoff_ready_for_c1: `{str(gate_status['handoff_ready_for_c1']).lower()}`",
    ]
    missing = gate_status.get("missing_seeds", [])
    if missing:
        lines.append(f"- missing_seeds: `{missing}`")

    # B1 vs A2 mean+-std 对比摘要
    lines.extend(["", "## B1 (ResNet34-U-Net) Mean+-Std Summary"])
    for split_role in ("testA", "testB"):
        lines.append(f"\n### {split_role}")
        for row in b1_agg_rows:
            if row.get("split_role") != split_role:
                continue
            try:
                m = float(row["mean"])
                s = float(row["std"])
                lines.append(f"- {row['metric_name']}: {m:.4f} +/- {s:.4f}")
            except (TypeError, ValueError, KeyError):
                pass

    lines.extend(["", "## Blocking Reasons", ""])
    if blockers:
        for b in blockers:
            lines.append(f"- {b}")
    else:
        lines.append("- none")

    if gate_status["stage_pass_b1"]:
        lines.extend([
            "",
            "## Conclusion",
            "",
            "B1 stage passed: ResNet34-U-Net three-seed runs are protocol-consistent, "
            "statistically traceable, and baseline assets are ready for 05_LKMA consumption.",
        ])
    else:
        lines.extend([
            "",
            "## Conclusion",
            "",
            "B1 stage blocked: prerequisites for 05_LKMA are not yet met. "
            "Resolve the listed comparison, stability, or asset blockers before handoff.",
        ])

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"stage_summary={_relative_path(output_path)}")
    return output_path


def write_baseline_stage_blockers(blockers: list[str]) -> Path:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md §8.3
    代码参考: 本项目自建，与 write_stage_blockers(A2) 对称
    本项目调整: 输出到 notes/b1_blockers.md
    """
    output_path = PROJECT_ROOT / "notes" / "b1_blockers.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# B1 Stage Blockers", ""]
    if blockers:
        for b in blockers:
            lines.append(f"- {b}")
    else:
        lines.append("- none")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def _summarize_baseline_contract(contract_path: Path) -> int:
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
    if not isinstance(contract, dict) or contract.get("stage") != "04_Baseline":
        raise RuntimeError(f"invalid baseline stage contract: {contract_path}")
    runs = contract.get("runs", [])
    expected = {(stage, seed) for stage in ("A2", "B1") for seed in A2_SEEDS}
    actual = {(str(item.get("run_name", "")).split("_", 1)[0], _parse_int(item.get("seed"))) for item in runs if isinstance(item, dict)}
    if len(runs) != 6 or actual != expected:
        raise RuntimeError(f"baseline contract must define the six A2/B1 runs, got {sorted(actual)}")
    for key in ("config_version", "train_proto_version", "eval_proto_version"):
        if not str(contract.get(key, "")).strip():
            raise RuntimeError(f"baseline contract missing {key}")

    per_seed: list[dict[str, Any]] = []
    aggregate: dict[str, list[dict[str, Any]]] = {"A2": [], "B1": []}
    b1_dirs: dict[int, Path] = {}
    for item in runs:
        run_name, seed, run_dir = str(item["run_name"]), _parse_int(item["seed"]), PROJECT_ROOT / str(item["output_dir"])
        stage = run_name.split("_", 1)[0]
        meta = _read_run_meta(run_dir)
        if meta is None:
            raise RuntimeError(f"contract run_meta missing: {run_dir}")
        for field, expected_value in {"run_name": run_name, "train_seed": seed, "stage_code": stage, "config_version": contract["config_version"], "train_proto_version": contract["train_proto_version"], "eval_proto_version": contract["eval_proto_version"]}.items():
            if str(meta.get(field)) != str(expected_value):
                raise RuntimeError(f"contract/run_meta identity mismatch: {run_name}:{field}")
        if stage == "B1":
            b1_dirs[seed] = run_dir
        for split, count in (("testA", 60), ("testB", 20)):
            samples = [row for row in _load_csv_rows(run_dir / f"{split}_metrics.csv") if row.get("row_type") == "sample"]
            if len(samples) != count:
                raise RuntimeError(f"sample row count mismatch: {run_name}:{split} expected={count} actual={len(samples)}")
            for field, expected_value in (("run_name", run_name), ("seed", seed), ("config_version", contract["config_version"]), ("eval_proto_version", contract["eval_proto_version"]), ("split_role", split)):
                if any(str(row.get(field, "")) != str(expected_value) for row in samples):
                    raise RuntimeError(f"sample identity mismatch: {run_name}:{split}:{field}")
            for column in _MIN_METRIC_COLS:
                values = [_parse_float(row.get(column)) for row in samples]
                if any(value is None or not math.isfinite(value) for value in values):
                    raise RuntimeError(f"invalid sample metric: {run_name}:{split}:{column}")
                per_seed.append({"run_name": run_name, "stage": stage, "seed": seed, "split_role": split, "metric_name": _METRIC_COL_TO_NAME[column], "metric_value": sum(values) / len(values), "config_version": contract["config_version"], "train_proto_version": contract["train_proto_version"], "eval_proto_version": contract["eval_proto_version"], "aggregation": "single_seed_sample_mean"})
    for stage in ("A2", "B1"):
        for split, metric in _expected_compare_pairs():
            values = [float(row["metric_value"]) for row in per_seed if row["stage"] == stage and row["split_role"] == split and row["metric_name"] == metric]
            if len(values) != 3:
                raise RuntimeError(f"incomplete aggregate: {stage}:{split}:{metric}")
            mean = sum(values) / 3
            aggregate[stage].append({"split_role": split, "metric_name": metric, "mean": mean, "std": math.sqrt(sum((value - mean) ** 2 for value in values) / 3), "n_runs": 3, "seeds": "3407,1234,2025", "config_version": contract["config_version"], "train_proto_version": contract["train_proto_version"], "eval_proto_version": contract["eval_proto_version"], "aggregation": "mean+-std_ddof0"})

    tables = PROJECT_ROOT / "reports" / "tables"
    def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader(); writer.writerows(rows)
    write_csv(tables / "baseline_per_seed_summary.csv", per_seed)
    write_csv(tables / "baseline_mean_std.csv", aggregate["B1"])
    a2, b1 = _rows_by_split_metric(aggregate["A2"]), _rows_by_split_metric(aggregate["B1"])
    comparison = [{"split_role": split, "metric_name": metric, "unet_mean": a2[(split, metric)]["mean"], "unet_std": a2[(split, metric)]["std"], "r34unet_mean": b1[(split, metric)]["mean"], "r34unet_std": b1[(split, metric)]["std"], "delta_mean_r34unet_minus_unet": b1[(split, metric)]["mean"] - a2[(split, metric)]["mean"], "config_version": contract["config_version"], "train_proto_version": contract["train_proto_version"], "eval_proto_version": contract["eval_proto_version"], "aggregation": "mean+-std_ddof0", "seeds": "3407,1234,2025", "n_runs": 3} for split, metric in _expected_compare_pairs()]
    write_csv(tables / "unet_vs_r34unet_comparison.csv", comparison)
    by_key = _rows_by_split_metric(comparison)
    main_ok, main_failures = _evaluate_main_metric_direction(by_key)
    stability_ok, stability_failures = _evaluate_stability(by_key)
    stage_pass = len(b1_dirs) == 3 and main_ok and stability_ok
    blockers = ([] if main_ok else [f"main_metrics_not_worse_failed reasons={main_failures}"]) + ([] if stability_ok else [f"stability_not_weaker_failed reasons={stability_failures}"])
    summary = PROJECT_ROOT / "reports" / "stage_reports" / "baseline_stage_summary.md"
    summary_lines = ["# Baseline Stage Summary (contract-derived v1 recovery)", "", "## Identity", f"- stage_contract: `{contract_path.relative_to(PROJECT_ROOT)}`", f"- config_version: `{contract['config_version']}`", f"- train_proto_version: `{contract['train_proto_version']}`", f"- eval_proto_version: `{contract['eval_proto_version']}`", "- source: `six contract runs; sample rows only; no legacy or v3 aggregate consumed`", "", "## Gate Status", "- complete_runs: `true`", f"- main_metrics_not_worse: `{str(main_ok).lower()}`", f"- stability_not_weaker: `{str(stability_ok).lower()}`", f"- gate_b1: `{str(stage_pass).lower()}`", f"- stage_pass_b1: `{str(stage_pass).lower()}`", f"- handoff_ready_for_c1: `{str(stage_pass).lower()}`", "", "## Blocking Reasons"]
    summary_lines.extend([f"- {item}" for item in blockers] if blockers else ["- none"])
    summary.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    manifest_rows = [{"asset_key": f"B1_run_{seed}_dir", "relative_path": _relative_path(path), "exists": True, "required_for_c1": True} for seed, path in sorted(b1_dirs.items())]
    manifest_rows += [{"asset_key": key, "relative_path": _relative_path(path), "exists": True, "required_for_c1": True} for key, path in [("baseline_per_seed_summary", tables / "baseline_per_seed_summary.csv"), ("baseline_mean_std", tables / "baseline_mean_std.csv"), ("unet_vs_r34unet_comparison", tables / "unet_vs_r34unet_comparison.csv"), ("baseline_stage_summary", summary)]]
    manifest_rows.append({"asset_key": "handoff_ready_for_c1", "relative_path": str(stage_pass).lower(), "exists": True, "required_for_c1": True})
    write_csv(tables / "baseline_stage_manifest.csv", manifest_rows)
    print(f"raw_table=reports/tables/baseline_per_seed_summary.csv rows={len(per_seed)}")
    print(f"comparison_table=reports/tables/unet_vs_r34unet_comparison.csv rows={len(comparison)}")
    print(f"stage_pass_b1={str(stage_pass).lower()}")
    return 0


def main_b1() -> int:
    contract_arg = next((sys.argv[index + 1] for index, value in enumerate(sys.argv[:-1]) if value == "--stage-contract"), None)
    return _summarize_baseline_contract((PROJECT_ROOT / contract_arg).resolve() if contract_arg else _CURRENT_STAGE_CONTRACT)


def _legacy_main_b1() -> int:
    """
    对应阶段: 04_Baseline
    理论依据: 计划 04_阶段验收.md Gate_B1 全部子门章节；
      顺序执行：collect → mean_std → compare → validate → blockers → manifest → finalize → re-validate
    代码参考:
      - 仓库: project_local_crc_gland_segmentation_project (本项目自建)
      - 文件: scripts/summarize_stage.py
      - commit: current_standard_clean_restart_20260715
      - 许可证: project_internal
    本项目调整: B1 专属产物路径，A2 只读不写
    """
    current_specs = _load_current_run_specs()
    run_dirs: dict[int, Path] = {}
    run_metas: dict[int, dict] = {}
    a2_run_dirs: dict[int, Path] = {}
    a2_run_metas: dict[int, dict] = {}
    missing_seeds: list[int] = []

    for spec in current_specs.values():
        run_name = spec["run_name"]
        run_dir = PROJECT_ROOT / spec["output_dir"]
        meta = _read_run_meta(run_dir)
        errors = [] if meta is None else _validate_current_run_identity(run_dir, meta, spec)
        if meta is None or errors:
            if errors:
                raise RuntimeError(f"current-round run identity mismatch: {errors}")
            missing_seeds.append(spec["seed"])
            continue
        if spec["stage_code"] == "B1":
            run_dirs[spec["seed"]] = run_dir
            run_metas[spec["seed"]] = meta
        elif spec["stage_code"] == "A2":
            a2_run_dirs[spec["seed"]] = run_dir
            a2_run_metas[spec["seed"]] = meta

    if set(run_metas) != set(B1_SEEDS) or set(a2_run_metas) != set(A2_SEEDS):
        raise RuntimeError(
            f"current-round six-run identity incomplete: B1={sorted(run_metas)}, A2={sorted(a2_run_metas)}"
        )

    print("=== B1 Baseline Stage Summary ===")
    print(f"seeds_total={len(B1_SEEDS)} seeds_found={len(run_metas)} missing={missing_seeds}")

    if run_metas:
        proto_ref = dict(run_metas[next(iter(run_metas))])
    else:
        proto_ref = {
                "model_name": "resnet34_unet", "model_version": "unknown", "config_version": "",
            "bn_policy_version": "",
            "data_proto_version": "01_data_protocol_v1",
            "train_proto_version": "train_proto_v1",
            "eval_proto_version": "eval_proto_v1",
            "eval_cast_policy": FORMAL_CAST_POLICY,
            "boundary_metric_width": str(FORMAL_BOUNDARY_WIDTH),
            "boundary_metric_impl": "binary_erosion_xor_plus_binary_dilation",
            "connected_components_impl": "scipy.ndimage.label",
            "connected_components_connectivity": str(FORMAL_CONNECTIVITY),
            "best_selector": FORMAL_BEST_SELECTOR,
            "threshold_source": FORMAL_THRESHOLD_SOURCE,
            "threshold_value": "0.5",
        }

    # Current round is the only A2 source; legacy prefix discovery remains available only to main_a2.
    # The manifest must also name the aggregate consumed below.
    a2_agg_csv = _current_a2_aggregate_path(current_specs)
    _validate_aggregate_identity(a2_agg_csv, a2_run_metas, "A2")

    # 1. 收集 raw per-seed 结果
    raw_rows = collect_baseline_seed_results(run_dirs, proto_ref)

    # 2. 构建 mean+-std 聚合表
    b1_agg_rows = build_baseline_mean_std(raw_rows, proto_ref)

    # 3. A2 聚合表路径来自 current manifest（只读，绝不写）

    # 4. UNet vs R34UNet 比较表
    compare_csv = build_unet_vs_r34unet_comparison(b1_agg_rows, a2_agg_csv, a2_run_metas)

    # 5. 产物路径解析
    raw_csv = PROJECT_ROOT / "reports" / "tables" / "baseline_per_seed_summary.csv"
    agg_csv = PROJECT_ROOT / "reports" / "tables" / "baseline_mean_std.csv"
    summary_path = PROJECT_ROOT / "reports" / "stage_reports" / "baseline_stage_summary.md"
    manifest_csv = PROJECT_ROOT / "reports" / "tables" / "baseline_stage_manifest.csv"

    # 6. Gate_B1 全部子门验证
    gate_status, blockers = validate_baseline_stage(
        run_metas, a2_run_metas, run_dirs, raw_csv, agg_csv, compare_csv, summary_path, manifest_csv, a2_agg_csv
    )

    # 8. 构建 handoff manifest
    build_baseline_stage_manifest(
        run_dirs, raw_csv, agg_csv, compare_csv, summary_path, proto_ref, run_metas.get(B1_SEEDS[0], {}), handoff_ready_for_c1=False
    )

    # 9. 最终阶段总结（summary_path 此时会被创建）
    finalize_stage_b1_handoff(gate_status, blockers, b1_agg_rows, a2_agg_csv)

    # 10. 再次校验 summary 和 manifest 已存在后重跑 gate 确认
    gate_status, blockers = validate_baseline_stage(
        run_metas, a2_run_metas, run_dirs, raw_csv, agg_csv, compare_csv, summary_path, manifest_csv, a2_agg_csv
    )
    build_baseline_stage_manifest(
        run_dirs,
        raw_csv,
        agg_csv,
        compare_csv,
        summary_path,
        proto_ref,
        run_metas.get(B1_SEEDS[0], {}),
        handoff_ready_for_c1=gate_status["handoff_ready_for_c1"],
    )
    gate_status, blockers = validate_baseline_stage(
        run_metas, a2_run_metas, run_dirs, raw_csv, agg_csv, compare_csv, summary_path, manifest_csv, a2_agg_csv
    )
    finalize_stage_b1_handoff(gate_status, blockers, b1_agg_rows, a2_agg_csv)
    write_baseline_stage_blockers(blockers)

    # 输出摘要
    print(f"stage_pass_b1={str(gate_status['stage_pass_b1']).lower()}")
    if missing_seeds:
        print(f"missing_runs={missing_seeds}")
    if blockers:
        for b in blockers:
            print(f"blocker: {b}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
