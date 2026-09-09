# Behavior Eval (output quality)

Routing fixtures declare intended ownership; actual invocation needs a trace.
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
python scripts/collect_behavior_data.py /tmp/authorized-rollout.jsonl --out-dir /tmp/output-eval
python scripts/collect_behavior_data.py /tmp/req-chat.jsonl --skill xc881-requirement-analysis --mode chat-only --out-dir /tmp/req-eval
```

Explicit files only: no default home-session scan or directory recursion. Mixed
owners/modes require separate known-mode inputs or auto attribution with limits.
Auto attribution recognizes current leading headings for all six owners, uses
`full`, and is not proof of skill invocation. An anchored truncated answer counts
as failure even if only one heading survived. Unknown/ambiguous/prose outputs are
visible as unscored, never dropped or treated as passes. Only final messages
(`phase: final_answer` or `channel: final`, with absent legacy fields allowed)
are eligible; commentary/recaps are excluded.
The report separates scored/unscored/excluded counts and marks malformed records
as incomplete collection. Rates describe scored messages only, not all tasks.
Stored samples contain locations, hashes and violations, not queries/excerpts.
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
paths and report text size, not actual selection or quality. Full-format output
fixtures apply to their full-response mode, not a compact delegated evidence return.
For a behavioral check, give an independent agent a realistic request, the skill
and minimum raw evidence without the intended answer. Inspect its actual file
reads, commands, result and safety boundaries. Compare identical old/new tasks
before claiming quality or token improvements; isolated smoke checks cannot prove
general compliance. No production session scan is required for ordinary editing.

## Multi-Turn Evaluation

Opt-in maintenance only; no runtime telemetry or default model calls. The
`continuations` in `evals/skill-load-paths.json` state preconditions, per-turn
expected manual instruction reads and quality criteria. They are not measured
traces or a simulator. Required invocation calls, project/current reads and host
body injection are distinct from those instruction-file counts.

1. Snapshot the pre-change and candidate skill contents outside the worktree.
   Record content identity once, and the available client/model/tool conditions;
   version strings alone are insufficient. Do not install dependencies or proxies.
2. Use independent contexts and identical raw tasks/permissions for each variant.
   Supply the complete body for warm tests; supply only a path/loaded marker for
   missing-body tests. Do not tell the executing agent the expected read counts,
   suspected bug or intended answer. Send actual follow-up turns, not a request
   to describe a hypothetical conversation.
3. Inspect authorized tool-call traces and actual outputs. Count repeated reads
   of still-available unchanged instructions separately from necessary reads;
   record metadata/notices and injected bodies only if independently observable.
   Do not treat self-reported counts alone as host-request evidence.
4. Cover unchanged continuations, repeated explicit invocation, new/returning
   concerns, known changes, requested rereads, context loss/retention and bounded
   delegation/current queues. Repeat a warm and missing-content case. Controlled
   removal/new-context tests must not be described as real host compaction.
5. Judge correctness, evidence freshness, permissions, owner return, continuous
   execution and scope along with reads. Report actual tokenizer/usage measures
   only with their scope; count characters as characters. No payload access means
   host duplication and whole-session savings remain unverified. An already-clean
   baseline is not evidence of improvement or grounds to weaken necessary reads.

Keep results in chat or authorized temporary traces, never dev-notes. Disclose
unexecuted scenarios and nondeterminism; a small matched experiment does not prove
general reliability. If only host reinjection repeats, report that separate cause
instead of changing unrelated client/provider configuration or adding a cache.

`scripts/audit_skill_continuations.py` parses recorded `run.json`/`events.jsonl`.
Usage is the delta of cumulative `tokenUsage.total`, never the sum of `last`
notifications. Failed, incomplete, mismatched model/client/case, missing usage
and character-count comparisons cannot claim savings. Unobserved boundaries
always include provider request bodies, host injection dedup and child usage.
`--compare BASELINE CANDIDATE` applies that rule to two independent run
directories. `item/completed` `contextCompaction` is real host compaction;
controlled missing-body cases must not set `compact`.

Each `continuations` row names an `executable` case under `evals/continuations/`
or `evals/queue-execution/`. Those JSON files are the matched-task inputs for
`scripts/run_skill_continuations.py --execute`; they do not contain expected
read counts or intended answers. CI never runs paid turns.

## Queue State History

`scripts/audit_queue_execution.py` is opt-in maintenance, not a runtime gate.
It checks append-only item/task transitions and rejects item `in-progress`
(task-only). `scripts/test_queue_execution.py` covers missing history,
block/resume, intermediate snapshots that a final `done` would hide, and
index/history/validator tool activity. `evals/queue-execution/*.json` are
fresh-context cases for `scripts/run_skill_continuations.py --execute`; CI
does not run paid turns. Inspect `state-*.json` plus commands, not the model's
claim that it followed the protocol.
