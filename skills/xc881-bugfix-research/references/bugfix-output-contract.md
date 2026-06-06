# Bugfix Output Contract

Default compact output:

```text
xc881 Bug/Vuln Analysis:
Context:
Evidence:
Web intel:
Root cause:
Repair plan:
Verification plan:
Risk:
Handoff to xc881-coding-skills:
```

Analysis-only output:

```text
Diagnosis:
Root cause hypothesis:
Confidence:
Repair plan:
Verification plan:
Question:
```

Security output additions:

```text
Severity:
CWE/OWASP/CVE/GHSA/OSV:
Affected versions:
Exploitability:
Mitigation:
```

Handoff format:

```text
$xc881-coding-skills
Use the bug/vulnerability analysis above as source of truth.
Implement the minimal repair plan.
Run the verification plan.
Report patch summary, verification, and residual risk.
```

Rules:

- Keep output compact.
- Use IDs only when multiple bugs/vulns exist.
- Expand only for high-risk security issues, conflicting evidence, or user request.
