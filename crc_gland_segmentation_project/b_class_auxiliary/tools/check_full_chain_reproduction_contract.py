#!/usr/bin/env python3
"""Generate and validate the pre-run-only 01-to-04 reproduction-chain contract."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CHAIN_DIR = Path("b_class_auxiliary/coding_guards/01_04_full_chain_reproduction")
CONTRACT_PATH = CHAIN_DIR / "full_chain_contract.yaml"
FREEZE_PATH = CHAIN_DIR / "01_data_freeze_manifest.json"
REPORT_PATH = CHAIN_DIR / "pre_run_check_report.md"
LINEAGE_FIELDS = (
    "source_stage", "source_manifest", "source_protocol_version", "source_run_name",
    "consumer_stage", "consumer_file", "consumption_boundary",
)
SPLITS = (
    ("train", "splits/glas/glas_train68.csv"),
    ("val", "splits/glas/glas_val17.csv"),
    ("testA", "splits/glas/glas_testA60.csv"),
    ("testB", "splits/glas/glas_testB20.csv"),
)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"YAML mapping required: {path}")
    return data


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_paths(paths: list[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted((item.resolve() for item in paths), key=lambda item: item.as_posix()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(sha256_file(path).encode("ascii"))
    return digest.hexdigest()


def current_hashes(root: Path) -> tuple[dict[str, str], list[dict[str, Any]]]:
    split_paths = [root / value for _, value in SPLITS]
    assets: set[Path] = set()
    split_assets: list[dict[str, Any]] = []
    for split_name, relative_path in SPLITS:
        split_path = root / relative_path
        if not split_path.is_file():
            raise FileNotFoundError(split_path)
        with split_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            for field in ("image_relpath", "mask_relpath"):
                asset = root / row[field].strip()
                if not asset.is_file():
                    raise FileNotFoundError(asset)
                assets.add(asset)
        split_assets.append({"dataset": "glas", "split_name": split_name, "relative_path": relative_path, "row_count": len(rows), "exists": True})
    source_asset_manifest = root / "reports/stage_reports/asset_manifest.json"
    return ({
        "data_config_sha256": sha256_file(root / "configs/data/glas.yaml"),
        "split_manifest_sha256": sha256_paths(split_paths, root),
        "asset_manifest_sha256": sha256_file(source_asset_manifest),
        "dataset_files_sha256": sha256_paths(list(assets), root),
    }, split_assets)


def write_freeze_manifest(root: Path, contract: dict[str, Any]) -> None:
    hashes, split_assets = current_hashes(root)
    payload = {
        "manifest_version": "01_data_freeze_manifest_v1",
        "status": "pre_run_only",
        "training_status": "pending_not_run",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root_policy": "project-root-relative paths only",
        "dataset": "glas",
        "data_protocol_package_version": "01_data_protocol_full_chain_freeze",
        "data_stage_pass": True,
        "handoff_ready": True,
        "preflight_pass": True,
        "config_source_assets": [{"type": "config", "relative_path": "configs/data/glas.yaml", "exists": True}],
        "split_assets": split_assets,
        "source_asset_manifest": "reports/stage_reports/asset_manifest.json",
        "hashes": hashes,
        "contract_round_id": contract["full_chain_round_id"],
        "history_consumption": "excluded",
    }
    (root / FREEZE_PATH).write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def require_lineage(mapping: dict[str, Any], label: str, errors: list[str]) -> None:
    lineage = mapping.get("lineage")
    if not isinstance(lineage, dict):
        errors.append(f"lineage_missing:{label}")
        return
    for field in LINEAGE_FIELDS:
        if not str(lineage.get(field, "")).strip():
            errors.append(f"lineage_missing:{label}:{field}")


def check_config(root: Path, config_rel: str, run: dict[str, Any], stage: str, errors: list[str]) -> dict[str, Any] | None:
    path = root / config_rel
    if not path.is_file():
        errors.append(f"config_missing:{config_rel}")
        return None
    config = load_yaml(path)
    for field in ("run_name", "stage_code", "stage", "dataset_code", "model_name", "model_version", "config_version", "train_seed", "result_tag", "aggregation", "experiment_root", "config_refs", "lineage"):
        if field not in config:
            errors.append(f"config_field_missing:{config_rel}:{field}")
    if config.get("run_name") != run["run_name"] or int(config.get("train_seed", -1)) != int(run["seed"]):
        errors.append(f"config_identity_mismatch:{config_rel}")
    batch_root = str(run["output_dir"]).rsplit("/", 1)[0]
    if config.get("experiment_root") != batch_root:
        errors.append(f"config_experiment_root_mismatch:{config_rel}")
    if config.get("stage") != stage or config.get("config_version") != "full_chain_reproduction_pending" or config.get("result_tag") != "full_chain_reproduction_pending":
        errors.append(f"config_pending_identity_mismatch:{config_rel}")
    refs = config.get("config_refs", {})
    for key in ("data", "model", "train", "eval", "asset_manifest"):
        value = refs.get(key) if isinstance(refs, dict) else None
        if not isinstance(value, str) or not (root / value).exists() and key != "asset_manifest":
            errors.append(f"config_ref_invalid:{config_rel}:{key}")
    if refs.get("asset_manifest") != FREEZE_PATH.as_posix():
        errors.append(f"config_freeze_manifest_mismatch:{config_rel}")
    if stage == "04_Baseline" and refs.get("source_a2_manifest") != (CHAIN_DIR / "03_a2_manifest_pending.yaml").as_posix():
        errors.append(f"config_a2_manifest_mismatch:{config_rel}")
    require_lineage(config, f"config:{config_rel}", errors)
    return config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=ROOT)
    parser.add_argument("--write-data-freeze-manifest", action="store_true")
    args = parser.parse_args()
    root = args.project_root.resolve()
    contract = load_yaml(root / CONTRACT_PATH)
    if args.write_data_freeze_manifest:
        write_freeze_manifest(root, contract)

    errors: list[str] = []
    warnings: list[str] = []
    if contract.get("contract_status") != "pre_run_only" or contract.get("training_status") != "pending_not_run":
        errors.append("contract_not_pre_run_pending")
    if not contract.get("full_chain_round_id") or "full_chain_round_id" in str(contract.get("02_A1", {})):
        errors.append("round_id_policy_invalid")
    if Path(str(contract.get("01_data_freeze", {}).get("manifest", ""))).is_absolute():
        errors.append("absolute_path_forbidden")

    actual_hashes, _ = current_hashes(root)
    expected_hashes = contract["01_data_freeze"]["current_hashes"]
    for key, actual in actual_hashes.items():
        if expected_hashes.get(key) != actual:
            errors.append(f"data_hash_mismatch:{key}")
    freeze_path = root / FREEZE_PATH
    if not freeze_path.is_file():
        errors.append("freeze_manifest_missing")
    else:
        freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
        for key, actual in actual_hashes.items():
            if freeze.get("hashes", {}).get(key) != actual:
                errors.append(f"freeze_manifest_hash_mismatch:{key}")
        if freeze.get("training_status") != "pending_not_run":
            errors.append("freeze_manifest_status_invalid")

    batch_output_root = str(contract.get("batch_output_root", "")).strip()
    if not batch_output_root.startswith("experiments/reproduction_") or Path(batch_output_root).is_absolute():
        errors.append("batch_output_root_invalid")
    elif (root / batch_output_root).exists():
        errors.append(f"batch_output_root_must_not_exist:{batch_output_root}")

    all_runs: list[tuple[str, dict[str, Any]]] = []
    for section, expected_stage, expected_count in (("02_A1", "02_UNetFlow", 1), ("03_A2", "03_UNetStability", 3), ("04_B1", "04_Baseline", 3)):
        item = contract[section]
        if item.get("status") != "pending_not_run" or len(item.get("runs", [])) != expected_count:
            errors.append(f"stage_shape_invalid:{section}")
        require_lineage(item, section, errors)
        for run in item.get("runs", []):
            all_runs.append((expected_stage, run))
            expected_output = f"{batch_output_root}/{run['run_name']}"
            if run.get("output_dir") != expected_output:
                errors.append(f"run_output_not_in_batch_root:{run['run_name']}")
            output = root / run["output_dir"]
            if output.exists():
                errors.append(f"new_output_must_not_exist:{run['output_dir']}")
            check_config(root, run["config"], run, expected_stage, errors)

    run_names = [run["run_name"] for _, run in all_runs]
    if len(run_names) != len(set(run_names)) or any("v" in name.split("_seed")[0].lower() for name in run_names):
        errors.append("new_run_name_collision_or_version_suffix")
    if contract["04_B1"].get("consumes_a2_once") is not True or contract["04_B1"].get("forbid_rerun_a2") is not True:
        errors.append("b1_a2_once_policy_missing")
    b1_lineage = contract["04_B1"]["lineage"]
    if b1_lineage.get("source_manifest") != (CHAIN_DIR / "03_a2_manifest_pending.yaml").as_posix() or "do not rerun A2" not in b1_lineage.get("consumption_boundary", ""):
        errors.append("b1_a2_lineage_or_rerun_policy_invalid")
    for pattern in contract["historical_assets"]["excluded_patterns"]:
        if "chain" in pattern:
            errors.append(f"historical_exclusion_invalid:{pattern}")

    status = "pass" if not errors else "fail"
    lines = ["# 01-04 Full Chain Pre-run Check Report", "", f"- status: `{status}`", "- scope: `pre-run only / pending_not_run`", f"- contract: `{CONTRACT_PATH.as_posix()}`", f"- freeze_manifest: `{FREEZE_PATH.as_posix()}`", f"- error_count: `{len(errors)}`", f"- warning_count: `{len(warnings)}`", "", "## Checked", "- seven new experiment configs: identity, seed, stage, pending version/tag, and config references", "- one new batch root and all seven new output directories: required to be absent and confined to the contract batch root", "- current four data hashes: actual files versus contract and generated freeze manifest", "- 02→03→04 seven-field lineage, 04 new-A2-manifest-only consumption, and no-rerun-A2 policy", "- historical run exclusions", "", "## Errors"]
    lines.extend([f"- {item}" for item in errors] or ["- none"])
    lines.extend(["", "## Warnings"])
    lines.extend([f"- {item}" for item in warnings] or ["- none"])
    (root / REPORT_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"full_chain_pre_run_status={status}")
    print(f"report={(root / REPORT_PATH).as_posix()}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
