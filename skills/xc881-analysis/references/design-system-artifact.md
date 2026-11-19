# Design-System Artifact

Use only for a durable visual contract. A generated greenfield baseline is a
candidate, not automatic persistence or a replacement for project/user authority.

## Gate

Create `dev-notes/design-system/<slug>/` only when the user asks, or a new or
reworked visual system must coordinate two or more surfaces, survive sessions,
or guide an active queue. One-surface work and evidence-complete changes keep
their decision in the current Design Read and create nothing.

## Shape

```text
dev-notes/design-system/<slug>/
  MASTER.md                 stable visual contract, <=3,000 chars
  surfaces/<surface>.md     optional deviation only, <=1,200 chars
  history.md                optional significant accepted changes
```

`MASTER.md` records only: surface/audience, evidence sources, precedence over
or under existing code, semantic color/type/spacing roles, component/state
rules, responsive/motion limits, asset ownership, and explicit exclusions.
An override contains only an approved difference from its master, never a copy.

## Write And Handoff

Requirement derives the whole master or override, then writes it once under
`dev-notes/`; no normal validator or generated project-root `design-system/`
directory. When Coding delegates bounded Design Read evidence and the gate passes,
Requirement creates it without user reconfirmation. A changed scope, brand, or
existing-code conflict returns here.

Accept bounded generator evidence after checking task fit, locale, accessibility,
and stack/dependency constraints. Preserve exact sources and unresolved fallback;
do not copy marketing sections into apps or treat catalog obligations as verified.
The Coding CLI can explicitly persist a bounded `Status: proposal` master via
`--design-system --persist --project-root <project> --slug <name>` without overwrite.
This is optional: normal Requirement authoring writes the accepted contract once,
not a generated proposal followed by mandatory validator/rewrite cycles. A proposal
must be reconciled into an accepted contract before handing it to execution.

Requirement hands Coding the exact `MASTER.md` path and optional surface path.
Coding never scans `dev-notes/design-system/`, loads a surface file only when the
current concern names it, and reports observed code conflicts without changing
the visual contract itself.

## Lifecycle

Do not create a second master for a semantic match. Reuse the exact handed-off
master, append a concise accepted change to optional history when needed, and
leave verification results/logs in chat. Explicit audit or observed corruption
may use a maintenance check; normal creation and updates are write-first.
