#!/usr/bin/env python3
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def tracked_files(path):
    return sorted(
        item.relative_to(path)
        for item in path.rglob("*")
        if item.is_file() and "__pycache__" not in item.parts and item.suffix != ".pyc"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target",
        nargs="?",
        type=Path,
        default=Path.home() / ".cc-switch/skills",
    )
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    errors = []
    checked = 0
    sources = {source.name: source for source in sorted((ROOT / "skills").glob("xc881-*")) if source.is_dir()}
    for name, source in sources.items():
        installed = target / name
        if not installed.is_dir():
            errors.append(f"missing {installed}")
            continue
        source_files = tracked_files(source)
        installed_files = tracked_files(installed)
        if source_files != installed_files:
            errors.append(f"{name}: file list differs")
            continue
        for relative in source_files:
            if (source / relative).read_bytes() != (installed / relative).read_bytes():
                errors.append(f"{name}/{relative}: content differs")
        checked += 1
    for installed in sorted(target.glob("xc881-*")):
        if installed.name not in sources:
            errors.append(f"stale {installed}")
    if errors:
        raise SystemExit("installed skill parity failed: " + "; ".join(errors))
    print(f"installed skill parity OK: {checked} skills at {target}")


if __name__ == "__main__":
    main()
