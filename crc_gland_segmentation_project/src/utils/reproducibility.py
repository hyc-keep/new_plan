"""Runtime metadata and content hashes for formal experiment reproducibility."""

from __future__ import annotations

import hashlib
import importlib.metadata
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping

import torch


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_frozen_paths(
    project_root: Path,
    config_path: Path,
    config_bundle: Mapping[str, Any],
    extra_paths: Iterable[Path] | None = None,
) -> list[Path]:
    paths: set[Path] = {Path(config_path).resolve()}
    paths.add((project_root / str(config_bundle["paths"]["data"])).resolve())
    for key in ("model", "train", "eval"):
        paths.add((project_root / str(config_bundle["paths"][key])).resolve())
    paths.add((project_root / "b_class_auxiliary/coding_guards/reproducibility_contract.yaml").resolve())
    if extra_paths:
        paths.update(Path(path).resolve() for path in extra_paths)
    return sorted(paths, key=lambda path: path.relative_to(project_root).as_posix())


def sha256_paths(paths: Iterable[Path], project_root: Path) -> str:
    digest = hashlib.sha256()
    unique_paths = {Path(path).resolve() for path in paths}
    for path in sorted(unique_paths, key=lambda item: item.relative_to(project_root).as_posix()):
        digest.update(path.relative_to(project_root).as_posix().encode("utf-8"))
        digest.update(sha256_file(path).encode("ascii"))
    return digest.hexdigest()


def formal_source_paths(project_root: Path) -> list[Path]:
    roots = ("scripts", "src", "reproducibility_audit", "b_class_auxiliary/tools")
    paths = [path for root in roots for path in (project_root / root).rglob("*.py")]
    paths.extend((project_root / "configs").rglob("*.yaml"))
    paths.extend((project_root / "configs").rglob("*.yml"))
    paths.extend((project_root / "b_class_auxiliary/coding_guards").rglob("*.yaml"))
    paths.extend((project_root / "b_class_auxiliary/coding_guards").rglob("*.yml"))
    return [path for path in paths if path.is_file() and "__pycache__" not in path.parts]


def source_tree_sha256(project_root: Path) -> str:
    return sha256_paths(formal_source_paths(project_root), project_root)


def sha256_state_dict(state_dict: dict[str, Any]) -> str:
    digest = hashlib.sha256()
    for key in sorted(state_dict):
        value = state_dict[key]
        if not torch.is_tensor(value):
            continue
        digest.update(key.encode("utf-8"))
        digest.update(str(value.dtype).encode("ascii"))
        digest.update(str(tuple(value.shape)).encode("ascii"))
        digest.update(value.detach().cpu().contiguous().numpy().tobytes())
    return digest.hexdigest()


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "missing"


def collect_reproducibility_values(
    project_root: Path,
    config_path: Path,
    config_bundle: Mapping[str, Any],
    data_trace_hashes: Mapping[str, Any],
    experiment_config: Mapping[str, Any],
    device: torch.device,
    amp_requested: bool,
    amp_scaler_values: Mapping[str, Any],
    extra_paths: Iterable[Path] | None = None,
    pretrained_weights_path: Path | None = None,
    pretrained_weights_sha256: str | None = None,
    env: Mapping[str, str | None] | None = None,
) -> dict[str, Any]:
    environment = os.environ if env is None else env
    actual_pretrained_hash = "not_applicable"
    if pretrained_weights_path is not None:
        if not pretrained_weights_path.is_file():
            raise FileNotFoundError(f"pretrained weights file not found: {pretrained_weights_path}")
        actual_pretrained_hash = sha256_file(pretrained_weights_path)
        if pretrained_weights_sha256 != actual_pretrained_hash:
            raise ValueError(
                "pretrained weights SHA256 is missing or does not match the local file: "
                f"{pretrained_weights_sha256!r} != {actual_pretrained_hash!r}"
            )
    frozen_paths = build_frozen_paths(project_root, config_path, config_bundle, extra_paths)
    computed_source_tree_sha256 = source_tree_sha256(project_root)
    try:
        git_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=project_root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        git_commit = f"source_tree_sha256:{computed_source_tree_sha256}"
    cuda_available = torch.cuda.is_available()
    contract_path = project_root / "b_class_auxiliary/coding_guards/reproducibility_contract.yaml"
    cuda_runtime_version = str(torch.version.cuda) if torch.version.cuda is not None else None
    values: dict[str, Any] = {
        **dict(data_trace_hashes),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "torch_version": torch.__version__,
        "torchvision_version": _package_version("torchvision"),
        "numpy_version": _package_version("numpy"),
        "scipy_version": _package_version("scipy"),
        "pillow_version": _package_version("Pillow"),
        "pyyaml_version": _package_version("PyYAML"),
        "cuda_available": cuda_available,
        "cuda_runtime_version": cuda_runtime_version,
        "cudnn_version": torch.backends.cudnn.version(),
        "cuda_device_count": torch.cuda.device_count() if cuda_available else 0,
        "cuda_devices": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())] if cuda_available else [],
        "device": str(device),
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "cudnn_deterministic": torch.backends.cudnn.deterministic,
        "cudnn_benchmark": torch.backends.cudnn.benchmark,
        "git_commit": git_commit,
        "source_tree_sha256": computed_source_tree_sha256,
        "frozen_source_config_sha256": sha256_paths(frozen_paths, project_root),
        "reproducibility_contract_sha256": sha256_file(contract_path),
        "pythonhashseed": environment.get("PYTHONHASHSEED"),
        "cublas_workspace_config": environment.get("CUBLAS_WORKSPACE_CONFIG"),
        "amp_requested": bool(amp_requested),
        "amp_active": bool(amp_requested and device.type == "cuda"),
        "resnet34_pretrained_source": "local pretrained_weights_path" if pretrained_weights_path is not None else "not_applicable",
        "resnet34_pretrained_weight_path": pretrained_weights_path.resolve().relative_to(project_root).as_posix() if pretrained_weights_path is not None else "not_applicable",
        "resnet34_pretrained_weight_sha256": actual_pretrained_hash,
        "pretrained_weights_path": pretrained_weights_path.resolve().relative_to(project_root).as_posix() if pretrained_weights_path is not None else "not_applicable",
        "pretrained_weights_sha256": actual_pretrained_hash,
        **dict(amp_scaler_values),
    }
    values["train_seed"] = int(experiment_config["train_seed"])
    return values


def collect_runtime_metadata(
    project_root: Path,
    frozen_paths: Iterable[Path],
    pretrained_weights_path: Path | None = None,
    pretrained_weights_sha256: str | None = None,
) -> dict[str, Any]:
    """Backward-compatible wrapper for non-entrypoint audit callers."""
    bundle = {"paths": {"data": "configs/data/glas.yaml", "model": "configs/model/unet_v1.yaml", "train": "configs/train/unet_flow_v1.yaml", "eval": "configs/eval/eval_proto_v1.yaml"}}
    return collect_reproducibility_values(
        project_root, project_root / "configs/experiments/A2_UNet_GlaS_seed3407.yaml", bundle,
        {}, {"train_seed": int(os.environ.get("PYTHONHASHSEED") or 0)}, torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        False, {}, extra_paths=frozen_paths, pretrained_weights_path=pretrained_weights_path,
        pretrained_weights_sha256=pretrained_weights_sha256,
    )
