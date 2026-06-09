---
name: xc881-coding-skills
description: 'Coding execution. Use for implementation, clear-cause bug fix, refactor, review, code quality, anti-overengineering, minimal diff, tests, performance, checkpoint/push. May trigger on $xc881-coding-skills or clear coding intent.'
when_to_use: 'Use when scope is clear and code must be changed/reviewed/verified. If feasibility, requirement, or root cause is unclear, request explicit analysis skill first.'
display_name: "xc881代码工程规范"
version: "2.1.0"
category: "coding"
tags:
  - coding
  - code-quality
  - refactor
  - anti-overengineering
  - surgical-change
  - testability
  - performance
  - xc881
aliases:
  - xc881-coding-skills
  - xc881
  - xc881-coding
  - xc881代码工程规范
---

# xc881 Coding

Execute clear coding tasks.

Gate:

```text
unclear feasibility → $xc881-solution-research
unclear requirement → $xc881-requirement-analysis
unclear root cause → $xc881-bugfix-research
```

Refs only when needed:

- `karpathy-guardrail.md`: always before edits.
- `xc881-code-quality-standard.md`: quality/refactor/review/perf.
- `high-constraint-coding-policy.md`: risky/minimal diff.
- `no-code-comments-policy.md`: comments.
- `git-checkpoint-policy.md`: explicit commit/push.
- `engineering-quality-rubric.md`: review.
- `project-optimization.md`: project optimization.

Steps:

1. Read real path.
2. State assumptions only if risky.
3. Bound task.
4. Define one success check.
5. Patch smallest traceable diff.
6. Verify before success.
7. Commit/push only if explicit.

Gate for non-trivial work:

```text
xc881 Gate:
Change:
Success:
Files:
Boundary:
Risk:
Overdesign:
Test:
```

Dependency:

```text
UI → UseCase → Domain → Port ← Infra
```

Output:

```text
Done:
Verify:
Risk:
```

Rules:

- No guessed paths.
- No unrelated cleanup/refactor.
- No single-use abstraction.
- No routine comments.
- No domain leakage from framework/DB/SDK/UI.
- No hidden business rules in UI/SQL/callbacks.
- No success claim beyond evidence.
