# AGENTS.md

This repository contains portable Agent Skills.

When editing this repository:

- Keep the root layout compatible with `skills/<skill-name>/SKILL.md`.
- Keep `SKILL.md` as the primary source of behavior.
- Put platform-specific defaults in `skills/<skill-name>/agents/`.
- Keep `agents/openai.yaml` and `agents/claude.yaml` in sync.
- Do not add `deepseek.yaml`, `glm.yaml`, or `mimo.yaml` unless a real loader for those files is documented.
- Put non-standard model instructions in `platform-prompts/`.
- Run `python skills/xc881-coding-skills/scripts/validate_skill.py` before publishing.
