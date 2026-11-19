---
name: xc881-coding-skills
description: 'Primary owner for code writes, complex/tracked reads (incl. codebase walkthroughs), reviews, UI, verification, and explicit git. Enter directly when scope and cause are concrete; chain after Analysis or Porting when open scope, cause, facts, or parity. Simple exact/local/low-risk reads stay direct.'
when_to_use: 'Use when execution needs project writes or complex/tracked reads. If scope, root cause, external facts, or cross-language parity are open, run Analysis or Porting first, then execute here.'
display_name: "xc881代码工程规范"
version: "3.0.0"
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
  - 非屎山代码
---

# xc881 Coding Skills

## Role

Run only needed branches; reuse valid evidence.

## References

- `./references/xc881-code-quality-standard.md`: nontrivial quality.
- `./references/high-constraint-coding-policy.md`: design/risk gate.
- `./references/no-code-comments-policy.md`: comments.
- `./references/git-checkpoint-policy.md`: explicit git.
- `./references/engineering-quality-rubric.md`: review.
- `./references/project-optimization.md`: optimization.
- `./references/adaptive-read-routing.md`: read gate.
- `./references/requirement-artifact-execution.md`: queue setup/contract change.
- `./references/execution-checkpoint-and-tool-policy.md`: recovery/tool failure.
- `./references/frontend-routing-and-design-read.md`: UI subroutes.

Route each turn by user intent and actual task needs, not literal wording; chain
or switch skills when open scope, cause, facts, parity, or code work requires it.
Full supplied bodies count; names/paths/markers do not. Reuse in-context rules;
read missing/changed or reread-requested exact paths only. Higher-priority rules win.
Execute scripts without reading source/data.

## Workflow

1. Read gate: explicit Coding invocation, every write, tracked work, or a
   task/project complexity trigger -> Coding. Ordinary simple reads stay direct.
   Pre-edit: parity -> `$xc881-porting-orchestration`; open scope/AC, cause, or fact -> `$xc881-analysis`, then resume.
2. Before opening project files or execution artifacts, classify `instant` or
   `queue` (exact handoff/unambiguous active task). Multiple tasks -> one question;
   never pick latest.
3. Queue: use the write-first exact handoff; do not validate normally. Load
   `current.md` and its current item only. Corruption returns to Analysis.
4. Classify action independently as `read` or `change`. Trace callers, wire/data
   contracts and tests before changing signatures/fields.
5. Frontend design starts with routing. Automatically load each relevant next ref
   only when its concern is reached. No handoff/preload; nonvisual work loads none.
   Substantial new/reworked UI without a system derives one locally reconciled candidate.
6. Read returns evidence, `file:line` anchors and limits without edits. Delegates
   stay bounded; reviews rank P0-P3 defects (trigger -> broken invariant) and
   missing tests, separating Spec/AC from Standards.
7. Change sets an observable target (internal design gate for risky work). Check
   manifests before imports; validate boundaries without swallowing errors; ship
   smallest sound fix and verify target + failure/non-regression. Perf needs
   request/measurement/hot path + trade-offs.
8. Queue: verify; patch item status (`pending|ready|blocked|done|skipped`),
   a history line, and `current.md` (`Task:` kept; `Previous/Current/Next`: `queue/Q-NNN-*.md|none` paths — item files keep bare `Q-NNN` links; terminal `State: done`, `Current/Next: none`) together; advance until terminal.
   Resume a blocked item as `ready`; item status is never `in-progress`.
   After compaction, resume the same window. Never ask the user to say continue.
   Stop only for explicit stepwise/pause intent or a real blocker/approval/safety/contract boundary.
9. Report verification and limits in chat. Commit/push only when asked. Patch changed sections only.

## Final response

Start directly with mode heading (no preamble); omit empty optionals.
One final contract per turn: fold Analysis findings in; if delegated by Porting/Article, return bounded evidence internally without a banner.

Change (`change` / git):

```text
完成内容: <核心改动>
验证:
需要注意:
下一步:
```

Read / review (`read`):

```text
代码结论: <核心结论或按P0-P3缺陷>
依据:
需要注意:
下一步:
```

## Hard rules

- Do not code from guessed paths. Do not scan `dev-notes` to infer a task.
- Do not load previous/next queue files. Do not read `index.md` by default; contract gaps stop and return to Analysis.
- No claims beyond evidence, unrelated cleanup, or speculative abstraction.
- Keep domain rules out of UI, SQL, SDK callbacks, and framework objects.
- Never trade correctness/security/bounded complexity for performance.
