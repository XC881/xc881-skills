# Cross-Language Understanding

Use for current-slice source->target mapping gaps affecting behavior or design.

## Understand

- Target-language traits: type system, memory model, concurrency model, error model, build/tooling.
- Source/target differences: what has no 1:1 mapping (GC vs ownership, exceptions vs Result, goroutines vs async, etc.).
- Architecture: module boundaries, data flow, entry points, external I/O.
- Target architecture (if the target project already exists): its layering, conventions,
  and extension points. The port lands INTO this, not the source's shape.
- Library map: each key source library -> target equivalent, or "no equivalent, must build / choose".

## Architecture-first

When the target project has an existing architecture, port the source INTO it; do not carry
the source's architecture over. Record each departure from the target architecture with a reason.
If the target is greenfield (no existing architecture), fall back to target-language idioms.

## Derive risks (requirement-analysis reasoning)

Select concrete risks evidenced by the current slice, prioritized:

- Semantics: behavior that depends on source-language specifics (int overflow, nil/None, ordering, precision).
- Concurrency: thread/async model mismatch, shared-state assumptions.
- Memory: lifetime/ownership, finalizers, leaks.
- Error handling: exception vs value-returned errors, panic boundaries.
- Ecosystem: missing/immature target libraries, API surface gaps.

For a blocking language/library fact, delegate one bounded RQ to
`$xc881-solution-research` with the versions, source construct and target constraint.
Request the supported mapping, limitations and next action from primary sources;
stop when the mapping decision is supported. Do not launch a language-wide survey.
