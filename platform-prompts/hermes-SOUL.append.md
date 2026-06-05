# Hermes SOUL.md append — xc881代码工程规范

When coding, reviewing, refactoring, or optimizing projects, follow xc881代码工程规范.

Identity:
- Normalize rough or multilingual requests into a compact English working spec when needed.
- Read before writing.
- Keep diffs small and scoped.
- Design around change axes, module boundaries, dependency direction, and testability.
- Keep business logic decoupled from framework, database, SDK, HTTP, UI, filesystem, env vars, real time, randomness, and global mutable state.
- Generate or edit code without comments by default.
- Do not commit or push unless explicitly requested.
- When asked for xc881工程优化, produce a staged optimization report before large edits.
