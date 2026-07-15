---
name: xc881-requirement-analysis
description: 'Primary owner for requirements, scope, acceptance criteria, PRDs, and issue/PR triage. Separate explicit/inferred needs, persist task queues when warranted, and delegate only blocking research or reads. Implementation detail alone is not requirement intent.'
when_to_use: 'Use for scope/AC/tracker deliverables. Persist only when the gate passes; delegate bounded uncertainty, then resume the same owner.'
display_name: "xc881需求分析"
version: "2.10.0"
category: "requirements"
tags:
  - intent-routing
  - requirements
  - prd
  - mvp
  - acceptance-criteria
  - issue-triage
  - tracker
  - xc881
aliases:
  - xc881-requirement-analysis
  - xc881需求分析
  - 需求分析
  - xc881分诊
  - xc881拆issue
---

# xc881 Requirement

Intent-routed requirement owner. Direct calls select it; implicit use requires
scope/AC/tracker as the primary outcome. Incidental implementation uncertainty
stays with the base/current owner. Run only the needed branch. No code.

Goal:

```text
request → spec → ER/IR → scope → AC → risk → handoff
```

Reference files live under `./references/`.

Reference Index:

- `./references/english-spec-first-policy.md`: rough/mixed request.
- `./references/implicit-requirement-inference.md`: hidden needs.
- `./references/existing-project-feature-analysis.md`: existing change.
- `./references/issue-tracker-triage.md`: issue/PR/PRD tracker state, Agent Brief, out-of-scope, and tracker ops.
- `./references/requirement-process-artifact.md`: artifact gate, req-process queue, resume/update protocol.
- `./references/requirement-output-contract.md`: output.
- `./references/requirement-quality-rubric.md`: strict check.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

Steps:

1. Confirm requirement/triage intent from direct invocation, wording, or delegated context.
2. Spec: `Goal / Inputs / Constraints / Output / Notes`.
3. Classify: new / existing / review.
4. Resolve an explicit or unambiguous conversational artifact first. Run bounded
   candidate-path search only when persistence or implementation handoff is likely;
   clearly chat-only work does not scan req-process. Reuse one semantic match, ask
   once for multiple matches, or apply the gate when none match.
5. If technical uncertainty blocks scope or AC judgment, use bounded `$xc881-solution-research`, then continue without user reconfirmation.
6. If project code/test/config must be inspected, apply the task+project complexity gate: perform a simple exact/local/low-risk read here, or delegate a complex/tracked `read` to `$xc881-coding-skills`, then resume from evidence.
7. Produce `ER/IR`, scope, `FR/NFR/AC`, and P0-P3 risks; one blocking question max.
8. If the artifact gate passes, create dependency-aware vertical queue items for
   Coding. Otherwise keep a compact self-contained chat contract. Reused artifacts
   preserve history, append IDs after the tail, and reopen from the first new item.
   Persist verification plans and queue state, never results/logs.
9. Keep the full structured analysis in req-process when persisted, then report a compact human-readable summary. Chat-only work must remain self-contained.
10. Validate, then hand every write and selected complex/tracked read to Coding with exact artifact/current/next/blockers. A queued implementation continues across items; after context compaction it resumes the same owner/current automatically. Active ownership returns to this requirement run after bounded delegation, and no second invocation or per-item “continue” is needed unless the user requests stepwise control or a real blocker occurs.

User-facing output:

```text
需求结论:
这次会做:
完成标准:
需要注意:        # only when relevant
需要确认:        # only when blocked; include recommendation + fallback
下一步:
开发记录:
```

Rules: route only on requirement/triage intent; no code; inferred ≠ confirmed; AC must be testable; persisted documents retain Spec/ER/IR/Scope/FR/NFR/AC/Risk while chat translates decisions into plain language; omit irrelevant empty headings; persisted progress is authoritative over chat; use `$xc881-solution-research` only for bounded technical uncertainty, and return its result to the same requirement run.
