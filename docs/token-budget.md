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

Optimize necessary reads across turns, not disk payload size: preserve useful local data,
execute a bounded lookup, and expand only needed complete records. Valid guidance
already in context needs no repeat read. `scripts/audit_skill_loads.py` compares
entry sizes, cold paths and continuation expectations; actual behavior needs
independent task evaluation. A supplied body needs no second manual read, but
lost/changed required rules do. Names/paths/loaded markers are not rule bodies.
Separate tool reads from host injection and later input cost; no per-turn registry
or client-cache mechanism belongs in this repository. Recorded provider usage, when
present, is the cumulative total delta for that thread. Summing repeated usage
events or converting character counts into saved tokens is invalid.
