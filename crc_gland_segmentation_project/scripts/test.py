"""
对应阶段: 03_UNet稳定性
理论依据:
  - 论文: Sirinukunwattana et al., 2017, "Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest"
  章节: §2.3 (Evaluation Metrics)
  公式/定义: Dice coefficient, Object-level Dice, Hausdorff distance
  - 协议冻结评估: 阶段总协议 §8.1 要求 test 链路固化 eval_cast_policy、boundary_metric_width、connected_components_connectivity 到三层 run_meta.yaml / raw CSV / aggregate CSV
  - 指标复算校验: metric_crosscheck_note.md 提供 per-split 的 sample_mean vs aggregate 交叉验证
  - 可视化导出: 每 split 导出 worst-case visual samples 用于错误模式分析
代码参考:
  - 仓库: https://github.com/milesial/Pytorch-UNet
  - 文件: predict.py (评估推理模式参考)
  - commit: 参考 master 分支
  - 许可证: GPL-3.0
  - 本项目调整: 从 train 模块复用 run_dir/build_output_dir、固化三层落盘、T-9 runtime probe 保护
冻结回链: 结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md
  - threshold_value=0.5, threshold_source=val17, connected_components_connectivity=8, boundary_metric_width=3
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
from pathlib import Path
import re
import shutil
import sys
from typing import Any

import os


def _validate_launcher_hash_seed() -> None:
    config_arg = next((sys.argv[i + 1] for i, value in enumerate(sys.argv[:-1]) if value == "--config"), None)
    if not config_arg:
        raise SystemExit("--config is required before importing torch")
    config_path = (Path(__file__).resolve().parents[1] / config_arg).resolve()
    match = re.search(r"^train_seed:\s*(\d+)\s*$", config_path.read_text(encoding="utf-8"), re.MULTILINE)
    if match is None:
        raise SystemExit(f"config train_seed missing: {config_path}")
    expected = match.group(1)
    actual = os.environ.get("PYTHONHASHSEED")
    if actual != expected:
        raise SystemExit(f"PYTHONHASHSEED must be launcher-set to {expected!r}; got {actual!r}")


_validate_launcher_hash_seed()
if os.environ.get("CUBLAS_WORKSPACE_CONFIG") != ":4096:8":
    raise SystemExit("CUBLAS_WORKSPACE_CONFIG must be launcher-set to ':4096:8' before importing torch")
from PIL import Image
import torch
from torch.utils.data import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from b_class_auxiliary.tools.experiment_environment import ensure_environment

ensure_environment()

import train as train_entry
from src.data import build_eval_transform, build_segmentation_dataset, export_binary_mask_png, load_data_config
from src.eval import evaluate_split, export_run_visual_assets
from src.losses import build_boundary_loss, build_distance_loss, build_seg_loss
from src.models import build_unet_model
from src.utils import collect_reproducibility_values, set_global_seed


def _validate_reproducibility(run_meta: dict[str, Any], config_path: Path, config_bundle: dict[str, Any], experiment_config: dict[str, Any], project_root: Path, device: torch.device) -> None:
    data_config_path = (project_root / config_bundle["paths"]["data"]).resolve()
    asset_manifest_path = train_entry.resolve_asset_manifest_path(project_root, experiment_config)
    hashes = train_entry.build_data_trace_hashes(project_root, data_config_path, asset_manifest_path)
    model_name = str(config_bundle["model"].get("model_name", config_bundle["model"].get("name", ""))).lower()
    pretrained_path: Path | None = None
    pretrained_hash: str | None = None
    if model_name == "resnet34_unet":
        configured_path = config_bundle["model"].get("pretrained_weights_path")
        configured_hash = config_bundle["model"].get("pretrained_weights_sha256")
        if not configured_path or not configured_hash:
            raise ValueError("B1 model config must define pretrained_weights_path and pretrained_weights_sha256")
        pretrained_path = (project_root / str(configured_path)).resolve()
        pretrained_hash = str(configured_hash)
    current = collect_reproducibility_values(
        project_root,
        config_path,
        config_bundle,
        hashes,
        experiment_config,
        device,
        bool(config_bundle["train"].get("amp", False)),
        {
            "amp_grad_scaler_init_scale": 65536.0,
            "amp_grad_scaler_growth_factor": 2.0,
            "amp_grad_scaler_backoff_factor": 0.5,
            "amp_grad_scaler_growth_interval": 2000,
        },
        extra_paths=(project_root / "scripts/train.py", project_root / "scripts/test.py"),
        pretrained_weights_path=pretrained_path,
        pretrained_weights_sha256=pretrained_hash,
    )
    metadata_template = train_entry.build_run_meta(
        experiment_config,
        config_bundle,
        load_data_config(project_root, data_config_path),
        str(run_meta.get("run_name", experiment_config.get("run_name", ""))),
        bool(run_meta.get("smoke_check", False)),
        hashes,
    )
    expected = {**run_meta.get("reproducibility", {}), **run_meta}
    amp_requested = bool(config_bundle["train"].get("amp", False))
    current_values = {
        **current,
        "amp_requested": amp_requested,
        "amp_active": amp_requested and device.type == "cuda",
        "pretrained_weights_path": pretrained_path.relative_to(project_root).as_posix() if pretrained_path else "not_applicable",
        "pretrained_weights_sha256": current["resnet34_pretrained_weight_sha256"] if pretrained_path else "not_applicable",
        "amp_grad_scaler_init_scale": metadata_template["amp_grad_scaler_init_scale"],
        "amp_grad_scaler_growth_factor": metadata_template["amp_grad_scaler_growth_factor"],
        "amp_grad_scaler_backoff_factor": metadata_template["amp_grad_scaler_backoff_factor"],
        "amp_grad_scaler_growth_interval": metadata_template["amp_grad_scaler_growth_interval"],
    }
    current_values["torch_version"] = current["torch_version"]
    current_values["cuda_runtime_version"] = current["cuda_runtime_version"]
    current_values["cudnn_version"] = current["cudnn_version"]
    current_values["cuda_devices"] = current["cuda_devices"]
    current_values["source_tree_sha256"] = current["source_tree_sha256"]
    current_values["frozen_source_config_sha256"] = current["frozen_source_config_sha256"]
    fields = (
        "data_config_sha256", "split_manifest_sha256", "asset_manifest_sha256", "dataset_files_sha256",
        "source_tree_sha256", "frozen_source_config_sha256", "reproducibility_contract_sha256",
        "pythonhashseed", "cublas_workspace_config", "torch_version", "cuda_runtime_version",
        "cudnn_version", "cuda_devices", "deterministic_algorithms", "cudnn_deterministic", "cudnn_benchmark",
        "amp_requested", "amp_active",
        "amp_grad_scaler_init_scale", "amp_grad_scaler_growth_factor",
        "amp_grad_scaler_backoff_factor", "amp_grad_scaler_growth_interval",
        "pretrained_weights_path", "pretrained_weights_sha256",
    )
    missing = [field for field in fields if field not in expected or expected[field] is None]
    if missing:
        raise ValueError(f"run_meta missing reproducibility fields: {missing}")
    def canonical_value(field: str, value: Any) -> Any:
        if field in {"pythonhashseed", "cuda_runtime_version"} and value is not None:
            return str(value)
        return value

    mismatches = {
        field: {"expected": expected[field], "current": current_values.get(field)}
        for field in fields
        if canonical_value(field, expected[field]) != canonical_value(field, current_values.get(field))
    }
    if mismatches:
        raise ValueError(f"reproducibility mismatch: {mismatches}")


def parse_args() -> argparse.Namespace:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    parser = argparse.ArgumentParser(description="Formal stage02 test entrypoint.")
    parser.add_argument("--config", required=True, help="Relative path to the experiment config.")
    parser.add_argument("--run-name", default=None, help="Optional run name override.")
    parser.add_argument("--reproducibility-run", action="store_true", help="Read/write this run under experiments/reproducibility_audit/repeat_runs/.")
    parser.add_argument("--device", default="cuda", help="Requested device hint (auto-fallback to CPU if CUDA unavailable).")
    parser.add_argument("--checkpoint", default=None, help="Optional checkpoint path override.")
    parser.add_argument(
        "--max-samples-per-split",
        type=int,
        default=None,
        help="Optional sample cap for local CPU connectivity checks.",
    )
    parser.add_argument(
        "--max-visual-samples",
        type=int,
        default=5,
        help="How many worst-case samples to export per split.",
    )
    parser.add_argument(
        "--skip-visuals",
        action="store_true",
        help="Skip visual export and only write metrics, predictions, note, and summary.",
    )
    return parser.parse_args()


def _relative_path(path: Path) -> str:
    return path.resolve().relative_to(PROJECT_ROOT).as_posix()


def _resolve_run_dir(
    experiment_config: dict[str, Any],
    run_name_override: str | None,
    reproducibility_run: bool,
) -> Path:
    run_name = run_name_override or str(experiment_config["run_name"])
    return train_entry.build_output_dir(PROJECT_ROOT, run_name, reproducibility_run=reproducibility_run)


def _resolve_checkpoint_path(run_dir: Path, checkpoint_override: str | None) -> Path:
    default_path = (run_dir / "checkpoints" / "best.ckpt").resolve()
    if checkpoint_override:
        candidate = Path(checkpoint_override)
        if not candidate.is_absolute():
            candidate = (PROJECT_ROOT / checkpoint_override).resolve()
        checkpoints_dir = (run_dir / "checkpoints").resolve()
        if candidate != default_path:
            raise ValueError(f"checkpoint override must equal current run best.ckpt: {candidate}")
        return candidate
    return default_path


def _load_checkpoint(model: torch.nn.Module, checkpoint_path: Path, device: torch.device) -> dict[str, Any]:
    checkpoint = torch.load(checkpoint_path, map_location=device)
    if not isinstance(checkpoint, dict) or "model_state_dict" not in checkpoint:
        raise ValueError(f"checkpoint format is invalid: {checkpoint_path}")
    model.load_state_dict(checkpoint["model_state_dict"])
    checkpoint["checkpoint_path"] = "checkpoints/best.ckpt"
    checkpoint["checkpoint_sha256"] = hashlib.sha256(checkpoint_path.read_bytes()).hexdigest()
    checkpoint["model_identity"] = {
        "model_module": model.__class__.__module__,
        "model_class": model.__class__.__qualname__,
    }
    return checkpoint


def _validate_test_identity(
    *,
    experiment_config: dict[str, Any],
    model_config: dict[str, Any],
    eval_config: dict[str, Any],
    run_meta: dict[str, Any],
    checkpoint: dict[str, Any],
    checkpoint_path: Path,
    run_dir: Path,
    run_name_override: str | None,
) -> tuple[str, int, str, int, float, str, str]:
    expected_run_name = run_name_override or str(experiment_config.get("run_name", ""))
    actual_run_name = str(run_meta.get("run_name", ""))
    if not expected_run_name or actual_run_name != expected_run_name:
        raise ValueError(
            f"run identity mismatch: expected={expected_run_name!r}, actual={actual_run_name!r}"
        )

    required_identity_fields = ("run_name", "train_seed", "config_version", "model_name", "stage_code", "dataset_code")
    missing_identity = [field for field in required_identity_fields if field not in run_meta]
    if missing_identity:
        raise ValueError(f"run_meta missing required identity fields: {missing_identity}")
    checkpoint_identity_fields = ("run_name", "seed", "config_version", "model_name", "stage_code", "dataset_code")
    missing_checkpoint_identity = [field for field in checkpoint_identity_fields if field not in checkpoint]
    if missing_checkpoint_identity:
        raise ValueError(f"checkpoint missing required identity fields: {missing_checkpoint_identity}")
    for field in ("stage_code", "dataset_code"):
        expected_value = str(experiment_config.get(field, ""))
        actual_value = str(run_meta.get(field, ""))
        if expected_value and actual_value != expected_value:
            raise ValueError(
                f"{field} identity mismatch: config={expected_value!r}, run_meta={actual_value!r}"
            )

    expected_seed = int(experiment_config.get("train_seed", 0))
    actual_seed = int(run_meta.get("train_seed", 0))
    if actual_seed != expected_seed or checkpoint.get("seed") not in (None, actual_seed):
        raise ValueError(f"seed identity mismatch: config={expected_seed}, run_meta={actual_seed}")

    expected_model_name = str(model_config.get("model_name", ""))
    actual_model_name = str(run_meta.get("model_name", expected_model_name))
    if expected_model_name and actual_model_name != expected_model_name:
        raise ValueError(f"model_name identity mismatch: config={expected_model_name}, run_meta={actual_model_name}")
    expected_module = str(run_meta.get("model_module", ""))
    actual_module = str(checkpoint["model_identity"]["model_module"])
    if expected_module and expected_module != actual_module:
        raise ValueError(f"model_module identity mismatch: run_meta={expected_module}, loaded={actual_module}")

    expected_config_version = str(experiment_config.get("config_version", ""))
    actual_config_version = str(run_meta.get("config_version", ""))
    if expected_config_version and actual_config_version != expected_config_version:
        raise ValueError(
            f"config_version mismatch: config={expected_config_version}, run_meta={actual_config_version}"
        )
    for field, expected in {
        "run_name": actual_run_name,
        "seed": actual_seed,
        "config_version": actual_config_version,
        "model_name": expected_model_name,
        "stage_code": str(experiment_config.get("stage_code", "")),
        "dataset_code": str(experiment_config.get("dataset_code", "")),
    }.items():
        if checkpoint.get(field) != expected:
            raise ValueError(f"checkpoint identity mismatch for {field}: {checkpoint.get(field)!r} != {expected!r}")
    checkpoint_config_version = checkpoint.get("config_version")
    if checkpoint_config_version not in (None, actual_config_version):
        raise ValueError(f"checkpoint config_version mismatch: {checkpoint_config_version!r} != {actual_config_version!r}")

    expected_eval_proto = str(eval_config.get("eval_proto_version", ""))
    actual_eval_proto = str(run_meta.get("eval_proto_version", ""))
    if expected_eval_proto and actual_eval_proto != expected_eval_proto:
        raise ValueError(f"eval_proto_version mismatch: config={expected_eval_proto}, run_meta={actual_eval_proto}")

    checkpoint_relative_path = "checkpoints/best.ckpt"
    if "best_checkpoint_path" not in run_meta:
        raise ValueError("run_meta missing best_checkpoint_path")
    expected_checkpoint_path = str(run_meta["best_checkpoint_path"])
    expected_path = Path(expected_checkpoint_path)
    if expected_path.is_absolute():
        expected_checkpoint_resolved = expected_path.resolve()
    elif expected_path.parts and expected_path.parts[0] == "experiments":
        expected_checkpoint_resolved = (PROJECT_ROOT / expected_path).resolve()
    else:
        expected_checkpoint_resolved = (run_dir / expected_path).resolve()
    loaded_checkpoint_resolved = (run_dir / checkpoint_relative_path).resolve()
    if expected_checkpoint_resolved != loaded_checkpoint_resolved:
        raise ValueError(
            f"checkpoint path mismatch: run_meta={expected_checkpoint_path}, loaded={checkpoint_relative_path}"
        )
    checkpoint_epoch = int(checkpoint.get("epoch", 0))
    if "best_checkpoint_epoch" not in run_meta:
        raise ValueError("run_meta missing best_checkpoint_epoch")
    expected_epoch = run_meta["best_checkpoint_epoch"]
    if int(expected_epoch) != checkpoint_epoch:
        raise ValueError(f"checkpoint epoch mismatch: run_meta={expected_epoch}, loaded={checkpoint_epoch}")
    if "best_metric_value" not in run_meta:
        raise ValueError("run_meta missing best_metric_value")
    checkpoint_metric_value = float(checkpoint.get("metric_value", float("nan")))
    expected_metric = run_meta["best_metric_value"]
    if not math.isclose(float(expected_metric), checkpoint_metric_value, rel_tol=0.0, abs_tol=1.0e-7):
        raise ValueError(f"checkpoint metric mismatch: run_meta={expected_metric}, loaded={checkpoint_metric_value}")
    checkpoint_sha256 = str(checkpoint["checkpoint_sha256"])
    if "best_checkpoint_sha256" not in run_meta:
        raise ValueError("run_meta missing best_checkpoint_sha256")
    expected_sha256 = str(run_meta["best_checkpoint_sha256"])
    if expected_sha256 != checkpoint_sha256:
        raise ValueError("checkpoint SHA256 mismatch with run_meta")

    model_identity = f"{actual_module}.{checkpoint['model_identity']['model_class']}"
    return (
        actual_run_name,
        actual_seed,
        model_identity,
        checkpoint_epoch,
        checkpoint_metric_value,
        checkpoint_sha256,
        actual_config_version,
    )


def _write_metrics_csv(
    output_path: Path,
    sample_rows: list[dict[str, Any]],
    split_role: str,
    run_name: str,
    seed: int,
    model_identity: str,
    checkpoint_path: str,
    checkpoint_epoch: int,
    checkpoint_metric_value: float,
    checkpoint_sha256: str,
    config_version: str,
    eval_protocol: dict[str, Any],
) -> None:
    fieldnames = [
        "row_type",
        "run_name",
        "seed",
        "model_identity",
        "checkpoint_relative_path",
        "checkpoint_epoch",
        "checkpoint_metric_value",
        "checkpoint_sha256",
        "config_version",
        "eval_proto_version",
        "boundary_metric_name",
        "boundary_metric_width",
        "boundary_metric_unit",
        "boundary_metric_source",
        "boundary_metric_impl",
        "boundary_metric_connectivity",
        "boundary_metric_border_value",
        "boundary_metric_tolerance",
        "hd95_impl",
        "empty_set_policy",
        "sample_id",
        "split_role",
        "sample_count",
        "source_image_path",
        "source_mask_path",
        "eval_image_path",
        "eval_gt_path",
        "pred_path",
        "loss",
        "loss_bce",
        "loss_dice",
        "objdice",
        "dice",
        "iou",
        "f1",
        "boundary_f1",
        "hd95",
        "object_hausdorff",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in sample_rows:
            row.update({
                "run_name": run_name,
                "seed": seed,
                "model_identity": model_identity,
                "checkpoint_relative_path": checkpoint_path,
                "checkpoint_epoch": checkpoint_epoch,
                "checkpoint_metric_value": checkpoint_metric_value,
                "checkpoint_sha256": checkpoint_sha256,
                "config_version": config_version,
                **{key: eval_protocol.get(key, "") for key in fieldnames if key in eval_protocol},
            })
            writer.writerow(row)


def _build_sample_rows(run_dir: Path, split_role: str, sample_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    predictions_dir = run_dir / "predictions" / split_role
    eval_images_dir = run_dir / "eval_assets" / split_role / "images"
    eval_gts_dir = run_dir / "eval_assets" / split_role / "gt"
    for output_dir in (predictions_dir, eval_images_dir, eval_gts_dir):
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    for record in sample_records:
        sample_id = str(record["sample_id"])
        pred_path = predictions_dir / f"{sample_id}_pred.png"
        eval_gt_path = eval_gts_dir / f"{sample_id}_gt.png"
        eval_image_path = eval_images_dir / f"{sample_id}_image.png"
        export_binary_mask_png(record["pred_mask"], pred_path)
        export_binary_mask_png(record["target_mask"], eval_gt_path)
        Image.open(record["image_path"]).convert("RGB").resize(
            (record["pred_mask"].shape[1], record["pred_mask"].shape[0]), Image.Resampling.BILINEAR
        ).save(eval_image_path)
        rows.append(
            {
                "row_type": "sample",
                "sample_id": sample_id,
                "split_role": split_role,
                "sample_count": 1,
                "source_image_path": _relative_path(Path(record["image_path"])),
                "source_mask_path": _relative_path(Path(record["mask_path"])),
                "eval_image_path": _relative_path(eval_image_path),
                "eval_gt_path": _relative_path(eval_gt_path),
                "pred_path": _relative_path(pred_path),
                "loss": "not_applicable",
                "loss_bce": "not_applicable",
                "loss_dice": "not_applicable",
                "objdice": record["metrics"]["objdice"],
                "dice": record["metrics"]["dice"],
                "iou": record["metrics"]["iou"],
                "f1": record["metrics"]["f1"],
                "boundary_f1": record["metrics"]["boundary_f1"],
                "hd95": record["metrics"]["hd95"],
                "object_hausdorff": record["metrics"]["object_hausdorff"],
            }
        )
    return rows


def _is_close_or_both_nan(left: float, right: float, atol: float = 1.0e-6) -> bool:
    if math.isnan(left) and math.isnan(right):
        return True
    return abs(left - right) <= atol


def _write_metric_crosscheck_note(
    run_dir: Path,
    sample_rows_by_split: dict[str, list[dict[str, Any]]],
    aggregate_by_split: dict[str, dict[str, float]],
    eval_config: dict[str, Any],
) -> str:
    metric_names = ["objdice", "dice", "iou", "f1", "boundary_f1", "hd95", "object_hausdorff"]
    lines = [
        "# Metric Crosscheck Note",
        "",
        "- crosscheck_scope: `python_reaggregation_from_split_csv`",
        "- official_reference_type: `project_internal_reaggregation_sanity_check`",
        f"- threshold_source: `{eval_config['threshold_source']}`",
        f"- threshold_value: `{eval_config['threshold_value']}`",
        f"- boundary_metric_width: `{eval_config['boundary_metric_width']}`",
        f"- boundary_metric_impl: `binary_erosion_xor_plus_binary_dilation`",
        f"- connected_components_connectivity: `{eval_config.get('connected_components_connectivity', 1)}`",
        "",
        "## Split Checks",
        "",
    ]

    overall_ok = True
    for split_role in ("testA", "testB"):
        sample_rows = sample_rows_by_split[split_role]
        aggregate = aggregate_by_split[split_role]
        lines.append(f"### {split_role}")
        lines.append("")
        lines.append(f"- sample_count: `{len(sample_rows)}`")
        lines.append(
            "- sampled_ids: `"
            + ", ".join(row["sample_id"] for row in sample_rows[: min(5, len(sample_rows))])
            + "`"
        )
        split_ok = True
        for metric_name in metric_names:
            sample_values = [float(row[metric_name]) for row in sample_rows]
            sample_mean = float(sum(sample_values) / len(sample_values)) if sample_values else float("nan")
            aggregate_value = float(aggregate[metric_name])
            is_ok = _is_close_or_both_nan(sample_mean, aggregate_value)
            split_ok = split_ok and is_ok
            lines.append(
                "- "
                + f"`{metric_name}`: sample_mean=`{sample_mean}` / aggregate=`{aggregate_value}` / "
                + f"status=`{'pass' if is_ok else 'fail'}`"
            )
        lines.append("")
        overall_ok = overall_ok and split_ok

    lines.insert(6, f"- metric_crosscheck_result: `{'pass' if overall_ok else 'partial'}`")
    note_path = run_dir / "metric_crosscheck_note.md"
    note_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "pass" if overall_ok else "partial"


def _update_run_meta(
    run_dir: Path,
    run_meta: dict[str, Any],
    aggregate_by_split: dict[str, dict[str, float]],
    crosscheck_result: str,
    visual_info: dict[str, Any] | None,
) -> None:
    run_meta["metric_list"] = [
        "f1",
        "objdice",
        "object_hausdorff",
        "dice",
        "iou",
        "hd95",
        "boundary_f1",
    ]
    run_meta["boundary_metric_width"] = int(run_meta.get("boundary_metric_width", 3))
    run_meta["metric_crosscheck_result"] = crosscheck_result
    run_meta["metric_crosscheck_note_path"] = _relative_path(run_dir / "metric_crosscheck_note.md")
    run_meta["visual_version"] = "visual_proto_v1"
    run_meta["testA_sample_count"] = int(aggregate_by_split["testA"]["sample_count"])
    run_meta["testB_sample_count"] = int(aggregate_by_split["testB"]["sample_count"])
    run_meta["testA_objdice"] = float(aggregate_by_split["testA"]["objdice"])
    run_meta["testB_objdice"] = float(aggregate_by_split["testB"]["objdice"])
    if visual_info is not None:
        run_meta["num_visual_samples_testA"] = int(visual_info["visual_counts"].get("testA", 0))
        run_meta["num_visual_samples_testB"] = int(visual_info["visual_counts"].get("testB", 0))
    (run_dir / "run_meta.yaml").write_text(train_entry.dump_simple_yaml(run_meta) + "\n", encoding="utf-8")


def _write_run_summary(
    run_dir: Path,
    run_meta: dict[str, Any],
    aggregate_by_split: dict[str, dict[str, float]],
    crosscheck_result: str,
    visual_info: dict[str, Any] | None,
) -> None:
    major_failure_modes = []
    if visual_info is not None:
        major_failure_modes = visual_info["major_failure_modes"]
    visuals_ready = visual_info is not None and all(count > 0 for count in visual_info["visual_counts"].values())
    baseline_ready = crosscheck_result == "pass"
    lines = [
        "# Run Summary",
        "",
        f"- stop_reason: `{run_meta.get('stop_reason', 'evaluation_completed')}`",
        f"- best_epoch: `{run_meta.get('best_epoch', 'unknown')}`",
        f"- best_metric_name: `val_objdice`",
        f"- best_metric_value: `{run_meta.get('best_metric_value', 'unknown')}`",
        f"- smoke_check: `{str(run_meta.get('smoke_check', False)).lower()}`",
        f"- amp_active: `{str(run_meta.get('amp_active', False)).lower()}`",
        f"- metric_crosscheck_result: `{crosscheck_result}`",
        f"- visuals_ready: `{str(visuals_ready).lower()}`",
        f"- baseline_ready: `{str(baseline_ready).lower()}`",
        "",
        "## Test Splits",
        "",
        f"- testA_objdice: `{aggregate_by_split['testA']['objdice']:.6f}`",
        f"- testA_dice: `{aggregate_by_split['testA']['dice']:.6f}`",
        f"- testB_objdice: `{aggregate_by_split['testB']['objdice']:.6f}`",
        f"- testB_dice: `{aggregate_by_split['testB']['dice']:.6f}`",
        "",
        "## Findings",
        "",
        "- main_findings: `Split-wise metrics, predictions, and crosscheck note have been exported.`",
        "- protocol_abnormal_signs: `No aggregate-vs-sample reaggregation mismatch was found.`"
        if crosscheck_result == "pass"
        else "- protocol_abnormal_signs: `Aggregate-vs-sample reaggregation mismatch still exists and must be checked.`",
        "- major_failure_modes: `" + (", ".join(major_failure_modes) if major_failure_modes else "not_exported") + "`",
    ]
    (run_dir / "summaries").mkdir(parents=True, exist_ok=True)
    (run_dir / "summaries" / "run_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    args = parse_args()
    config_path, experiment_config = train_entry.load_experiment_config(PROJECT_ROOT, args.config)
    config_bundle = train_entry.load_training_configs(PROJECT_ROOT, experiment_config)
    run_dir = _resolve_run_dir(experiment_config, args.run_name, args.reproducibility_run)
    run_meta_path = run_dir / "run_meta.yaml"
    if not run_meta_path.exists():
        raise FileNotFoundError(f"run_meta.yaml not found: {run_meta_path}")

    set_global_seed(int(experiment_config["train_seed"]))
    data_config_path = (PROJECT_ROOT / config_bundle["paths"]["data"]).resolve()
    data_config = load_data_config(PROJECT_ROOT, data_config_path)
    eval_transform = build_eval_transform(data_config)
    train_config = config_bundle["train"]
    eval_config = config_bundle["eval"]

    test_datasets = {
        "testA": build_segmentation_dataset(PROJECT_ROOT, data_config, "testA", transform=eval_transform),
        "testB": build_segmentation_dataset(PROJECT_ROOT, data_config, "testB", transform=eval_transform),
    }
    test_loaders = {
        split_role: DataLoader(
            dataset,
            batch_size=int(train_config["batch_size"]),
            shuffle=False,
            num_workers=int(train_config["num_workers"]),
        )
        for split_role, dataset in test_datasets.items()
    }

    device = train_entry.resolve_device(args.device)
    model = build_unet_model(config_bundle["model"]).to(device)
    if bool(config_bundle["model"].get("use_boundary_head", False)):
        loss_fn = build_boundary_loss(train_config)
    elif bool(config_bundle["model"].get("use_distance_head", False)):
        loss_fn = build_distance_loss(train_config)
    else:
        loss_fn = build_seg_loss(train_config)
    checkpoint_path = _resolve_checkpoint_path(run_dir, args.checkpoint)
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"checkpoint not found: {checkpoint_path}")
    checkpoint = _load_checkpoint(model, checkpoint_path, device)

    run_meta = train_entry.simple_yaml_load(run_meta_path.read_text(encoding="utf-8"))
    _validate_reproducibility(run_meta, config_path, config_bundle, experiment_config, PROJECT_ROOT, device)
    (
        run_name,
        seed,
        model_identity,
        checkpoint_epoch,
        checkpoint_metric_value,
        checkpoint_sha256,
        config_version,
    ) = _validate_test_identity(
        experiment_config=experiment_config,
        model_config=config_bundle["model"],
        eval_config=eval_config,
        run_meta=run_meta,
        checkpoint=checkpoint,
        checkpoint_path=checkpoint_path,
        run_dir=run_dir,
        run_name_override=args.run_name,
    )
    checkpoint_relative_path = str(checkpoint["checkpoint_path"])

    split_results: dict[str, dict[str, Any]] = {}
    sample_rows_by_split: dict[str, list[dict[str, Any]]] = {}
    aggregate_by_split: dict[str, dict[str, float]] = {}
    for split_role in ("testA", "testB"):
        result = evaluate_split(
            model=model,
            dataloader=test_loaders[split_role],
            loss_fn=loss_fn,
            device=device,
            threshold_value=float(eval_config["threshold_value"]),
            boundary_width=int(eval_config["boundary_metric_width"]),
            connected_components_connectivity=int(eval_config["connected_components_connectivity"]),
            split_role=split_role,
            max_samples=args.max_samples_per_split,
            include_distance_metrics=args.max_samples_per_split is None,
            eval_protocol=eval_config,
        )
        sample_rows = _build_sample_rows(run_dir, split_role, result["sample_records"])
        _write_metrics_csv(
            run_dir / f"{split_role}_metrics.csv", sample_rows, split_role,
            run_name, seed, model_identity, checkpoint_relative_path, checkpoint_epoch,
            checkpoint_metric_value, checkpoint_sha256, config_version, eval_config,
        )
        split_results[split_role] = result
        sample_rows_by_split[split_role] = sample_rows
        aggregate_by_split[split_role] = dict(result["metrics"])
        aggregate_by_split[split_role]["sample_count"] = float(result["sample_count"])

    crosscheck_result = _write_metric_crosscheck_note(
        run_dir=run_dir,
        sample_rows_by_split=sample_rows_by_split,
        aggregate_by_split=aggregate_by_split,
        eval_config=eval_config,
    )

    visual_info: dict[str, Any] | None = None
    if not args.skip_visuals:
        visual_info = export_run_visual_assets(run_dir=run_dir, max_samples_per_split=args.max_visual_samples)

    run_meta = train_entry.simple_yaml_load(run_meta_path.read_text(encoding="utf-8"))
    run_meta["best_checkpoint_path"] = _relative_path(checkpoint_path)
    run_meta["best_checkpoint_epoch"] = int(checkpoint.get("epoch", run_meta.get("best_epoch", 0)))
    run_meta["best_checkpoint_sha256"] = str(checkpoint["checkpoint_sha256"])
    run_meta["checkpoint_identity_status"] = "pass"
    run_meta["evidence_mode"] = "sample_only"
    run_meta["per_run_aggregate_rows"] = False
    run_meta["boundary_metric_width"] = int(eval_config["boundary_metric_width"])
    run_meta["eval_cast_policy"] = str(eval_config["eval_cast_policy"])
    run_meta["connected_components_connectivity"] = int(eval_config["connected_components_connectivity"])
    for key in (
        "eval_proto_version", "boundary_metric_name", "boundary_metric_width", "boundary_metric_unit",
        "boundary_metric_source", "boundary_metric_impl", "boundary_metric_connectivity",
        "boundary_metric_border_value", "boundary_metric_tolerance", "hd95_impl", "empty_set_policy",
        "pixel_spacing", "stability_std_ddof", "stability_std_tolerance_multiplier",
    ):
        if key in eval_config:
            run_meta[key] = eval_config[key]
    _update_run_meta(run_dir, run_meta, aggregate_by_split, crosscheck_result, visual_info)
    _write_run_summary(run_dir, run_meta, aggregate_by_split, crosscheck_result, visual_info)

    print(f"run_dir={_relative_path(run_dir)}")
    print(f"checkpoint={_relative_path(checkpoint_path)}")
    print(f"testA_metrics={_relative_path(run_dir / 'testA_metrics.csv')}")
    print(f"testB_metrics={_relative_path(run_dir / 'testB_metrics.csv')}")
    print(f"metric_crosscheck_result={crosscheck_result}")
    if visual_info is not None:
        print(f"error_cases={visual_info['error_cases_path']}")
        print(f"testA_visual_count={visual_info['visual_counts']['testA']}")
        print(f"testB_visual_count={visual_info['visual_counts']['testB']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
