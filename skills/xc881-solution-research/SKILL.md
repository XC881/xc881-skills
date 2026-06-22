---
name: xc881-solution-research
description: 'Explicit-only. Use with $xc881-solution-research or any explicit xc881-scoped technical-research intent such as 用xc881调研, or as bounded delegated research from an explicitly invoked $xc881-source-article-style or $xc881-requirement-analysis run. Research technical feasibility and external technical facts before coding: normalize idea, infer research questions, search authoritative sources, compare options, recommend, hand off. No broad auto-trigger. No code.'
when_to_use: 'Use for web-backed technical research only when the user explicitly asks xc881 to research feasibility, compare options, inspect docs/standards/advisories, or judge a technical route. Enter requirement analysis only when the user asks for both in one request, invokes requirement after solution output, or the current run was delegated by requirement-analysis.'
display_name: "xc881技术方案联网调研"
version: "2.1.0"
category: "solution-research"
tags:
  - explicit-only
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

Explicit xc881-scoped intent only. No code.

Delegated explicit: an active `$xc881-source-article-style` run may use this skill automatically for one bounded unexplained term/concept that affects article understanding. An active `$xc881-requirement-analysis` run may use this skill automatically for bounded technical uncertainty that affects requirement judgment, and the result should return to that same requirement run automatically.

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

1. Confirm explicit xc881 technical-research intent.
2. Spec: `Goal / Inputs / Constraints / Unknowns / Output`.
3. Make explicit + inferred `RQ-*`.
4. Infer stack candidates.
5. Search targeted primary sources.
6. Compare 2-4 options.
7. Pick only if evidence is enough.
8. Hand off.

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

Rules: explicit xc881-scoped intent only; no code; papers first for principles; cite only useful sources; fact ≠ inference ≠ recommendation; do not default into requirement analysis unless the user asks for both in one request or invokes requirement after solution output; requirement-delegated research may return to the same requirement run automatically.
