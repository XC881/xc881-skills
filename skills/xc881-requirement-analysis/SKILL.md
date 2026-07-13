---
name: xc881-requirement-analysis
description: 'Intent-routed. Use with $xc881-requirement-analysis or clear requirement/triage intent such as 分析需求, 定范围, 写验收标准, 分诊 issue/PR, or 拆 PRD issues. Normalize requirements, separate explicit/inferred/assumed needs, define scope/FR/NFR/AC/risks, and hand off. Persist non-trivial work as a resumable queue under dev-notes/req-process. May delegate bounded technical uncertainty to $xc881-solution-research. No code.'
when_to_use: 'Use for requirement analysis, scope/MVP/user-flow/acceptance criteria, issue tracker triage, Agent Brief, or PRD-to-issues splitting. Apply the requirement-artifact gate when documentation preference is unstated. Use bounded $xc881-solution-research only when technical feasibility or external facts block judgment.'
display_name: "xc881需求分析"
version: "2.9.0"
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

Intent-routed requirement analysis. Direct `$xc881-requirement-analysis` calls and clear requirement/triage intent both trigger. No code.

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
4. Before the artifact gate, resolve whether this changes an existing requirement: prefer an explicit path or one unambiguous conversational artifact; otherwise run the bounded candidate-path search, read only plausible matches, and compare goal/authority semantically. Reuse one match, ask one selection question for multiple matches, or apply the gate only when none match.
5. If technical uncertainty blocks scope or AC judgment, use bounded `$xc881-solution-research`, then continue without user reconfirmation.
6. If project code/test/config must be inspected, apply the task+project complexity gate: perform a simple exact/local/low-risk read here, or delegate a complex/tracked `read` to `$xc881-coding-skills`, then resume from evidence.
7. Produce `ER/IR`, scope, `FR/NFR/AC`, and P0-P3 risks; one blocking question max.
8. For a new artifact, create dependency-aware vertical queue items self-contained for Coding. For a reused artifact, preserve accepted history, append IDs after the tail, reopen terminal state to `ready`, and set previous/current/next to old-tail/first-new/second-new. Persist verification plans and queue state, never verification results/logs.
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
