# Forensics

```text
tight repro loop → minimise → hypotheses → instrumentation → cause → fix plan → verify plan → handoff
```

Evidence: expected, actual, log/stack, env/version, trigger input, recent change, affected module, tests.

Cause = smallest explanation predicting failure.

Hypotheses: list 3-5 ranked, falsifiable predictions before testing. Instrument only to test a prediction. Tag temporary debug output and require cleanup in the coding handoff.
