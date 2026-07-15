# Authoring

Principle: accurate, low-token, effective agent reading.

## Runtime shape

- `SKILL.md` is the fast path: role, trigger, reference index, workflow, output, hard rules.
- `references/` are runtime-only support files. Load only when the task branch needs them.
- `docs/` are maintenance-only. Do not rely on docs for runtime behavior.
- Keep each meaning in one authoritative place; link to it instead of repeating it.
- Compact output by default; write large artifacts to files and report path + verification.
- `dev-notes/` is the preferred durable task-note root; requirement state uses `req-process/` and porting-specific state uses `cross-process/`.

## Invocation

- All skills are intent-routed. Direct `$skill-name` calls remain valid, but clear user intent without `xc881` may trigger the matching skill.
- Implicit routing chooses the minimum sufficient skill set. A skill earns
  activation only when its unique final outcome or reusable contract changes the
  result; ordinary model capability is not a reason to wrap the task in a skill.
- Front-load descriptions with the primary outcome and boundaries. Do not spend
  discovery metadata on `Intent-routed`, invocation boilerplate, or synonym piles.
- One skill owns the active phase. Incidental subtask words never create a second
  owner; bounded delegation returns to the original owner.
- Route reads from both requested-read complexity and relevant project coupling. Simple exact/local/low-risk reads may stay direct; complex/tracked reads and all writes enter Coding. Project size alone is insufficient.
- Selected Coding classifies `instant | queue` before opening project/execution-artifact files, then `read | change`.
- If scope/AC/lifecycle/root cause is unclear, the matching analysis skill retains ownership. It may perform a simple read, delegate a complex Coding read, resume from evidence, and hand confirmed writes back automatically.
- Requirement artifact maintenance is not project execution and does not recursively trigger Coding.
- A description is a trigger surface. Use intent words the user actually says; avoid synonym piles.
- Agent prompts are compatibility shims, not a second workflow authority. Keep
  provider variants behaviorally identical and point execution to `SKILL.md`.
- Provider custom instructions preserve only global routing/safety boundaries;
  branch workflow belongs to the selected skill and reference.
- Skills define recovery state only; environment context management is outside
  this repository.
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
- Queue checkpoints are recovery points, not confirmation points. After verification, advance current and continue through runnable items to task terminal without asking for “continue”.
- Context compaction is not a confirmation point: preserve the active owner and
  exact current window, then resume the same skill chain automatically.
- Stop between items only for explicit stepwise/pause intent or a real blocker, approval/input, safety, contract/scope change, or no runnable item.
- Instant Coding never scans task-note directories. Queue Coding requires an explicit path/handoff or one unambiguous active context.
- Normal Coding continuation reads `current.md` plus its current queue item only; previous requires an explicit evidence/dependency link and next waits until advancement. `index.md` is for requirement creation/audit.
- Non-terminal queue items must be self-contained with goal, relevant scope/AC, targets, constraints, and verification.
- Context hard limits: req current 1,200 chars, non-terminal queue item 3,500, index 10,000, cross-process ledger 3,000.
- Move only bounded requirement research to linked evidence; verification output, pass/fail details, and logs remain in chat.
- Defer unused tools when supported; otherwise expose only the next action's tool
  class, cap results, and keep decision impact instead of raw output.
- Significant accepted decisions are append-only and superseded rather than rewritten.
- Progress stores queue/current/blockers, not subjective percentages or validation results. Keep verification plans in artifacts and report actual results/logs in chat.
- Provide a validator for any artifact state machine or linked-file contract.

## Pruning

- Delete no-op lines that do not change agent behavior.
- Remove sediment: stale examples, duplicated policy, and old branches that no longer trigger.
- Push branch-specific reference down to `references/`; pull must-have rules back into `SKILL.md`.
- Validate after edits and audit trigger/eval coverage.
