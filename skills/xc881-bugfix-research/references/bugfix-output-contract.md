# Output

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

Security add: `Severity / CVE-GHSA-OSV-CWE-OWASP / Affected / Exploitability / Mitigation`.

Tracker add:

```text
Issue state: needs-info | ready-for-agent | ready-for-human
Agent Brief bug fields: current / desired / repro / AC / verify
```

Use tracker labels/comments through `$xc881-requirement-analysis`; this skill supplies bug evidence, cause, fix, and verify plan.

For repository evidence, perform a simple exact/local/low-risk read directly or
hand Coding a complex/tracked read-only question, then resume Bugfix. `Handoff`
sends the confirmed repair contract to Coding for the write stage.
