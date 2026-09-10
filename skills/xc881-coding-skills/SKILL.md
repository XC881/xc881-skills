---
name: xc881-coding-skills
description: 'Primary owner for project writes and complex/tracked reads. Use when the requested outcome is implement, review, verify, or explicit git. Simple exact local reads stay direct. Do not use for scope/AC, diagnosis-only, or research-only outcomes.'
when_to_use: 'Use when the requested outcome is a project write or complex/tracked read. Classify instant|queue, then read|change; bounded delegates do only their contract.'
display_name: "xc881代码工程规范"
version: "2.3.2"
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

Run only needed branches; reuse valid evidence.

## References

- `./references/xc881-code-quality-standard.md`: nontrivial change quality.
- `./references/high-constraint-coding-policy.md`: nontrivial design/risk gate.
- `./references/no-code-comments-policy.md`: comment exception; no routine comments.
- `./references/git-checkpoint-policy.md`: explicit git only.
- `./references/engineering-quality-rubric.md`: review.
- `./references/project-optimization.md`: optimization.
- `./references/adaptive-read-routing.md`: ambiguous read gate.
- `./references/requirement-artifact-execution.md`: first queue setup/contract change.
- `./references/execution-checkpoint-and-tool-policy.md`: recovery/tool failure.
- `./references/frontend-routing-and-design-read.md`: visible UI and frontend subroutes.

Route by intent each turn. Full supplied bodies count; names/paths/markers do not.
Reuse in-context rules; read needed exact paths automatically only for missing
rules, known changes or requested rereads. Higher-priority invocation rules win.
Execute scripts without reading source/data.

## Workflow

1. Read gate: explicit Coding invocation, every write, tracked work, or a
   task/project complexity trigger -> Coding. Ordinary simple reads stay direct.
2. Before opening project files or execution artifacts, classify `instant` (direct
   work) or `queue` (exact handoff/unambiguous active task). Multiple tasks -> one
   selection question; never choose latest.
3. Queue: use the write-first exact handoff; do not validate normally. Load
   `current.md` and its current item only. Observed corruption returns to Requirement.
4. Classify action independently as `read` or `change`. Trace relevant entry,
   dependencies, state and tests.
5. Frontend design starts with routing. Automatically load each relevant next ref
   only when its concern is reached. No user handoff/preload; nonvisual work loads
   none. For substantial new/reworked UI without a reusable system, generate a
   project-specific candidate; reconcile it with project evidence before use.
6. Read returns evidence, anchors and limits without edits. Delegates stay bounded;
   reviews lead with defects and missing tests.
7. Change sets an observable target; use the design gate for nontrivial/risky work.
   Make the smallest sound change; verify behavior/boundaries. Performance needs
   a request/measurement/hot path and trade-offs.
8. Queue: verify; patch item status (`pending|ready|blocked|done|skipped`, never `in-progress`),
   a history line and current pointers/counts together; advance until terminal.
   Resume a blocked item as `ready`; only task State uses `in-progress`.
   After compaction, resume the same current window automatically.
   Never ask the user to say continue at item boundaries. Stop only for explicit stepwise/pause intent
   or a real blocker, approval, safety, contract-change or no-runnable boundary.
9. Report verification in chat. Commit/push only on explicit request.

Write large output in file/section-sized patches; update changed sections only.

## Final response

Report relevant fields; omit empty ones:

```text
完成内容:
验证:
风险/假设:
```

## Hard rules

- Do not code from guessed paths.
- Do not scan `dev-notes` to infer an active task.
- Do not load previous/next queue files by default.
- Do not read `index.md` by default; contract gaps stop and return to Requirement.
- No claims beyond evidence, unrelated cleanup, or speculative abstraction.
- Keep business/domain rules out of UI, SQL, SDK callbacks, and framework objects.
- Never trade correctness/security/bounded complexity for performance.
