#!/usr/bin/env python3
from pathlib import Path
import argparse
import re


def field(text, name):
    match = re.search(rf"^{re.escape(name)}(?:\s*[（(][^()（）]*[)）])?:\s*`?([^`\n]+?)`?\s*$", text, re.M)
    if not match:
        raise SystemExit(f"missing field {name}")
    return match.group(1).strip()


def chars(path):
    return len(Path(path).read_text(encoding="utf-8"))


def show(name, size):
    print(f"{name:28s} {size:6d} chars")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--cross-ledger", type=Path)
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    artifact = args.artifact.resolve()
    current_path = artifact / "current.md"
    current_text = current_path.read_text(encoding="utf-8")
    current_value = field(current_text, "Current")
    if current_value == "none":
        raise SystemExit("artifact has no active current item")

    coding_skill = chars(repo / "skills/xc881-coding-skills/SKILL.md")
    requirement_skill = chars(repo / "skills/xc881-analysis/SKILL.md")
    porting_skill = chars(repo / "skills/xc881-porting-orchestration/SKILL.md")
    current_size = len(current_text)
    current_item_size = chars(artifact / current_value)
    dynamic = current_size + current_item_size

    legacy_dynamic = current_size
    for name in ("Previous", "Current", "Next"):
        value = field(current_text, name)
        if value != "none":
            legacy_dynamic += chars(artifact / value)

    print("Skill-owned context size audit")
    show("instant Coding", coding_skill)
    show("queue dynamic (current-only)", dynamic)
    show("queue dynamic (legacy)", legacy_dynamic)
    show("queue Coding", coding_skill + dynamic)
    show("Requirement resume", requirement_skill + chars(artifact / "index.md") + dynamic)

    porting_base = porting_skill + dynamic
    if args.cross_ledger:
        show("Porting resume", porting_base + chars(args.cross_ledger))
    else:
        show("Porting resume base", porting_base)
        show("Porting resume hard max", porting_base + 4500)

    saved = legacy_dynamic - dynamic
    percent = 0 if legacy_dynamic == 0 else saved * 100 / legacy_dynamic
    print(f"dynamic window saved          {saved:6d} chars ({percent:.1f}%)")


if __name__ == "__main__":
    main()
