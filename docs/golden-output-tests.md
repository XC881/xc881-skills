# Behavior Eval (output quality)

Trigger evals answer "was the skill invoked". Behavior evals answer "was the
output shaped correctly once invoked". Two layers:

## Structural layer (default CI, offline)

- File: `skills/<skill>/evals/behavior-contract.json`.
- Fields: `skill`, `layer: structural`, `required_sections[]`, `forbid_impl_code`, `pass_sample`.
- `check_structural_output` flags: `missing_section:*`, `empty_section:*`, `no_impl_code`.
- Section boundaries come only from `required_sections` labels (label alone, or `label:`).
  Sample body lines must not start with a section label.
- Self-test in `validate_behavior_contracts`: `pass_sample` must pass clean;
  deleting any required section must be detected; if `forbid_impl_code`, injected
  fenced code must be detected. This gives two-way coverage, not positive-only.
- Scope: proves the acceptance standard is well-formed and the checker enforces it.
  It removes formal false-green (missing section, analysis skill emitting impl code).
  It does NOT judge semantic correctness.

## Semantic layer (opt-in, not in default CI)

- File: `skills/<skill>/evals/behavior-rubric.json`.
- Fields: `skill`, `layer: semantic`, `ci: false`, `cases[] {query, checklist[]}`.
- Checklist items are natural-language pass criteria for a human or LLM judge.
- Default `validate_all.py` only checks the rubric file's shape; it never runs a
  model, so CI stays offline and reproducible.

## What structural layer cannot catch

A section can be present and non-empty but wrong (bad root cause, untestable AC).
That is the semantic layer's job and requires golden outputs or a judge.
