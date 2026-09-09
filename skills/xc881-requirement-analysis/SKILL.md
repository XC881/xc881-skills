---
name: xc881-requirement-analysis
description: 'Primary owner for requirements, scope, acceptance criteria, PRDs, and issue/PR triage. Separate explicit/inferred needs, persist task queues when warranted, and delegate only blocking research or reads. Implementation detail alone is not requirement intent.'
when_to_use: 'Use for scope/AC/tracker deliverables. Persist only when the gate passes; delegate bounded uncertainty, then resume the same owner.'
display_name: "xc881需求分析"
version: "2.10.1"
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

Intent-routed scope/AC/tracker owner, not incidental implementation uncertainty.
Direct calls select it. No code; maintain requirement artifacts here.

## Reference Routes

- `./references/english-spec-first-policy.md`: normalize a rough/mixed request.
- `./references/implicit-requirement-inference.md`: missing prerequisite/decision affects AC.
- `./references/existing-project-feature-analysis.md`: existing behavior/contract changes.
- `./references/issue-tracker-triage.md`: tracker state, Agent Brief, or operations.
- `./references/requirement-process-artifact.md`: artifact identity, persistence gate, queue update/resume.
- `./references/design-system-artifact.md`: explicit or reusable visual contract.
- `./references/requirement-output-contract.md`: persisted summary, tracker add-on, or blocking question.
- `./references/requirement-quality-rubric.md`: requested review or unresolved scope/AC quality risk.

Route by intent each turn. Full supplied bodies count; names/paths/markers do not.
Reuse in-context rules; read needed exact paths automatically only for missing
rules, known changes or requested rereads. Higher-priority invocation rules win.

## Workflow

1. Classify new / existing / review. Reuse scope/version-matched Spec/ER/IR and
   evidence; fill scope/AC gaps. Spec:
   `Goal / Inputs / Constraints / Output / Notes`.
2. Resolve explicit/unambiguous conversational artifacts first. Bounded candidate
   search requires likely persistence/handoff; chat-only work never scans.
   Reuse one semantic match, ask once for multiple, or apply the gate if none.
3. For missing project facts, perform a simple exact/local/low-risk read here, or delegate a complex/tracked `read` to `$xc881-coding-skills` using task+project complexity.
   External uncertainty blocking scope/AC goes to `$xc881-solution-research`.
   Send question/evidence/permissions; receive needed anchors, uncertainty and
   next step. Resume without repeating discovery.
4. Produce `ER/IR`, scope, `FR/NFR/AC`, and P0-P3 risks. Link AC to needs and
   observable results; inferred is not confirmed. Ask one blocking product
   decision max, with recommendation/fallback; discover facts instead of asking.
5. If the artifact gate passes, create dependency-aware vertical queue items for
   Coding; otherwise use a self-contained chat contract. Reused artifacts
   preserve history, append IDs after the tail, and reopen from the first new item.
   Visual contracts failing their gate stay in the current Design Read.
   Persist verification plans and queue state, never results/logs.
6. Before artifact creation, reopening, or checkpointing, derive the complete
   linked write from its template and apply one coherent patch. Validators are
   explicit audit/repair or repository/CI tools, not normal authoring or
   handoff loops. Outside requirement artifact maintenance, hand every write and selected complex/tracked read
   to Coding with exact artifact/current/next/blockers, or the chat-only contract.
7. Queued implementation continues to task terminal; context compaction resumes
   the same owner/current automatically. Bounded delegates return here;
   no second invocation or per-item “continue” unless explicit stepwise/pause intent
   or a real blocker. Persisted progress is authoritative over chat.

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

Persist Spec/ER/IR/Scope/FR/NFR/AC/Risk; summarize decisions in chat. Chat-only output
is self-contained. Omit empty headings.
