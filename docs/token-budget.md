# Token Budget

Canonical repository-owned budgets live in `docs/skill-context-budget.md` and
are checked by `scripts/validate_context_budgets.py`.

```text
SKILL.md             <= 5,000 chars (xc881-analysis merged entry <= 7,000)
description          <=   320 chars each
all descriptions    <= 1,650 chars
agent default_prompt <=   180 chars
```

References remain branch-specific and use each skill validator's line limit.
Output sections are conditional; do not emit empty fields to satisfy a template.
These are static bloat guards.

Optimize necessary reads across turns, not disk payload size: preserve useful local data,
execute a bounded lookup, and expand only needed complete records. Valid guidance
already in context needs no repeat read. `scripts/audit_skill_loads.py` compares
entry sizes, cold paths and continuation expectations. A supplied body needs no
second manual read, but lost/changed required rules do. Names/paths/loaded markers
are not rule bodies.
