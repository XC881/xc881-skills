# Output

```text
xc881 Solution:
Spec:
RQ:
Evidence:
Risk:
Handoff:
```

For an actual option decision, add:

```text
Options:
Pick:
```

Do not add empty `Options`/`Pick` sections to fact checks, standards lookups, or
single API/version verification.

Handoff: original owner, supported decision, uncertainty and exact next action.
Delegates return only requested claims/anchors or evidence path; do not start
another workflow. Implement only when authorized, through Coding.

Large research:

```text
Artifact: <path>
Claims: <count/types>
Use: <which RQ/decision it supports>
```

Requirement-delegated evidence:

```text
Artifact: dev-notes/req-process/<task>/evidence/RQ-NNN-<slug>.md
Return: same requirement run
Use: <RQ / scope / AC / decision affected>
Next: <exact owner action or remaining blocking check>
```
