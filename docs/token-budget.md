# Token Budget

Canonical repository-owned budgets live in `docs/skill-context-budget.md` and
are checked by `scripts/validate_context_budgets.py`.

```text
SKILL.md             <= 5,000 chars
description          <=   320 chars each
all descriptions    <= 1,650 chars
agent default_prompt <=   180 chars
```

References remain branch-specific and use each skill validator's line limit.
Output sections are conditional; do not emit empty fields to satisfy a template.
These are static bloat guards, not provider token/cost estimates.
