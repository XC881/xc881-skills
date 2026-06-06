# Bugfix Research Basis

Repository-level background, not runtime reference.

`xc881-bugfix-research` is explicit-only and analysis-only.

Reason:

- ordinary bug/error/security words are too common and would cause noisy auto-triggering;
- bug/vulnerability diagnosis can require web research and longer reasoning, so it should be user-controlled;
- implementation and verification should remain in `xc881-coding-skills`.

Flow:

```text
explicit invocation
→ evidence and external research
→ root-cause hypothesis
→ repair plan
→ verification plan
→ handoff to xc881-coding-skills
```
