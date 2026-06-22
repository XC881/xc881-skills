---
name: xc881-requirement-analysis
description: 'Explicit-only. Use with $xc881-requirement-analysis or any explicit xc881-scoped requirement intent such as 用xc881分析需求. Analyze requirements before coding: normalize, split explicit/inferred/assumed, define scope, FR/NFR/AC, risks, handoff. May automatically use bounded $xc881-solution-research when technical uncertainty blocks clean requirement judgment. No broad auto-trigger. No code.'
when_to_use: 'Use only when the user explicitly asks xc881 to analyze requirements, scope, MVP, user flow, or acceptance criteria. Automatically use bounded $xc881-solution-research only when technical feasibility or external facts are required to judge the requirement.'
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

Explicit xc881-scoped intent only. No code.

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

1. Confirm explicit xc881 requirement intent.
2. Spec: `Goal / Inputs / Constraints / Output / Notes`.
3. Classify: new / existing / review.
4. If technical uncertainty blocks clean scope or AC judgment, automatically use bounded `$xc881-solution-research`, then continue the same requirement-analysis run without user reconfirmation.
5. List `ER-*`.
6. Infer `IR-*` with confidence.
7. Scope: in / later / out / affected / must-not-regress.
8. Produce `FR-*`, `NFR-*`, `AC-*`.
9. Risks P0-P3; one blocking question max.
10. Hand off.

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

Rules: explicit xc881-scoped intent only; no code; inferred ≠ confirmed; AC must be testable; use `$xc881-solution-research` only for bounded technical uncertainty, not as a default prerequisite; when requirement delegates solution research, the result returns into the same requirement run automatically.
