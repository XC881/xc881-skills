---

name: xc881-requirement-analysis
description: 'Use for explicit requirement analysis before coding: rough/multilingual request normalization, new project requirements, existing project feature requirements, implicit prerequisite/dependency/consequence requirement inference, PRD, MVP, user roles, user flows, functional and non-functional requirements, acceptance criteria, risks, unknowns, and engineering implementation planning. Trigger on 需求分析, 需求理解, PRD, MVP, 用户角色, 用户流程, 验收标准, 隐含需求, 依赖需求, 后果需求, 增量需求, 已有项目新增功能, 工程实施方案, 技术方案, 先别写代码, 先分析需求.'
when_to_use: 'Use when the user wants requirements understood before implementation, especially for a new project idea, an existing-project feature/change, unclear product behavior, hidden dependency/consequence requirements, MVP boundaries, acceptance criteria, or an engineering handoff to xc881-coding-skills. Do not use for ordinary coding unless requirements need clarification first.'
display_name: "xc881需求分析"
version: "1.0.0"
category: "requirements"
tags:
  - requirements
  - requirement-analysis
  - prd
  - mvp
  - acceptance-criteria
  - implicit-requirements
  - project-planning
  - xc881
aliases:
  - xc881-requirement
  - xc881-requirements
  - 需求分析
  - 需求理解
  - PRD
  - MVP
---

# xc881 Requirement Analysis

## Role

Turn a raw idea or feature request into a compact, verifiable, engineering-ready requirement package.

Do not write implementation code. Do not start with folder structure.

Use `$xc881-coding-skills` after this skill when implementation begins.

## Load policy

`SKILL.md` is the fast path. Read references only when needed:

- `references/english-spec-first-policy.md`: rough, multilingual, ambiguous, scattered, or mixed Chinese-English requests.
- `references/implicit-requirement-inference.md`: hidden prerequisite, dependency, consequence, state, permission, data, failure, audit, migration, NFR, or abuse-case needs.
- `references/existing-project-feature-analysis.md`: adding/changing features in an existing product/codebase.
- `references/requirement-output-contract.md`: exact compact and detailed output contracts.
- `references/requirement-quality-rubric.md`: quality review or strict validation.

## Default output mode

Default to compact output. Expand only when the user asks for detail, the requirement is risky, or implementation would be unsafe without detail.

Compact output target:

- 8-14 bullets or sections
- IDs instead of prose where possible
- no repeated explanations
- only one clarification question when necessary

## Workflow

1. Classify context:
   - New project
   - Existing project feature/change
   - Requirement review only

2. Normalize when needed:
   - `Standard English Spec: Goal / Inputs / Constraints / Output / Process Notes`
   - Keep names, APIs, files, technologies, metrics, deadlines exactly.
   - Do not invent missing requirements.

3. Capture explicit requirements:
   - `ER-001`, `ER-002`
   - Only what the user actually stated.

4. Infer hidden requirements:
   - `IR-001`
   - Mark as inferred, with confidence and confirmation need.
   - Check prerequisite, dependency, consequence, state, permission, data, failure, audit, notification, migration, NFR, abuse-case.

5. Define scope:
   - New project: MVP / later / out-of-scope.
   - Existing project: in-scope change / affected areas / must-not-regress / migration or rollout.

6. Produce requirements:
   - `FR-*`: functional behavior.
   - `NFR-*`: security, privacy, reliability, performance, compatibility, accessibility, maintainability, observability, cost, compliance, retention when relevant.
   - `AC-*`: acceptance criteria, preferably Given/When/Then.

7. Identify risks and unknowns:
   - P0: safety, security, legal, payment, data loss, production-blocking.
   - P1: MVP success, compatibility, architecture-changing.
   - P2: important UX/product uncertainty.
   - P3: minor detail.

8. Create engineering handoff:
   - phases
   - dependency order
   - validation targets
   - minimal safe first milestone
   - handoff notes for `$xc881-coding-skills`

## Compact output contract

For most requests:

```text
xc881 需求分析：
Context:
Spec: ...
Explicit: ER-001...
Inferred: IR-001...
Scope: MVP/In-scope, Out-of-scope
Flows: ...
Requirements: FR-001..., NFR-001...
Acceptance: AC-001...
Risks: P0/P1/P2/P3...
Questions: max 1 blocking question
Handoff to xc881-coding-skills: ...
```

For existing projects, include:

```text
Affected: UI / API / Domain / Data / Permissions / Integrations / Tests
Must not regress:
Migration / rollout:
```

## Rules

- Separate explicit, inferred, and assumed requirements.
- Do not present inferred requirements as confirmed.
- Do not hide dependencies or consequences.
- Do not expand MVP without marking it as inferred or later.
- Do not ask many questions; ask one blocking question or proceed with assumptions.
- Do not output code.
- Make acceptance criteria testable.
- Make the engineering handoff specific enough for implementation.
