# Output

```text
xc881 Req:
Spec:
ER:
IR:
Scope:
FR/NFR:
AC:
Risk:
Q:
Handoff:
```

## AC form
State each AC as given input/precondition → expected observable output, not an abstract assertion. Given/When/Then is allowed. Keep simple cases one line; do not force three-part form.
Example: `AC-1 given empty email on submit → reject with "email required", no request sent.`

## Q form
Ask only when blocked. One question, one decision. Include:

```text
Q: <blocking decision>
Recommend: <answer + why>
If no answer: <safe default or stop>
```

## Tracker add-on
For issue/PR/PRD triage, include inside `Handoff`:

```text
Tracker:
State: from -> to + why
Brief/Issues:
Tracker Ops: executed | planned | skipped
```
