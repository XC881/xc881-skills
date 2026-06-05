# No Code Comments Policy

Default: generated, edited, patched, scaffolded, regenerated, or shown code should be comment-free.

Do not add:

- inline comments
- block comments
- banner comments
- docstrings
- JSDoc
- XML docs
- TODO/FIXME placeholders
- explanatory annotations

Prefer:

- clear names
- small helpers
- straightforward control flow
- explanation in the response outside the code

Allowed exceptions:

- user explicitly asks for comments or annotated teaching code
- tooling requires directive comments
- legal or generated-file headers are mandatory
- public API docs are required by tooling or convention
- preserving existing comments avoids unrelated churn

When an exception applies, keep the comment minimal.
