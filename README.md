# xc881-skills

Token-efficient Agent Skills for explicit solution research, explicit requirement analysis, explicit bug/vulnerability diagnosis, and engineering execution.

## Skills

| Skill | Use for | Trigger |
| --- | --- | --- |
| `xc881-solution-research` | Idea-to-technical research, paper-first principle analysis, tech-stack feasibility, source-backed options, handoff. | Explicit only: `$xc881-solution-research` |
| `xc881-requirement-analysis` | Requirement understanding, English Spec First, MVP/scope, explicit/inferred requirements, acceptance criteria, engineering handoff. | Explicit only: `$xc881-requirement-analysis` |
| `xc881-bugfix-research` | Bug/vulnerability diagnosis, web research, root-cause hypothesis, repair plan, verification plan, handoff. | Explicit only: `$xc881-bugfix-research` |
| `xc881-coding-skills` | Implementation, refactor, code quality, decoupling, tests/verification, performance mode, checkpoint/push. | Explicit or clear coding/engineering request |

## Recommended flows

```text
$xc881-solution-research
Research feasible technical options and produce a source-backed recommendation.

$xc881-requirement-analysis
Use the selected option as technical context. Produce requirements and acceptance criteria.

$xc881-coding-skills
Implement from the requirement handoff.
```

```text
$xc881-bugfix-research
Analyze evidence, research if needed, produce repair and verification plan.

$xc881-coding-skills
Implement the repair plan and run verification.
```

## Explicit-only skills

These do not auto-trigger from ordinary keywords:

```text
xc881-solution-research
xc881-requirement-analysis
xc881-bugfix-research
```

Use exact invocation when needed.

## Token policy

- `SKILL.md` files are compact fast paths.
- Detailed behavior lives in per-skill `references/`.
- Repository-level guidance lives in `docs/`.
- Agents should read references only when needed.
- Default outputs are compact; detailed reports are opt-in or risk-triggered.

## Compatibility

Use the skill folders through whichever loader your agent supports:

```text
.agents/skills/<skill-name>
~/.agents/skills/<skill-name>
.claude/skills/<skill-name>
~/.claude/skills/<skill-name>
.codex/skills/<skill-name>
~/.codex/skills/<skill-name>
.cursor/skills/<skill-name>
~/.cursor/skills/<skill-name>
```

For DeepSeek, GLM, Mimo, or wrappers without Skill loading, use `platform-prompts/*.md`.

## Install

```bash
mkdir -p ~/.agents/skills ~/.claude/skills ~/.codex/skills ~/.cursor/skills
cp -r skills/xc881-solution-research ~/.agents/skills/
cp -r skills/xc881-requirement-analysis ~/.agents/skills/
cp -r skills/xc881-bugfix-research ~/.agents/skills/
cp -r skills/xc881-coding-skills ~/.agents/skills/
```
