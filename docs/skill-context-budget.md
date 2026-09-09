# Skill Context Budget

xc881-skills controls filesystem-based skill content, not runtime-client internals.

## Owned surfaces

- skill metadata for routing;
- selected `SKILL.md` fast path;
- branch-specific references loaded on demand;
- bounded script output;
- agent compatibility prompt;
- req-process/cross-process current execution window.

Progressive disclosure is the primary context strategy: metadata discovers,
`SKILL.md` executes, and references/scripts load only for the active branch.

Low-token means the smallest sufficient missing instruction/evidence read across
activations and turns that supports effective behavior. It does not mean the smallest knowledge
collection or a quota on useful reasoning. Reuse valid guidance already in context;
reload only missing/changed material. Execute bundled tools without opening their
source/data, and consume bounded outputs with exact expansion for missing detail.
Never discard necessary contracts, safety constraints or source evidence for size.

## Instruction Lifecycle

Reassess applicability each turn, not loading. A complete supplied/injected body
counts as available; metadata, notices, paths and loaded markers do not. Reuse
available applicable entry/ref instructions unless a relevant change is known.
Acquire only missing or known-changed required content, or explicit rereads,
using exact selected paths. A new concern does not reload a covered router.
Higher-priority invocation requirements win, but an invocation need not be followed
by a duplicate manual file read of its supplied body.

After compaction/delegation, check instruction sufficiency in the actual context.
A new child receives needed instructions or reads them, not a parent's loaded
flag. Return bounded evidence to the same owner. Queue/code/evidence freshness
is independent; static-rule reuse never authorizes acting on stale mutable state.

No runtime loaded ledger, hash polling, mandatory shared ref, cache/proxy or host
hook. Skills cannot implement host request deduplication or guarantee retention.
Distinguish metadata, notices, tool reads and injected bodies. Retaining one body
does not make later requests zero-token; cache statistics do not prove deduplication.

## Repository limits

```text
SKILL.md                5,000 chars
skill description        320 chars each
all descriptions       1,650 chars total
agent default_prompt      180 chars
req-process/current.md  1,200 chars
active queue item       3,500 chars
req-process/index.md   10,000 chars
cross-process ledger    3,000 chars
```

Descriptions are the always-discoverable routing surface; their aggregate limit
reduces accidental crowding and forces unique ownership to appear first. Other
limits prevent repository instruction and artifact bloat. They are not token,
cost, latency, or context-window estimates.

## Checks

```bash
python scripts/validate_context_budgets.py --report
python scripts/audit_context_sizes.py dev-notes/req-process/<active-task>
python scripts/audit_skill_loads.py --baseline HEAD
```

The audit compares current-only loading with the legacy previous/current/next
window using character counts from files this repository owns.

The skill-load audit reports six entry sizes and declared branch paths separately
from tool-output bounds and on-disk data. Cases live in
`evals/skill-load-paths.json`; they are not observed agent execution traces.
Its `continuations` describe preconditions, per-turn expected tool reads and
quality criteria across all six owners. The checker validates their shape/paths,
not model compliance, compaction or client injection. Zero declared reads assumes
the required body is actually available and no higher-priority reread is required.
Optional `--encoding <name>` uses an already installed tiktoken tokenizer; its
first encoding load may download vocabulary. There is no automatic installation.
Without it, report characters only. Neither mode measures full sessions or proves
behavioral gains; compare matched real tasks and outputs for those claims.
Use the opt-in procedure in `docs/golden-output-tests.md` for real multi-turn
comparison. Inspect only authorized evaluation traces, not unrelated sessions.
