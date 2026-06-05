# xc881-coding-skills

Agent skill repository for `xc881-coding-skills`, the xc881代码工程规范 skill set.

## Skills

| Skill | Purpose |
| --- | --- |
| `xc881-coding-skills` | Apply xc881 engineering discipline: English spec first, high-constraint coding, code splitting, decoupling, no-code-comments by default, safe verification, and explicit-only git checkpoint/push. |

## Layout

```txt
skills/
  <skill-name>/
    SKILL.md
    references/
    scripts/
    evals/
    agents/
```

Only `SKILL.md` is required. Other folders are included when the skill needs extra references, helper scripts, evaluation files, or agent-specific configuration.

The `agents/` directory contains per-platform YAML files (`claude.yaml`, `openai.yaml`) with display names, short descriptions, default prompts, and invocation policy. These are non-standard extensions on top of the Agent Skills open standard.

## Install

Agent Skills are commonly discovered from these directories:

| Path | Scope |
| --- | --- |
| `.agents/skills/` | Project-level |
| `.cursor/skills/` | Project-level (Cursor) |
| `.claude/skills/` | Project-level (Claude Code) |
| `.codex/skills/` | Project-level (Codex CLI) |
| `~/.agents/skills/` | User-level (global) |
| `~/.cursor/skills/` | User-level (Cursor) |
| `~/.claude/skills/` | User-level (Claude Code) |
| `~/.codex/skills/` | User-level (Codex CLI) |

Copy the skill folder into whichever directory matches your agent.

PowerShell:

```powershell
Copy-Item -Recurse .\skills\xc881-coding-skills $env:USERPROFILE\.agents\skills\
Copy-Item -Recurse .\skills\xc881-coding-skills $env:USERPROFILE\.claude\skills\
Copy-Item -Recurse .\skills\xc881-coding-skills $env:USERPROFILE\.codex\skills\
Copy-Item -Recurse .\skills\xc881-coding-skills $env:USERPROFILE\.cursor\skills\
```

macOS / Linux:

```bash
cp -r skills/xc881-coding-skills ~/.agents/skills/
cp -r skills/xc881-coding-skills ~/.claude/skills/
cp -r skills/xc881-coding-skills ~/.codex/skills/
cp -r skills/xc881-coding-skills ~/.cursor/skills/
```

## Use

```text
按 xc881代码工程规范写这个功能。
```

```text
对这个老项目做 xc881工程优化，先给报告，不要直接大改。
```

```text
Use $xc881-coding-skills before implementing this.
```

## Notes

This repository is intentionally plain and focused on repeatable behavior rather than presentation.

For DeepSeek, GLM, Mimo, or other wrappers without reliable Skill loading, use `platform-prompts/*.md` as custom instructions.
