---

name: xc881-coding-skills
description: 'Use for serious coding after requirements are clear: implementation, bug fixes, refactors, code review, production changes, existing project optimization, architecture decisions, code splitting, decoupling, maintainability, testability, low-quality-code prevention, minimal diffs, no-code-comments by default, verification, or explicit git checkpoint/push. Trigger on xc881, xc881代码工程规范, xc881工程优化, 代码分割, 解耦, 可维护性, 低质量代码, 老项目优化, 高质量代码, 最小改动, 先读代码, 不要乱改, 不要注释, 提交代码, 保存进度, 推送到 GitHub.'
when_to_use: 'Use when the user asks to write, edit, fix, refactor, review, scaffold, or optimize code; when generated/edited code should stay comment-free by default; when explicit checkpoint/commit/push is requested; or when engineering quality, decoupling, testability, and maintainability matter. If requirements are unclear or implicit dependency/consequence requirements need analysis, use xc881-requirement-analysis first.'
display_name: "xc881代码工程规范"
version: "1.0.0"
category: "coding"
tags:
  - coding
  - refactor
  - code-review
  - decoupling
  - maintainability
  - testability
  - no-comments
  - git-checkpoint
  - xc881
aliases:
  - xc881
  - xc881-coding
  - xc881-engineering
  - xc881代码工程规范
  - xc881工程优化
---

# xc881 Coding Skills

## Role

Engineering execution layer for safe, maintainable code changes.

Use after requirements are clear. If the task is still about PRD, MVP, user roles, hidden requirements, or acceptance criteria, use `$xc881-requirement-analysis` first.

## Load policy

`SKILL.md` is the fast path. Read references only when needed:

- `references/high-constraint-coding-policy.md`: risky edits, bug fixes, refactors, production changes, minimal diff work.
- `references/no-code-comments-policy.md`: before generating or editing code.
- `references/git-checkpoint-policy.md`: only when user explicitly asks to commit/checkpoint/push.
- `references/engineering-quality-rubric.md`: quality review, low-quality code, or weak verification.
- `references/project-optimization.md`: new project engineering after requirements are clear, or legacy optimization.

## Default output mode

Default to compact output.

- Small tasks: apply rules silently, then summarize changes and verification.
- Non-trivial tasks: show a short design gate.
- Detailed reports only when user asks, project risk is high, or legacy optimization is requested.

## Requirement readiness gate

Before coding, check whether the requirement is implementation-ready.

If unclear product behavior, missing permissions, hidden dependencies, state lifecycle, data migration, or acceptance criteria would materially change implementation, use or request:

```text
$xc881-requirement-analysis
```

## Core workflow

1. Bound task:
   - behavior to add/fix/preserve
   - affected files/modules/contracts
   - assumptions
   - verification target

2. Read before writing:
   - entry point
   - call chain
   - data flow
   - adjacent tests/types/config
   - local style

3. Design gate for non-trivial work:

```text
xc881 设计门禁：
变化轴:
职责拆分:
边界/文件:
依赖方向:
低质量风险:
避免方式:
测试策略:
```

4. Implement smallest maintainable change:
   - no unrelated refactor
   - no speculative abstraction
   - preserve local style
   - keep contracts stable unless required
   - avoid circular dependencies
   - push side effects to edges

5. Enforce dependency direction:

```text
UI/Controller/Framework
→ Application/Use Case
→ Domain/Core
→ Ports/Interfaces
Infrastructure implements ports.
```

6. No code comments by default:
   - no inline/block/doc/TODO/FIXME comments unless user, tooling, legal header, generated marker, or public API convention requires it.

7. Verify:
   - targeted tests
   - adjacent regression tests
   - typecheck/build/lint
   - manual steps only when automation is unavailable

8. Git checkpoint only when explicitly requested:
   - inspect status/branch/remotes
   - stage relevant files only
   - Conventional Commit
   - no secrets
   - no force push unless explicitly requested

## Compact final response

```text
完成内容:
验证:
风险/假设:
```

If checkpoint was requested:

```text
Commit:
Branch:
Push:
Remaining changes:
```

## Rules

- Do not code from guessed paths.
- Do not claim success beyond evidence.
- Do not leak framework/database/SDK objects into domain logic.
- Do not hide business rules in UI, SQL, SDK callbacks, or framework handlers.
- Do not add comments by default.
- Do not commit/push unless explicitly requested.
