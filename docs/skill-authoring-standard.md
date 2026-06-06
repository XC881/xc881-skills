# Skill Authoring Standard

First principle for all future xc881 skill changes:

Optimize for accurate, low-token, effective agent reading.

## Rules

1. `SKILL.md` is the fast path.
   - Keep it compact.
   - Include trigger, role, routing, core workflow, default output.
   - Do not duplicate reference details.

2. `references/` is runtime-only.
   - Include only task-execution rules an agent may need.
   - Do not put install, compatibility, indexing, research background, or changelog content there.

3. `docs/` is human/maintenance-only.
   - Install notes
   - Compatibility
   - Indexing troubleshooting
   - Research basis
   - Authoring rules

4. Default output must be compact.
   - Expand only when user asks, risk is high, or correctness would suffer.

5. Use precise routing.
   - Requirement analysis stays in `xc881-requirement-analysis`.
   - Coding execution stays in `xc881-coding-skills`.
   - New references must state when to read them.

6. Preserve indexing metadata.
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
