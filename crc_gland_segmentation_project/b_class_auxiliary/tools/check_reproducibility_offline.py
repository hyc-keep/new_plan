"""Offline reproducibility consistency check; never changes experiment artifacts."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path
from typing import Any
import sys

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
FORMAL_ENTRIES = (PROJECT_ROOT / "scripts/train.py", PROJECT_ROOT / "scripts/test.py")


def _git_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _find_config(run_meta: dict[str, Any]) -> Path:
    config_refs = run_meta.get("config_refs", {})
    run_name = str(run_meta.get("run_name", ""))
    candidates = list((PROJECT_ROOT / "configs/experiment").glob(f"{run_name}*.yaml"))
    if candidates:
        return candidates[0]
    candidates = list((PROJECT_ROOT / "configs").rglob("*.yaml"))
    for path in candidates:
        try:
            config = _load(path)
        except yaml.YAMLError:
            continue
        if config.get("config_version") == run_meta.get("config_version"):
            return path
    raise FileNotFoundError(f"cannot infer experiment config from {config_refs!r}")


def check_metadata(path: Path) -> int:
    from src.utils.reproducibility import build_frozen_paths, sha256_file, sha256_paths, source_tree_sha256

    run_meta = _load(path)
    reproducibility = run_meta.get("reproducibility", {})
    config_path = _find_config(run_meta)
    bundle = {"paths": run_meta["config_refs"]}
    frozen_paths = build_frozen_paths(PROJECT_ROOT, config_path, bundle, FORMAL_ENTRIES)
    current = {
        "git_commit": _git_commit(),
        "source_tree_sha256": source_tree_sha256(PROJECT_ROOT),
        "frozen_source_config_sha256": sha256_paths(frozen_paths, PROJECT_ROOT),
        "reproducibility_contract_sha256": sha256_file(PROJECT_ROOT / "b_class_auxiliary/coding_guards/reproducibility_contract.yaml"),
    }
    recorded = {key: reproducibility.get(key, run_meta.get(key)) for key in current}
    stale_fields = [key for key in current if recorded[key] != current[key]]
    if stale_fields:
        print(f"BASELINE_STALE: {path}")
        for key in stale_fields:
            print(f"  {key}: recorded={recorded[key]!r} current={current[key]!r}")
        return 2
    print(f"PASS: {path}")
    return 0


def check_positive_metadata(path: Path) -> int:
    run_meta = _load(path)
    nested = run_meta.get("reproducibility", {})
    fields = ("pythonhashseed", "cublas_workspace_config", "cuda_runtime_version", "source_tree_sha256", "frozen_source_config_sha256")
    mismatches = {
        field: {"top_level": run_meta.get(field), "nested": nested.get(field)}
        for field in fields
        if field not in run_meta or field not in nested or run_meta[field] != nested[field]
    }
    if mismatches:
        print(f"FAIL: metadata field inconsistency in {path}: {mismatches}")
        return 1
    print(f"PASS: metadata field consistency in {path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_meta", type=Path)
    parser.add_argument("--positive", action="store_true", help="Check top-level and nested fields in newly generated metadata.")
    args = parser.parse_args()
    return check_positive_metadata(args.run_meta) if args.positive else check_metadata(args.run_meta)


if __name__ == "__main__":
    raise SystemExit(main())
