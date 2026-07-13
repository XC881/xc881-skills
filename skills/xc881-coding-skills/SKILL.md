---
name: xc881-coding-skills
description: 'Intent-routed engineering execution. Use for all project writes and reads made complex by task/project coupling: unknown paths, multi-module flows, runtime evidence, architecture, security, performance, concurrency, generated/framework code, or tracked work. Simple exact local low-risk reads may run directly.'
when_to_use: 'Use when explicitly invoked, for every project write, or when the adaptive read gate selects Coding. Classify instant|queue before read|change. Analysis skills may perform simple bounded reads directly or delegate complex reads and resume.'
display_name: "xc881代码工程规范"
version: "2.1.0"
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
  - git-checkpoint
  - xc881
aliases:
  - xc881
  - xc881-coding
  - xc881-engineering
  - xc881代码工程规范
  - xc881工程优化
  - 代码规范
  - 非屎山代码
---

# xc881 Coding Skills

## Role

Own all project writes and complex engineering reads: inspect real evidence or
make the smallest maintainable verified change.

## References

- `./references/xc881-code-quality-standard.md`: non-trivial change/review/refactor/performance.
- `./references/high-constraint-coding-policy.md`: risky/minimal changes and design gate.
- `./references/no-code-comments-policy.md`: before editing code.
- `./references/git-checkpoint-policy.md`: explicit commit/checkpoint/push only.
- `./references/engineering-quality-rubric.md`: quality review/verification.
- `./references/project-optimization.md`: legacy/project optimization.
- `./references/adaptive-read-routing.md`: decide direct read vs Coding read.
- `./references/requirement-artifact-execution.md`: task mode and queue checkpoint.
- `./references/execution-checkpoint-and-tool-policy.md`: queue recovery and tool budget.

Open references only by the exact relative paths above and only for the active branch.

## Workflow

1. Read gate: explicit Coding invocation, every write, tracked work, or any task/project complexity trigger -> Coding. An ordinary read may stay direct only when every simple condition in `adaptive-read-routing.md` holds. Analysis may perform that simple read or delegate a complex read and resume.
2. Once Coding is selected, before opening project files or execution artifacts classify persistence: `instant` works directly; `queue` needs an exact handoff or one unambiguous active task. Multiple candidates -> one blocking question. Do not scan `dev-notes` or choose latest.
3. Queue: validate, then load `current.md` and the current queue item only. Previous needs an explicit evidence/dependency link; next waits until advancement. Do not read `index.md` by default.
4. Classify action independently as `read` or `change`. Inspect real entry points, call/data flow, tests/types/config, and local style in both modes.
5. Read: report evidence without editing. Change: define one success target, then load quality/high-constraint/comment references as applicable.
6. For non-trivial/risky changes, use the design gate in high-constraint policy; keep every changed line traceable and avoid unrelated cleanup, speculative flexibility, or one-use abstraction.
7. Implement the smallest maintainable change; verify observable behavior. Performance mode requires request/measurement/hot path and reports trade-offs.
8. A delegated `read` returns bounded evidence; it does not silently become a change.
9. Queue loop: verify current, checkpoint status/history/current, advance, then load the new current item and continue until task terminal. After context compaction, reload the same current window and continue automatically. Never ask the user to say continue at item boundaries. Stop only for explicit stepwise/pause intent or a real blocker/approval/safety/contract-change/no-runnable boundary.
10. Report verification in chat. Commit/push only on explicit request using the git reference.

Large output goes to bounded files; chat reports path, progress, and verification.

## Final response

Always close with exactly:

```text
完成内容:
验证:
风险/假设:
```

Append performance trade-off/benchmark or commit/branch/push/remaining fields only
when those modes were used.

## Hard rules

- Do not code from guessed paths.
- Do not force simple bounded reads through Coding or bypass Coding for writes/complex reads.
- Do not scan `dev-notes` to infer an active task.
- Do not load previous/next queue files by default.
- Do not read `index.md` by default; contract gaps stop and return to Requirement.
- Do not claim success beyond evidence or improve adjacent code unless required.
- Keep business/domain rules out of UI, SQL, SDK callbacks, and framework objects.
- Never trade correctness/security/bounded complexity for performance.
- Do not commit/push unless explicitly requested.
