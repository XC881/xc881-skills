# Requirement Process Artifact

Use `dev-notes/` as the preferred xc881 note root; Requirement artifacts live at `dev-notes/req-process/<YYYYMMDD>-<task-slug>/`.
## Reuse Before Gate
- Prefer an explicit artifact path or one unambiguous artifact in conversation.
- If persistence or implementation handoff is likely, run
  `python <skill-dir>/scripts/find_req_process_candidates.py <project-root> <identity terms>` (ships with the skill); it returns paths only. Clearly chat-only lightweight analysis does not scan the directory.
- Read only plausible candidates and compare the request to their goal and
  authority surface. Keywords or newest-directory order never decide identity.
- Reuse one semantic match, ask one blocking selection question for multiple
  plausible matches, and apply the normal gate only when no match exists.
## Gate

- User requests a document: create it.
- User rejects a document: do not create it; report persistence risk.
- When silent, create one for multi-turn/handoff work, 3+ verifiable items,
  cross-module contracts, migration/data/permission/security/rollout risk,
  external research/hard-to-reverse decisions, PRD/tracker breakdown, project
  optimization, or other long-running implementation.
- Otherwise keep the result in chat and report `Artifact: none + reason`.
## Shape

```text
<task>/index.md        stable contract, ceiling 20,000 chars
<task>/current.md      resume capsule, max 1,200 chars
<task>/history.md      append-only completion/block/resume/reopen/terminal transitions
<task>/queue/Q-NNN-*.md verifiable slice; non-terminal max 3,500 chars
<task>/decisions/D-NNN-*.md optional append-only significant decisions
<task>/evidence/RQ-NNN-*.md optional bounded research
```

Machine fields (exact `Name:` lines the audit validator parses):
- index.md: `ID: <task-id>`; never a `State:` line.
- current.md: `Task:` = index `ID:` verbatim (not a title); `State:` `Previous|Current|Next: none | queue/Q-NNN-*.md` paths;
  `Progress:`/`Blockers:`/`Last completed:`/`Next action:` summaries (last two non-empty while active).
- queue item: `ID: Q-NNN` (= filename prefix) `Status:` `Previous|Next: none | Q-NNN` **bare
  IDs — never paths**; `Blocked by: none | Q-NNN,...`; non-terminal keeps the five `##` execution sections.
- history.md: one `Q-NNN: old -> new` per transition; never empty.

Size rule: hard caps bound only per-resume reads — `current.md` and the current
queue item (3,500 overflow means split the slice). Cold files keep only the
`index.md` 20,000 ceiling; spill stable detail into decisions/evidence.

Task state: `draft | ready | in-progress | blocked | done | cancelled | superseded`;
queue state: `pending | ready | blocked | done | skipped`. `current.md` is the sole task-state/active-item authority; never duplicate mutable `State` in `index.md` or add another in-progress marker.
A `blocked` task must point `Current` at an item whose `Status: blocked` (and a
`blocked` item requires task `State: blocked`); terminal states point `Current/Next: none`.

Progress stores queue done/total, current item, and blockers only. Verification
results/logs stay in chat/tool output; dev-notes stores the verification plan.
## Resume + Update

`index.md` is the stable authority. Requirement reads it by default for a resolved
artifact, scope/AC/out-of-scope changes, audit, or repair, then loads the current
window as needed. Full scans stay audit/repair-only. Coding does not read `index.md`
during normal continuation. Before artifact reads, Coding classifies:

- instant: no explicit path/handoff and no unambiguous active context; skip all
  req-process/cross-process reads.
- queue: explicit path/handoff or one unambiguous active task; read `current.md`
  and its current queue item only.
- ambiguous: ask one blocking artifact-selection question; never scan and guess.

For active tasks, `current.md` must keep non-empty bounded `Last completed` and
`Next action` summaries. Previous loads only through an explicit current-item
evidence/dependency link; next loads after advancement makes it current.
Each non-terminal queue item carries an index-free local contract with `## Goal`,
`## Contract`, `## Targets`, `## Constraints`, and `## Verification`.
Load linked decisions/evidence only when the current item needs them.
After compaction, keep the active owner and resume the same current window.
Keep `current.md`, accepted contract changes, blockers, and exact evidence paths
durable, then resume automatically.
To reopen, append IDs after the old tail, update `Next`, preserve completed items/history, set terminal state to `ready`, and set previous/current/next to old-tail/first-new/second-new.
Before normal creation/reopen/checkpoint, derive every linked field and write one coherent patch; never use Python to discover ordinary omissions.
Validators are only for explicit audit, observed-corruption repair, or repository/CI maintenance. Then hand Coding the exact `Artifact path / Current / Next / Blockers`.
Append one history line per item-state change: `Q-ID: old -> new`, next current
and task state, in the item/current patch. Task-only transitions need a line; never
replay. Append at EOF (bounded tail only if the tool needs context). Results stay in chat.
