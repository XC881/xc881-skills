---
name: xc881-bugfix-research
description: 'Explicit-only skill. Use only when the user explicitly invokes $xc881-bugfix-research, says 使用 xc881-bugfix-research, or clearly asks to enable the xc881漏洞与Bug诊断 Skill. It performs bug/vulnerability diagnosis before coding: web-assisted research, advisory analysis, stack trace/log triage, root-cause hypothesis, reproducer plan, repair plan, verification plan, and handoff to xc881-coding-skills. Do not auto-trigger from ordinary bug/error/vulnerability keywords.'
when_to_use: 'Use only on explicit invocation of this skill. Do not use implicitly for ordinary mentions of bug, error, stack trace, CVE, vulnerability, crash, or regression. Once explicitly invoked, analyze symptoms/advisories/logs, use web research when useful, produce root-cause and repair/verification plans, and hand off implementation to xc881-coding-skills. Do not implement code or run verification in this skill.'
display_name: "xc881漏洞与Bug诊断"
version: "1.2.0"
category: "debugging-security"
tags:
  - explicit-only
  - bugfix
  - debugging
  - vulnerability
  - security
  - root-cause
  - web-research
  - cve
  - cwe
  - owasp
  - xc881
aliases:
  - xc881-bugfix-research
  - xc881-bugfix
  - xc881-debug
  - xc881-security-fix
  - xc881漏洞与Bug诊断
---

# xc881 Bugfix Research

## Role

Explicit-only bug/vulnerability diagnosis and repair-planning layer.

Activate only when the user explicitly invokes:

```text
$xc881-bugfix-research
```

or clearly says to use/enable `xc881-bugfix-research`.

Do not auto-trigger from ordinary bug, error, crash, stack trace, CVE, vulnerability, regression, or security keywords.

This skill turns symptoms, logs, advisories, issues, or failing behavior into:

```text
evidence → likely root cause → safe repair plan → verification plan → handoff
```

Do not write implementation code. Do not edit files. Do not claim verification was run.

Use `$xc881-coding-skills` after this skill to implement the repair plan and run validation.

## Load policy

`SKILL.md` is the fast path. Read references only when needed:

- `references/web-research-policy.md`: internet/advisory/forum/doc research, source trust, citations, version matching.
- `references/bugfix-forensics-workflow.md`: reproduce planning, localization, root-cause reasoning.
- `references/vulnerability-triage-policy.md`: CVE/CWE/OWASP/security advisory analysis and remediation planning.
- `references/reproducer-verification-plan.md`: minimal reproducer and verification plan design.
- `references/bugfix-output-contract.md`: compact and detailed output shapes.

## Default output

Compact by default.

- Analysis-only: root cause hypothesis, evidence, repair plan, verification plan, handoff.
- Security issue: add severity, affected versions, exploitability, mitigation.
- Expand only when risk is high, evidence conflicts, reproduction is unclear, or user asks.

## Workflow

1. Confirm explicit invocation:
   - If not explicitly invoked, do not use this skill.
   - Suggest explicit invocation only when the user asks about Skill usage.

2. Classify context:
   - user-described bug
   - failing test
   - stack trace/log error
   - dependency vulnerability/advisory
   - source-code vulnerability
   - regression after change
   - performance bug

3. Gather evidence:
   - expected vs actual behavior
   - symptoms/logs/stack trace
   - environment/version
   - input/request/data
   - recent changes
   - affected module/path
   - security/advisory metadata if relevant

4. Research when useful:
   - official docs, release notes, changelogs, security advisories, CVE/NVD, GHSA, OSV, CWE, OWASP, maintainer issues/PRs, trusted forum threads.
   - Match exact package, framework, runtime, platform, and version.
   - Separate sourced facts from hypotheses.
   - Do not copy untrusted patch code.

5. Reproducer plan:
   - existing failing test, or
   - new minimal failing test idea, or
   - minimal command/request/input, or
   - manual reproduction steps.
   - For security issues, keep proof safe and non-weaponized.

6. Localize:
   - likely entry point
   - call chain
   - data/state flow
   - boundary validation
   - dependency/API behavior
   - likely changed commit/config/version

7. Root cause:
   - state the smallest sufficient cause.
   - confidence: high / medium / low.
   - list alternative hypotheses only if they affect the fix.

8. Repair plan:
   - minimal safe change
   - affected files/modules to inspect
   - compatibility/migration impact
   - security impact
   - regression risk
   - verification plan

9. Handoff:
   - produce implementation instructions for `$xc881-coding-skills`.
   - coding skill performs patching, tests, verification, and optional checkpoint.

## Compact output contract

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

For vulnerabilities include:

```text
Severity:
CWE/OWASP/CVE/GHSA/OSV:
Affected versions:
Exploitability:
Mitigation:
```

## Rules

- Explicit invocation only.
- Do not edit code.
- Do not claim tests or verification were run.
- Do not patch before evidence.
- Do not treat search results as truth without version/context match.
- Do not provide weaponized exploit instructions.
- Do not hide uncertainty.
- Do not skip repair and verification planning.
- Do not commit/push.
