# Cross-Process Plan File

The source of truth for porting-specific execution state. Requirement scope/AC
remain authoritative in the linked req-process Artifact.

Keep the active ledger at or below 3,000 characters; link long logs/reports.
Validators are for explicit audit, observed-corruption repair, and repository/CI, not normal ledger authoring.

## Location

`dev-notes/cross-process/<task-slug>.md`, relative to the TARGET project
workspace (the project being ported into) — not the skill install dir.

If `dev-notes/` does not exist: create it, then ask the user whether to add it
to `.gitignore`. The user decides; never assume. Do not port until answered.

## Hard precondition

- After the req-process boundary is locked, generate this file and link it.
- Before ANY porting action, require an explicit path/handoff or one unambiguous
  active porting context. Never scan `cross-process/` to guess a task.
- Read this current ledger plus linked req-process `current.md` and its current
  queue item only. Previous requires an explicit current-item evidence link; next
  waits until advancement. Do not read req-process `index.md` by default.
- Missing or stale linked state -> do not port.
- After every iteration, derive the next ledger first, then update it once. The
  plan, not the conversation, is authoritative. A stale checkpoint is worse than none.
- A checkpoint is a recovery point. After
  advancement, load the new current window and continue automatically until task
  terminal. Stop only for explicit stepwise/pause intent or a real blocker.
- Context compaction preserves Porting ownership. Keep the linked req current,
  porting item state, equivalence method, open risks, and exact next action durable,
  then resume automatically.

## Template

```text
# Porting plan: <source> -> <target>

Requirement artifact: dev-notes/req-process/<task>/
Magnitude: whole-project / module / feature / logic-slice / abstract-intent
Equivalence method: IO parity / ported tests / golden / intent-fidelity
Items:
  - <module/feature>: not-started / in-progress / done
Progress: <done N of M> — <last calibrated at>
Open risks: <P0-P3, carried across sessions>
```

## Rules

- Keep it a ledger: derive required fields first, update once, and store the
  equivalence method, not its result; report verdict/evidence in chat.
- One file per porting task; `cross-process/` holds many tasks.
- Scope/AC/boundary are never copied here; they are read from Requirement artifact.
- The linked req-process + cross-process pair must be resumable without chat memory.
