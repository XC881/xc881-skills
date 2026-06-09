# Karpathy Guardrail

Purpose:

```text
think → simplify → surgical diff → verify
```

Rules:

1. If ambiguous behavior/contract changes, stop and ask or hand off.
2. No feature, flexibility, config, adapter, abstraction, or error branch not required.
3. Every changed line traces to request, evidence, success check, or cleanup caused by this change.
4. Touch only needed files. Match local style. Mention old dead code; do not delete.
5. Clean only new orphans.
6. If solution is bigger than problem, simplify.
7. Convert task to one success check before editing.
