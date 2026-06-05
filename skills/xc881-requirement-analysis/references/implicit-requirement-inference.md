# Implicit Requirement Inference

If user states A and B, but A/B require C to work safely, identify C as inferred.

Inference lenses:
1. prerequisite
2. dependency
3. consequence
4. state/lifecycle
5. permission/security
6. data
7. failure/recovery
8. observability/audit
9. notification
10. compatibility/migration
11. non-functional
12. abuse/edge case

Format:

```text
IR-001:
Derived from:
Type:
Reasoning:
Confidence: high | medium | low
Needs confirmation: yes | no
Acceptance:
```

Never present inferred requirements as confirmed facts.
