#!/usr/bin/env python3
"""Import an explicitly selected upstream Git snapshot; never fetch at runtime."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "skills/xc881-coding-skills/vendor/ui-ux-pro-max"
PREFIX = "src/ui-ux-pro-max/"
SCRIPTS = {"core.py", "search.py", "design_system.py", "reasoning_contract.py", "validate_data.py"}


def git(source, *args):
    return subprocess.run(["git", "-C", str(source), *args], check=True,
                          stdout=subprocess.PIPE).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="local upstream Git checkout")
    parser.add_argument("--revision", required=True, help="explicit reviewed commit")
    args = parser.parse_args()
    revision = git(args.source, "rev-parse", "--verify", args.revision + "^{commit}").decode().strip()
    paths = git(args.source, "ls-tree", "-r", "--name-only", revision, "--", PREFIX).decode().splitlines()
    selected = {"LICENSE": "LICENSE"}
    for path in paths:
        relative = path.removeprefix(PREFIX)
        if relative.startswith("data/") or relative in {f"scripts/{name}" for name in SCRIPTS}:
            selected[relative] = path
    if not all(f"scripts/{name}" in selected for name in SCRIPTS):
        parser.error("upstream runtime inventory changed; review the import contract")
    if not any(name.endswith(".csv") for name in selected):
        parser.error("upstream data inventory is empty")
    snapshot = {name: git(args.source, "show", f"{revision}:{path}")
                for name, path in selected.items()}
    old = DEST / "upstream.json"
    if old.exists():
        old_manifest = json.loads(old.read_text(encoding="utf-8"))
        for name, expected in old_manifest["files"].items():
            path = DEST / name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                parser.error(f"locally modified vendor file: {name}; preserve/reconcile before updating")
        removed = set(old_manifest["files"]) - set(snapshot)
        if removed:
            parser.error(f"upstream removed files; review before importing: {sorted(removed)}")
    for name, content in snapshot.items():
        path = DEST / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    manifest = {
        "repository": "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill",
        "revision": revision,
        "source_root": PREFIX.rstrip("/"),
        "license": "MIT",
        "files": {name: hashlib.sha256(content).hexdigest()
                  for name, content in sorted(snapshot.items())},
    }
    old.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(snapshot)} upstream files at {revision}")


if __name__ == "__main__":
    main()
