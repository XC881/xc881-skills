---
name: xc881-porting-orchestration
description: 'Explicit-only. Use when the user explicitly invokes $xc881-porting-orchestration or gives explicit xc881-scoped porting/migration intent such as 用xc881移植/用xc881迁移. Orchestrates cross-language and cross-project porting: classify goal vs non-goal task, lock a stop boundary before work (anti-infinite-loop), understand target-language traits and project architecture, derive pre/post porting risks, and verify behavioral equivalence. Thin orchestrator: delegates to $xc881-requirement-analysis, $xc881-coding-skills, and $xc881-solution-research; does not re-implement them. Trigger on xc881, 移植, 迁移, 跨语言, 跨项目, port, migrate, 语言迁移, 项目迁移.'
when_to_use: 'Use to orchestrate porting code across languages or projects after the user explicitly asks. For goal (long-horizon) porting, lock an explicit stop boundary first. Delegate requirement analysis, coding, and research to their skills; do not do their work here.'
display_name: "xc881移植编排"
version: "1.0.0"
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

Explicit xc881-scoped intent only. Thin orchestrator. Delegate; do not re-implement.

Reference files live under `./references/`.

Reference Index:

- `./references/goal-boundary-contract.md`: goal vs non-goal classification and the hard stop-boundary gate.
- `./references/cross-language-understanding.md`: target-language traits, architecture, library mapping, risk derivation.
- `./references/equivalence-and-idiomatic-porting.md`: behavioral-equivalence check and idiomatic-first rule.
- `./references/cross-process-plan.md`: the persistent plan file that anchors progress across context loss.
- `./references/porting-output-contract.md`: output format.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

## Delegation

This skill coordinates; it does not replace the specialists.

- Boundary + risk derivation → `$xc881-requirement-analysis`.
- Deep code understanding + equivalence analysis + the actual port → `$xc881-coding-skills`.
- Language-pair conventions and pitfalls → `$xc881-solution-research` (broad web search).

## Workflow

1. Read & judge magnitude first: read the actual code, do not infer "whole project" from wording. Classify into whole-project / module / feature / logic-slice / abstract-architectural-intent, with evidence. Then classify goal vs non-goal. State both + why. Deep reading delegates to `$xc881-coding-skills`; this skill only consumes and classifies.
2. Hard gate (goal only): before ANY porting action, lock a stop-boundary contract via `$xc881-requirement-analysis`:
   - measurable done-criteria
   - explicit exit conditions
   - out-of-scope list
   If the boundary is vague, STOP and ask one blocking question. Do not start porting.
3. Plan file (hard precondition): write the locked magnitude + boundary + item checklist to `dev-notes/cross-process/<task>.md` in the TARGET project workspace. If `dev-notes/` is absent, create it and ask one blocking question: add to .gitignore or not (user decides; never assume). No current plan file → do not port. See `./references/cross-process-plan.md`.
4. Understand (cross-language): target-language traits, source/target differences, architecture, key libraries + their target-side mapping.
5. Derive risks with requirement-analysis reasoning: behavior, concurrency model, memory model, error handling, ecosystem/library gaps, pre/post porting problems.
6. Research pitfalls: delegate broad web search to `$xc881-solution-research` for the specific language pair / domain.
7. Before any port/reference action: read the plan file and state progress vs plan. It is the single source of truth, not session memory.
8. Port: delegate implementation to `$xc881-coding-skills`. Prefer target-language idioms and strong features over literal transliteration.
9. Verify equivalence via `$xc881-coding-skills`: behavioral equivalence (IO/behavior parity, ported tests, golden comparison), not structural sameness. State consistent / inconsistent + evidence.
10. Iterate (goal): update the plan file (item done/not-done + reason), then re-check the boundary and report progress vs done-criteria + explicit done / not-done.

## Equivalence rule (three layers, order fixed)

1. Hard invariant: behavioral equivalence. Never relaxed.
2. Soft: when the target project already has an architecture, port into it; record departures.
3. Soft: within the above, prefer target-language idioms / strong features over source paradigms.

Idiomatic and architecture give way to correctness. Record each choice: source paradigm -> target feature/architecture -> why better -> evidence it stays equivalent.

Abstract-architectural-intent magnitude only: when no source code is transliterated, equivalence downgrades from IO parity to intent/design fidelity. Mark the downgrade + reason explicitly.

## Output

```text
xc881 Porting:
Magnitude: whole-project / module / feature / logic-slice / abstract-intent + evidence
Task class: goal / non-goal + why
Stop boundary: done-criteria / exit / out-of-scope
Understanding: language diff / architecture / library map
Risks: pre/post porting problems, prioritized
Equivalence: method + consistent/inconsistent + evidence
Progress: vs done-criteria + done/not-done
Handoff:
```

## Hard rules

- Thin orchestrator: delegate to the specialist skills; do not duplicate their logic here.
- Goal task without a locked stop boundary: do not start porting.
- Vague boundary: ask, do not loop.
- Equivalence means behavior, not structure.
- Idiomatic rewrite must not break behavioral equivalence.
- No idiomatic over-engineering: use target features for real correctness/readability/performance gains, not to show off.
- No code in this skill's own output; code work happens in the delegated coding run.
- Plan file is the single source of truth: read before acting, update after each iteration. A stale plan is worse than none.
- No current plan file: do not port. dev-notes/.gitignore choice is the user's; never assume.
