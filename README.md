# xc881-skills

Agent skill repository for the xc881 workflow.

## Skills

| Skill | Purpose |
| --- | --- |
| `xc881-requirement-analysis` | Normalize rough or mixed-language requests with English Spec First, analyze new project requirements or existing project feature requirements, infer hidden dependency/consequence requirements, define acceptance criteria, risks, and engineering implementation plan. |
| `xc881-coding-skills` | Execute safe engineering work after requirements are clear: coding, refactor, code splitting, decoupling, verification, no-code-comments, and explicit-only git checkpoint/push. |

## Recommended workflow

```text
$xc881-requirement-analysis
Normalize the rough request first if needed, then analyze this existing project feature or new project idea. Identify explicit requirements, inferred requirements, acceptance criteria, risks, and an engineering plan.

$xc881-coding-skills
Use the requirement analysis above as the source of truth. Produce the xc881 design gate and implement Phase 1 only.
```

## Compatibility

This repository centralizes compatibility guidance here instead of duplicating `real-compatibility.md` inside each skill.

### Reliable entry points

#### OpenAI / Codex

Use:

```text
SKILL.md
.agents/skills/<skill-name>/SKILL.md
AGENTS.md
```

Optional extension in this repository:

```text
skills/<skill-name>/agents/openai.yaml
```

For Codex, the recommended global install path is:

```text
~/.agents/skills/<skill-name>
```

Project-level install path:

```text
<project>/.agents/skills/<skill-name>
```

#### Claude / Claude Code

Use:

```text
SKILL.md
.claude/skills/<skill-name>/SKILL.md
CLAUDE.md
```

Optional extension in this repository:

```text
skills/<skill-name>/agents/claude.yaml
```

#### Cursor and compatible agents

Use whichever entry the wrapper supports:

```text
SKILL.md
.cursor/skills/<skill-name>/SKILL.md
.agents/skills/<skill-name>/SKILL.md
AGENTS.md
```

#### DeepSeek / GLM / Mimo

These do not share one reliable public YAML Skill standard.

Use:

```text
AGENTS.md
SKILL.md
platform-prompts/*.md
```

depending on what the wrapper or IDE actually reads.

Do not add `deepseek.yaml`, `glm.yaml`, or `mimo.yaml` unless a real loader for those files is documented.

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
