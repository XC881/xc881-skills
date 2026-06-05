---
name: xc881-coding-skills
description: 'Use for serious coding tasks, bug fixes, refactors, code review, production changes, architecture decisions after requirements are understood, existing project implementation, legacy project optimization, code splitting, decoupling, maintainability, testability, low-quality-code prevention, minimal diff requests, comment-free code output, or explicit git checkpoint/push. Trigger on xc881, xc881代码工程规范, xc881工程优化, 代码分割, 解耦, 可维护性, 低质量代码, 老项目优化, 高质量代码, 最小改动, 先读代码, 不要乱改, 不要注释, 提交代码, 保存进度, 推送到 GitHub.'
when_to_use: 'Use when the user asks to write, edit, fix, refactor, review, scaffold, or optimize code; when generated or edited code should stay comment-free by default; when the user explicitly asks to create a git checkpoint, commit, save progress, push to GitHub, or write a Conventional Commit message; and whenever xc881 engineering quality, decoupling, maintainability, code splitting, or legacy/new project engineering is requested. If product/project requirements are unclear, or hidden/dependency/consequence requirements must be inferred, use xc881-requirement-analysis before this skill.'
---

# xc881代码工程规范

## What this skill is

xc881-coding-skills is the engineering execution layer.

Use it after requirements are clear enough to support engineering decisions. If the request is mainly about product/project requirement analysis, MVP, user roles, acceptance criteria, hidden dependencies, or implied requirements, use `$xc881-requirement-analysis` first.

This skill focuses on:

- High-Constraint Coding
- No Code Comments
- Git Checkpoint Push
- xc881 Engineering Optimization

## Primary goals

- Do not code from guesses.
- Do not create low-quality code that only works today.
- Keep changes small, readable, and safe.
- Split code by responsibility and reason to change.
- Keep business logic away from framework, database, SDK, HTTP, UI, filesystem, environment variables, real time, randomness, and global mutable state.
- Avoid unnecessary abstraction while still protecting real change points.
- Generate code without comments by default; make the code itself clear.
- Verify before claiming completion.
- Commit or push only when the user explicitly asks.

## Requirement readiness rule

Before coding, check whether the requirement is implementation-ready.

If the task depends on unclear product behavior, missing user roles, hidden dependencies, permission rules, data lifecycle, acceptance criteria, or migration consequences, do not guess silently.

Use or request:

```text
$xc881-requirement-analysis
```

Then use the requirement analysis as the source of truth.

## Reference Index

- [high-constraint-coding-policy.md](./references/high-constraint-coding-policy.md): read for serious implementation, bug fixes, refactors, reviews, minimal-diff work, or regression-sensitive edits.
- [no-code-comments-policy.md](./references/no-code-comments-policy.md): read before generating, editing, patching, scaffolding, regenerating, or showing code when comment policy matters.
- [git-checkpoint-policy.md](./references/git-checkpoint-policy.md): read only when the user explicitly asks to commit, checkpoint, save progress, stage files, or push.
- [quality-bar.md](./references/quality-bar.md): read when deciding whether a patch is good enough to ship or when verification evidence is weak.
- [low-quality-code-rubric.md](./references/low-quality-code-rubric.md): read for reviews, legacy risk ranking, maintainability audits, and low-quality code findings.
- [project-optimization.md](./references/project-optimization.md): read for new project engineering plans, legacy cleanup, staged refactors, and xc881工程优化 reports.

## High-Constraint Coding

Use for:

- bug fixes
- refactors
- code review
- implementation
- production changes
- regression-sensitive edits
- minimal diff requests

Rules:

- bound the task before editing
- read the real implementation path before writing
- state what the relevant current code does before patching
- choose the narrowest maintainable solution
- preserve local style
- avoid speculative abstraction
- verify before reporting success
- if two attempted fixes fail, stop patching and diagnose root cause

## No Code Comments

Use whenever code is generated, edited, patched, scaffolded, regenerated, or shown.

Do not add inline comments, block comments, banner comments, docstrings, JSDoc, XML docs, TODO/FIXME placeholders, or explanatory annotations unless an allowed exception applies.

Allowed exceptions:

- user explicitly asks for comments
- tooling requires directive comments
- repository requires legal headers or generated-file markers
- public API, schema, or framework convention truly depends on documentation comments
- preserving existing comments avoids unrelated churn

## Git Checkpoint Push

Use only when the user explicitly asks to commit, push, save progress, create a checkpoint, stage relevant files, write a Conventional Commit message, or push to GitHub.

Do not commit or push just because a repository exists.

## xc881 engineering workflow

### 1. Bound the task

Before coding, identify:

- exact behavior to add, fix, preserve, review, or optimize
- files/modules likely involved
- affected data flow and public contracts
- assumptions that affect behavior, interfaces, data shape, persistence, security, or user-visible output
- validation target

### 2. Read before writing

For existing code, this is mandatory.

Inspect the real implementation path:

- entry point
- call chain
- affected data flow
- shared helpers and contracts
- adjacent tests
- types, interfaces, schemas, configuration
- local style and naming patterns

### 3. Run the xc881 design gate

For non-trivial coding tasks, output:

```text
xc881 设计门禁：
1. 变化轴：
- ...

2. 职责拆分：
- ...

3. 模块/文件边界：
- ...

4. 依赖方向：
- ...

5. 低质量代码风险：
- ...

6. 避免方式：
- ...

7. 测试策略：
- ...
```

For small tasks, compress it, but still cover boundary, risk, and verification.

### 4. Enforce boundaries

Default dependency direction:

```text
UI / Controller / Route / Framework
        ↓
Application / Use Case
        ↓
Domain / Core Business Logic
        ↓
Ports / Interfaces

Infrastructure / Adapters implement ports.
Core business logic does not directly depend on infrastructure.
```

Keep business/domain logic independent from framework APIs, ORM/database clients, HTTP request/response objects, third-party SDK objects, UI components, filesystem, environment variables, real clock, randomness, and global mutable state.

### 5. Verify before claiming success

Preferred evidence order:

1. targeted tests proving the changed behavior
2. adjacent regression tests
3. typecheck, build, lint, or static analysis
4. manual reproduction steps when automated checks are unavailable

## Final response shape

```text
完成内容：
- ...

验证：
- ...

假设 / 风险：
- ...
```
