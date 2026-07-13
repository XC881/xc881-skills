---
name: xc881-solution-research
description: 'Intent-routed. Use with $xc881-solution-research or clear technical-research intent such as 调研技术方案, 选技术栈, 比较方案, 查官方资料, or bounded delegated research from $xc881-source-article-style or $xc881-requirement-analysis. Research technical feasibility and external technical facts before coding: normalize idea, infer research questions, search authoritative sources, compare options, recommend, hand off. No code.'
when_to_use: 'Use for web-backed technical research when the user intent is feasibility research, option comparison, docs/standards/advisory inspection, stale external fact checking, or technical-route judgment. Enter requirement analysis only when the user asks for both in one request, invokes requirement after solution output, or the current run was delegated by requirement-analysis.'
display_name: "xc881技术方案联网调研"
version: "2.2.0"
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

Intent-routed technical research. Direct `$xc881-solution-research` calls and clear research intent both trigger. No code.

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
3. Make explicit + inferred `RQ-*`.
4. Infer stack candidates.
5. Search targeted primary sources.
6. If delegated from a req-process Artifact, write bounded evidence under its `evidence/` directory.
7. Compare 2-4 options.
8. Pick only if evidence is enough, then hand off.

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

Rules: route only on technical-research intent; no code; papers first for principles; cite only useful sources; fact ≠ inference ≠ recommendation; do not default into requirement analysis unless the user asks for both in one request or invokes requirement after solution output; requirement-delegated research may return to the same requirement run automatically.
