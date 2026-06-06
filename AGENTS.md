# AGENTS.md

This repository contains portable, token-efficient Agent Skills.

## First principle

```text
accurate, low-token, effective agent reading
```

## Layering

- `xc881-requirement-analysis`: requirement understanding before coding.
- `xc881-bugfix-research`: explicit-only bug/vulnerability diagnosis and repair planning.
- `xc881-coding-skills`: implementation, validation, code quality, checkpoint/push.

## Rules

- Keep requirement analysis separate from coding execution.
- Keep bugfix research explicit-only and analysis-only.
- Do not let ordinary bug/error/security keywords implicitly trigger `xc881-bugfix-research`.
- `xc881-bugfix-research` must produce diagnosis, repair plan, verification plan, and handoff; it must not edit code or claim tests were run.
- Implementation, testing, validation, and checkpointing belong to `xc881-coding-skills`.
- Web research must prefer official docs, advisories, changelogs, CVE/GHSA/OSV/NVD, CWE/OWASP, and maintainer issues before forums/blogs.
- Do not provide weaponized exploit instructions.
- Keep `SKILL.md` compact; move detailed runtime rules to references.
- Keep per-skill `references/` limited to runtime task-execution rules.
- Put install, compatibility, indexing, and research-background documents in root `README.md` or `docs/`.
- Do not add `skill-indexing-troubleshooting.md`, `real-compatibility.md`, or `research-basis.md` to per-skill `references/`.
- Keep frontmatter tags non-empty so skill indexers and `skills_list` can discover the skill.
- Keep `agents/openai.yaml` and `agents/claude.yaml` in sync for each skill.
- Do not add platform YAML files without a documented loader.
- Validate before publishing:
  - `python skills/xc881-requirement-analysis/scripts/validate_skill.py`
  - `python skills/xc881-bugfix-research/scripts/validate_skill.py`
  - `python skills/xc881-coding-skills/scripts/validate_skill.py`

