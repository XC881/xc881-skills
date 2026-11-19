# Repro/Verify

Repro: existing failing test → new minimal test → curl/CLI/request fixture → headless UI → manual.

Prefer the cheapest supplied/existing repro testing the live prediction in the
same revision/environment.
Tight loop:

- red-capable: asserts the user's exact symptom
- deterministic or high repro-rate for flaky bugs
- fast enough to run repeatedly
- agent-runnable when possible

If a tight loop is unavailable, distinguish observed attempts from a proposed plan
and name the exact missing log/input/access. Do not promote the hypothesis to cause.

After repro: minimise one variable at a time; remaining inputs/steps should all be load-bearing.

```text
Repro:
Regression:
Security:
Build/type/lint:
Manual:
```

Plan only for the post-repair verification; Coding runs it within delegated
permissions. Running the cheapest existing repro to confirm cause is forensic
observation and may happen inside Analysis. Verify both the symptom and the
relevant non-regression contract; an unrun plan is not successful verification.
