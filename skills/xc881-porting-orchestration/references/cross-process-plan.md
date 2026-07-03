# Cross-Process Plan File

The single source of truth for porting progress. It survives context
compaction: when the session forgets, re-read this file, not the chat history.

## Location

`dev-notes/cross-process/<task-slug>.md`, relative to the TARGET project
workspace (the project being ported into) — not the skill install dir.

If `dev-notes/` does not exist: create it, then ask the user whether to add it
to `.gitignore`. The user decides; never assume. Do not port until answered.

## Hard precondition

- After magnitude + boundary are locked, generate the plan file.
- Before ANY porting or reference action, read the plan and state "progress vs plan".
- No current plan file (missing or stale) -> do not port. Same gate as the boundary.
- After every iteration, update the plan. Read first, update after. The plan, not
  the conversation, is authoritative. A stale checkpoint is worse than none.

## Template

```text
# Porting plan: <source> -> <target>

Magnitude: whole-project / module / feature / logic-slice / abstract-intent
Stop boundary:
  done-criteria: <measurable, checkable per iteration>
  exit: <success end / give-up-escalate end>
  out-of-scope: <listed>
Equivalence method: IO parity / ported tests / golden / intent-fidelity
Items:
  - <module/feature>: not-started / in-progress / done  (+ note/evidence)
Progress: <done N of M> — <last calibrated at>
Open risks: <P0-P3, carried across sessions>
```

## Rules

- Keep it a ledger, not prose. Update item status + evidence, not narrative.
- One file per porting task; `cross-process/` holds many tasks.
- Must be self-sufficient: resumable from this file alone, no chat memory.
