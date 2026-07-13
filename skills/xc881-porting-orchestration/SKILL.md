---
name: xc881-porting-orchestration
description: 'Intent-routed porting orchestration for 移植, 迁移, 跨语言, 跨项目, port, migrate, or 改写成另一种语言. Classifies magnitude and goal/non-goal, locks long-task boundaries, derives language/architecture risks, delegates implementation, and verifies behavioral equivalence.'
when_to_use: 'Use for cross-language/project porting. Goal tasks require a persisted stop boundary and linked progress ledger before work. Delegate requirement, research, and code work to specialist skills.'
display_name: "xc881移植编排"
version: "1.6.0"
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

Intent-routed thin orchestrator. Delegate; do not re-implement specialists.

## References

- `./references/goal-boundary-contract.md`: magnitude, goal class, hard stop gate.
- `./references/cross-language-understanding.md`: language, architecture, library risks.
- `./references/equivalence-and-idiomatic-porting.md`: equivalence and idiomatic rule.
- `./references/cross-process-plan.md`: persistent porting ledger.
- `./references/porting-output-contract.md`: user-facing output.

Open only the exact relative path for the active branch.

## Delegation

- Boundary/risk/req-process -> `$xc881-requirement-analysis`.
- Deep reading, port, equivalence check -> `$xc881-coding-skills`.
- Language-pair conventions/pitfalls -> `$xc881-solution-research`.

## Workflow

1. Delegate code reading, then classify magnitude and goal/non-goal with evidence using the boundary reference.
2. Goal gate: Requirement persists measurable done criteria, exit conditions, and out-of-scope. Vague/missing boundary -> one blocking question; no porting.
3. Create the <=3,000-char cross-process ledger linked to req-process; never copy scope/AC/boundary. Ask before changing `.gitignore`.
4. Use the understanding reference for language/architecture/library risks; delegate authoritative web research when needed.
5. Continue only an explicit/unambiguous task: read cross-process plus linked req `current.md + current item`; previous needs an explicit evidence link and next waits until advancement. Never scan or read req index by default.
6. Delegate the port and verification to Coding. Behavioral equivalence is hard; target architecture and idioms are subordinate. Use intent fidelity only for true abstract-intent work.
7. After each item, update status/checkpoints and re-check the stop boundary. After context compaction, preserve Porting ownership and equivalence state. If another runnable current item exists, delegate it automatically and continue to task terminal without asking for “continue”. Stop only for explicit stepwise/pause intent or a real blocker/boundary. Report verification/equivalence in chat only.

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

- Goal task without a locked stop boundary: do not start porting.
- Equivalence means behavior, not structure; idiom never overrides correctness.
- No code in this skill output; delegated Coding performs implementation.
- Req-process owns scope/AC; cross-process owns magnitude/equivalence/progress.
- Missing/stale linked state: do not port. Never assume `.gitignore` choice.
