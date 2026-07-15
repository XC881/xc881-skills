---
name: xc881-bugfix-research
description: 'Primary owner for bug, regression, vulnerability, or performance diagnosis. Gather evidence, rank hypotheses, identify cause, and plan repair/verification. Use implicitly only when diagnosis is the requested outcome; implementation-only work belongs to Coding.'
when_to_use: 'Use for diagnosis before repair. Diagnosis-only stops in Bugfix; hand to Coding only when the user or parent owner requested implementation.'
display_name: "xc881漏洞与Bug诊断"
version: "2.4.0"
category: "debugging-security"
tags:
  - intent-routing
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

Intent-routed diagnosis owner. Direct calls select it; implicit use requires the
primary outcome in the description. Incidental errors stay with the base/current
owner. Run only the needed branch. No code/test/commit.

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

1. Confirm diagnosis is the requested outcome, not an incidental implementation detail.
2. Classify: bug / regression / stack / dependency vuln / code vuln / perf.
3. Gather only missing expected/actual, env/version, input, logs, and affected path.
4. Research only when external/version facts affect the diagnosis.
5. Plan the smallest repro needed to test cause confidence.
6. For repository evidence, combine read complexity with project coupling: perform a simple exact/local/low-risk read here, or delegate a complex/tracked `read` to `$xc881-coding-skills`, then resume diagnosis. Bugfix retains cause ownership.
7. State smallest cause + confidence.
8. Plan minimal fix + risk + verification.
9. Hand repair to `$xc881-coding-skills` only when implementation intent is
   explicit or delegated. Diagnosis-only stops after the plan; `Handoff` states
   `none` or the evidence needed next. Existing implementation intent needs no
   second user invocation.

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

Rules: route only on diagnosis intent; no exploit steps; fact ≠ hypothesis; weak
evidence ≠ certainty; delegated Coding reads never grant change permission; do
not convert diagnosis-only into a patch. After context compaction, resume the same
diagnosis owner and evidence/cause loop automatically.
