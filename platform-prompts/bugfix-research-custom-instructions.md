# xc881 Bugfix Research custom instruction

`xc881-bugfix-research` is intent-routed.

Use it when the user writes:

```text
$xc881-bugfix-research
```

or clearly asks to diagnose, repair-plan, or research a bug, regression, runtime error, crash, CVE, security advisory, or vulnerability.

Do not trigger it from a bare word such as bug, error, CVE, vulnerability, crash, stack trace, or regression without a diagnostic or repair-planning intent.

When active, it should diagnose, research, plan repair, plan verification, and hand off to xc881-coding-skills. It should not edit code or claim verification.
