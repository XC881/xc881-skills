---
name: xc881-requirement-analysis
description: 'Explicit-only. Use only with $xc881-requirement-analysis. Analyze requirements before coding: normalize, split explicit/inferred/assumed, define scope, FR/NFR/AC, risks, handoff. No auto-trigger. No code.'
when_to_use: 'Only explicit invocation. Use for PRD/MVP/scope/user flow/acceptance criteria/new project/existing feature analysis.'
display_name: "xc881需求分析"
version: "2.1.0"
category: "requirements"
tags:
  - explicit-only
  - requirements
  - prd
  - mvp
  - acceptance-criteria
  - xc881
aliases:
  - xc881-requirement-analysis
  - xc881需求分析
  - 需求分析
---

# xc881 Requirement

Explicit only. No code.

Goal:

```text
request → spec → ER/IR → scope → AC → risk → handoff
```

Reference files live under `./references/`.

Reference Index:

- `./references/english-spec-first-policy.md`: rough/mixed request.
- `./references/implicit-requirement-inference.md`: hidden needs.
- `./references/existing-project-feature-analysis.md`: existing change.
- `./references/requirement-output-contract.md`: output.
- `./references/requirement-quality-rubric.md`: strict check.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

Steps:

1. Confirm explicit call.
2. Spec: `Goal / Inputs / Constraints / Output / Notes`.
3. Classify: new / existing / review.
4. List `ER-*`.
5. Infer `IR-*` with confidence.
6. Scope: in / later / out / affected / must-not-regress.
7. Produce `FR-*`, `NFR-*`, `AC-*`.
8. Risks P0-P3; one blocking question max.
9. Hand off.

Output:

```text
xc881 Req:
Spec:
ER:
IR:
Scope:
FR/NFR:
AC:
Risk:
Q:
Handoff:
```

Rules: explicit only; no code; inferred ≠ confirmed; AC must be testable.
