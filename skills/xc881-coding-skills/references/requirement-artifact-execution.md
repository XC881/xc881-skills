# Coding Task Mode and Artifact Execution

After the adaptive gate selects Coding, classify persistence before opening
project files or execution artifacts. Writes and tracked reads always select
Coding; simple bounded reads may remain with the active analysis/writing skill.

## Instant mode

Use when the user did not provide a req-process/cross-process path or handoff and
the current conversation does not unambiguously identify one active queue task.

- Do not scan `dev-notes` merely because it exists.
- Read, explain, trace, review, change, or verify the actual code directly.
- Do not create/update a queue unless requirement analysis decides persistence is
  needed for the task's complexity.

## Queue mode

Use only for an explicit artifact/path/handoff or an unambiguous active task in
the current conversation. If multiple artifacts are plausible, ask one blocking
selection question. A Requirement handoff for new or reopened work names the
exact artifact, current item, next item, and blockers; validate and use it without
searching directories or selecting the newest artifact.

Before work:

1. Run the requirement skill's `scripts/validate_req_process.py <task-dir>` as a
   mechanical check; validator file access does not expand model context.
2. Read `current.md` and only the current queue item it names. Do not read
   `index.md`, previous, or next by default.
3. Read a previous item only when the current item explicitly links evidence or a
   dependency detail that its local contract does not contain. Read next only
   after checkpoint advancement makes it current.
4. Load a linked decision/evidence file only when the current queue item names it.
5. Treat `current.md + current item` as goal, scope/AC, targets,
   constraints, and verification contract. Behavior-changing contract gaps return
   to requirement analysis.

Return to Requirement instead of reading `index.md` when the current item lacks
required contract, actual code conflicts with it, the user changes scope/AC, or
the queue needs replanning. Requirement owns the full-contract read and produces
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

A Requirement/Bugfix/source-article run may perform a simple read directly or
delegate complex read-only evidence while retaining ownership. Execute delegated
`read` in the selected mode, return evidence, and do not infer change permission.

Execution:

- `current.md` is the sole active pointer; do not add another in-progress marker.
- Update task state to `in-progress` when work starts.
- Work only the current vertical slice and its declared dependencies.
- A blocked item records the blocker and sets task state `blocked`; do not skip
  ahead unless the queue explicitly identifies another runnable item.

After a queue item:

- Run declared verification before `done`, but report results/logs only in chat.
- Append only the significant state/decision transition to `history.md`.
- Advance previous/current/next and queue counters in `current.md` in the same patch.
- If no current item remains, set task `done`. Otherwise advance next to current,
  re-run the validator, load only the new current item, and continue in the same
  requirement run without asking the user to say continue.
- Context compaction resumes from the exact current window and is not a
  stop condition. Stop after a valid checkpoint only for explicit stepwise/pause intent or a real
  blocker, approval/input, safety boundary, contract/scope change, or no runnable
  item.
- Do not persist command output, pass/fail details, or completion evidence.

For porting, requirement scope/AC remain in req-process; cross-process owns only
porting magnitude, equivalence, and port execution progress.
