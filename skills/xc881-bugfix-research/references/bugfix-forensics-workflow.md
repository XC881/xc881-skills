# Bugfix Forensics Workflow

Use only after explicit invocation.

## Reasoning loop

1. Reproducer plan
2. Localization hypothesis
3. Root-cause hypothesis
4. Repair plan
5. Verification plan
6. Handoff to xc881-coding-skills

## Evidence checklist

- expected behavior
- actual behavior
- exact error/log/stack
- version/environment
- triggering input/request/data
- recent changes
- affected files/modules
- existing tests
- adjacent behavior that must not regress

## Root cause standard

A good root cause is the smallest sufficient explanation that predicts the observed failure.

Bad root causes:

- restating the symptom
- blaming a broad module
- guessing without evidence
- ignoring version/environment
- ignoring a boundary condition

## Stop rule for analysis

If evidence supports multiple incompatible causes, do not guess. Rank hypotheses and ask one blocking question or propose the smallest experiment to disambiguate.
