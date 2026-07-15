---
name: xc881-solution-research
description: 'Primary owner for web-backed technical research: feasibility, option decisions, standards/advisories, and stale external facts. Use when external evidence is the outcome or a bounded delegate is blocked; ordinary explanations and incidental terms stay with the current owner.'
when_to_use: 'Use for external technical evidence or decisions. Single-fact checks skip option comparison; delegated research returns to its owner.'
display_name: "xc881技术方案联网调研"
version: "2.3.0"
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

Intent-routed external-evidence owner. Direct calls select it; implicit use
requires the primary outcome in the description. Incidental terms stay with the
base/current owner. Run only the needed branch. No code.

Delegated use: an active `$xc881-source-article-style` run may use this skill automatically for one bounded unexplained term/concept that affects article understanding. An active `$xc881-requirement-analysis` run may use this skill automatically for bounded technical uncertainty that affects requirement judgment, and the result returns to that same owner automatically, including after context compaction.

Goal:

```text
idea → spec → RQ → evidence → options → pick → handoff
```

Reference files live under `./references/`.

Reference Index:

- `./references/english-spec-and-research-questions.md`: rough idea/RQ.
- `./references/source-priority-policy.md`: source trust/conflict.
- `./references/paper-first-policy.md`: principles.
- `./references/tech-stack-feasibility-policy.md`: option compare.
- `./references/solution-output-contract.md`: output.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

Steps:

1. Confirm technical-research intent from direct invocation, wording, or delegated context.
2. Spec: `Goal / Inputs / Constraints / Unknowns / Output`.
3. Make only the explicit/inferred `RQ-*` needed for the decision.
4. Infer stack candidates.
5. Search the smallest useful set of primary sources.
6. If delegated from a req-process Artifact, write bounded evidence under its `evidence/` directory.
7. Fact check: report evidence, impact, risk, and handoff; do not invent options.
8. Decision: compare 2-4 real options and pick only when evidence is enough.

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

Rules: route only on external technical evidence/decision intent; no code; papers
first for principles; cite only used sources; fact ≠ inference ≠ recommendation;
do not default into Requirement unless requested or delegated. Delegated research
returns to the same owner automatically.
