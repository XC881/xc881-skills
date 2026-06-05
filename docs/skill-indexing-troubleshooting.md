# Skill Indexing Troubleshooting

This repository keeps indexing and installation troubleshooting at the repository level, not inside each skill's runtime `references/`.

Some launchers or wrappers build `skills_list` from frontmatter metadata instead of loading the full `SKILL.md`.

Each xc881 skill includes:

- `name`
- `description`
- `when_to_use`
- `display_name`
- `version`
- `category`
- non-empty `tags`
- `aliases`

## If a skill exists but does not appear in skills_list

Check:

1. The skill folder name matches `name` in `SKILL.md`.
2. `SKILL.md` starts with valid YAML frontmatter.
3. `tags` is present and non-empty.
4. The launcher scans the expected directory.
5. Restart or refresh the launcher after installing.
6. If the skill is installed through a symlink, try copying the real directory instead.

## Symlink note

Some launchers handle symlinked skill directories inconsistently.

Preferred install:

```bash
mkdir -p ~/.agents/skills
cp -r skills/xc881-requirement-analysis ~/.agents/skills/
cp -r skills/xc881-coding-skills ~/.agents/skills/
```

If using symlinks, ensure the target directory is readable and the launcher follows symlinks.
