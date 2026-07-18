---
name: xc881-coding-skills
description: 'Primary owner for project writes and complex/tracked reads. Implement, review, verify, and handle explicit git. Simple exact local reads stay direct; delegates stay bounded.'
when_to_use: 'Use for project writes and complex/tracked reads. Classify instant|queue, then read|change; bounded delegates do only their contract.'
display_name: "xc881代码工程规范"
version: "2.3.0"
category: "coding"
tags:
  - coding
  - code-reading
  - code-quality
  - refactor
  - decoupling
  - maintainability
  - testability
  - anti-overengineering
  - performance
  - frontend
  - git-checkpoint
  - xc881
aliases:
  - xc881-coding
  - xc881-engineering
  - xc881代码工程规范
  - xc881工程优化
  - 代码规范
  - 非屎山代码
---

# xc881 Coding Skills

## Role

Own writes/complex reads; run only needed branches; make the smallest sound change.

## References

- `./references/xc881-code-quality-standard.md`: quality/performance.
- `./references/high-constraint-coding-policy.md`: risky change/design gate.
- `./references/no-code-comments-policy.md`: before editing code.
- `./references/git-checkpoint-policy.md`: explicit commit/checkpoint/push only.
- `./references/engineering-quality-rubric.md`: review.
- `./references/project-optimization.md`: optimization.
- `./references/adaptive-read-routing.md`: decide direct read vs Coding read.
- `./references/requirement-artifact-execution.md`: task mode and queue checkpoint.
- `./references/execution-checkpoint-and-tool-policy.md`: queue recovery.
- `./references/frontend-routing-and-design-read.md`: routing/Design Read.
- `./references/frontend-design-intelligence.md`: unresolved design decisions.
- `./references/frontend-implementation-standard.md`: implementation.
- `./references/frontend-image-reference-workflow.md`: image-to-code.
- `./references/frontend-redesign-and-visual-qa.md`: visual QA.
- `./references/frontend-pattern-catalog.md`: visual patterns.

Open only needed exact paths above.

## Workflow

1. Read gate: explicit Coding invocation, every write, tracked work, or a
   task/project complexity trigger -> Coding. Ordinary simple reads stay direct.
2. Once selected, before opening project files or execution artifacts classify
   persistence: `instant` works directly; `queue` needs an exact handoff or one
   unambiguous active task. Multiple candidates -> one question. Do not scan
   `dev-notes` or choose latest.
3. Queue: use the write-first exact handoff; do not validate normally. Load
   `current.md` and its current item only. Directly observed corruption returns
   to Requirement; only audit/repair validates.
4. Classify action independently as `read` or `change`. Inspect real entry
   points, flow, tests/types/config, and local style.
5. Frontend design starts with routing. Automatically load each relevant next ref
   only when its concern is reached: design intelligence, implementation, image,
   redesign/QA, or pattern. No user handoff/preload; nonvisual or unrelated work
   loads none. Make a Design Read only for substantial greenfield, visual, or redesign work.
6. Read reports evidence without editing. Change sets one success target, then
   loads risk-relevant quality, constraint, and comment references.
7. For non-trivial/risky changes, use the design gate; keep every changed line
   traceable and avoid unrelated cleanup or speculative abstraction.
8. Implement the smallest maintainable change and verify observable behavior.
   Performance mode needs a request/measurement/hot path and trade-offs.
9. A delegated `read` returns bounded evidence; it does not silently change.
10. Queue loop: verify current, checkpoint status/history/current, advance, and
    continue until task terminal. After context compaction, reload the same
    current window and continue automatically. Never ask the user to say continue
    at item boundaries. Stop only for explicit stepwise/pause intent
    or a real blocker/approval/safety/contract-change/no-runnable boundary.
11. Report verification in chat. Commit/push only on explicit request using the
    git reference.

Large output uses bounded files; chat reports path, progress, verification.

## Final response

Always close with exactly:

```text
完成内容:
验证:
风险/假设:
```

Append performance or git fields only when those modes were used.

## Hard rules

- Do not code from guessed paths.
- Do not force simple bounded reads through Coding or bypass it for writes/complex reads.
- Do not scan `dev-notes` to infer an active task.
- Do not load previous/next queue files by default.
- Do not read `index.md` by default; contract gaps stop and return to Requirement.
- Do not claim success beyond evidence or improve adjacent code unless required.
- Keep business/domain rules out of UI, SQL, SDK callbacks, and framework objects.
- Never trade correctness/security/bounded complexity for performance.
- Do not commit/push unless explicitly requested.
