# Code Quality

Priority:

```text
correctness > safety > clarity > modularity > testability > performance > brevity
```

Rules:

- Encode requested behavior directly.
- Validate boundaries.
- Make invalid states hard.
- Keep state/errors explicit.
- Keep permission/security/data checks visible.
- Prefer obvious control flow and domain names.
- Modularize by reason to change.
- Keep domain independent of framework/DB/SDK/HTTP/UI/env/time/random/global state.
- Keep serialization at edges.
- Avoid God object / 万能 service / 万能 utils.
- Core logic testable without real infra.
- Comment only core difficulty.
- Perf mode needs objective, local complexity, benchmark when practical, tradeoff report.

Blockers: circular deps, globals, duplicated rules, framework leakage, swallowed errors, unchecked input, secrets, speculative abstraction, unrelated cleanup, unmeasured optimization.
