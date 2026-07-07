# Authoring

Principle: accurate, low-token, effective agent reading.

## Runtime shape

- `SKILL.md` is the fast path: role, trigger, reference index, workflow, output, hard rules.
- `references/` are runtime-only support files. Load only when the task branch needs them.
- `docs/` are maintenance-only. Do not rely on docs for runtime behavior.
- Keep each meaning in one authoritative place; link to it instead of repeating it.
- Compact output by default; write large artifacts to files and report path + verification.

## Invocation

- All skills are intent-routed. Direct `$skill-name` calls remain valid, but clear user intent without `xc881` may trigger the matching skill.
- Coding executes after scope is clear. If scope, AC, lifecycle, migration, or root cause is unclear, route to the matching analysis skill first.
- A description is a trigger surface. Use intent words the user actually says; avoid synonym piles.
- Split a skill only when it earns a trigger boundary, reduces runtime context, or prevents rushing a fuzzy step.

## Instruction quality

- Prefer checkable completion criteria over vague advice.
- Ask only blocking questions; look up facts from repo/docs/research before asking.
- Separate facts, inference, decisions, and recommendations.
- Use strong leading terms consistently: scope, AC, handoff, seam, equivalence, evidence.
- State positive target behavior. Use prohibitions only for hard guardrails and pair with the desired action.

## Pruning

- Delete no-op lines that do not change agent behavior.
- Remove sediment: stale examples, duplicated policy, and old branches that no longer trigger.
- Push branch-specific reference down to `references/`; pull must-have rules back into `SKILL.md`.
- Validate after edits and audit trigger/eval coverage.
