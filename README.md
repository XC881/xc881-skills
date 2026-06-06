# xc881-skills

Token-efficient Agent Skills for requirement analysis and engineering execution.

## Skills

| Skill | Use for |
| --- | --- |
| `xc881-requirement-analysis` | Before coding: normalize rough requests, analyze new projects or existing-feature requirements, infer hidden dependency/consequence requirements, define acceptance criteria, risks, and engineering handoff. |
| `xc881-coding-skills` | After requirements are clear: implement, refactor, review, optimize, split code, decouple, verify, keep code comment-free by default, and checkpoint/push only when requested. |

## Recommended flow

```text
$xc881-requirement-analysis
Analyze requirements, infer hidden needs, define acceptance criteria and implementation handoff.

$xc881-coding-skills
Use the analysis as source of truth. Read code, run compact design gate, implement Phase 1.
```

## Token policy

- `SKILL.md` files are compact fast paths.
- Detailed behavior lives in `references/`.
- Agents should read references only when needed.
- Default outputs are compact; detailed reports are opt-in or risk-triggered.

## Runtime references vs repository docs

Per-skill `references/` directories contain only files that an agent may need during task execution.

Repository-level docs live in `docs/`:

| File | Purpose |
| --- | --- |
| `docs/skill-indexing-troubleshooting.md` | Human-facing install/indexing troubleshooting, including `skills_list` issues and symlink notes. |
| `docs/requirement-analysis-research-basis.md` | Design rationale and research basis for requirement analysis; not needed during normal execution. |

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
cp -r skills/xc881-coding-skills ~/.agents/skills/
cp -r skills/xc881-requirement-analysis ~/.claude/skills/
cp -r skills/xc881-coding-skills ~/.claude/skills/
cp -r skills/xc881-requirement-analysis ~/.codex/skills/
cp -r skills/xc881-coding-skills ~/.codex/skills/
cp -r skills/xc881-requirement-analysis ~/.cursor/skills/
cp -r skills/xc881-coding-skills ~/.cursor/skills/
```


## Skill indexing / skills_list troubleshooting

See `docs/skill-indexing-troubleshooting.md`.
## Skill authoring standard

All future skill additions and reference updates must follow `docs/skill-authoring-standard.md`.

First principle:

```text
accurate, low-token, effective agent reading
```

## Code quality standard

`xc881-coding-skills` includes `references/xc881-code-quality-standard.md`.

It formalizes correctness, stability, logical modularity, testability, edge isolation, core-difficulty-only comments, and performance mode trade-offs.
