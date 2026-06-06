# AGENTS.md

This repository contains portable, token-efficient Agent Skills.

## First principle

```text
accurate, low-token, effective agent reading
```

## Layering

- `xc881-solution-research`: explicit-only solution/technology web research and feasibility planning.
- `xc881-requirement-analysis`: explicit-only requirement understanding before coding.
- `xc881-bugfix-research`: explicit-only bug/vulnerability diagnosis and repair planning.
- `xc881-coding-skills`: implementation, validation, code quality, checkpoint/push.

## Rules

- Keep `xc881-solution-research`, `xc881-requirement-analysis`, and `xc881-bugfix-research` explicit-only.
- Do not let ordinary research/requirement/bug/security keywords implicitly trigger explicit-only skills.
- Keep research/analysis skills analysis-only; implementation, testing, validation, and checkpointing belong to `xc881-coding-skills`.
- Solution research must normalize ideas, derive explicit/inferred research questions, prefer papers for principle-level knowledge, use authoritative sources, compare feasible options compactly, and hand off.
- Keep `SKILL.md` compact; move detailed runtime rules to references.
- Put install, compatibility, indexing, and research background in root `README.md` or `docs/`.
- Keep frontmatter tags non-empty.
- Validate before publishing:
  - `python skills/xc881-solution-research/scripts/validate_skill.py`
  - `python skills/xc881-requirement-analysis/scripts/validate_skill.py`
  - `python skills/xc881-bugfix-research/scripts/validate_skill.py`
  - `python skills/xc881-coding-skills/scripts/validate_skill.py`
