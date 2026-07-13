#!/usr/bin/env python3
from pathlib import Path
import re
import sys


SKILL_CHAR_LIMIT = 5000
AGENT_PROMPT_CHAR_LIMIT = 260


def validate(root, report=False):
    root = Path(root)
    rows = []
    for skill in sorted((root / "skills").iterdir()):
        if not skill.is_dir():
            continue
        skill_path = skill / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        size = len(text)
        if size > SKILL_CHAR_LIMIT:
            raise SystemExit(
                f"{skill_path}: {size} chars exceeds limit {SKILL_CHAR_LIMIT}"
            )
        rows.append((str(skill_path.relative_to(root)), size, SKILL_CHAR_LIMIT))
        for agent_path in sorted((skill / "agents").glob("*.yaml")):
            agent_text = agent_path.read_text(encoding="utf-8")
            match = re.search(r'^\s*default_prompt:\s*"(.*)"\s*$', agent_text, re.M)
            if not match:
                raise SystemExit(f"{agent_path}: missing quoted default_prompt")
            prompt_size = len(match.group(1))
            if prompt_size > AGENT_PROMPT_CHAR_LIMIT:
                raise SystemExit(
                    f"{agent_path}: {prompt_size} chars exceeds limit "
                    f"{AGENT_PROMPT_CHAR_LIMIT}"
                )
            rows.append(
                (
                    str(agent_path.relative_to(root)),
                    prompt_size,
                    AGENT_PROMPT_CHAR_LIMIT,
                )
            )
    if report:
        for path, size, limit in rows:
            print(f"{size:5d}/{limit:<5d} {path}")
    return len(rows)


def main():
    root = Path(__file__).resolve().parents[1]
    count = validate(root, report="--report" in sys.argv[1:])
    print(f"context budgets OK: {count} files")


if __name__ == "__main__":
    main()
