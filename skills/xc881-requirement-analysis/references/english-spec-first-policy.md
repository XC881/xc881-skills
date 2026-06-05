# English Spec First Policy

Use before deeper requirement analysis when the user's request is rough, multilingual, mixed Chinese-English, ambiguous, emotional, scattered, or needs precise execution.

## Output shape

```text
Standard English Spec:
Goal:
Inputs:
Constraints:
Output:
Process Notes:
```

## Rules

- Keep the spec compact.
- Preserve names, paths, APIs, technologies, metrics, and deadlines exactly.
- Convert vague intent into operational language only when the intent is clear.
- Separate hard requirements from inferred preferences.
- Do not invent requirements.
- If missing information blocks correct requirement analysis, ask one concise question.
- If missing information does not block requirement analysis, proceed with a labeled assumption.
- Use the spec as the working contract for the rest of the requirement analysis.
- Answer in the user's language unless they request English.

## Relationship to requirement analysis

English Spec First only normalizes the request.

After normalization, still perform:

- context classification
- explicit requirement capture
- implicit/dependency/consequence requirement inference
- MVP or in-scope/out-of-scope analysis
- functional and non-functional requirements
- acceptance criteria
- risk analysis
- engineering implementation plan
