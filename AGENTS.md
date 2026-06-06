# AGENTS.md

This repository contains portable, token-efficient Agent Skills.

Rules:
- Keep requirement analysis separate from coding execution.
- Keep `SKILL.md` compact; move detailed rules to references.
- Default outputs should be compact.
- Do not re-add English Spec First to `xc881-coding-skills`.
- Keep compatibility guidance in root README.md.
- Keep `agents/openai.yaml` and `agents/claude.yaml` in sync for each skill.
- Do not add platform YAML files without a documented loader.
- Validate before publishing:
  - `python skills/xc881-requirement-analysis/scripts/validate_skill.py`
  - `python skills/xc881-coding-skills/scripts/validate_skill.py`

- Keep frontmatter tags non-empty so skill indexers and skills_list can discover the skill.
- Prefer real copied skill directories over symlink-only installs when a launcher does not follow symlinks reliably.

- Keep per-skill `references/` limited to runtime task-execution rules.
- Put install, compatibility, indexing, and research-background documents in root `README.md` or `docs/`.
- Do not add `skill-indexing-troubleshooting.md`, `real-compatibility.md`, or `research-basis.md` to per-skill `references/`.
- First principle for all skill updates: accurate, low-token, effective agent reading.
- Follow `docs/skill-authoring-standard.md` for new skills and reference updates.
- Keep `xc881-code-quality-standard.md` in `xc881-coding-skills/references/`; it is runtime execution policy.
- Comments policy is not "never comment"; it is "comment only core difficulty".
- Keep `xc881-bugfix-research` explicit-only and analysis-only.
- Do not let ordinary bug/error/security keywords implicitly trigger `xc881-bugfix-research`.
- It must produce diagnosis, repair plan, verification plan, and handoff; it must not edit code or claim tests were run.
- Implementation, testing, validation, and checkpointing belong to `xc881-coding-skills`.
- Web research must prefer official docs, advisories, changelogs, CVE/GHSA/OSV/NVD, CWE/OWASP, and maintainer issues before forums/blogs.
- Do not provide weaponized exploit instructions in the bugfix skill.
