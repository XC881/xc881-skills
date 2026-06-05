# Low-Quality Code Rubric

Low-quality code may run today but makes future maintenance, modification, testing, debugging, reuse, security review, or extension difficult, expensive, or risky.

## P0: production, security, or data risk

- Missing or scattered authorization.
- Data writes lack transaction, idempotency, rollback, or consistency protection where needed.
- Unsafe external input flows into SQL, command execution, templates, file paths, or network calls.
- Errors are swallowed or invisible in production.
- Secrets or sensitive data are logged, committed, or exposed.
- External input lacks boundary validation.

## P1: serious engineering risk

- Business rules are scattered through UI, controllers, SQL, SDK adapters, or framework callbacks.
- Core logic needs real infrastructure to test.
- Circular dependencies exist.
- One small change touches many unrelated files.
- Third-party SDK objects flow through the application.
- A service, controller, hook, component, or utils file has become a dumping ground.
- Public contracts leak implementation details.

## P2: maintenance-cost risk

- Long functions with multiple responsibilities.
- Large files or classes with mixed concepts.
- Duplicated business rules.
- Long parameter lists or data clumps.
- Deep nesting or complex branching.
- Magic values and implicit conventions.
- Names do not express business meaning.
- Error handling is inconsistent.

## P3: local quality issue

- Inconsistent style.
- Outdated comments.
- Small local duplication.
- Limited readability problems.
- Missing nearby tests for simple logic.

## Finding format

```text
问题：
证据：
影响：
优先级：
最小修复：
测试保护：
```
