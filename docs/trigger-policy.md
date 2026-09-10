# Trigger

All xc881 skills are intent-routed. Direct `$skill-name` calls select that skill.
Implicit routing matches the requested deliverable to each skill `description`.
The table below illustrates outcomes; it is not a runtime keyword switch.

```text
$xc881-solution-research
$xc881-requirement-analysis
$xc881-bugfix-research
$xc881-source-article-style
$xc881-porting-orchestration
```

Requested deliverable:

```text
external technical evidence or a stack decision -> xc881-solution-research
scope, acceptance criteria, a PRD, or issue/PR triage -> xc881-requirement-analysis
cause of a bug, regression, vulnerability, or performance issue -> xc881-bugfix-research
project write, review, verification, or explicit git -> xc881-coding-skills
Chinese source-article prose -> xc881-source-article-style
cross-language or cross-project migration -> xc881-porting-orchestration
```

Selection rules:

- Choose one primary owner from the user's requested final outcome, not every
  intermediate verb or noun in the prompt.
- Incidental errors, code, terms, languages, or research needs do not activate a
  second skill. The primary owner delegates one bounded subtask only when blocked.
- Ordinary explanations, generic writing, and simple exact/local/low-risk reads
  may use no xc881 skill.
- Ambiguity alone is not requirement intent. Use base-agent judgment when safe,
  or ask one blocking question when the final outcome truly cannot be inferred.
- A combined user request may chain skills, but only one owns the active phase;
  delegated skills return to that owner instead of becoming parallel owners.
- Do not run a full workflow merely because a skill was plausibly relevant. Run
  only the branch needed for the requested outcome.
