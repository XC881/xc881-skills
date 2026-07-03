# Equivalence And Idiomatic Porting

## Equivalence is behavioral, not structural

Verify via `$xc881-coding-skills`. Same observable behavior, not same code shape.

Methods (pick per case, state which):

- IO/behavior parity: same inputs -> same outputs/side effects across source and port.
- Ported tests: source test suite translated and passing on the port.
- Golden comparison: recorded source outputs replayed against the port.

State a consistent / inconsistent verdict with evidence. Structural difference alone is NOT inconsistency.

## Three-layer rule (order fixed)

1. Hard invariant: behavioral equivalence. Never relaxed.
2. Soft preference: within (1), use the target project's existing architecture over the source's shape.
3. Soft preference: within (1) and (2), prefer target-language idioms/strong features over literal transliteration.

Correctness first, then target architecture, then idiom. A more elegant or better-layered rewrite that changes behavior is wrong.

## Abstract-intent exception (guarded)

When magnitude is "architecture abstract intent" (borrow the design, no source code moved line-by-line),
there may be no 1:1 source behavior to reproduce. Only then, equivalence downgrades from IO/behavior
parity to intent/design fidelity. Guardrails:

- Applies ONLY to the abstract-intent magnitude, and ONLY when no source code is transliterated.
- State the downgrade explicitly with the reason; never use it to skip a check that is actually feasible.
- Any concrete logic that IS ported still holds the hard behavioral invariant.

## Idiomatic decision record

For each place that departs from line-by-line translation, record:

- source paradigm
- target feature used
- why it is better (correctness / readability / performance)
- evidence behavior stays equivalent

Do not use target features to show off. Idiomatic only for real gains, under the coding skill's anti-over-engineering guard.
