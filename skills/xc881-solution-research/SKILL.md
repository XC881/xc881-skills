---
name: xc881-solution-research
description: 'Primary owner for web-backed technical research: feasibility, option decisions, standards/advisories, and stale external facts. Use when external evidence is the requested outcome. Ordinary explanations and incidental terms stay with the current owner.'
when_to_use: 'Use when external evidence is the requested outcome. Single-fact checks skip option comparison; delegated research returns to its owner.'
display_name: "xc881技术方案联网调研"
version: "2.3.1"
category: "solution-research"
tags:
  - intent-routing
  - web-research
  - solution-research
  - feasibility
  - papers
  - tech-stack
  - xc881
aliases:
  - xc881-solution-research
  - xc881-tech-research
  - xc881技术调研
---

# xc881 Solution Research

Intent-routed external-evidence owner; direct calls select it. Incidental terms
stay with the current owner. No code; bounded delegates return to their owner.

## Reference Routes

- `./references/english-spec-and-research-questions.md`: rough request or missing RQ.
- `./references/source-priority-policy.md`: source/version/conflict checks or evidence artifacts.
- `./references/paper-first-policy.md`: principle/algorithm evidence.
- `./references/tech-stack-feasibility-policy.md`: real implementation choices.
- `./references/solution-output-contract.md`: artifact or specialist handoff details.

Route by intent each turn. Full supplied bodies count; names/paths/markers do not.
Reuse in-context rules; read needed exact paths automatically only for missing
rules, known changes or requested rereads. Higher-priority invocation rules win.

## Workflow

1. Classify fact check / option decision. Reuse spec/RQ; add `RQ-*` only for
   decision-relevant goals, constraints and unknowns.
2. Reuse scope/version/freshness-matched citations. Search missing, conflicting or
   stale claims only, using the smallest useful primary-source set.
3. Fact check: evidence/impact/risk/handoff; do not invent options. Decision:
   compare viable choices on binding constraints, explain exclusions and require
   evidence before picking.
4. Stop when blocking RQs support the decision. Retain consequential uncertainty;
   insufficient evidence returns a blocker/next check, not aimless expansion.
5. Put req-process-delegated findings in the supplied Artifact's `evidence/`.
   Return needed claims/citations or path, impact, uncertainty and next action to
   the same owner. Context compaction resumes that RQ/evidence.

Output:

```text
xc881 Solution:
Spec:
RQ:
Evidence:
Options:
Pick:
Risk:
Handoff:
```

`Options` and `Pick` are decision-only; omit them for a single-fact check.

Papers first for principles; cite used sources; fact ≠ inference ≠ recommendation.
Do not default into Requirement unless requested or delegated.
