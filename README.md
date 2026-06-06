# xc881-skills

Token-efficient Agent Skills for requirement analysis, explicit bug/vulnerability diagnosis, and engineering execution.

## Skills

| Skill | Use for | Trigger |
| --- | --- | --- |
| `xc881-requirement-analysis` | Requirement understanding, English Spec First, MVP/scope, explicit/inferred requirements, acceptance criteria, engineering handoff. | Explicit or clear requirement-analysis request |
| `xc881-bugfix-research` | Bug/vulnerability diagnosis, web research, root-cause hypothesis, repair plan, verification plan, handoff to coding. | Explicit only: `$xc881-bugfix-research` |
| `xc881-coding-skills` | Implementation, refactor, code quality, decoupling, tests/verification, performance mode, checkpoint/push. | Explicit or clear coding/engineering request |

## Recommended flows

### New feature / project

```text
$xc881-requirement-analysis
Analyze requirements and produce handoff.

$xc881-coding-skills
Implement from the requirement handoff.
```

### Bug / vulnerability diagnosis

```text
$xc881-bugfix-research
Analyze evidence, research if needed, produce repair and verification plan.

$xc881-coding-skills
Implement the repair plan and run verification.
```

## Trigger policy

`xc881-bugfix-research` is explicit-only.

These should trigger it:

```text
$xc881-bugfix-research ...
使用 xc881-bugfix-research ...
启用 xc881漏洞与Bug诊断 Skill ...
```

These should not trigger it by themselves:

```text
bug
报错
异常
CVE
漏洞
stack trace
500
regression
```

## Token policy

- `SKILL.md` files are compact fast paths.
- Detailed behavior lives in per-skill `references/`.
- Repository-level guidance lives in `docs/`.
- Agents should read references only when needed.
- Default outputs are compact; detailed reports are opt-in or risk-triggered.

## Runtime references vs repository docs

Per-skill `references/` directories contain only files that an agent may need during task execution.

Repository-level docs live in `docs/`:

| File | Purpose |
| --- | --- |
| `docs/skills-overview.md` | Human-facing overview of all xc881 skills and layering. |
| `docs/skill-authoring-standard.md` | Authoring standard: accurate, low-token, effective agent reading. |
| `docs/skill-indexing-troubleshooting.md` | Human-facing install/indexing troubleshooting. |
| `docs/requirement-analysis-research-basis.md` | Requirement-analysis design background. |
| `docs/bugfix-research-basis.md` | Bugfix research design background. |
| `docs/reference-inventory.md` | Generated inventory of runtime references. |

Do not duplicate compatibility, install, indexing, or research-background files inside every skill's `references/`.

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

`agents/openai.yaml` and `agents/claude.yaml` are optional platform metadata.

For DeepSeek, GLM, Mimo, or wrappers without Skill loading, use `platform-prompts/*.md`.

## Install

```bash
mkdir -p ~/.agents/skills ~/.claude/skills ~/.codex/skills ~/.cursor/skills
cp -r skills/xc881-requirement-analysis ~/.agents/skills/
cp -r skills/xc881-bugfix-research ~/.agents/skills/
cp -r skills/xc881-coding-skills ~/.agents/skills/
cp -r skills/xc881-requirement-analysis ~/.claude/skills/
cp -r skills/xc881-bugfix-research ~/.claude/skills/
cp -r skills/xc881-coding-skills ~/.claude/skills/
cp -r skills/xc881-requirement-analysis ~/.codex/skills/
cp -r skills/xc881-bugfix-research ~/.codex/skills/
cp -r skills/xc881-coding-skills ~/.codex/skills/
cp -r skills/xc881-requirement-analysis ~/.cursor/skills/
cp -r skills/xc881-bugfix-research ~/.cursor/skills/
cp -r skills/xc881-coding-skills ~/.cursor/skills/
```

## Skill indexing / skills_list troubleshooting

See `docs/skill-indexing-troubleshooting.md`.

