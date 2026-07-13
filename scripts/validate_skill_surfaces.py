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

    forbidden = [
        "docs/context-budget-and-cache.md",
        "docs/provider-capability-matrix.md",
        "docs/runtime-context-orchestration.md",
        "evals/context-scenarios.json",
        "evals/runtime-faults.json",
        "scripts/audit_runtime_context.py",
        "scripts/validate_runtime_contracts.py",
    ]
    for relative in forbidden:
        if (ROOT / relative).exists():
            raise SystemExit(f"out-of-scope runtime artifact exists: {relative}")
    forbidden_phrases = [
        "prompt cache",
        "prompt-cache",
        "cached input",
        "cache state",
        "provider-native",
        "native compaction",
        "provider pressure",
        "host/session/runner",
        "host compaction",
        "provider compaction",
        "provider usage",
        "input_tokens",
        "cache_write",
        "compact_threshold",
        "responses.compact",
        "billing",
        "计费",
        "缓存",
    ]
    public_files = [ROOT / "README.md", ROOT / "AGENTS.md"]
    for directory in ["docs", "platform-prompts", "skills", "evals", "scripts"]:
        public_files.extend(
            path
            for path in (ROOT / directory).rglob("*")
            if path.is_file()
            and path.resolve() != Path(__file__).resolve()
            and path.suffix in {".md", ".json", ".yaml", ".py"}
        )
    for path in public_files:
        text = path.read_text(encoding="utf-8").lower()
        for phrase in forbidden_phrases:
            if phrase.lower() in text:
                raise SystemExit(
                    f"{path.relative_to(ROOT)}: out-of-scope runtime phrase {phrase!r}"
                )
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
