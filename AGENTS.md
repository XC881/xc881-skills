# AGENTS.md

Principle:

```text
accurate, low-token, effective agent reading
```

Rules:

- `SKILL.md` fast path.
- `references/` runtime only.
- `docs/` maintenance only.
- select skills autonomously from both user intent and actual task readiness/direction (not literal wording or keywords): concrete changes/complex reads enter coding directly; underspecified builds, unconfirmed bugs, or missing external facts start in analysis (or porting for cross-language parity) and chain into coding automatically.
- AI combines requested-read and relevant project complexity: simple exact/local/low-risk reads may stay direct; complex/tracked reads and all writes enter coding.
- selected coding classifies `instant | queue` before project/artifact access, then `read | change`.
- analysis may perform simple reads or delegate complex coding reads, resume from evidence, and hand confirmed writes back automatically.
- queued execution checkpoints, advances, and continues to task terminal; only explicit stepwise/pause intent or a real blocker stops it.
- if the environment compacts context, resume the same active owner/current window automatically.
- analysis owns scope/AC/triage, diagnosis, and external research as three internal branches; branch switches never delegate.
- requirement artifact maintenance stays in the analysis requirement branch and does not recurse into coding.
- `dev-notes/req-process/` is the durable requirement queue; resume from its bounded current window.
- `current.md` is the sole mutable task-state authority; `index.md` does not duplicate `State`.
- requirement branch reuses one semantic req-process match before creating; coding consumes the exact handoff and never searches for latest.
- artifacts keep verification plans and queue state, never verification results/logs.
- `dev-notes/cross-process/` stores porting-specific execution state only.
- no implicit commit/push.
