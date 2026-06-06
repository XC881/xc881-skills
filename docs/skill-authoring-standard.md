# Skill Authoring Standard

First principle:

```text
accurate, low-token, effective agent reading
```

## Rules

1. `SKILL.md` is the fast path.
   - role
   - trigger policy
   - routing
   - core workflow
   - compact output
   - when to read references

2. `references/` is runtime-only.
   - Only task-execution rules an agent may need.
   - No install notes, compatibility notes, indexing docs, research background, changelog, or design notes.

3. `docs/` is human/maintenance-only.
   - overview
   - compatibility
   - indexing troubleshooting
   - research basis
   - authoring standard

4. Default output is compact.
   - Expand only when user asks, risk is high, evidence conflicts, or correctness would suffer.

5. Keep layer boundaries.
   - requirement analysis: product/project understanding
   - bugfix research: explicit-only diagnosis and repair planning
   - coding skills: implementation, tests, verification, checkpoint

6. Preserve metadata.
   - `name`
   - `description`
   - `when_to_use`
   - `display_name`
   - `version`
   - `category`
   - non-empty `tags`
   - `aliases`

7. Validate before publishing.
   - Update evals for new trigger behavior.
   - Update reference inventory.
   - Keep validation scripts strict.
