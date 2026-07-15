#!/usr/bin/env python3
from pathlib import Path
import re
import sys


SKILL_CHAR_LIMIT = 5000
SKILL_DESCRIPTION_CHAR_LIMIT = 320
TOTAL_DESCRIPTION_CHAR_LIMIT = 1650
AGENT_PROMPT_CHAR_LIMIT = 180


def validate(root, report=False):
    root = Path(root)
    rows = []
    description_total = 0
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
        description_match = re.search(
            r"^description:\s*(['\"])(.*?)\1\s*$", text, re.M
        )
        if not description_match:
            raise SystemExit(f"{skill_path}: missing single-line quoted description")
        description = description_match.group(2)
        description_size = len(description)
        if not description.startswith("Primary owner for "):
            raise SystemExit(
                f"{skill_path}: description must front-load primary ownership"
            )
        if description_size > SKILL_DESCRIPTION_CHAR_LIMIT:
            raise SystemExit(
                f"{skill_path}: description {description_size} chars exceeds limit "
                f"{SKILL_DESCRIPTION_CHAR_LIMIT}"
            )
        frontmatter = text.split("---", 2)[1]
        aliases_match = re.search(r"^aliases:\n((?:  - .+\n?)+)", frontmatter, re.M)
        if aliases_match and re.search(
            r"^\s{2}- xc881\s*$", aliases_match.group(1), re.M
        ):
            raise SystemExit(f"{skill_path}: broad namespace-only alias is forbidden")
        description_total += description_size
        rows.append(
            (
                f"{skill_path.relative_to(root)} description",
                description_size,
                SKILL_DESCRIPTION_CHAR_LIMIT,
            )
        )
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
    if description_total > TOTAL_DESCRIPTION_CHAR_LIMIT:
        raise SystemExit(
            f"all skill descriptions: {description_total} chars exceeds limit "
            f"{TOTAL_DESCRIPTION_CHAR_LIMIT}"
        )
    rows.append(("all skill descriptions", description_total, TOTAL_DESCRIPTION_CHAR_LIMIT))
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
