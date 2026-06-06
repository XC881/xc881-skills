---
name: xc881-requirement-analysis
description: 'Explicit-only skill. Use only when the user explicitly invokes $xc881-requirement-analysis, says 使用 xc881-requirement-analysis, or clearly asks to enable the xc881需求分析 Skill. It performs requirement understanding before coding: English Spec First normalization, new/existing project requirements, implicit prerequisite/dependency/consequence requirement inference, PRD/MVP scope, user roles, acceptance criteria, risks, and engineering handoff. Do not auto-trigger from ordinary requirement/product/planning keywords.'
when_to_use: 'Use only on explicit invocation of this skill. Do not use implicitly for ordinary mentions of 需求分析, PRD, MVP, 产品需求, 用户故事, or 验收标准. Once explicitly invoked, normalize rough requests when needed, separate explicit/inferred/assumed requirements, define scope, acceptance criteria, risks, and handoff to xc881-coding-skills.'
display_name: "xc881需求分析"
version: "1.1.0"
category: "requirements"
tags:
  - explicit-only
  - requirements
  - requirement-analysis
  - prd
  - mvp
  - acceptance-criteria
  - implicit-requirements
  - xc881
aliases:
  - xc881-requirement-analysis
  - xc881-requirement
  - xc881需求分析
  - 需求分析
---

# xc881 Requirement Analysis

## Role

Explicit-only requirement understanding and engineering-handoff layer.

Activate only when the user explicitly invokes:

```text
$xc881-requirement-analysis
```

or clearly says to use/enable `xc881-requirement-analysis`.

Do not auto-trigger from ordinary requirement, PRD, MVP, user story, product planning, or 需求分析 keywords.

Do not write implementation code. Use `$xc881-coding-skills` after this skill when implementation begins.

## Load policy

`SKILL.md` is the fast path. Read references only when needed:

- `references/english-spec-first-policy.md`: rough, multilingual, ambiguous, scattered, or mixed Chinese-English requests.
- `references/implicit-requirement-inference.md`: hidden prerequisite, dependency, consequence, state, permission, data, failure, audit, migration, NFR, or abuse-case needs.
- `references/existing-project-feature-analysis.md`: adding/changing features in an existing product/codebase.
- `references/requirement-output-contract.md`: exact compact and detailed output contracts.
- `references/requirement-quality-rubric.md`: quality review or strict validation.

## Default output

Compact by default. Ask at most one blocking question. Expand only when user asks, risk is high, or implementation would be unsafe without detail.

## Workflow

1. Confirm explicit invocation.
2. Normalize when needed: `Standard English Spec: Goal / Inputs / Constraints / Output / Process Notes`.
3. Classify context: new project, existing project feature/change, or review only.
4. Capture explicit requirements: `ER-*`.
5. Infer hidden requirements: `IR-*`, with confidence and confirmation need.
6. Define scope: MVP/in-scope, later, out-of-scope, affected areas, must-not-regress.
7. Produce `FR-*`, `NFR-*`, and `AC-*`.
8. Identify P0/P1/P2/P3 risks and unknowns.
9. Create handoff: phases, dependency order, validation targets, minimal safe first milestone.

## Compact output contract

```text
xc881 需求分析：
Context:
Spec:
Explicit:
Inferred:
Scope:
Flows:
Requirements:
Acceptance:
Risks:
Questions:
Handoff to xc881-coding-skills:
```

## Rules

- Explicit invocation only.
- Separate explicit, inferred, and assumed requirements.
- Do not present inferred requirements as confirmed.
- Do not hide dependencies or consequences.
- Do not output code.
- Make acceptance criteria testable.
