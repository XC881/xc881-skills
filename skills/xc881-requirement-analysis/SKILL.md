---
name: xc881-requirement-analysis
description: 'Intent-routed. Use with $xc881-requirement-analysis or clear requirement/triage intent such as 分析需求, 定范围, 写验收标准, 分诊 issue/PR, or 拆 PRD issues. Analyze requirements before coding: normalize, split explicit/inferred/assumed, define scope, FR/NFR/AC, risks, tracker handoff. May automatically use bounded $xc881-solution-research when technical uncertainty blocks clean requirement judgment. No code.'
when_to_use: 'Use when the user intent is requirement analysis, scope/MVP/user-flow/acceptance-criteria work, issue tracker triage, Agent Brief, or PRD-to-issues splitting. Automatically use bounded $xc881-solution-research only when technical feasibility or external facts are required to judge the requirement.'
display_name: "xc881需求分析"
version: "2.1.0"
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
- `./references/requirement-output-contract.md`: output.
- `./references/requirement-quality-rubric.md`: strict check.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

Steps:

1. Confirm requirement/triage intent from direct invocation, wording, or delegated context.
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

Rules: route only on requirement/triage intent; no code; inferred ≠ confirmed; AC must be testable; use `$xc881-solution-research` only for bounded technical uncertainty, not as a default prerequisite; when requirement delegates solution research, the result returns into the same requirement run automatically.
