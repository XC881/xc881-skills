---
name: xc881-coding-skills
description: 'Use for any serious coding task, bug fix, refactor, code review, production change, architecture decision, new project setup, legacy project optimization, code splitting, decoupling, maintainability, testability, low-quality-code prevention, minimal diff request, comment-free code output, English spec normalization, or explicit git checkpoint/push. Trigger on xc881, xc881工程优化, xc881代码工程规范, 代码分割, 解耦, 可维护性, 低质量代码, 老项目优化, 新项目工程化, 高质量代码, 最小改动, 先读代码, 不要乱改, 不要注释, 提交代码, 保存进度, 推送到 GitHub.'
when_to_use: 'Use whenever the user asks to write, edit, fix, refactor, review, scaffold, or optimize code; when a request is rough, multilingual, ambiguous, or needs a precise English working spec; when generated or edited code should stay comment-free by default; when the user explicitly asks to create a git checkpoint, commit, save progress, push to GitHub, or write a Conventional Commit message; and whenever xc881 engineering quality, decoupling, maintainability, or legacy/new project optimization is requested.'
---

# xc881代码工程规范

## What this skill is

xc881 is a single integrated engineering-quality skill for AI coding.

It merges these workflows into one standard:

- English Spec First
- High-Constraint Coding
- No Code Comments
- Git Checkpoint Push
- xc881 Engineering Optimization

The merged result is trigger-based, not a rigid checklist that must always print every section.

```text
rough / multilingual / ambiguous request
→ normalize into a compact English working spec

serious coding / bug fix / refactor / review
→ use high-constraint coding discipline

new or edited code output
→ keep code comment-free by default

explicit commit / checkpoint / push request
→ use safe git checkpoint workflow

architecture / decoupling / maintainability / xc881工程优化
→ use xc881 engineering gate and optimization flow
```

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

## Priority order

When tradeoffs appear:

1. correctness
2. safety, security, and data integrity
3. maintainability and clarity
4. decoupling and testability
5. local extensibility
6. performance
7. brevity

Brevity only wins when the result is still obvious to another engineer. Performance optimization needs evidence, an explicit requirement, or a known hot path.

## Trigger map

### English Spec First

Use when:

- the request is rough, scattered, emotional, multilingual, or mixed Chinese-English
- the user asks to think in English first
- the user asks to make requirements professional
- the task needs precise execution before planning or coding

Output:

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
- Separate hard requirements from inferred preferences.
- Remove filler without changing meaning.
- Do not invent requirements to make the spec look complete.
- If missing information materially changes the result, ask one concise question.
- If missing information is not blocking, proceed with a labeled assumption.
- Use the spec as the working contract.
- Respond to the user in their language unless they ask otherwise.

For clear small tasks, this can be internal or compressed.

### High-Constraint Coding

Use for:

- bug fixes
- refactors
- code review
- implementation
- production changes
- regression-sensitive edits
- minimal diff requests
- requests that say `最小改动`, `高质量代码`, `别乱重构`, `先看清楚再改`, `先读代码`, `不要乱改`, or `保证正确`

Rules:

- bound the task before editing
- read the real implementation path before writing
- state what the relevant current code does before patching
- choose the narrowest maintainable solution
- preserve local style
- avoid speculative abstraction
- verify before reporting success
- if two attempted fixes fail, stop patching and diagnose root cause

### No Code Comments

Use whenever code is generated, edited, patched, scaffolded, regenerated, or shown.

Do not add:

- inline comments
- block comments
- banner comments
- docstrings
- JSDoc
- XML docs
- TODO/FIXME placeholders
- explanatory annotations

Prefer:

- clearer names
- smaller helpers
- straightforward control flow
- external explanation in the chat response

Allowed exceptions:

- the user explicitly asks for comments or teaching-style annotated code
- tooling requires directive comments
- the repository requires legal headers or generated-file markers
- a public API, schema, or framework convention truly depends on documentation comments
- removing unrelated existing comments would create risky or noisy churn

When an exception applies, keep the comment minimal.

### Git Checkpoint Push

Use only when the user explicitly asks to:

- commit
- push
- save progress
- create a checkpoint
- stage relevant files
- write a Conventional Commit message
- push to GitHub or a remote

Do not commit or push just because a repository exists.

Preflight:

- inspect `git status --short`
- inspect current branch
- inspect `git remote -v`
- inspect upstream and divergence when a remote exists
- inspect GitHub-specific constraints when visible or relevant

Rules:

- stage only relevant files
- do not include unrelated user changes
- do not commit secrets, credentials, `.env` secrets, local auth files, private keys, or generated secrets
- verify before committing when practical
- if verification fails, do not push unless the user explicitly wants a failing checkpoint saved
- use Conventional Commits
- do not force push unless explicitly requested
- do not bypass branch protection, required reviews, required checks, signed-commit rules, secret scanning, or repository rulesets

Final git report:

```text
Checkpoint:
- Commit:
- Branch:
- Push:
- Verification:
- Remaining changes:
```

## xc881 engineering workflow

### 1. Bound the task

Before coding, identify:

- exact behavior to add, fix, preserve, review, or optimize
- files/modules likely involved
- affected data flow and public contracts
- assumptions that affect behavior, interfaces, data shape, persistence, security, or user-visible output
- validation target

If multiple interpretations would lead to materially different implementations, ask one short clarification question.

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

Before writing code, be able to state in one sentence what the relevant current code does. If that sentence is vague, keep reading.

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

### 4. Choose the narrowest maintainable solution

Prefer:

- extending an existing correct path
- direct logic instead of one-off abstractions
- explicit control flow instead of clever compactness
- stable contracts over broad rewrites
- small seams over speculative frameworks
- local changes that leave sibling paths consistent

Reject changes larger than the problem. Minimal diff is not enough if it leaves the code hard to understand; aim for the smallest clear solution.

### 5. Preserve local style

Before editing, mirror nearby patterns:

- naming conventions
- control-flow style
- error-handling shape
- function size and decomposition
- type/interface style
- test structure
- dependency-injection style
- file organization

Correct but stylistically foreign code still lowers quality.

### 6. Enforce xc881 boundaries

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

Keep business/domain logic independent from:

- framework APIs
- ORM/database clients
- HTTP request/response objects
- third-party SDK objects
- UI components
- filesystem
- environment variables
- real clock and randomness
- global mutable state

Put side effects at the edges. Use adapters, ports, parameters, or dependency injection only when they reduce coupling, improve testability, or protect a real volatility point.

### 7. Implement with hard constraints

While editing:

- change only what is required for the task
- do not rewrite unrelated code for style
- do not rename unrelated symbols
- do not mix bug fixes with opportunistic cleanup
- do not add dependencies unless necessary and justified
- remove imports, branches, helpers, tests, or config made obsolete by your change
- keep important state transitions visible
- avoid circular dependencies
- avoid万能 service, 万能 utils, God Object, hidden side effects, and framework-leaked domain logic
- avoid premature caching, batching, async complexity, or performance work without evidence

### 8. Verify before claiming success

Preferred evidence order:

1. targeted tests proving the changed behavior
2. adjacent regression tests
3. typecheck, build, lint, or static analysis
4. manual reproduction steps when automated checks are unavailable

If the change touches shared logic, try to verify at least one adjacent consumer. If verification cannot be run, say what remains unproven.

## New project mode

When the user asks for a new project, starter architecture, or `xc881 新项目工程化`, output:

```text
xc881 新项目工程方案：
1. 项目边界
2. 未来变化轴
3. 推荐目录结构
4. 模块职责表
5. 依赖方向
6. 数据/接口契约
7. 测试策略
8. 首批实现步骤
9. 暂不做什么以及原因
```

Do not over-engineer the first version. Create abstractions only for real volatility, testability, or boundary protection.

## Legacy project mode

When the user asks for `xc881工程优化`, legacy cleanup, or refactoring an existing project, do not jump into a rewrite.

Output:

```text
xc881 老项目工程优化报告：
1. 当前结构判断
2. 主要耦合点
3. 低质量代码风险
4. P0/P1/P2/P3 优先级
5. 建议改造路径
6. 每一步收益/风险
7. 需要新增的测试
8. 可立即执行的最小安全改动
```

Staged path:

1. characterize current behavior
2. add or identify tests
3. extract pure logic
4. isolate side effects
5. introduce interfaces only where they reduce coupling or protect volatility
6. remove circular dependencies
7. clean naming and duplicate business rules
8. keep every step small, reversible, and verifiable

## Review mode

When reviewing code, prioritize findings over summaries:

1. correctness bugs
2. security, data loss, and regression risks
3. missing validation and unsafe assumptions
4. hidden coupling and boundary violations
5. testability problems
6. needless complexity or speculative abstraction
7. comment-policy violations in generated or modified code
8. naming/style issues that hurt maintainability

Use evidence and file/line references when possible. If no findings are found, state what was checked.

## Low-quality code definition

Low-quality code may run today but makes future maintenance, modification, testing, debugging, reuse, security review, or extension difficult, expensive, or risky.

Signals:

- a small change requires editing unrelated files
- business rules are scattered across UI, controllers, SQL, adapters, SDK calls, or framework callbacks
- modules know each other's implementation details
- core logic requires real database, network, filesystem, clock, random source, or third-party service to test
- circular dependencies
-万能 service, 万能 utils, God Object
- unstable public contracts
- hidden side effects and global mutable state
- unclear names, long functions, mixed-concept files, magic values, deep nesting
- swallowed errors, implicit security assumptions, missing boundary validation

## Skill composition

If another skill or project rule is active:

1. Use English Spec First if requirements need normalization.
2. Use xc881 design gate before implementation.
3. Use domain-specific rules for language, framework, database, UI, security, testing, performance, or deployment details.
4. Apply no-code-comments to code output.
5. Apply high-constraint verification before reporting completion.
6. Apply git checkpoint only when explicitly requested.

Priority:

```text
User current instruction
> repository-specific instruction files
> domain-specific skill
> xc881 integrated standard
> model defaults
```

## Strict do nots

Do not:

- code from a guessed implementation path
- silently invent requirements when wrong assumptions matter
- claim a fix without tests or credible verification
- introduce dependencies, configuration toggles, frameworks, or abstractions for one-off logic
- rewrite unrelated code
- hide business rules inside framework callbacks, SQL strings, SDK response handling, or UI rendering
- leak infrastructure objects into domain logic
- add comments to generated or edited code by default
- commit, push, amend, reset, discard, or force-push unless explicitly requested
- bury uncertainty behind confident language

## Final response shape

For coding work:

```text
完成内容：
- ...

验证：
- ...

假设 / 风险：
- ...
```

If git checkpoint was requested, also include branch, commit, push result, and remaining changes.
