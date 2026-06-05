---
name: xc881-requirement-analysis
description: 'Use for explicit product/project requirement understanding before coding, including English Spec First normalization for rough, multilingual, ambiguous, scattered, or mixed Chinese-English requests, new project analysis, existing project feature analysis, PRD creation, MVP scoping, user roles, user journeys, acceptance criteria, non-functional requirements, implicit/derived requirement discovery, dependency and consequence analysis, risk analysis, requirement quality review, and engineering implementation planning. Trigger on 需求分析, 需求理解, 产品需求, 项目需求, 新项目需求, 已有项目新增功能, 增量需求, 隐含需求, 依赖需求, 后果需求, PRD, MVP, 用户故事, 用户角色, 用户流程, 验收标准, 功能边界, 非功能需求, 工程实施方案, 技术方案, 先别写代码, 先分析需求, 把想法变成方案.'
when_to_use: 'Use when the user explicitly asks to analyze or clarify product/project requirements before coding; when the request is rough, multilingual, ambiguous, scattered, emotional, or needs a precise English working specification before requirement analysis; when a new product idea needs scope, personas, user flows, MVP boundaries, acceptance criteria, risks, assumptions, or an implementation plan; when an existing project needs a new feature analyzed against current behavior, constraints, integrations, data model, compatibility, and migration impact; or when the user wants implicit prerequisite, dependency, or consequence requirements inferred before handoff to xc881-coding-skills. Do not use for ordinary code edits unless the user asks to revisit requirements first.'
---

# xc881需求分析与工程实施方案

## What this skill is

xc881-requirement-analysis turns unclear product or project intent into a reliable, testable, engineering-ready requirement package.

It supports two major requirement-analysis modes:

1. New project mode: analyze a product idea or project from zero.
2. Existing project feature mode: analyze a new feature or change inside an existing codebase/product.

It also performs implicit requirement inference: when the user mentions A and B, but A/B logically require C, this skill should identify C as an inferred requirement, dependency, constraint, or consequence.

This is not a coding skill. Do not write implementation code. Produce a requirement and engineering-planning handoff for `$xc881-coding-skills`.

## Core philosophy

Do not jump from idea to architecture or code.

Move in this order:

```text
raw idea / feature request
→ English Spec First normalization when needed
→ context classification
→ explicit requirements
→ implicit and derived requirements
→ product and user analysis
→ acceptance criteria
→ risks and unknowns
→ engineering implementation plan
→ handoff to xc881-coding-skills
```

Requirements are good only when they are understandable, bounded, consistent, testable, traceable to value, and detailed enough to support design.

## English Spec First normalization

Use this step before deeper requirement analysis when the user's request is rough, multilingual, mixed Chinese-English, ambiguous, emotional, scattered, or not yet precise enough to analyze.

Output a compact working specification:

```text
Standard English Spec:
Goal:
Inputs:
Constraints:
Output:
Process Notes:
```

Rules:

- Keep the spec compact.
- Preserve file names, APIs, technologies, metrics, deadlines, and named entities exactly.
- Convert vague intent into operational language only when the intent is clear.
- Separate hard requirements from inferred preferences.
- Do not invent requirements to make the spec look complete.
- If missing information materially changes the requirement analysis, ask one concise clarification question.
- If missing information is not blocking, proceed with a labeled assumption.
- Use the English spec as the working contract for the rest of the requirement analysis.
- Respond to the user in their language unless they explicitly ask for English.

This step normalizes language and intent. It does not replace product requirement analysis, implicit requirement inference, acceptance criteria, or engineering planning.

## Requirement context classification

First classify the request:

```text
Requirement Context:
- New project
- Existing project new feature
- Existing project change/refactor with product impact
- Requirement review / clarification only
```

### New project

Use when there is no existing product/codebase or when the user is planning from zero.

Focus on:

- product goal
- target users
- MVP and non-goals
- user journeys
- core entities
- external dependencies
- first milestone
- engineering phases

### Existing project new feature

Use when the user wants to add, adjust, or analyze a feature in an existing project.

Before producing the plan, identify or ask for:

- current product behavior
- existing user roles and permissions
- affected modules/screens/API endpoints
- current data model and states
- existing external integrations
- compatibility and migration constraints
- current tests and release workflow
- what must not regress

If repository files are available, inspect relevant docs/code before making project-specific claims. If files are not available, label project-specific assumptions clearly.

## Implicit requirement inference

When explicit requirements mention A and B, infer unmentioned C requirements when C is necessary for A/B to work safely, consistently, or verifiably.

Treat inferred items as hypotheses until confirmed.

### Inference categories

For every important explicit requirement, check these inference lenses:

1. Prerequisite requirements
   - What must exist before this can work?
   - Example: "team invitation" implies user identity, email delivery, invitation token, expiration, and acceptance flow.

2. Dependency requirements
   - What capability, data, integration, or permission does this depend on?
   - Example: "subscription checkout" implies plan catalog, payment provider, webhook handling, entitlement state.

3. Consequence requirements
   - What downstream behavior happens after this?
   - Example: "cancel subscription" implies access downgrade, invoice history, data retention, and grace period rules.

4. State and lifecycle requirements
   - What states can the object enter?
   - Example: invitation = pending, accepted, expired, revoked.

5. Permission and security requirements
   - Who may do this? Who must not?
   - Example: only workspace owner can remove members; user cannot remove self if sole owner.

6. Data requirements
   - What data must be stored, derived, audited, or deleted?
   - Example: password reset implies reset token hash, expiry, used-at timestamp.

7. Failure and recovery requirements
   - What happens when external services fail?
   - Example: email send failure, payment webhook retry, partial upload.

8. Observability and audit requirements
   - What must be logged or auditable?
   - Example: admin role change implies audit event.

9. Notification requirements
   - Who needs to know when this happens?
   - Example: member removed implies user notification or owner confirmation.

10. Compatibility and migration requirements
   - What existing behavior/data must remain valid?
   - Example: adding roles implies migrating existing users to a default role.

11. Non-functional requirements
   - Security, privacy, reliability, performance, accessibility, scalability, maintainability, portability, cost.

12. Abuse and edge-case requirements
   - How can this be misused?
   - Example: repeated invite spam, brute force reset tokens, duplicate payment webhooks.

### Inferred requirement format

Use this format:

```text
Inferred Requirement:
- ID:
- Derived from:
- Type: prerequisite | dependency | consequence | state | permission | data | failure | observability | notification | migration | non-functional | abuse-case
- Reasoning:
- Confidence: high | medium | low
- Needs confirmation: yes | no
- Acceptance criteria:
```

Do not present inferred requirements as user-confirmed facts.

## Required behavior

When this skill is active:

- Do not write implementation code.
- Do not start with folder structure.
- Normalize rough, multilingual, ambiguous, scattered, or mixed Chinese-English requests with English Spec First before deeper analysis.
- Classify whether this is a new project or existing project feature/change.
- Separate explicit requirements from inferred requirements.
- Separate facts from assumptions.
- Ask at most one concise clarification question if a missing answer materially changes MVP scope, safety, permissions, data model, compatibility, migration, or architecture.
- If missing details are not blocking, proceed with labeled assumptions.
- Convert vague wishes into observable requirements and acceptance criteria.
- Split requirements into atomic items when practical.
- Mark uncertainty explicitly instead of hiding it.
- Produce an engineering implementation plan that can be handed to `$xc881-coding-skills`.

## Workflow

### 0. Normalize the request when needed

If English Spec First is triggered, produce:

```text
Standard English Spec:
Goal:
Inputs:
Constraints:
Output:
Process Notes:
```

Then continue with explicit requirements, inferred requirements, context classification, and acceptance criteria.

### 1. Restate the intent

Briefly restate what the user appears to want.

Include:

- product/project idea or feature request
- context classification
- target outcome
- stated constraints
- what must not be done yet

### 2. Capture explicit requirements

List what the user actually said.

Use:

```text
Explicit Requirements:
- ER-001: ...
- ER-002: ...
```

Do not mix inferred requirements into this section.

### 3. Infer hidden, dependency, and consequence requirements

Use the inference lenses above.

Output:

```text
Inferred / Derived Requirements:
- IR-001: ...
  Derived from: ER-...
  Type:
  Reasoning:
  Confidence:
  Needs confirmation:
```

### 4. Identify stakeholders and users

Define:

- primary users
- secondary users
- administrators or operators
- external systems
- paying customer if different from end user
- stakeholders affected by security, compliance, or operations

If unknown, infer likely roles and label them as assumptions.

### 5. Define problem, goal, and value

Clarify:

- problem being solved
- why it matters
- success outcome
- business or user value
- non-goals

### 6. Define scope

For new projects:

- MVP must-have
- should-have soon
- later / not now
- explicitly out of scope

For existing projects:

- in-scope change
- affected existing behavior
- must-not-regress behavior
- compatibility expectations
- migration or rollout requirements
- out-of-scope cleanup

### 7. Model core user journeys

For each important role, describe the main flow:

```text
Actor:
Goal:
Trigger:
Main path:
Edge cases:
Failure states:
Success outcome:
```

### 8. Extract functional requirements

Write functional requirements as atomic, testable statements.

```text
FR-001: The system shall ...
Source: explicit | inferred
Trace: ER-... / IR-...
Priority: must | should | later
```

### 9. Extract non-functional requirements

Cover only relevant categories:

- functional suitability
- performance efficiency
- compatibility
- usability and accessibility
- reliability
- security and privacy
- maintainability
- portability
- observability and operability
- cost constraints
- compliance
- data retention

Each non-functional requirement should be measurable or at least verifiable.

### 10. Define data and integration boundaries

Define:

- core entities
- ownership of each entity
- lifecycle states
- sensitive data
- external APIs or providers
- import/export needs
- audit/logging needs
- migration concerns

For existing projects, distinguish:

- existing entities likely reused
- new entities likely required
- schema changes
- backward compatibility risks

### 11. Define acceptance criteria

Use:

```text
AC-001:
Given ...
When ...
Then ...
Trace: FR-...
```

or:

```text
When <trigger>, the system shall <observable response>.
Trace: FR-...
```

### 12. Identify risks and unknowns

Rank risks:

- P0: safety, security, legal, payment, data loss, production-blocking risk
- P1: MVP success, compatibility, or architecture-changing risk
- P2: important product or UX uncertainty
- P3: minor detail that can wait

For each:

```text
Risk:
Impact:
Mitigation:
Decision needed:
```

### 13. Produce engineering implementation plan

Only after requirement understanding.

For new projects:

- recommended phases
- capabilities per phase
- dependency order
- validation and testing strategy
- minimal first milestone
- handoff to `$xc881-coding-skills`

For existing project features:

- affected areas to inspect
- likely implementation seams
- migration/compatibility plan
- rollout strategy
- regression test targets
- minimal safe implementation order
- handoff to `$xc881-coding-skills`

## Required output format

### New project output

```text
Standard English Spec:  # only when normalization is needed
Goal:
Inputs:
Constraints:
Output:
Process Notes:

xc881 新项目需求理解分析：

1. 原始意图复述
- ...

2. 需求上下文
- New project

3. 显式需求
- ER-001: ...

4. 隐含 / 推导需求
- IR-001: ...
  Derived from:
  Type:
  Reasoning:
  Confidence:
  Needs confirmation:

5. 产品目标
- ...

6. 目标用户 / 角色
- ...

7. 核心问题与价值
- ...

8. MVP 范围
- ...

9. 暂不纳入范围
- ...

10. 核心用户流程
- ...

11. 功能需求
- FR-001: ...

12. 非功能需求
- Security:
- Performance:
- Reliability:
- Maintainability:

13. 数据实体与外部依赖
- ...

14. 验收标准
- AC-001: Given ... When ... Then ...

15. 风险与未知点
- ...

16. 需要用户确认的问题
- ...

17. 工程实施方案
- Phase 1:
- Phase 2:
- Phase 3:

18. 交给 xc881-coding-skills 的工程输入
- ...
```

### Existing project feature output

```text
Standard English Spec:  # only when normalization is needed
Goal:
Inputs:
Constraints:
Output:
Process Notes:

xc881 既有项目新增功能需求理解分析：

1. 原始意图复述
- ...

2. 需求上下文
- Existing project new feature

3. 显式需求
- ER-001: ...

4. 隐含 / 推导需求
- IR-001: ...
  Derived from:
  Type:
  Reasoning:
  Confidence:
  Needs confirmation:

5. 当前项目上下文假设 / 已知事实
- ...

6. 影响范围
- UI:
- API:
- Domain:
- Data:
- Permissions:
- Integrations:
- Tests:

7. 必须保持不变的现有行为
- ...

8. 功能需求
- FR-001: ...

9. 非功能需求
- ...

10. 数据 / 状态 / 迁移影响
- ...

11. 验收标准
- AC-001: Given ... When ... Then ...

12. 风险与未知点
- ...

13. 需要用户确认的问题
- ...

14. 最小安全实施方案
- Step 1:
- Step 2:
- Step 3:

15. 交给 xc881-coding-skills 的工程输入
- ...
```

For small tasks, compress the format but keep: context, explicit requirements, inferred requirements, acceptance criteria, risks, and implementation handoff.

## Quality bar

A good output must be:

- faithful to the user's stated intent
- explicit about assumptions
- clear about new project vs existing project context
- explicit about hidden/dependency/consequence requirements
- bounded by MVP, in-scope, and out-of-scope items
- written so both product and engineering can understand it
- testable through acceptance criteria
- traceable from explicit/inferred requirements to acceptance criteria and implementation phases
- specific enough for `$xc881-coding-skills` to design and implement later

## Composition with xc881-coding-skills

Use this skill first when product/project requirements are unclear.

Then use `$xc881-coding-skills` for engineering design and implementation.

Recommended handoff:

```text
$xc881-coding-skills
Use the requirement analysis above as the source of truth. Produce the xc881 engineering design gate and implement Phase 1 only.
```

## Strict do nots

Do not:

- write implementation code
- start from directory structure before understanding the product
- invent business rules silently
- treat inferred requirements as confirmed requirements
- ignore requirements implied by dependencies or consequences
- turn every idea into MVP scope
- bury unknowns
- skip acceptance criteria
- skip risks
- treat technical preferences as product requirements unless the user stated them
- produce a vague plan that cannot guide engineering work
