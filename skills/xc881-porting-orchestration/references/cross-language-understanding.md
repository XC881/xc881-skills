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

## Derive risks (semantic trap audit)

Audit concrete traps active in the current slice, prioritized:

- Numeric: negative integer `div`/`mod` sign (floor vs trunc-toward-zero), int width/signedness/overflow wrap, float rounding mode (`round` half-to-even vs away-from-zero) and `NaN`/`-0.0`.
- Text & bytes: UTF-8 byte length vs UTF-16 code units vs Unicode scalar indexing/slicing, regex `\d`/`\w` Unicode vs ASCII and multiline `$` on trailing `\n`.
- Wire & data: JSON field casing, `null` vs omitted key (`omitempty`/`Option`), map iteration order in hashes/signatures/canonical output, timestamp unit/timezone.
- Control, memory & concurrency: value copy vs shared reference/slice aliasing, nil vs empty collection, exception unwind vs value-returned error/partial mutation, thread/async cancellation and lock reentrancy.
- Ecosystem: missing/immature target libraries, API surface or protocol gaps.

For a blocking language/library fact, delegate one bounded RQ to
`$xc881-analysis` with the versions, source construct and target constraint.
Request the supported mapping, limitations and next action from primary sources;
stop when the mapping decision is supported. Do not launch a language-wide survey.
