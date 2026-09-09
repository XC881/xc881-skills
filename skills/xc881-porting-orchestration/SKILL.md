---
name: xc881-porting-orchestration
description: 'Primary owner for cross-language/project porting. Classify magnitude and boundaries, preserve behavioral equivalence, and call only specialists needed by the current migration step. Ordinary refactors, data migrations, and incidental language mentions do not trigger it.'
when_to_use: 'Use for cross-language/project migration outcomes. Small non-goal work may stay chat-only; goal work locks boundaries and linked state.'
display_name: "xc881移植编排"
version: "1.7.1"
category: "orchestration"
tags:
  - porting
  - migration
  - cross-language
  - orchestration
  - goal-boundary
  - equivalence
  - xc881
aliases:
  - xc881-porting-orchestration
  - xc881移植编排
  - xc881移植
  - xc881迁移
---

# xc881 Porting Orchestration

Intent-routed cross-language/project migration owner; direct calls select it.
Incidental languages stay with the current owner. No code; delegate implementation.

## Reference Routes

- `./references/goal-boundary-contract.md`: unclear magnitude or goal stop boundary.
- `./references/cross-language-understanding.md`: unresolved semantic/architecture/library mappings.
- `./references/equivalence-and-idiomatic-porting.md`: parity proof or idiomatic departure.
- `./references/cross-process-plan.md`: ledger creation/update/resume.
- `./references/porting-output-contract.md`: persisted progress or blocking/handoff summary.

Route by intent each turn. Full supplied bodies count; names/paths/markers do not.
Reuse in-context rules; read needed exact paths automatically only for missing
rules, known changes or requested rereads. Higher-priority invocation rules win.

## Delegation

- Boundary/risk/req-process -> `$xc881-requirement-analysis`.
- Deep reading, port, equivalence check -> `$xc881-coding-skills`.
- Unresolved language/library facts -> `$xc881-solution-research`.

Send current question/slice, evidence, constraints and permissions; receive needed
anchors, uncertainty and next step. Resume Porting without rediscovery.

## Workflow

1. Classify magnitude and goal/non-goal from supplied or cheap evidence. Reuse
   revision/scope-matched mappings; delegate missing boundary/parity gaps only.
2. Goal gate: reuse a locked boundary or have Requirement persist measurable done
   criteria, exit conditions and exclusions. Unclear boundary -> one question; no port.
3. Goal/queue: reuse or derive/write the linked <=3,000-char cross-process ledger;
   do not use a normal validator loop or copy scope/AC. Small non-goal planning stays
   chat-only. Ask before changing `.gitignore`.
4. Explicit/unambiguous task only: read cross-process and linked req
   `current.md + current item`; previous needs an evidence link, next waits for
   advancement. Never scan or read req index by default.
5. Resolve current-slice semantic/library gaps. Select proof of source-observable
   outputs, errors, state and side effects before porting; tests support only covered behavior.
6. Planning/boundary-only intent stops with a plan. Requested implementation/executable
   queue delegates current port/verification to Coding. Behavior outranks target
   architecture, then idiom; intent fidelity is for abstract-intent work only.
7. Unresolved parity blocks completion. Checkpoint status/blockers, advance verified
   items, recheck boundaries and continue automatically to task terminal. Compaction retains Porting
   ownership/current equivalence state. Stop only for explicit stepwise/pause intent
   or real blockers/boundaries. Verification/equivalence results stay in chat.

## User-facing output

```text
迁移结论:
本次迁移:
如何确认成功:
需要注意:        # only when relevant
需要确认:        # only when blocked; include recommendation + fallback
当前进度:
下一步:
开发记录:
```

## Hard rules

- Req-process owns scope/AC; cross-process owns magnitude/equivalence/progress.
- Missing/stale linked state: do not port. Never assume `.gitignore` choice.
