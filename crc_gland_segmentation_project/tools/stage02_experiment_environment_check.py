"""Write the server environment preflight report for formal experiments."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from b_class_auxiliary.tools.experiment_environment import check_environment, format_report


REPORT_PATH = PROJECT_ROOT / "reports" / "environment" / "experiment_environment_check.md"


def main() -> int:
    blockers = check_environment()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(format_report(PROJECT_ROOT), encoding="utf-8")
    print(f"environment_report={REPORT_PATH.relative_to(PROJECT_ROOT).as_posix()}")
    print(f"environment_status={'pass' if not blockers else 'blocked'}")
    if blockers:
        for blocker in blockers:
            print(f"blocker: {blocker}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
