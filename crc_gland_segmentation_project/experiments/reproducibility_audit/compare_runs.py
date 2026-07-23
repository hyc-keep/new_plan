"""Entry point for comparing two runs inside the project reproducibility audit area."""

from __future__ import annotations

import runpy
from pathlib import Path


if __name__ == "__main__":
    runpy.run_path(
        str(Path(__file__).resolve().parents[2] / "reproducibility_audit" / "compare_runs.py"),
        run_name="__main__",
    )
