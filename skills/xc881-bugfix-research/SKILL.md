---
name: xc881-bugfix-research
description: 'Explicit-only. Use only with $xc881-bugfix-research. Analyze bug/vulnerability before coding: evidence, research, cause, reproducer plan, repair plan, verification plan, handoff. No auto-trigger. No code/test/commit.'
when_to_use: 'Only explicit invocation. Use for logs/stack traces/user-described bugs/CVE/GHSA/OSV/CWE/OWASP/security advisories/regressions.'
display_name: "xc881漏洞与Bug诊断"
version: "2.1.0"
category: "debugging-security"
tags:
  - explicit-only
  - bugfix
  - vulnerability
  - security
  - root-cause
  - xc881
aliases:
  - xc881-bugfix-research
  - xc881-bugfix
  - xc881漏洞与Bug诊断
---

# xc881 BugFix

Explicit only. No code/test/commit.

Goal:

```text
symptom → evidence → cause → fix plan → verify plan → handoff
```

Reference files live under `./references/`.

Reference Index:

- `./references/web-research-policy.md`: docs/advisory/forum.
- `./references/bugfix-forensics-workflow.md`: cause.
- `./references/vulnerability-triage-policy.md`: security.
- `./references/reproducer-verification-plan.md`: repro/verify.
- `./references/bugfix-output-contract.md`: output.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

Steps:

1. Confirm explicit call.
2. Classify: bug / regression / stack / dependency vuln / code vuln / perf.
3. Gather expected, actual, env/version, input, logs, affected path.
4. Research if useful; match version/context.
5. Plan repro.
6. Localize entry/call/data/state/boundary/API.
7. State smallest cause + confidence.
8. Plan minimal fix + risk + verification.
9. Hand off.

Output:

```text
xc881 BugFix:
Context:
Evidence:
Cause:
Fix:
Verify:
Risk:
Handoff:
```

Security add:

```text
Severity:
CVE/GHSA/OSV/CWE/OWASP:
Affected:
Exploitability:
Mitigation:
```

Rules: explicit only; no exploit steps; fact ≠ hypothesis; weak evidence ≠ certainty.
