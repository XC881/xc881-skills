---
name: xc881-coding-skills
description: 'Use for serious coding after requirements are clear: implementation, bug fixes, refactors, review, production changes, architecture decisions, code quality standards, modular structure, code splitting, decoupling, maintainability, testability, low-quality-code prevention, surgical/minimal diffs, anti-overengineering, core-difficulty-only comments, verification, high-performance/high-efficiency optimization, or explicit git checkpoint/push. Trigger on xc881, xc881代码工程规范, xc881工程优化, 代码规范, 非屎山代码, 稳定代码, 可维护代码, 哲学结构, 逻辑模块化, 代码分割, 解耦, 低质量代码, 高性能, 高效率, 高优化, 最小改动, 先读代码, 不要乱改, 核心难点注释, 提交代码, 保存进度, 推送到 GitHub.'
when_to_use: 'Use for coding execution after requirements are clear. Apply the xc881 code quality standard for non-trivial implementation, refactor, review, optimization, or code-quality requests. Apply high-constraint policy for risky edits, bug fixes, production changes, surgical changes, minimal diffs, and anti-overengineering. In performance mode, optimize only with explicit requirement, measured bottleneck, or clear hot path. If requirements are unclear or hidden dependencies need analysis, use explicit xc881-requirement-analysis first.'
display_name: "xc881代码工程规范"
version: "1.2.0"
category: "coding"
tags:
  - coding
  - code-quality
  - refactor
  - decoupling
  - maintainability
  - testability
  - anti-overengineering
  - performance
  - git-checkpoint
  - xc881
aliases:
  - xc881
  - xc881-coding
  - xc881-engineering
  - xc881代码工程规范
  - xc881工程优化
  - 代码规范
  - 非屎山代码
---

# xc881 Coding Skills

## Role

Engineering execution layer for safe, stable, maintainable code changes.

Use after requirements are clear. If the task is about PRD, MVP, users, hidden requirements, or acceptance criteria, use explicit `$xc881-requirement-analysis` first.

## Load policy

`SKILL.md` is the fast path.

Reference files live under `./references/`.

Reference Index:

- `./references/xc881-code-quality-standard.md`: non-trivial coding, review, refactor, performance mode, or code-quality/代码规范/非屎山代码 requests.
- `./references/high-constraint-coding-policy.md`: risky edits, bug fixes, production changes, surgical changes, minimal diff work, or anti-overengineering risk.
- `./references/no-code-comments-policy.md`: before generating or editing code.
- `./references/git-checkpoint-policy.md`: only when user explicitly asks to commit/checkpoint/push.
- `./references/engineering-quality-rubric.md`: low-quality code review or weak verification.
- `./references/project-optimization.md`: legacy optimization or new project engineering after requirements are clear.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

## Default output

Compact by default.

- Small task: apply rules silently, report changes + verification.
- Non-trivial task: show compact design gate.
- Detailed report only when requested, risk is high, performance trade-off exists, or legacy optimization is requested.

## Workflow

1. Requirement gate: use explicit `$xc881-requirement-analysis` if behavior, permissions, hidden dependencies, lifecycle, migration, or acceptance criteria are unclear.
2. Read before writing: entry point, call chain, data flow, tests/types/config, local style.
3. Bound task: behavior, files/contracts, assumptions, one verifiable success target.
4. Apply surgical-change guard:
   - do not assume; surface behavior-changing ambiguity
   - no requested-unrelated feature/flexibility/abstraction
   - every changed line traces to request, evidence, verification, or direct cleanup caused by this change
   - clean only new orphans; mention old dead code, do not delete
5. Apply code quality standard: correctness, stability, modularity, testability, edge isolation, core-difficulty-only comments.
6. Compact design gate for non-trivial work:

```text
xc881 设计门禁：
变化轴:
成功标准:
职责拆分:
边界/文件:
依赖方向:
代码质量风险:
过度设计风险:
性能模式: yes/no
测试策略:
```

7. Implement smallest maintainable change:
   - no unrelated refactor
   - no speculative or single-use abstraction
   - preserve local style
   - avoid circular dependencies
   - make invalid states difficult to represent
   - keep side effects at edges
8. Dependency direction:

```text
UI/Controller/Framework
→ Application/Use Case
→ Domain/Core
→ Ports/Interfaces
Infrastructure implements ports.
```

9. Comments:
   - no routine comments
   - comment only core difficulty: algorithm, concurrency/memory invariant, security assumption, performance trade-off, protocol quirk, migration hazard, intentionally unusual code
10. Performance mode:
   - activate only when requested/measured/hot-path
   - preserve correctness and safety
   - prefer algorithm/data-structure gains before micro-optimization
   - localize complexity
   - test/benchmark when practical
   - report trade-off
11. Verify before success. Commit/push only when explicitly requested.

## Final response

```text
完成内容:
验证:
风险/假设:
```

If performance mode was used:

```text
性能取舍:
验证/基准:
```

If checkpoint was requested:

```text
Commit:
Branch:
Push:
Remaining changes:
```

## Hard rules

- Do not code from guessed paths.
- Do not claim success beyond evidence.
- Do not leak framework/database/SDK/UI objects into domain logic.
- Do not hide business rules in UI, SQL, SDK callbacks, or framework handlers.
- Do not sacrifice correctness, security, or bounded complexity for performance.
- Do not improve adjacent code unless required.
- Do not commit/push unless explicitly requested.
