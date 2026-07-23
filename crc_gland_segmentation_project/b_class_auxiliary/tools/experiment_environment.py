"""Preflight checks for the reproducible experiment environment."""

from __future__ import annotations

import importlib
import importlib.metadata
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Requirement:
    distribution: str
    import_name: str
    expected_version: str | None = None


REQUIREMENTS = (
    Requirement("torch", "torch", "2.2.2"),
    Requirement("numpy", "numpy", "1.26.4"),
    Requirement("scipy", "scipy", "1.17.1"),
    Requirement("Pillow", "PIL", "10.3.0"),
    Requirement("PyYAML", "yaml", None),
)


def check_environment() -> list[str]:
    """Return actionable blockers; an empty list means the environment is ready."""
    blockers: list[str] = []
    for requirement in REQUIREMENTS:
        try:
            installed_version = importlib.metadata.version(requirement.distribution)
        except importlib.metadata.PackageNotFoundError:
            blockers.append(
                f"missing {requirement.distribution}; install with "
                f"'/environment/miniconda3/bin/python -m pip install -r requirements.txt'"
            )
            continue

        if requirement.expected_version and installed_version != requirement.expected_version:
            blockers.append(
                f"{requirement.distribution} version mismatch: "
                f"expected {requirement.expected_version}, found {installed_version}"
            )

        try:
            importlib.import_module(requirement.import_name)
        except Exception as exc:  # import errors must remain visible at the boundary
            blockers.append(f"{requirement.distribution} import failed: {exc}")
    return blockers


def ensure_environment() -> None:
    blockers = check_environment()
    if blockers:
        message = "Experiment environment blocked:\n- " + "\n- ".join(blockers)
        raise RuntimeError(message)


def format_report(project_root: Path) -> str:
    blockers = check_environment()
    status = "pass" if not blockers else "blocked"
    lines = [
        "# Experiment Environment Check",
        "",
        f"- project_root: `{project_root}`",
        "- python: `/environment/miniconda3/bin/python`",
        f"- environment_status: `{status}`",
        "",
        "## Packages",
        "",
        "| Distribution | Import | Required | Installed | Import status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for requirement in REQUIREMENTS:
        try:
            installed = importlib.metadata.version(requirement.distribution)
        except importlib.metadata.PackageNotFoundError:
            installed = "missing"
        try:
            importlib.import_module(requirement.import_name)
            import_status = "pass"
        except Exception as exc:
            import_status = f"blocked: {exc}"
        required = requirement.expected_version or "installed"
        lines.append(
            f"| `{requirement.distribution}` | `{requirement.import_name}` | "
            f"`{required}` | `{installed}` | `{import_status}` |"
        )
    lines.extend(
        [
            "",
            "## Installation",
            "",
            "```bash",
            "/environment/miniconda3/bin/python -m pip install -r requirements.txt",
            "```",
            "",
            "- The training and testing entrypoints run this check before importing the project model/evaluation chain.",
            "- A blocked check must be fixed before any formal training, testing, or runtime evidence run.",
        ]
    )
    if blockers:
        lines.extend(["", "## Blockers", "", *[f"- {item}" for item in blockers]])
    return "\n".join(lines) + "\n"
