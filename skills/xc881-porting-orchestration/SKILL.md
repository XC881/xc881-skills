---
name: xc881-porting-orchestration
description: 'Primary owner for cross-language or cross-project migration with preserved behavior, whether planning boundaries or shipping the port (chaining Analysis for open scope/library facts and Coding for edits/parity checks). Ordinary same-stack refactors and incidental language mentions skip it.'
when_to_use: 'Use when intent or task direction is cross-language/project migration with behavioral parity; chain Analysis for open boundaries/facts and Coding for implementation and equivalence checks.'
display_name: "xc881移植编排"
version: "3.0.0"
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

Route each turn by user intent and actual task needs, not literal wording; chain
or switch skills when open scope, cause, facts, parity, or code work requires it.
Full supplied bodies count; names/paths/markers do not. Reuse in-context rules;
read missing/changed or reread-requested exact paths only. Higher-priority rules win.

## Delegation

- Boundary/risk/req-process -> `$xc881-analysis`.
- Deep reading, port, equivalence check -> `$xc881-coding-skills`.
- Unresolved language/library facts -> `$xc881-analysis`.

Send current question/slice, evidence, constraints and permissions; receive needed
anchors, uncertainty and next step. Resume Porting without rediscovery.

## Workflow

1. Classify magnitude and `goal` (whole-project/multi-module loop) vs `non-goal`
   (bounded one-shot function/file/slice) from supplied or simple exact/local/low-risk
   evidence (known target, 1-2 local files, no flow/risk/write). Reuse revision/scope-matched mappings; delegate missing boundary/parity gaps only.
2. Goal gate (`goal` only): reuse a locked boundary or have Analysis persist measurable done
   criteria, exit conditions and exclusions. Unclear boundary -> one question; no port.
3. Goal/queue (`goal` only): reuse or derive/write the linked <=4,500-char cross-process ledger
   (roll up completed slices; item status never `in-progress`);
   do not use a normal validator loop or copy scope/AC. Small non-goal ports (planning or shipped code) stay chat-only, skip ledgers, and run Coding `instant`. Ask before changing `.gitignore`.
4. Explicit/unambiguous task only: read cross-process and linked req
   `current.md + current item`; previous needs an evidence link, next waits for
   advancement. Never scan or read req index by default.
5. Resolve current-slice semantic/library gaps (numeric sign/overflow/rounding,
   UTF-8 vs code-unit len/regex, JSON null/omission/order, aliasing, error/cancel).
   Select proof of observable outputs, errors, state and side effects before
   porting; when source runs, capture boundary + adversarial golden vectors from
   source instead of hand-computing expected values. Tests support covered paths only.
6. Planning/boundary-only intent stops with a plan. Requested implementation/executable
   queue delegates current port/verification to Coding. Behavior outranks target
   architecture, then idiom; intent fidelity is for abstract-intent work only.
7. Unresolved parity blocks completion. Checkpoint status/blockers, advance verified
   items, recheck boundaries and continue automatically to task terminal. Compaction retains Porting
   ownership/current equivalence state. Stop only for explicit stepwise/pause intent
   or real blockers/boundaries. Verification/equivalence results stay in chat.

## User-facing output

Start directly with `迁移结论:` (no preamble); omit empty optionals. Same-turn Analysis/Coding chains emit one final `迁移结论:` response only (fold delegated evidence in; never stack `需求结论`/`完成内容`).

```text
迁移结论: <一句话结论与可否推进>
本次迁移: <源 -> 目标与有界范围>
如何确认成功: <等价验证方法与覆盖边界>
需要注意:        # only when relevant
需要确认:        # only when blocked; include recommendation + fallback
当前进度: <基于状态的完成/剩余计数>   # goal/persisted only
下一步: <后续动作>
开发记录: <req-process + cross-process 路径> # goal/persisted only
```

## Hard rules

- Req-process owns scope/AC; cross-process owns magnitude/equivalence/progress.
- Missing/stale linked state: do not port. Never assume `.gitignore` choice.
