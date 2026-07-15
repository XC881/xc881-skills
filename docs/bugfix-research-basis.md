# Bugfix Research Basis

Repository-level background, not runtime reference.

`xc881-bugfix-research` is intent-routed and analysis-only.

Reason:

- ordinary bug/error/security words need symptom/diagnosis context to avoid noisy auto-triggering;
- bug/vulnerability diagnosis can require web research and longer reasoning, so it should only trigger on clear diagnostic intent;
- implementation and verification remain in `xc881-coding-skills` only when the
  user or delegating owner requested a change.

Flow:

```text
bug/vulnerability diagnosis intent
→ evidence and external research
→ root-cause hypothesis
→ repair plan
→ verification plan
→ optional handoff to xc881-coding-skills when implementation was requested
```
