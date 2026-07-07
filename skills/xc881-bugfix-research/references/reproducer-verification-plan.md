# Repro/Verify

Repro: existing failing test → new minimal test → curl/CLI/request fixture → headless UI → manual.

Tight loop:

- red-capable: asserts the user's exact symptom
- deterministic or high repro-rate for flaky bugs
- fast enough to run repeatedly
- agent-runnable when possible

If no tight loop can be built, state what was tried and request missing logs/artifact/access. Do not jump to a confident hypothesis.

After repro: minimise one variable at a time; remaining inputs/steps should all be load-bearing.

```text
Repro:
Regression:
Security:
Build/type/lint:
Manual:
```

Plan only; coding runs.
