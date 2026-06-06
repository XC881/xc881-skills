# Reproducer and Verification Plan

This skill designs verification; it does not run it.

## Reproducer plan

Prefer:

1. existing failing test to run later
2. new minimal failing test idea
3. minimal command/request/input
4. manual reproduction steps

For user-described bugs, infer a minimal reproducer and label assumptions.

## Verification plan

For normal bugs:

- failing case should fail before fix and pass after fix
- adjacent regression tests
- typecheck/build/lint if relevant

For vulnerabilities:

- vulnerable path no longer succeeds
- safe negative test added when practical
- auth/permission boundary tested when relevant
- dependency fixed version confirmed when relevant

For performance bugs:

- objective stated
- baseline and after measurement suggested
- no correctness regression

## Output

```text
Verification plan:
- Reproducer:
- Regression tests:
- Security checks:
- Build/type/lint:
- Manual check:
```
