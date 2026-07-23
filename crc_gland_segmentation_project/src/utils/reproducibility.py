"""Runtime metadata and content hashes for formal experiment reproducibility."""

from __future__ import annotations

import hashlib
import importlib.metadata
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

import torch


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_paths(paths: Iterable[Path], project_root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((path.resolve() for path in paths), key=lambda item: item.as_posix()):
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


def collect_runtime_metadata(
    project_root: Path,
    frozen_paths: Iterable[Path],
    pretrained_weights_path: Path | None = None,
    pretrained_weights_sha256: str | None = None,
) -> dict[str, Any]:
    actual_pretrained_hash = "not_applicable"
    if pretrained_weights_path is not None:
        if not pretrained_weights_path.is_file():
            raise FileNotFoundError(f"pretrained weights file not found: {pretrained_weights_path}")
        actual_pretrained_hash = sha256_file(pretrained_weights_path)
        if not pretrained_weights_sha256 or pretrained_weights_sha256 != actual_pretrained_hash:
            raise ValueError(
                "pretrained weights SHA256 is missing or does not match the local file: "
                f"{pretrained_weights_sha256!r} != {actual_pretrained_hash!r}"
            )
    git_commit = "unavailable"
    computed_source_tree_sha256 = source_tree_sha256(project_root)
    try:
        git_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        git_commit = f"source_tree_sha256:{computed_source_tree_sha256}"

    cuda_available = torch.cuda.is_available()
    metadata: dict[str, Any] = {
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
        "cuda_runtime_version": torch.version.cuda,
        "cudnn_version": torch.backends.cudnn.version(),
        "cuda_device_count": torch.cuda.device_count() if cuda_available else 0,
        "cuda_devices": [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())]
        if cuda_available
        else [],
        "deterministic_algorithms": torch.are_deterministic_algorithms_enabled(),
        "cudnn_deterministic": torch.backends.cudnn.deterministic,
        "cudnn_benchmark": torch.backends.cudnn.benchmark,
        "git_commit": git_commit,
        "source_tree_sha256": computed_source_tree_sha256,
        "frozen_source_config_sha256": sha256_paths(frozen_paths, project_root),
        "resnet34_pretrained_source": "local pretrained_weights_path" if pretrained_weights_path is not None else "not_applicable",
        "resnet34_pretrained_weight_path": pretrained_weights_path.resolve().relative_to(project_root).as_posix() if pretrained_weights_path is not None else "not_applicable",
        "resnet34_pretrained_weight_sha256": actual_pretrained_hash or "not_applicable",
    }
    return metadata
