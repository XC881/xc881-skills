# High-Constraint Coding Policy

Use for serious coding, bug fixes, refactors, reviews, production edits, regression-sensitive changes, and minimal-diff requests.

## Required behavior

1. Bound the task.
2. Read the real implementation path.
3. State what the relevant current code does before editing.
4. Choose the narrowest maintainable solution.
5. Preserve local style.
6. Keep changes scoped.
7. Avoid speculative abstractions.
8. Verify before claiming success.
9. Report outcome, evidence, assumptions, and residual risk.

## Stop rule

If two attempted fixes fail, stop patching. Re-read the relevant code, diagnose the root cause from evidence, and choose a different strategy.

## Avoid

- unrelated rewrites
- broad renames
- dense clever code
- one-off wrapper abstractions
- generic utilities to avoid a few explicit lines
- premature caching, batching, async complexity, or performance optimization without evidence
