# Coding Task Mode and Artifact Execution

After the adaptive gate selects Coding, classify persistence before opening
project files or execution artifacts. Writes and tracked reads always select
Coding; simple bounded reads may remain with the active analysis/writing skill.

## Instant mode

Use when the user did not provide a req-process/cross-process path or handoff and
the current conversation does not unambiguously identify one active queue task.

- Do not scan `dev-notes` merely because it exists.
- Read, explain, trace, review, change, or verify the actual code directly.
- Do not create/update a queue unless `$xc881-analysis` (Requirement branch) decides persistence is
  needed for the task's complexity.

## Queue mode

Use only for an explicit artifact/path/handoff or an unambiguous active task in
the current conversation. If multiple artifacts are plausible, ask one blocking
selection question. An Analysis (Requirement branch) handoff for new or reopened work names the
exact artifact, current item, next item, and blockers; consume it without
searching directories or selecting the newest artifact.

Before work:

1. Consume the exact write-first handoff; do not run a process validator in
   normal execution. Directly observed malformed fields or links return to
   `$xc881-analysis`; explicit audit/repair may validate once.
2. Read `current.md` and only the current queue item it names. Use an exact fresh
   window already supplied/read; known advancement, edits or missing context need
   the current state again. Reusing static rules does not prove queue freshness.
   Do not read `index.md`, previous, or next by default.
3. Read a previous item only when the current item explicitly links evidence or a
   dependency detail that its local contract does not contain. Read next only
   after checkpoint advancement makes it current.
4. Load a linked decision/evidence file only when the current queue item names it.
5. Treat `current.md + current item` as goal, scope/AC, targets,
   constraints, and verification contract. Behavior-changing contract gaps return
   to `$xc881-analysis`.

Return to `$xc881-analysis` instead of reading `index.md` when the current item lacks
required contract, actual code conflicts with it, the user changes scope/AC, or
the queue needs replanning. Analysis (Requirement branch) owns the full-contract read and produces
a refreshed current window before Coding resumes.

For cross-process continuation, read the selected current cross-process ledger,
linked req-process `current.md`, and linked current item only. Do not search for
other ledgers or task history.

## Action mode

Persistence and action are independent:

- `instant + read`: inspect real code and report evidence; no artifact read.
- `instant + change`: patch and verify directly; no artifact read.
- `queue + read`: inspect the current slice, report findings, checkpoint state.
- `queue + change`: implement the current slice, verify, checkpoint state.

An Analysis or source-article run may perform a simple read directly or
delegate complex read-only evidence while retaining ownership. Execute delegated
`read` in the selected mode, return evidence, and do not infer change permission.

Execution:

- `current.md` alone marks active work: task `State` becomes `in-progress`.
  Item `Status` is only `pending | ready | blocked | done | skipped`, never
  `in-progress`. Resume a blocked item as `ready`; keep activity in `current.md`.
- Work only the current vertical slice and its declared dependencies.
- A blocked item records the blocker and sets task state `blocked`; do not skip
  ahead unless the queue explicitly identifies another runnable item.

After a queue item:

- Run declared verification before `done`, but report results/logs only in chat.
- Preserve exact machine fields:
  - `current.md`: `Task: <index ID>`, `State:`, `Previous|Current|Next: none | queue/Q-NNN-<slug>.md` (relative paths, never bare IDs; terminal `done|cancelled|superseded` sets `Current: none` and `Next: none`), `Progress:`, `Blockers:`, plus non-empty `Last completed:` and `Next action:` while active.
  - `queue/Q-NNN-*.md`: `ID: Q-NNN`, `Status:`, `Previous|Next: none | Q-NNN` (bare IDs, never paths), `Blocked by: none | Q-NNN,...`.
- Derive item status, current pointers/counts and one `history.md` line per
  changed item before one coherent patch. Name `Q-ID: old -> new`, next current
  and task state. Record completion/advancement, block/resume, reopen and task
  terminal, not results. Task-only transitions also need a line. Never replay an
  already checkpointed transition or use a normal validator call.
- Append history at EOF without loading its body; if the edit tool needs an
  anchor, read only a bounded tail. History is an immutable trail, not authority.
- If no current item remains, set task `done`. Otherwise advance next to current,
  load only the new current item, and continue in the same requirement run
  without asking the user to say continue.
- Context compaction resumes from the exact current window. Continue the same
  read or change. Stop after a valid checkpoint only for explicit stepwise/pause intent or a real
  blocker, approval/input, safety boundary, contract/scope change, or no runnable
  item.
- Do not persist command output, pass/fail details, or completion evidence.

For porting, requirement scope/AC remain in req-process; cross-process owns only
porting magnitude, equivalence, and port execution progress.
