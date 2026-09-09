# Behavior Eval (output quality)

Routing fixtures declare intended ownership.
Behavior evaluation separates output form from task quality. Two layers:

## Structural layer (default CI, offline)

- File: `skills/<skill>/evals/behavior-contract.json`.
- Fields: `skill`, `layer: structural`, `anchors[]`, `required_sections[]`,
  `optional_sections[]`, `forbid_impl_code`, `pass_sample`, optional `modes{}`.
- `check_structural_output` flags missing/empty/duplicate sections and forbidden
  implementation fences. Required and optional labels both delimit sections;
  quoted/fenced/indented code is evidence content, not a heading.
- The `full` mode uses the base contract. Task-known `chat-only` Requirement and
  `decision` Solution modes override it. Never choose a mode by fewest violations.
  `prose` is explicitly unscored: brief/delegated answers, code reviews, article
  outlines/function analyses and planning-only summaries have semantic criteria,
  not an obligation to inflate themselves into full-format fixtures.
- Coding's verification/risk fields are structurally optional. Whether a real
  check, limitation or material risk must be reported is judged from task intent
  and actual tools; an omitted relevant field is still a semantic failure.
- Self-test in `validate_behavior_contracts`: `pass_sample` must pass clean;
  deleting any required section must be detected; if `forbid_impl_code`, injected
  fenced code must be detected. This gives two-way coverage, not positive-only.
- Scope: proves the acceptance standard is well-formed and the checker enforces it.
  It removes formal false-green (missing section, analysis skill emitting impl code).
  It does NOT judge semantic correctness.

### Scoped collection

```bash
python scripts/collect_behavior_data.py /tmp/outputs.jsonl --out-dir /tmp/output-eval
python scripts/collect_behavior_data.py /tmp/req-chat.jsonl --skill xc881-requirement-analysis --mode chat-only --out-dir /tmp/req-eval
```

Each input line is `{"text": "<output>"}`. Mixed owners/modes require separate
known-mode inputs or auto attribution with limits.
Auto attribution recognizes current leading headings for all six owners and uses
`full`. An anchored truncated answer counts as failure even if only one heading
survived. Unknown/ambiguous/prose outputs are visible as unscored, never dropped
or treated as passes.
The report separates scored/unscored/excluded counts and marks malformed records
as incomplete collection. Rates describe scored records. Stored samples contain
locations, hashes and violations.
`scripts/test_behavior_evaluation.py` exercises these behaviors in offline CI.

## Semantic layer (opt-in, not in default CI)

- File: `skills/<skill>/evals/behavior-rubric.json`.
- Fields: `skill`, `layer: semantic`, `ci: false`, `cases[] {query, checklist[]}`.
- Checklist items are natural-language pass criteria for a human or LLM judge.
- Default `validate_all.py` only checks the rubric file's shape; it never runs a
  model, so CI stays offline and reproducible.

## What structural layer cannot catch

A section can be present and non-empty but wrong (bad root cause, untestable AC).
That is the semantic layer's job and requires golden outputs or a judge.

## Reading Paths And Real Tasks

`evals/skill-load-paths.json` and `scripts/audit_skill_loads.py` validate declared
instruction paths and report text size. Full-format output fixtures apply to their
full-response mode, not a compact delegated evidence return.

## Multi-Turn Constraints

The `continuations` in `evals/skill-load-paths.json` state preconditions,
per-turn expected instruction reads and quality criteria. They constrain what
the skill may read. Project/current reads stay separate from those
instruction-file counts.

## Queue State History

`scripts/audit_queue_execution.py` checks append-only item/task transitions and
rejects item `in-progress` (task-only). `scripts/test_queue_execution.py` covers
missing history, block/resume (blocked item returns as `ready`), intermediate
snapshots that a final `done` would hide, and index/history/validator tool
activity. `evals/queue-execution/*.json` are queue-constraint fixtures.
