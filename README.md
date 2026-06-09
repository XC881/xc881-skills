# xc881-skills

Token-compact Agent Skills.

```text
$xc881-solution-research     tech research; no code
$xc881-requirement-analysis  requirements; no code
$xc881-bugfix-research       bug/vuln diagnosis; no code
$xc881-coding-skills         implementation/verify
```

Flow:

```text
solution → requirement → coding
bugfix → coding
```

Rule: analysis skills are explicit-only and hand off. Coding executes clear scope.

```bash
bash scripts/install.sh all
python scripts/validate_all.py
```
