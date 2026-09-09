#!/usr/bin/env python3
"""Maintenance-only integrity check for the pinned frontend engine and data."""

import hashlib
import json
from pathlib import Path
import re


VENDOR = Path(__file__).resolve().parents[1] / "skills/xc881-coding-skills/vendor/ui-ux-pro-max"


def validate():
    manifest = json.loads((VENDOR / "upstream.json").read_text(encoding="utf-8"))
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["revision"]):
        raise SystemExit("frontend vendor revision must be a full commit hash")
    expected = manifest["files"]
    actual = {str(path.relative_to(VENDOR)) for path in VENDOR.rglob("*")
              if path.is_file() and path.name != "upstream.json"
              and "__pycache__" not in path.parts and path.suffix != ".pyc"}
    if actual != set(expected):
        raise SystemExit(f"frontend vendor inventory differs: {actual ^ set(expected)}")
    for name, digest in expected.items():
        if hashlib.sha256((VENDOR / name).read_bytes()).hexdigest() != digest:
            raise SystemExit(f"frontend vendor content differs from pinned snapshot: {name}")
    for name in ("LICENSE", "scripts/core.py", "scripts/search.py", "scripts/design_system.py",
                 "scripts/reasoning_contract.py", "data/catalog-summary.json",
                 "data/data-provenance.json", "data/google-font-licenses.json"):
        if name not in expected:
            raise SystemExit(f"missing frontend vendor capability/provenance: {name}")
    if manifest["license"] != "MIT":
        raise SystemExit("frontend vendor license changed; review required")
    return len(expected)


if __name__ == "__main__":
    print(f"frontend vendor integrity OK: {validate()} pinned files")
