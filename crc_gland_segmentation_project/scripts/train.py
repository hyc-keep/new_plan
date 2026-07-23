"""
对应阶段: 03_UNet稳定性
理论依据:
  - 论文: Ronneberger et al., 2015, "U-Net: Convolutional Networks for Biomedical Image Segmentation"
  章节: §3 (Network Architecture)
  公式/定义: 双侧收缩-扩张路径 + skip connection; §2 (Training) 数据增强策略
  - 论文: Sirinukunwattana et al., 2017, "Gland Segmentation in Colon Histology Images: The GlaS Challenge Contest"
  章节: §2.1-2.2 (Dataset and Ground Truth)
  - 可复现训练: 阶段实现卡要求 3-seed 独立训练 + 协议冻结
  - 三层落盘机制: 阶段总协议 §8.1 (run_meta.yaml / raw CSV / aggregate CSV 必须含 eval_cast_policy、boundary_metric_*、connected_components_*)
代码参考:
  - 仓库: https://github.com/milesial/Pytorch-UNet
  - 文件: unet/unet_parts.py, unet/unet_model.py
  - commit: 参考 master 分支
  - 许可证: GPL-3.0
  - 本项目调整: 适配三段式实验链 (train→test→summarize)、固化三层落盘协议、T-9 runtime probe 保护
冻结回链: 结直肠腺体分割_plan_优化版/01_实验执行/00_总览与规范/02_参数冻结总表.md
  - eval_cast_policy=float32_before_threshold, boundary_metric_width=3, connected_components_connectivity=8
"""

from __future__ import annotations

import argparse
import csv
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
from typing import Any


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
import torch
from torch.cuda.amp import GradScaler
from torch.optim import AdamW
from torch.utils.data import DataLoader

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency
    Image = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from b_class_auxiliary.tools.experiment_environment import ensure_environment

ensure_environment()

from src.data import (
    build_augment_config,
    build_dataset_from_csv,
    build_eval_transform,
    build_segmentation_dataset,
    build_train_transform,
    load_data_config,
    simple_yaml_load,
)
from src.engine import EarlyStopper, build_scheduler, train_model
from src.eval.checkpoint_selector import BestCheckpointState, update_best_checkpoint
from src.losses import build_boundary_loss, build_distance_loss, build_seg_loss
from src.models import build_unet_model
from src.utils import collect_runtime_metadata, formal_source_paths, set_global_seed, seed_worker, sha256_file, sha256_paths, sha256_state_dict


def parse_args() -> argparse.Namespace:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    parser = argparse.ArgumentParser(description="Formal project-local training entrypoint.")
    parser.add_argument("--config", required=True, help="Relative path to the experiment config.")
    parser.add_argument("--run-name", default=None, help="Optional logical run name override.")
    parser.add_argument("--device", default="cuda", help="Requested device hint (auto-fallback to CPU if CUDA unavailable).")
    parser.add_argument("--smoke-check", action="store_true", help="Run only the minimal local smoke training loop.")
    parser.add_argument(
        "--resume-from-last",
        action="store_true",
        help="Resume the interrupted formal training run from `checkpoints/last.ckpt`.",
    )
    parser.add_argument("--max-steps", type=int, default=1, help="Reserved for stage01 preflight compatibility.")
    parser.add_argument(
        "--runtime-check",
        action="store_true",
        help="Emit a lightweight payload after formal asset checks for stage01 preflight compatibility.",
    )
    parser.add_argument(
        "--runtime-check-output",
        default="b_class_auxiliary/runtime_checks/train_runtime_payload.json",
        help="Relative path for the runtime-check payload JSON.",
    )
    return parser.parse_args()


def normalize_relpath(value: str) -> str:
    return value.strip().replace("\\", "/").strip()


def load_experiment_config(project_root: Path, relative_path: str) -> tuple[Path, dict[str, Any]]:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    config_path = (project_root / normalize_relpath(relative_path)).resolve()
    if not config_path.exists():
        raise FileNotFoundError(f"experiment config not found: {config_path}")
    data = simple_yaml_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"experiment config must be a mapping: {config_path}")
    return config_path, data


def load_json_mapping(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"json payload must be a mapping: {path}")
    return data


def load_csv_rows(path: Path) -> list[dict[str, str]]:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_data_trace_hashes(project_root: Path, data_config_path: Path, asset_manifest_path: Path) -> dict[str, str]:
    split_paths = [
        project_root / "splits/glas/glas_train68.csv",
        project_root / "splits/glas/glas_val17.csv",
        project_root / "splits/glas/glas_testA60.csv",
        project_root / "splits/glas/glas_testB20.csv",
    ]
    if any(not path.is_file() for path in split_paths):
        raise FileNotFoundError("all four GlaS split CSV files are required")
    dataset_files: set[Path] = set()
    for split_path in split_paths:
        for row in load_csv_rows(split_path):
            for key in ("image_relpath", "mask_relpath"):
                value = row.get(key, "").strip()
                if not value:
                    raise ValueError(f"missing {key} in {split_path}")
                asset_path = (project_root / value).resolve()
                if not asset_path.is_file():
                    raise FileNotFoundError(f"dataset asset missing: {asset_path}")
                dataset_files.add(asset_path)
    return {
        "data_config_sha256": sha256_file(data_config_path),
        "split_manifest_sha256": sha256_paths(split_paths, project_root),
        "asset_manifest_sha256": sha256_file(asset_manifest_path),
        "dataset_files_sha256": sha256_paths(sorted(dataset_files), project_root),
    }


def filter_rows_through_epoch(rows: list[dict[str, str]], max_epoch: int) -> list[dict[str, str]]:
    filtered: list[dict[str, str]] = []
    for row in rows:
        try:
            epoch_value = int(row["epoch"])
        except (KeyError, TypeError, ValueError):
            continue
        if epoch_value <= max_epoch:
            filtered.append(row)
    return filtered


def dump_simple_yaml(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(dump_simple_yaml(item, indent + 2))
            elif isinstance(item, list):
                rendered = ", ".join(str(element) for element in item)
                lines.append(f"{prefix}{key}: [{rendered}]")
            elif isinstance(item, bool):
                lines.append(f"{prefix}{key}: {'true' if item else 'false'}")
            else:
                lines.append(f"{prefix}{key}: {item}")
        return "\n".join(lines)
    raise TypeError(f"Unsupported yaml dump value: {type(value)!r}")


def _cuda_really_usable(device_hint: str) -> bool:
    """Probe real CUDA usability instead of trusting torch.cuda.is_available().

    某些受限运行环境(如 sandbox)会让 torch 的 fork 式 `is_available()` 探测触发
    CUDA Error 304 而假阴性, 即使 GPU 实际可用。这里直接做一次真实的
    `torch.zeros(1).cuda()` 试探: 真能算才返回 True; 真无 GPU 会抛异常并回退 CPU,
    因此不会假阳性。只改设备判定, 不影响训练/损失/指标逻辑。
    """
    try:
        torch.zeros(1).to(torch.device(device_hint))
        return True
    except Exception:
        return False


def resolve_device(device_hint: str) -> torch.device:
    if device_hint.startswith("cuda"):
        if _cuda_really_usable(device_hint):
            return torch.device(device_hint)
        raise RuntimeError(
            f"CUDA requested via --device={device_hint!r}, but no usable CUDA device is available. "
            "Formal GPU experiments are blocked; fix the server/launcher GPU access or explicitly use --device cpu for non-formal debugging."
        )
    if device_hint == "cpu":
        return torch.device("cpu")
    raise ValueError(f"unsupported device hint: {device_hint!r}; use 'cuda' or 'cpu'")


def resolve_config_ref(project_root: Path, experiment_config: dict[str, Any], key: str) -> Path:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    config_refs = experiment_config.get("config_refs", {})
    if not isinstance(config_refs, dict):
        raise ValueError("experiment config must provide config_refs mapping")
    ref = config_refs.get(key)
    if not isinstance(ref, str) or not ref.strip():
        raise ValueError(f"missing config_refs.{key}")
    return (project_root / normalize_relpath(ref)).resolve()


def resolve_data_config_path(project_root: Path, experiment_config: dict[str, Any]) -> Path:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    config_refs = experiment_config.get("config_refs", {})
    if isinstance(config_refs, dict):
        data_ref = config_refs.get("data")
        if isinstance(data_ref, str) and data_ref.strip():
            return (project_root / normalize_relpath(data_ref)).resolve()

    dataset_code = str(experiment_config.get("dataset_code", "")).strip().lower()
    if dataset_code in {"glas", "crag"}:
        return (project_root / "configs" / "data" / f"{dataset_code}.yaml").resolve()
    raise ValueError("experiment config must provide config_refs.data or dataset_code in {glas, crag}")


def resolve_asset_manifest_path(project_root: Path, experiment_config: dict[str, Any]) -> Path:
    config_refs = experiment_config.get("config_refs", {})
    if isinstance(config_refs, dict):
        manifest_ref = config_refs.get("asset_manifest")
        if isinstance(manifest_ref, str) and manifest_ref.strip():
            return (project_root / normalize_relpath(manifest_ref)).resolve()
    return (project_root / "reports" / "stage_reports" / "asset_manifest.json").resolve()


def resolve_split_name(experiment_config: dict[str, Any]) -> str:
    split_name = str(experiment_config.get("runtime_split", experiment_config.get("train_split", "train"))).strip()
    return split_name or "train"


def validate_formal_handoff(
    project_root: Path,
    manifest_path: Path,
    manifest: dict[str, Any],
    data_config_path: Path,
    data_proto_version: str,
    dataset_code: str,
    split_name: str,
) -> dict[str, Any]:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    blockers: list[str] = []
    if manifest.get("data_stage_pass") is not True:
        blockers.append("data_stage_pass_false")
    if manifest.get("handoff_ready") is not True:
        blockers.append("handoff_ready_false")
    if manifest.get("preflight_pass") is not True:
        blockers.append("preflight_pass_false")

    manifest_proto_version = str(manifest.get("data_protocol_package_version", "")).strip()
    if manifest_proto_version != data_proto_version:
        blockers.append(f"data_protocol_version_mismatch:{manifest_proto_version or 'missing'}!={data_proto_version}")

    split_assets = manifest.get("split_assets", [])
    split_asset_exists = False
    if isinstance(split_assets, list):
        for item in split_assets:
            if not isinstance(item, dict):
                continue
            if (
                str(item.get("dataset", "")).strip().lower() == dataset_code.lower()
                and str(item.get("split_name", "")).strip() == split_name
                and item.get("exists") is True
            ):
                split_asset_exists = True
                break
    if not split_asset_exists:
        blockers.append(f"split_asset_missing:{dataset_code}:{split_name}")

    data_config_relpath = data_config_path.relative_to(project_root).as_posix()
    config_assets = manifest.get("config_source_assets", [])
    data_config_registered = False
    if isinstance(config_assets, list):
        for item in config_assets:
            if not isinstance(item, dict):
                continue
            if (
                str(item.get("type", "")).strip() == "config"
                and str(item.get("relative_path", "")).strip() == data_config_relpath
                and item.get("exists") is True
            ):
                data_config_registered = True
                break
    if not data_config_registered:
        blockers.append(f"data_config_not_registered:{data_config_relpath}")

    return {
        "asset_manifest": manifest_path.relative_to(project_root).as_posix(),
        "asset_manifest_version": str(manifest.get("asset_manifest_version", "")),
        "data_protocol_package_version": manifest_proto_version,
        "data_stage_pass": manifest.get("data_stage_pass") is True,
        "handoff_ready": manifest.get("handoff_ready") is True,
        "preflight_pass": manifest.get("preflight_pass") is True,
        "split_asset_exists": split_asset_exists,
        "data_config_registered": data_config_registered,
        "blockers": blockers,
    }


def inspect_sample_paths(image_path: Path, mask_path: Path) -> dict[str, Any]:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    if Image is None:
        return {
            "input_shape": None,
            "input_dtype": None,
            "target_shape": None,
            "target_dtype": None,
            "target_unique_values": None,
        }

    with Image.open(image_path) as image:
        image.load()
        input_shape = [image.size[1], image.size[0], len(image.getbands())]
        input_dtype = "uint8"

    with Image.open(mask_path) as mask:
        mask.load()
        colors = mask.getcolors(maxcolors=2048)
        if colors is None:
            target_unique_values: list[str] | None = [">2048_unique_values"]
        else:
            target_unique_values = [str(color) for _, color in colors[:32]]
        target_shape = [mask.size[1], mask.size[0]]
        target_dtype = "uint8"

    return {
        "input_shape": input_shape,
        "input_dtype": input_dtype,
        "target_shape": target_shape,
        "target_dtype": target_dtype,
        "target_unique_values": target_unique_values,
    }


def build_runtime_payload(
    project_root: Path,
    config_path: Path,
    data_config_path: Path,
    handoff_check: dict[str, Any],
    sample: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    image_path = Path(sample["image_path"]).resolve()
    mask_path = Path(sample["mask_path"]).resolve()
    sample_inspection = inspect_sample_paths(image_path, mask_path)
    return {
        "run_name": args.run_name,
        "mode": "runtime_check" if args.runtime_check else "normal",
        "device": args.device,
        "max_steps": args.max_steps,
        "experiment_config": config_path.relative_to(project_root).as_posix(),
        "data_config": data_config_path.relative_to(project_root).as_posix(),
        "asset_manifest": handoff_check["asset_manifest"],
        "asset_manifest_version": handoff_check["asset_manifest_version"],
        "data_protocol_package_version": handoff_check["data_protocol_package_version"],
        "data_stage_pass": handoff_check["data_stage_pass"],
        "handoff_ready": handoff_check["handoff_ready"],
        "preflight_pass": handoff_check["preflight_pass"],
        "split_asset_exists": handoff_check["split_asset_exists"],
        "data_config_registered": handoff_check["data_config_registered"],
        "sample_id": sample["sample_id"],
        "sample_path": image_path.relative_to(project_root).as_posix(),
        "mask_path": mask_path.relative_to(project_root).as_posix(),
        "input_shape": sample_inspection["input_shape"],
        "input_dtype": sample_inspection["input_dtype"],
        "target_shape": sample_inspection["target_shape"],
        "target_dtype": sample_inspection["target_dtype"],
        "target_unique_values": sample_inspection["target_unique_values"],
        "output_shape": None,
        "output_dtype": None,
        "loss_value": None,
        "loss_is_finite": None,
        "backward_executed": None,
        "optimizer_step_executed": None,
        "runtime_profile": "data_protocol_preflight",
        "entrypoint_check_pass": True,
        "entrypoint_check_reason": "formal_split_assets_and_handoff_gates_resolved",
    }


def run_stage01_preflight(
    args: argparse.Namespace,
    project_root: Path,
    config_path: Path,
    experiment_config: dict[str, Any],
) -> int:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    data_config_path = resolve_data_config_path(project_root, experiment_config)
    data_config = load_data_config(project_root, data_config_path)
    asset_manifest_path = resolve_asset_manifest_path(project_root, experiment_config)
    asset_manifest = load_json_mapping(asset_manifest_path)
    split_name = resolve_split_name(experiment_config)
    handoff_check = validate_formal_handoff(
        project_root=project_root,
        manifest_path=asset_manifest_path,
        manifest=asset_manifest,
        data_config_path=data_config_path,
        data_proto_version=data_config.data_proto_version,
        dataset_code=data_config.dataset_code,
        split_name=split_name,
    )
    if handoff_check["blockers"]:
        raise RuntimeError("formal handoff gate blocked: " + ", ".join(handoff_check["blockers"]))

    samples = build_dataset_from_csv(project_root, data_config, split_name)
    if not samples:
        raise RuntimeError(f"formal split is empty: {split_name}")
    sample = samples[0]
    if not Path(sample["image_path"]).exists() or not Path(sample["mask_path"]).exists():
        raise FileNotFoundError("formal split resolved a missing image or mask asset")

    payload = build_runtime_payload(project_root, config_path, data_config_path, handoff_check, sample, args)
    if args.runtime_check:
        output_path = (project_root / normalize_relpath(args.runtime_check_output)).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"run_name={args.run_name}")
    print(f"experiment_config={config_path.relative_to(project_root).as_posix()}")
    print(f"data_config={data_config_path.relative_to(project_root).as_posix()}")
    print(f"asset_manifest={handoff_check['asset_manifest']}")
    print(f"dataset_code={data_config.dataset_code}")
    print(f"split_name={split_name}")
    print(f"sample_id={sample['sample_id']}")
    print(f"image_path={Path(sample['image_path']).resolve().relative_to(project_root).as_posix()}")
    print(f"mask_path={Path(sample['mask_path']).resolve().relative_to(project_root).as_posix()}")
    if args.runtime_check:
        print(f"runtime_check_output={normalize_relpath(args.runtime_check_output)}")
    return 0


def should_run_stage01_preflight(experiment_config: dict[str, Any]) -> bool:
    stage_code = str(experiment_config.get("stage_code", "")).strip()
    model_code = str(experiment_config.get("model_code", "")).strip()
    return stage_code == "01_data_protocol_preflight" or model_code == "train_entrypoint_preflight_only"


def load_training_configs(project_root: Path, experiment_config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    data_config_path = resolve_config_ref(project_root, experiment_config, "data")
    model_config_path = resolve_config_ref(project_root, experiment_config, "model")
    train_config_path = resolve_config_ref(project_root, experiment_config, "train")
    eval_config_path = resolve_config_ref(project_root, experiment_config, "eval")
    return {
        "data": simple_yaml_load(data_config_path.read_text(encoding="utf-8")),
        "model": simple_yaml_load(model_config_path.read_text(encoding="utf-8")),
        "train": simple_yaml_load(train_config_path.read_text(encoding="utf-8")),
        "eval": simple_yaml_load(eval_config_path.read_text(encoding="utf-8")),
        "paths": {
            "data": data_config_path.relative_to(project_root).as_posix(),
            "model": model_config_path.relative_to(project_root).as_posix(),
            "train": train_config_path.relative_to(project_root).as_posix(),
            "eval": eval_config_path.relative_to(project_root).as_posix(),
        },
    }


def build_output_dir(project_root: Path, run_name: str) -> Path:
    return (project_root / "experiments" / run_name).resolve()


def build_optimizer(
    model: torch.nn.Module,
    model_config: dict[str, Any],
    train_config: dict[str, Any],
) -> torch.optim.Optimizer:
    model_name = str(model_config.get("model_name", model_config.get("name", ""))).lower()
    train_proto = str(train_config.get("train_proto_version", ""))
    if train_proto not in {"train_proto_v2", "train_proto_v3_encoder_bn_policy"}:
        return AdamW(model.parameters(), lr=float(train_config["lr"]), weight_decay=float(train_config["weight_decay"]))

    if model_name == "resnet34_unet":
        encoder_modules = (model.stem, model.layer1, model.layer2, model.layer3, model.layer4)
        encoder_group_name = "encoder"
    elif model_name == "unet":
        encoder_modules = (model.inc, model.down1, model.down2, model.down3, model.down4)
        encoder_group_name = "encoder"
    else:
        raise ValueError(f"train_proto_v2 does not define parameter groups for model: {model_name}")

    encoder_parameters = [
        parameter
        for module in encoder_modules
        for parameter in module.parameters()
        if parameter.requires_grad
    ]
    encoder_ids = {id(parameter) for parameter in encoder_parameters}
    decoder_parameters = [
        parameter
        for parameter in model.parameters()
        if parameter.requires_grad and id(parameter) not in encoder_ids
    ]
    if not encoder_parameters or not decoder_parameters:
        raise RuntimeError("train_proto_v2 requires non-empty encoder and decoder parameter groups")
    return AdamW(
        [
            {"params": encoder_parameters, "lr": float(train_config["encoder_lr"]), "group_name": encoder_group_name},
            {"params": decoder_parameters, "lr": float(train_config["decoder_lr"]), "group_name": "decoder_head"},
        ],
        weight_decay=float(train_config["weight_decay"]),
    )


def build_run_meta(
    experiment_config: dict[str, Any],
    config_bundle: dict[str, Any],
    data_config_obj: Any,
    train_run_name: str,
    smoke_check: bool,
    data_trace_hashes: dict[str, str],
) -> dict[str, Any]:
    train_config = config_bundle["train"]
    eval_config = config_bundle["eval"]
    model_config = config_bundle["model"]
    return {
        "run_name": train_run_name,
        "stage_code": str(experiment_config["stage_code"]),
        "dataset_code": str(experiment_config["dataset_code"]),
        "model_name": str(model_config["model_name"]),
        "model_module": "src.models.resnet34_unet" if str(model_config.get("name", "")).lower() == "resnet34unet" else "src.models.unet",
        "model_version": str(model_config["model_version"]),
        "config_version": str(experiment_config["config_version"]),
        "data_proto_version": str(data_config_obj.data_proto_version),
        "train_proto_version": str(train_config["train_proto_version"]),
        "aug_version": str(train_config["aug_version"]),
        "aug_profile_name": str(train_config["aug_profile_name"]),
        "eval_aug_enable": bool(train_config["eval_aug_enable"]),
        "eval_proto_version": str(eval_config["eval_proto_version"]),
        "loss_name": str(train_config["loss_name"]),
        "loss_version": str(train_config["loss_version"]),
        "postprocess_version": str(eval_config["postprocess_version"]),
        "optimizer": str(train_config["optimizer"]),
        "optimizer_param_groups": (
            [
                {"group_name": "encoder", "lr": float(train_config["encoder_lr"])},
                {"group_name": "decoder_head", "lr": float(train_config["decoder_lr"])},
            ]
            if str(model_config.get("model_name", model_config.get("name", ""))).lower() in {"unet", "resnet34_unet"}
             and str(train_config.get("train_proto_version", "")) == "train_proto_v2"
            else [{"group_name": "default", "lr": float(train_config["lr"])}]
        ),
        "lr": float(train_config["lr"]),
        "weight_decay": float(train_config["weight_decay"]),
        "scheduler": str(train_config["scheduler"]),
        "scheduler_monitor": str(train_config["scheduler_monitor"]),
        "epoch_max": int(train_config["epoch_max"]),
        "early_stop_patience": int(train_config["early_stop_patience"]),
        "batch_size": int(train_config["batch_size"]),
        "amp": bool(train_config["amp"]),
        "train_seed": int(experiment_config["train_seed"]),
        "best_selector": str(eval_config["best_selector"]),
        "threshold_value": float(eval_config["threshold_value"]),
        "threshold_source": str(eval_config["threshold_source"]),
        "result_tag": str(experiment_config["result_tag"]),
        "aggregation": str(experiment_config["aggregation"]),
        "smoke_check": smoke_check,
        "config_refs": config_bundle["paths"],
        "boundary_metric_impl": str(eval_config.get("boundary_metric_impl", "missing")),
        "connected_components_impl": str(eval_config.get("connected_components_impl", "missing")),
        "eval_cast_policy": str(eval_config.get("eval_cast_policy", "missing")),
        "connected_components_connectivity": str(eval_config.get("connected_components_connectivity", "missing")),
        "bn_policy_version": str(experiment_config.get("bn_policy_version", "not_applicable")),
        "bn_policy_scope": str(experiment_config.get("bn_policy_scope", "none")),
        "bn_affine_trainable": bool(experiment_config.get("bn_affine_trainable", False)),
        **data_trace_hashes,
        "amp_grad_scaler_init_scale": 65536.0,
        "amp_grad_scaler_growth_factor": 2.0,
        "amp_grad_scaler_backoff_factor": 0.5,
        "amp_grad_scaler_growth_interval": 2000,
        "best_checkpoint_path": "checkpoints/best.ckpt",
    }


def _relative_path_or_posix(path_value: str | Path, project_root: Path) -> str:
    path = Path(path_value)
    if not path.is_absolute():
        return path.as_posix()
    return path.resolve().relative_to(project_root).as_posix()


def _tensor_dtype_name(tensor: torch.Tensor) -> str:
    return str(tensor.dtype).replace("torch.", "")


def _normalize_unique_value(value: float) -> int | float:
    rounded = round(value)
    if abs(value - rounded) < 1.0e-6:
        return int(rounded)
    return float(value)


def _extract_first_string(value: Any) -> str:
    if isinstance(value, (list, tuple)) and value:
        return str(value[0])
    return str(value)


def run_stage02_runtime_check(
    args: argparse.Namespace,
    project_root: Path,
    config_path: Path,
    config_bundle: dict[str, Any],
    train_loader: DataLoader[dict[str, Any]],
    model: torch.nn.Module,
    loss_fn: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> int:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    model.to(device)
    model.train()
    amp_requested = bool(config_bundle["train"].get("amp", False))
    amp_active = amp_requested and device.type == "cuda"
    scaler = GradScaler(
        init_scale=65536.0,
        growth_factor=2.0,
        backoff_factor=0.5,
        growth_interval=2000,
        enabled=amp_active,
    )
    max_steps = max(1, int(args.max_steps))
    payload: dict[str, Any] | None = None

    for batch_index, batch in enumerate(train_loader, start=1):
        images = batch["image"].to(device=device, dtype=torch.float32)
        targets = batch["mask"].to(device=device, dtype=torch.float32)
        boundary_targets = batch.get("boundary_target")
        if boundary_targets is not None:
            boundary_targets = boundary_targets.to(device=device, dtype=torch.float32)

        optimizer.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=amp_active):
            outputs = model(images)
            if isinstance(outputs, dict):
                if boundary_targets is None:
                    raise RuntimeError("boundary model requires boundary_target in runtime check batch")
                logits = outputs["seg_logits"]
                loss_dict = loss_fn(outputs, targets, boundary_targets)
            else:
                logits = outputs
                loss_dict = loss_fn(logits, targets)
            loss_total = loss_dict["loss_total"]
        scaler.scale(loss_total).backward()
        scaler.step(optimizer)
        scaler.update()

        target_unique_values = [
            _normalize_unique_value(float(item))
            for item in torch.unique(targets.detach().cpu()).tolist()
        ]

        payload = {
            "run_name": args.run_name,
            "mode": "runtime_check",
            "device": device.type,
            "amp_requested": amp_requested,
            "amp_active": amp_active,
            "grad_scaler_used": True,
            "model_identity": {
                "model_name": str(config_bundle["model"].get("model_name", config_bundle["model"].get("name", "unknown"))),
                "model_module": model.__class__.__module__,
                "model_class": model.__class__.__qualname__,
            },
            "max_steps": max_steps,
            "steps_executed": batch_index,
            "experiment_config": config_path.relative_to(project_root).as_posix(),
            "data_config": config_bundle["paths"]["data"],
            "model_config": config_bundle["paths"]["model"],
            "train_config": config_bundle["paths"]["train"],
            "eval_config": config_bundle["paths"]["eval"],
            "sample_id": _extract_first_string(batch["sample_id"]),
            "sample_path": _relative_path_or_posix(_extract_first_string(batch["image_path"]), project_root),
            "mask_path": _relative_path_or_posix(_extract_first_string(batch["mask_path"]), project_root),
            "input_shape": list(images.shape),
            "input_dtype": _tensor_dtype_name(images),
            "target_shape": list(targets.shape),
            "target_dtype": _tensor_dtype_name(targets),
            "target_unique_values": target_unique_values,
            "output_shape": list(logits.shape),
            "output_dtype": _tensor_dtype_name(logits),
            "loss_value": float(loss_total.detach().item()),
            "loss_is_finite": bool(torch.isfinite(loss_total.detach()).item()),
            "backward_executed": True,
            "optimizer_step_executed": True,
            "runtime_profile": "full_training_runtime",
            "entrypoint_check_pass": True,
            "entrypoint_check_reason": "formal_train_step_completed",
        }
        if batch_index >= max_steps:
            break

    if payload is None:
        raise RuntimeError("runtime-check dataloader produced zero batches")

    output_path = (project_root / normalize_relpath(args.runtime_check_output)).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"run_name={args.run_name}")
    print(f"device={device.type}")
    print(f"runtime_check_output={normalize_relpath(args.runtime_check_output)}")
    print(f"steps_executed={payload['steps_executed']}")
    print(f"sample_id={payload['sample_id']}")
    print(f"loss_value={payload['loss_value']:.6f}")
    return 0


def run_stage02_training(
    args: argparse.Namespace,
    project_root: Path,
    config_path: Path,
    experiment_config: dict[str, Any],
) -> int:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    config_bundle = load_training_configs(project_root, experiment_config)
    data_config_path = (project_root / config_bundle["paths"]["data"]).resolve()
    data_config_obj = load_data_config(project_root, data_config_path)
    smoke_check = bool(args.smoke_check)
    train_run_name = args.run_name or (
        str(experiment_config["smoke_check_run_name"]) if smoke_check else str(experiment_config["run_name"])
    )
    output_dir = project_root / "experiments" / train_run_name
    output_dir.mkdir(parents=True, exist_ok=True)
    lock_path = output_dir / ".run.lock"
    lock_handle = lock_path.open("a+", encoding="utf-8")
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        lock_handle.close()
        raise RuntimeError(f"run is already active: {train_run_name}") from exc
    if not args.resume_from_last and any(output_dir.iterdir()):
        for child in output_dir.iterdir():
            if child.name != ".run.lock":
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
    print(f"preflight_output_dir={output_dir.relative_to(project_root).as_posix()}", flush=True)
    print("preflight=loading_asset_manifest", flush=True)

    asset_manifest_path = resolve_asset_manifest_path(project_root, experiment_config)
    asset_manifest = load_json_mapping(asset_manifest_path)
    print("preflight=validating_train_handoff", flush=True)
    train_handoff = validate_formal_handoff(
        project_root=project_root,
        manifest_path=asset_manifest_path,
        manifest=asset_manifest,
        data_config_path=data_config_path,
        data_proto_version=data_config_obj.data_proto_version,
        dataset_code=data_config_obj.dataset_code,
        split_name="train",
    )
    print("preflight=train_handoff_done", flush=True)
    print("preflight=validating_val_handoff", flush=True)
    val_handoff = validate_formal_handoff(
        project_root=project_root,
        manifest_path=asset_manifest_path,
        manifest=asset_manifest,
        data_config_path=data_config_path,
        data_proto_version=data_config_obj.data_proto_version,
        dataset_code=data_config_obj.dataset_code,
        split_name="val",
    )
    blockers = train_handoff["blockers"] + val_handoff["blockers"]
    if blockers:
        raise RuntimeError("stage02 handoff gate blocked: " + ", ".join(blockers))
    print("preflight=handoff_pass", flush=True)

    device = resolve_device(args.device)

    train_seed = int(experiment_config["train_seed"])
    set_global_seed(train_seed)

    train_config = config_bundle["train"]
    model_config = dict(config_bundle["model"])
    config_bundle["model"] = model_config
    eval_config = config_bundle["eval"]
    # BN policy is an explicit model-config choice; train_proto_v1 must not inherit v3 behavior.
    model_config["bn_policy_enabled"] = bool(model_config.get("bn_policy_enabled", False))

    augment_config = build_augment_config(train_config)
    train_transform = build_train_transform(data_config_obj, augment_config)
    eval_transform = build_eval_transform(data_config_obj)

    train_dataset = build_segmentation_dataset(project_root, data_config_obj, "train", transform=train_transform)
    val_dataset = build_segmentation_dataset(project_root, data_config_obj, "val", transform=eval_transform)

    # D6修复: 为DataLoader worker提供确定性随机种子，避免多worker时的可复现性问题
    generator = torch.Generator()
    generator.manual_seed(int(experiment_config["train_seed"]))

    train_loader = DataLoader(
        train_dataset,
        batch_size=int(train_config["batch_size"]),
        shuffle=True,
        num_workers=int(train_config["num_workers"]),
        worker_init_fn=seed_worker,
        generator=generator,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=int(train_config["batch_size"]),
        shuffle=False,
        num_workers=int(train_config["num_workers"]),
    )

    model = build_unet_model(model_config)
    if bool(model_config.get("use_boundary_head", False)):
        loss_fn = build_boundary_loss(train_config)
    elif bool(model_config.get("use_distance_head", False)):
        loss_fn = build_distance_loss(train_config)
    else:
        loss_fn = build_seg_loss(train_config)
    optimizer = build_optimizer(model, model_config, train_config)
    print("preflight=model_ready", flush=True)

    if args.runtime_check:
        formal_run_name = str(experiment_config.get("run_name", ""))
        if not args.run_name or args.run_name == formal_run_name:
            raise ValueError("runtime-check requires an isolated probe run_name, not the formal run_name")
        if not args.run_name.endswith("__runtime_probe"):
            raise ValueError("runtime-check run_name must end with '__runtime_probe'")
        return run_stage02_runtime_check(
            args=args,
            project_root=project_root,
            config_path=config_path,
            config_bundle=config_bundle,
            train_loader=train_loader,
            model=model,
            loss_fn=loss_fn,
            optimizer=optimizer,
            device=device,
        )

    print("preflight=building_datasets", flush=True)
    scheduler = build_scheduler(optimizer, train_config)
    early_stopper = EarlyStopper(patience=int(train_config["early_stop_patience"]), mode="max")
    print("preflight=starting_training", flush=True)

    resume_state: dict[str, Any] | None = None
    if args.resume_from_last:
        last_checkpoint_path = output_dir / "checkpoints" / "last.ckpt"
        if not last_checkpoint_path.exists():
            raise FileNotFoundError(f"resume checkpoint not found: {last_checkpoint_path}")
        checkpoint = torch.load(last_checkpoint_path, map_location="cpu")
        if not isinstance(checkpoint, dict):
            raise ValueError(f"resume checkpoint format is invalid: {last_checkpoint_path}")
        required_checkpoint_fields = {
            "checkpoint_schema_version", "scheduler_state_dict", "scaler_state_dict",
            "early_stopper_state_dict", "run_name", "seed", "config_version",
        }
        missing_fields = sorted(required_checkpoint_fields.difference(checkpoint))
        if missing_fields:
            raise ValueError(f"checkpoint schema is not resumable; missing fields: {missing_fields}")
        expected_identity = {
            "run_name": train_run_name,
            "seed": int(experiment_config["train_seed"]),
            "config_version": str(experiment_config["config_version"]),
        }
        for key, expected in expected_identity.items():
            if checkpoint[key] != expected:
                raise ValueError(f"checkpoint identity mismatch for {key}: {checkpoint[key]!r} != {expected!r}")
        model.load_state_dict(checkpoint["model_state_dict"])
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        # 将optimizer state张量从cpu移到实际训练device，避免device mismatch
        for state in optimizer.state.values():
            for k, v in state.items():
                if isinstance(v, torch.Tensor):
                    state[k] = v.to(device)

        train_rows = load_csv_rows(output_dir / "train_log.csv")
        val_rows = load_csv_rows(output_dir / "val_metrics.csv")
        if not val_rows:
            raise RuntimeError("cannot resume without existing val_metrics.csv rows")

        resume_epoch = int(checkpoint.get("epoch", 0))
        train_rows = filter_rows_through_epoch(train_rows, max_epoch=resume_epoch)
        val_rows = filter_rows_through_epoch(val_rows, max_epoch=resume_epoch)
        if not val_rows:
            raise RuntimeError(
                "cannot resume because no validated epochs remain after aligning CSV history to last.ckpt"
            )

        best_state: BestCheckpointState | None = None
        for row in val_rows:
            metric_value = float(row["val_objdice"])
            epoch_value = int(row["epoch"])
            scheduler.step(metric_value)
            early_stopper.update(metric_value)
            best_state, _ = update_best_checkpoint(best_state, epoch=epoch_value, metric_value=metric_value)

        resume_state = {
            "next_epoch": resume_epoch + 1,
            "train_rows": train_rows,
            "val_rows": val_rows,
            "best_state": best_state,
            "scheduler_state_dict": checkpoint["scheduler_state_dict"],
            "scaler_state_dict": checkpoint["scaler_state_dict"],
            "early_stopper_state_dict": checkpoint["early_stopper_state_dict"],
            "python_random_state": checkpoint["python_random_state"],
            "numpy_random_state": checkpoint["numpy_random_state"],
            "torch_rng_state": checkpoint["torch_rng_state"],
            "cuda_rng_state": checkpoint.get("cuda_rng_state"),
            "dataloader_generator_state": checkpoint.get("dataloader_generator_state"),
            "resume_source_checkpoint": str(last_checkpoint_path.relative_to(project_root)),
        }

    frozen_paths = [
        config_path,
        data_config_path,
        (project_root / config_bundle["paths"]["model"]).resolve(),
        (project_root / config_bundle["paths"]["train"]).resolve(),
        (project_root / config_bundle["paths"]["eval"]).resolve(),
        Path(__file__).resolve(),
        (project_root / "src/engine/trainer.py").resolve(),
        (project_root / "src/utils/seed.py").resolve(),
        (project_root / "src/utils/reproducibility.py").resolve(),
        (project_root / "b_class_auxiliary/coding_guards/reproducibility_contract.yaml").resolve(),
    ]
    reproducibility_contract_path = project_root / "b_class_auxiliary/coding_guards/reproducibility_contract.yaml"
    reproducibility_contract_sha256 = sha256_file(reproducibility_contract_path)
    frozen_paths.extend(formal_source_paths(project_root))
    data_trace_hashes = build_data_trace_hashes(project_root, data_config_path, asset_manifest_path)
    run_meta = build_run_meta(
        experiment_config, config_bundle, data_config_obj, train_run_name, smoke_check, data_trace_hashes
    )
    pretrained_path_value = getattr(model, "pretrained_weights_path", None)
    pretrained_hash_value = getattr(model, "pretrained_weights_sha256", None)
    run_meta["reproducibility"] = collect_runtime_metadata(
        project_root,
        frozen_paths,
        pretrained_weights_path=Path(pretrained_path_value).resolve() if pretrained_path_value else None,
        pretrained_weights_sha256=str(pretrained_hash_value) if pretrained_hash_value else None,
    )
    run_meta["pythonhashseed"] = os.environ.get("PYTHONHASHSEED")
    run_meta["cublas_workspace_config"] = os.environ.get("CUBLAS_WORKSPACE_CONFIG")
    run_meta["reproducibility_contract_sha256"] = reproducibility_contract_sha256
    run_meta["amp_requested"] = bool(train_config.get("amp", False))
    run_meta["amp_grad_scaler_init_scale"] = 65536.0
    run_meta["amp_grad_scaler_growth_factor"] = 2.0
    run_meta["amp_grad_scaler_backoff_factor"] = 0.5
    run_meta["amp_grad_scaler_growth_interval"] = 2000
    run_meta["initial_model_state_sha256"] = sha256_state_dict(model.state_dict())
    run_meta["pretrained_weights_path"] = str(model_config.get("pretrained_weights_path") or "not_applicable")
    run_meta["pretrained_weights_sha256"] = str(model_config.get("pretrained_weights_sha256") or "not_applicable")
    run_meta["initial_model_state_finite"] = all(
        torch.isfinite(value).all().item() for value in model.state_dict().values() if torch.is_tensor(value)
    )
    if resume_state is not None:
        run_meta["resume_from_last"] = True
        run_meta["resume_start_epoch"] = int(resume_state["next_epoch"])
    config_snapshot = {
        "experiment": experiment_config,
        "data": config_bundle["data"],
        "model": model_config,
        "train": train_config,
        "eval": eval_config,
    }
    (output_dir / "config.yaml").write_text(dump_simple_yaml(config_snapshot) + "\n", encoding="utf-8")
    (output_dir / "run_meta.yaml").write_text(dump_simple_yaml(run_meta) + "\n", encoding="utf-8")

    summary = train_model(
        model=model,
        loss_fn=loss_fn,
        optimizer=optimizer,
        scheduler=scheduler,
        early_stopper=early_stopper,
        train_loader=train_loader,
        val_loader=val_loader,
        device=device,
        output_dir=output_dir,
        train_config=train_config,
        eval_config=eval_config,
        smoke_check=smoke_check,
        resume_state=resume_state,
        run_identity={
            "run_name": train_run_name,
            "seed": int(experiment_config["train_seed"]),
            "config_version": str(experiment_config["config_version"]),
            "model_name": str(model_config.get("model_name", model_config.get("name", "unknown"))),
            "stage_code": str(experiment_config.get("stage_code", "")),
            "dataset_code": str(experiment_config.get("dataset_code", "")),
            "train_proto_version": str(experiment_config.get("train_proto_version", train_config.get("train_proto_version", ""))),
            "bn_policy_version": run_meta["bn_policy_version"],
            "bn_policy_scope": run_meta["bn_policy_scope"],
            "bn_affine_trainable": run_meta["bn_affine_trainable"],
        },
        dataloader_generator=generator,
    )

    best_checkpoint_path = output_dir / "checkpoints" / "best.ckpt"
    if not best_checkpoint_path.is_file():
        raise FileNotFoundError(f"best checkpoint not found after training: {best_checkpoint_path}")
    run_meta.update(
        {
            "best_checkpoint_path": "checkpoints/best.ckpt",
            "best_checkpoint_epoch": int(summary["best_epoch"]),
            "best_checkpoint_sha256": sha256_file(best_checkpoint_path),
            "stop_reason": summary["stop_reason"],
            "best_epoch": summary["best_epoch"],
            "best_metric_value": summary["best_metric_value"],
            "amp_active": summary["amp_active"],
            "epoch_count": summary["epoch_count"],
            "device": device.type,
        }
    )
    (output_dir / "run_meta.yaml").write_text(dump_simple_yaml(run_meta) + "\n", encoding="utf-8")

    print(f"run_name={train_run_name}")
    print(f"output_dir={output_dir.relative_to(project_root).as_posix()}")
    print(f"device={device.type}")
    print(f"smoke_check={str(smoke_check).lower()}")
    print(f"best_epoch={summary['best_epoch']}")
    print(f"best_metric_name=val_objdice")
    print(f"best_metric_value={summary['best_metric_value']:.6f}")
    print(f"stop_reason={summary['stop_reason']}")
    return 0


def main() -> int:
    """
    对应阶段: 03_UNet稳定性
    理论依据: 模块级 docstring 已给出完整论文引用（Ronneberger 2015 §3 / Sirinukunwattana 2017 §2.1-2.2），本函数承担该论文框架在本项目三段式实验链中的特定工程落地
    代码参考: 仓库 https://github.com/milesial/Pytorch-UNet（master 分支，未固定具体 commit）文件 unet/unet_model.py、unet/unet_parts.py 许可证 GPL-3.0
    本项目调整: 适配 03 阶段，固化协议
    """
    args = parse_args()
    project_root = PROJECT_ROOT
    config_path, experiment_config = load_experiment_config(project_root, args.config)

    if should_run_stage01_preflight(experiment_config):
        if args.run_name is None:
            args.run_name = str(experiment_config.get("run_name", "manual_run"))
        return run_stage01_preflight(args, project_root, config_path, experiment_config)
    return run_stage02_training(args, project_root, config_path, experiment_config)


if __name__ == "__main__":
    raise SystemExit(main())
