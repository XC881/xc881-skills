#!/usr/bin/env python3
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPATIBILITY_PROMPT_LIMIT = 700


def prompt(path):
    text = path.read_text(encoding="utf-8")
    match = re.search(r'^\s*default_prompt:\s*"(.*)"\s*$', text, re.M)
    if not match:
        raise SystemExit(f"{path}: missing quoted default_prompt")
    return match.group(1)


def main():
    checked = 0
    for skill in sorted((ROOT / "skills").iterdir()):
        if not skill.is_dir():
            continue
        openai = prompt(skill / "agents/openai.yaml")
        claude = prompt(skill / "agents/claude.yaml")
        if openai != claude:
            raise SystemExit(f"{skill.name}: agent prompt variants drift")
        if "SKILL.md owns workflow" not in openai:
            raise SystemExit(f"{skill.name}: agent prompt must remain a workflow shim")
        checked += 1

    for path in sorted((ROOT / "platform-prompts").glob("*-custom-instructions.md")):
        text = path.read_text(encoding="utf-8")
        if "Compatibility Shim" not in text:
            raise SystemExit(f"{path}: missing compatibility-shim marker")
        if len(text) > COMPATIBILITY_PROMPT_LIMIT:
            raise SystemExit(
                f"{path}: {len(text)} chars exceeds {COMPATIBILITY_PROMPT_LIMIT}"
            )
        checked += 1

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for required in [
        "docs/skill-context-budget.md",
        "scripts/validate_context_budgets.py --report",
        "scripts/audit_context_sizes.py",
    ]:
        if required not in readme:
            raise SystemExit(f"README missing skills-only context guidance: {required}")
    print(f"skill surfaces OK: {checked} shims")


if __name__ == "__main__":
    main()
