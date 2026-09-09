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

`Cause`: supported + confidence, or unconfirmed + missing check.
`Verify`: a plan unless Coding returned observed results.

Tracker add:

```text
Issue state: needs-info | ready-for-agent | ready-for-human
Agent Brief bug fields: current / desired / repro / AC / verify
```

Use tracker labels/comments through `$xc881-requirement-analysis`; this skill supplies bug evidence, cause, fix, and verify plan.

For repository evidence, perform a simple exact/local/low-risk read directly or
hand Coding a complex/tracked read-only question, then resume Bugfix. `Handoff`
sends cause/evidence anchors, bounded repair, non-regression constraints and exact
verification step to Coding only when implementation was requested or delegated
and the repair is supported; diagnosis-only uses `Handoff: none` or names missing evidence.
