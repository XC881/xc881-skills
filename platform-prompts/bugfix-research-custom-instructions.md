# xc881 Bugfix Research custom instruction

`xc881-bugfix-research` is explicit-only.

Use it when the user explicitly writes:

```text
$xc881-bugfix-research
```

or explicitly asks `xc881` to diagnose, repair, or research a bug, regression, or vulnerability.

Do not auto-trigger it from ordinary bug, error, CVE, vulnerability, crash, stack trace, or regression mentions that do not mention `xc881` or the direct skill name.

When active, it should diagnose, research, plan repair, plan verification, and hand off to xc881-coding-skills. It should not edit code or claim verification.
