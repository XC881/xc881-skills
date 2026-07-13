# Skill Context Budget

xc881-skills controls filesystem-based skill content, not runtime-client internals.

## Owned surfaces

- skill metadata for routing;
- selected `SKILL.md` fast path;
- branch-specific references loaded on demand;
- bounded script output;
- agent compatibility prompt;
- req-process/cross-process current execution window.

Progressive disclosure is the primary context strategy: metadata discovers,
`SKILL.md` executes, and references/scripts load only for the active branch.

## Repository limits

```text
SKILL.md                5,000 chars
agent default_prompt      260 chars
req-process/current.md  1,200 chars
active queue item       3,500 chars
req-process/index.md   10,000 chars
cross-process ledger    3,000 chars
```

These limits prevent repository instruction and artifact bloat. They are not
token, cost, latency, or context-window estimates.

## Checks

```bash
python scripts/validate_context_budgets.py --report
python scripts/audit_context_sizes.py dev-notes/req-process/<active-task>
```

The audit compares current-only loading with the legacy previous/current/next
window using character counts from files this repository owns.
