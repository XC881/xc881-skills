# xc881 Bugfix Research custom instruction

`xc881-bugfix-research` is explicit-only.

Use it only when the user explicitly writes:

```text
$xc881-bugfix-research
```

or clearly asks to use/enable the xc881 bugfix research skill.

Do not auto-trigger it from ordinary bug, error, CVE, vulnerability, crash, stack trace, or regression mentions.

When active, it should diagnose, research, plan repair, plan verification, and hand off to xc881-coding-skills. It should not edit code or claim verification.
