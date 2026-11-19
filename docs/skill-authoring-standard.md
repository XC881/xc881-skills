# Authoring

Principle: accurate, low-token, effective agent reading.

## Runtime shape

- `SKILL.md` is the fast path: role, trigger, reference index, workflow, output, hard rules.
- `references/` are runtime-only support files. Load only when the task branch needs them.
- `docs/` are maintenance-only. Do not rely on docs for runtime behavior.
- Keep each meaning in one authoritative place; link to it instead of repeating it.
- Optimize the smallest sufficient missing read across turns, not the number of useful
  capabilities stored on disk. Reuse valid in-context rules/evidence. Execute data
  tools and return locatable summaries; expand complete needed fields, not a dump.
- Each self-contained entry states supplied-body reuse and missing/known-changed
  rule acquisition briefly. Replace overlapping prose; do not add a mandatory
  shared loading ref, per-turn ledger or file polling. Metadata/markers alone are
  not instructions. User rereads and higher-priority invocation rules still win.
- Compact output by default; write large artifacts to files and report path + verification.
- `dev-notes/` is the preferred durable task-note root; requirement state uses `req-process/` and porting-specific state uses `cross-process/`.

## Invocation

- Select skills autonomously from both user intent and actual task readiness/direction, not literal phrasing. Direct `$skill-name` calls remain valid, and natural requests without `xc881` route automatically: concrete edits enter Coding directly, while underspecified builds, unconfirmed bugs, or cross-language migrations start in Analysis or Porting and chain into Coding without requiring the user to script steps.
- Implicit routing chooses the minimum sufficient skill set. A skill earns
  activation only when its unique final outcome or reusable contract changes the
  result; ordinary model capability is not a reason to wrap the task in a skill.
- Front-load descriptions with the primary outcome, when to use, and when not.
  Do not spend discovery metadata on `Intent-routed`, invocation boilerplate, or
  synonym piles. Docs examples are illustrations, not the match table.
- One skill owns the active phase. Incidental subtask words never create a second
  owner; bounded delegation returns to the original owner.
- Route reads from both requested-read complexity and relevant project coupling. Simple exact/local/low-risk reads may stay direct; complex/tracked reads and all writes enter Coding. Project size alone is insufficient.
- Selected Coding classifies `instant | queue` before opening project/execution-artifact files, then `read | change`.
- If scope/AC/lifecycle/root cause is unclear, the matching analysis skill retains ownership. It may perform a simple read, delegate a complex Coding read, resume from evidence, and hand confirmed writes back automatically.
- Requirement artifact maintenance is not project execution and does not recursively trigger Coding.
- A description is the host discovery surface: requested outcome, when to use,
  and when not. Avoid synonym piles.
- Agent prompts are compatibility shims, not a second workflow authority. Keep
  provider variants behaviorally identical and point execution to `SKILL.md`.
- Provider custom instructions preserve only global routing/safety boundaries;
  branch workflow belongs to the selected skill and reference.
- Recovery/delegation reuses available rules and reacquires missing ones in the
  actual context. Never force an entry reload merely for another turn.
- Compare effective installed content before rollout; equal version strings do
  not prove parity. Preserve independent installed changes and unrelated skills.
- Split a skill only when it earns a trigger boundary, reduces runtime context, or prevents rushing a fuzzy step.

## Instruction quality

- Assume the model already knows general software engineering. Keep only xc881
  contracts, project-specific policy, or failure-preventing behavior.
- Make expensive branches conditional. A fact check need not compare products; a
  diagnosis-only request need not change code; supplied evidence need not be read
  again; small non-goal work need not create durable state.
- Prefer checkable completion criteria over vague advice.
- Ask only blocking questions; look up facts from repo/docs/research before asking.
- Separate facts, inference, decisions, and recommendations.
- Use strong leading terms consistently: scope, AC, handoff, seam, equivalence, evidence.
- State positive target behavior. Use prohibitions only for hard guardrails and pair with the desired action.

## User-facing output

- Durable artifacts keep structured agent fields; user chat translates them into plain conclusions, impact, completion criteria, decisions, next action, and record paths.
- Persisted work must not dump internal labels or repeat the full plan in chat.
- Chat-only work remains self-contained because no artifact carries omitted detail.
- Omit irrelevant optional headings; a blocking decision always includes a recommendation and safe fallback/stop behavior.
- Human-readable presentation must not weaken traceability, acceptance criteria, stop boundaries, equivalence evidence, or machine validation.

## Durable artifacts

- Keep one authority per field: req-process owns scope/AC; cross-process owns porting magnitude/equivalence/progress.
- Before the document gate, Requirement resolves explicit/context identity, then uses bounded path-only candidate search plus semantic comparison. Reuse one match, ask once for multiple matches, and create only when none match.
- Reopened work appends queue IDs after the old tail and hands Coding exact artifact/current/next/blockers. Coding never searches directories or chooses latest.
- Separate stable contract (`index.md`) from mutable checkpoint (`current.md`).
- Coding classifies `instant | queue` before project/artifact reads and `read | change` independently.
- Analysis/writing-delegated Coding reads return only bounded evidence; they never infer change permission or take analysis/prose ownership.
- Queue checkpoints are recovery points. After verification, advance current and continue through runnable items to task terminal without asking for “continue”.
- After context compaction, preserve the active owner and exact current window,
  then resume the same skill chain automatically.
- Reusing static skill instructions does not establish fresh code, external
  evidence or mutable current state. Genuine missing task identity is a blocker;
  never infer a latest task or trust a loaded marker after context loss.
- Stop between items only for explicit stepwise/pause intent or a real blocker, approval/input, safety, contract/scope change, or no runnable item.
- Instant Coding never scans task-note directories. Queue Coding requires an explicit path/handoff or one unambiguous active context.
- Normal Coding continuation reads `current.md` plus its current queue item only; previous requires an explicit evidence/dependency link and next waits until advancement. `index.md` is for requirement creation/audit.
- Non-terminal queue items must be self-contained with goal, relevant scope/AC, targets, constraints, and verification.
- Context limits: hot per-resume caps on req `current.md` (1,200 chars) and active queue item (3,500 chars); ceilings on cold `index.md` (20,000 chars) and `cross-process` ledger (4,500 chars, rolling up completed slices).
- Move only bounded requirement research to linked evidence; verification output, pass/fail details, and logs remain in chat.
- A durable visual contract is created only after its gate passes under
  `dev-notes/design-system/<slug>/`; Requirement owns writes, Coding consumes an
  exact master/override handoff, and ordinary one-surface work creates none.
- New/reworked UI without a reusable system generates a project-specific candidate
  by default; generation is not persistence or authority. Full pinned frontend data
  stays on disk; the CLI returns bounded evidence and named fallbacks, never proof.
- Defer unused tools when supported; otherwise expose only the next action's tool
  class, cap results, and keep decision impact instead of raw output.
- Significant accepted decisions are append-only and superseded rather than rewritten.
- Progress stores queue/current/blockers, not subjective percentages or validation results. Keep verification plans in artifacts and report actual results/logs in chat.
- Provide a validator for any artifact state machine or linked-file contract, but
  reserve it for explicit audit, recovery, and CI rather than normal authoring.

## Pruning

- Delete no-op lines that do not change agent behavior.
- Remove sediment: stale examples, duplicated policy, and old branches that no longer trigger.
- Push branch-specific reference down to `references/`; pull must-have rules back into `SKILL.md`.
- Validate repository/skill edits and audit trigger/eval coverage; never turn
  normal artifact creation or checkpointing into a validator-led write loop.
