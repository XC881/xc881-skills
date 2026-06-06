# Skills Overview

## Layering

```text
xc881-requirement-analysis
→ xc881-bugfix-research
→ xc881-coding-skills
```

Use the layers by intent, not by keyword frequency.

## xc881-requirement-analysis

Purpose:

- requirement understanding before coding
- English Spec First normalization
- new project analysis
- existing project feature analysis
- explicit and inferred requirements
- acceptance criteria
- engineering handoff

Default trigger style:

```text
$xc881-requirement-analysis
```

Implicit use may be acceptable when the user clearly asks for requirement analysis.

## xc881-bugfix-research

Purpose:

- bug/vulnerability diagnosis before coding
- web-assisted research
- CVE/GHSA/OSV/CWE/OWASP analysis
- stack trace/log triage
- root-cause hypothesis
- repair plan
- verification plan
- handoff to `xc881-coding-skills`

Trigger policy:

```text
explicit-only
```

Use only when the user writes:

```text
$xc881-bugfix-research
```

or clearly asks to use/enable `xc881-bugfix-research`.

Do not auto-trigger from ordinary words like bug, error, CVE, vulnerability, crash, stack trace, regression, or 报错.

## xc881-coding-skills

Purpose:

- implementation after requirements/bug diagnosis are clear
- refactor
- code quality
- decoupling
- verification
- performance mode
- explicit checkpoint/push

Implementation, testing, validation, and checkpointing belong here.
