---
name: xc881-bugfix-research
description: 'Primary owner for bug, regression, vulnerability, or performance diagnosis. Use when the requested outcome is cause and a repair plan. Implementation-only work belongs to Coding.'
when_to_use: 'Use when the requested outcome is diagnosis before repair. Diagnosis-only stops in Bugfix; hand to Coding only when implementation was requested.'
display_name: "xc881漏洞与Bug诊断"
version: "2.4.1"
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

Intent-routed diagnosis owner; direct calls select it. Incidental errors stay with
the current owner. No code/test/commit; Coding performs authorized execution.

## Reference Routes

- `./references/bugfix-forensics-workflow.md`: uncertain cause/competing explanations.
- `./references/reproducer-verification-plan.md`: missing repro/repair verification plan.
- `./references/web-research-policy.md`: external/version facts affect diagnosis.
- `./references/vulnerability-triage-policy.md`: security exposure, severity, or mitigation.
- `./references/bugfix-output-contract.md`: tracker fields or repair handoff details.

Route by intent each turn. Full supplied bodies count; names/paths/markers do not.
Reuse in-context rules; read needed exact paths automatically only for missing
rules, known changes or requested rereads. Higher-priority invocation rules win.

## Workflow

1. Classify bug / regression / stack / dependency vuln / code vuln / perf.
   Reuse expected/actual, env/version, inputs, logs and paths; refresh changed or
   conflicting evidence.
2. Rank falsifiable explanations without quotas; choose the smallest distinguishing
   observation. Reuse valid reproductions.
3. For repository evidence, perform a simple exact/local/low-risk read here, or delegate a complex/tracked `read` to `$xc881-coding-skills` using task+project complexity.
   Send prediction/evidence; receive anchors, observations, limits and next check.
   Resume diagnosis.
4. Cause + confidence needs evidence explaining symptoms and separating alternatives;
   otherwise report unconfirmed + missing check. A plausible fix/stack is not cause.
5. Plan minimal fix/risk/verification; stop when evidence supports repair.
   Unconfirmed repairs stay conditional; retain uncertainty and untested behavior.
6. Hand repair to `$xc881-coding-skills` when implementation intent is explicit or
   delegated; no second user invocation. Diagnosis-only stops with `Handoff: none`
   or missing evidence. Reads never grant changes.

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

No exploit steps. Context compaction resumes the same diagnosis/evidence loop automatically.
