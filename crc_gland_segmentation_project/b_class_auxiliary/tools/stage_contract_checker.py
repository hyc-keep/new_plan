"""Generic pre-run stage contract checker for stages 04-11."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any

import yaml


REQUIRED_LINEAGE = (
    "source_stage",
    "source_manifest",
    "source_protocol_version",
    "source_run_name",
    "consumer_stage",
    "consumer_file",
    "consumption_boundary",
)
REQUIRED_SCHEMA = (
    "splits",
    "sample_count",
    "metric_set",
    "raw_schema",
    "aggregate_policy",
)
REQUIRED_IDENTITY = (
    "stage",
    "dataset",
    "model",
    "eval_proto_version",
    "runs",
)


def load_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"contract must be a mapping: {path}")
    return data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_path(project_root: Path, value: str, label: str, errors: list[str]) -> Path | None:
    candidate = (project_root / value).resolve()
    if not candidate.exists():
        errors.append(f"path_missing:{label}:{value}")
        return None
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a formal stage contract before implementation or runs.")
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    contract_path = args.contract.resolve()
    contract = load_mapping(contract_path)
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_IDENTITY:
        if not contract.get(key):
            errors.append(f"identity_missing:{key}")
    for key in REQUIRED_SCHEMA:
        if not contract.get(key):
            errors.append(f"schema_missing:{key}")
    for key in REQUIRED_LINEAGE:
        if not contract.get("lineage", {}).get(key):
            errors.append(f"lineage_missing:{key}")

    for item in contract.get("required_paths", []):
        if not isinstance(item, dict) or not item.get("path"):
            errors.append("required_paths_invalid_entry")
            continue
        check_path(project_root, str(item["path"]), str(item.get("name", item["path"])), errors)

    for run in contract.get("runs", []):
        if not isinstance(run, dict):
            errors.append("identity_invalid_run_entry")
            continue
        for key in ("run_name", "seed", "config", "output_dir"):
            if not run.get(key):
                errors.append(f"identity_missing_run_field:{key}")
        config = run.get("config")
        output_dir = run.get("output_dir")
        if config:
            check_path(project_root, str(config), f"config:{run.get('run_name', '<unknown>')}", errors)
        if output_dir:
            output_path = (project_root / str(output_dir)).resolve()
            if output_path.exists():
                warnings.append(f"freshness_output_exists:{output_dir}")

    weight = contract.get("pretrained_weight", {})
    for key in ("source", "torchvision_version", "cache_path", "sha256", "offline_policy"):
        value = weight.get(key)
        if not value or value in {"UNVERIFIED", "TO_BE_FROZEN", "UNKNOWN"}:
            errors.append(f"weight_unverified:{key}")
    cache_path = weight.get("cache_path")
    if cache_path and cache_path not in {"UNVERIFIED", "TO_BE_FROZEN", "UNKNOWN"}:
        resolved_cache = check_path(project_root, str(cache_path), "pretrained_weight.cache_path", errors)
        if resolved_cache and resolved_cache.is_file():
            actual_hash = sha256(resolved_cache)
            if actual_hash != str(weight.get("sha256")):
                errors.append("weight_sha256_mismatch")

    freshness = contract.get("freshness", {})
    for key in ("current_round", "historical_exclusion", "required_before_run"):
        if not freshness.get(key):
            errors.append(f"freshness_missing:{key}")

    status = "pass" if not errors else "fail"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    error_lines = [f"- {item}" for item in errors] if errors else ["- none"]
    warning_lines = [f"- {item}" for item in warnings] if warnings else ["- none"]
    lines = [
        "# Stage Contract Check Report",
        "",
        f"- contract: `{contract_path}`",
        f"- status: `{status}`",
        f"- error_count: `{len(errors)}`",
        f"- warning_count: `{len(warnings)}`",
        "",
        "## Errors",
        *error_lines,
        "",
        "## Warnings",
        *warning_lines,
    ]
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"stage_contract_status={status}")
    print(f"wrote_report={args.output.resolve()}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
