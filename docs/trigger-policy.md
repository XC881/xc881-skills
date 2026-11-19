# Trigger

Select skills autonomously from **user intent** AND **actual task readiness/direction**—never from literal phrasing or a keyword list. Direct `$skill-name` calls remain valid; old analysis names (`$xc881-requirement-analysis`, `$xc881-bugfix-research`, `$xc881-solution-research`) remain aliases of `$xc881-analysis`.

```text
$xc881-analysis
$xc881-coding-skills
$xc881-source-article-style
$xc881-porting-orchestration
```

Two-axis selection (`User Intent × Task Readiness`):

```text
ordinary Q&A, generic writing, or simple exact/local/low-risk read -> no skill
analysis-only (scope/AC/PRD/triage, bug cause, or external research) -> xc881-analysis
build/fix with concrete scope and confirmed cause -> xc881-coding-skills directly
build/fix with open scope/AC, unconfirmed cause, or missing external facts -> xc881-analysis -> xc881-coding-skills
cross-language or cross-project migration (boundary only or full port) -> xc881-porting-orchestration (+ xc881-coding-skills / xc881-analysis as needed)
Chinese source-article prose -> xc881-source-article-style (+ xc881-coding-skills / xc881-analysis for gaps)
```

Selection rules:

- Users do not need to script workflow steps ("analyze first, then implement" or "diagnose first, then fix"). When the user says "build X" or "fix Y" and scope, root cause, external facts, or cross-language parity are still open, start in Analysis or Porting and chain into Coding automatically once resolved.
- Conversely, when scope, target, and cause are already concrete, skip Analysis and enter Coding directly—do not add ceremony to ready work.
- One skill owns the active phase; mid-task surprises (contract conflicts, hidden scope choices, two failed fixes) pivot back to Analysis instead of guessing.
- Incidental nouns ("code", "requirement", a language name) do not trigger a skill whose work the task does not actually need. Inside Analysis, cross-branch gaps switch branches without delegation.
- Run only the branch needed for the current task gap, never the whole workflow for form's sake.
