# Real Compatibility Notes

## Reliable entries

### OpenAI / Codex

- `SKILL.md`
- `.codex/skills/<skill-name>/SKILL.md`
- `.agents/skills/<skill-name>/SKILL.md`
- `AGENTS.md`

Optional extension in this repository:

- `agents/openai.yaml`

### Claude / Claude Code

- `SKILL.md`
- `.claude/skills/<skill-name>/SKILL.md`
- `CLAUDE.md`

Optional extension in this repository:

- `agents/claude.yaml`

### Cursor and compatible agents

- `SKILL.md`
- `.cursor/skills/<skill-name>/SKILL.md`
- `.agents/skills/<skill-name>/SKILL.md`
- `AGENTS.md`

### DeepSeek / GLM / Mimo

These do not share one reliable public YAML Skill standard.

Use:

- `AGENTS.md` if the wrapper reads it
- `SKILL.md` if the wrapper supports Agent Skills
- `platform-prompts/*.md` as custom instructions or system prompt text
