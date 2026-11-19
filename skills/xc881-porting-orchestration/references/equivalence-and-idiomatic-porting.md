# Equivalence And Idiomatic Porting

## Equivalence is behavioral, not structural

Verify via `$xc881-coding-skills`. Same observable behavior, not same code shape.

Map required inputs/outputs, errors, state, side effects and relevant
ordering/lifetime/encoding to parity checks. Reuse version/config-matched source
fixtures; state nondeterminism.

Methods (pick per case, state which):

- IO/behavior parity: same inputs -> same outputs/errors/side effects across source and port.
- Ported tests: source test suite translated and passing on the port.
- Golden comparison: when the source code is runnable, execute it on boundary + adversarial vectors (empty, zero/negative, non-ASCII UTF-8, max/boundary, malformed/error input) to capture ground-truth outputs rather than mentally computing expected values, then replay against the port.

Report consistent/inconsistent only for checked behavior, with evidence in chat.
Missing coverage is unverified, not equivalent; an unresolved required check or
mismatch blocks completion. Dev-notes stores method and item status, not results.
Structural difference alone is NOT inconsistency.

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
- For skill/process porting, intent fidelity means: each adopted source capability has a target file, each rejected capability has a reason, and target invariants are still true. Record this as an adopt/adapt/reject map before claiming equivalence.

## Idiomatic decision record

For a material semantic/architecture departure, record:

- source paradigm
- target feature used
- why it is better (correctness / readability / performance)
- the parity obligation; report verification evidence in chat, not the ledger

Routine syntax translation needs no separate record. Use idioms for real gains
under Coding's anti-over-engineering guard, never to bypass a parity obligation.
