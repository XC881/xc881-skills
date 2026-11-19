#!/usr/bin/env python3
from pathlib import Path
import runpy
import sys

SKILL_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/xc881-analysis/scripts/find_req_process_candidates.py"
)


if __name__ == "__main__":
    if not SKILL_SCRIPT.is_file():
        raise SystemExit(f"missing skill candidate finder: {SKILL_SCRIPT}")
    sys.argv[0] = str(SKILL_SCRIPT)
    runpy.run_path(str(SKILL_SCRIPT), run_name="__main__")
