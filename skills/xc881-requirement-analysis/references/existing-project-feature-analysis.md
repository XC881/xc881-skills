# Existing Change

Add:

```text
Affected:
Must not regress:
Migration:
Rollout:
```

Check behavior, contracts, data, permissions, tests, compatibility.

Breakdown: prefer vertical slices/tracer bullets that are independently verifiable and dependency-ordered. Avoid file-path implementation scripts in requirement handoff unless the path is part of the public contract.

Domain clarity: when a term or hard-to-reverse decision is resolved, include it in Handoff as `Term:` or `Decision:`. Create/update project docs only when the repo already has that convention or the user asks.
