# xc881 Code Quality Standard

Runtime policy for writing, refactoring, reviewing, or optimizing code.

## Goal

Accurate, stable, modular, readable, testable code whose structure explains the business logic.

Default priority:

1. correctness and data safety
2. observable simple behavior
3. reader clarity
4. logical modularity
5. testability
6. local performance
7. brevity

In explicit performance mode, performance may outrank some maintainability, but never correctness, safety, bounded complexity, or verification.

## Core rules

### Correctness

- Encode requested behavior directly.
- Preserve public contracts unless change is required.
- Validate inputs at boundaries.
- Make invalid states difficult to represent.
- Keep state transitions explicit.
- Handle errors intentionally.
- Keep permission, security, and data-integrity checks visible.

### Simplicity

- Prefer the minimum readable code that solves the requested problem.
- Do not add features beyond what was asked.
- Do not add flexibility or configurability that was not requested.
- Do not add impossible-scenario error handling just to look robust.
- If the solution is much larger than the problem, simplify before patching.
- Every changed line must trace to user request, bug evidence, verification need, or cleanup caused by this change.

### Clarity

- Prefer obvious control flow over clever expressions.
- Use names that reveal domain intent.
- Avoid surprising side effects.
- Keep related logic near its concept.
- Follow local style unless local style is the problem.

### Modularity

Modularize by reason to change:

- domain rules
- use-case orchestration
- validation
- persistence
- external adapters
- UI/presentation
- authorization
- configuration
- observability

Create boundaries only when they reduce coupling, protect volatility, or improve testability.

Do not add abstraction for one known use case unless it removes real coupling, protects a confirmed change axis, or makes core logic testable.

### Boundaries

- Keep domain logic independent from framework, DB/ORM, SDK, HTTP, UI, filesystem, env, real time, randomness, and global mutable state.
- Keep infrastructure at edges.
- Public APIs express intent, not internal steps.
- Serialization/deserialization stays at boundaries.

### Focus

Refactor when one unit mixes validation, business decisions, persistence, network calls, formatting, authorization, logging, or response rendering.

Avoid God objects, 万能 service, 万能 utils, and catch-all managers.

### Data and errors

- Prefer explicit data shapes and typed contracts when available.
- Name lifecycle states explicitly.
- Avoid booleans that hide state machines.
- Separate retryable, user-correctable, and fatal failures.
- Do not swallow failures.
- Debug context must not leak secrets.

### Tests

- Core logic should test without real DB, network, clock, randomness, filesystem, or third-party service.
- Convert each task into one verifiable success target before editing.
- Test behavior, edge cases, permissions, state transitions, and failure paths.
- Add regression tests before risky refactors when practical.
- Report what remains unverified.

### Comments

Default: code explains itself through names, structure, and types.

Comment only core difficulty:

- non-obvious algorithm
- concurrency or memory invariant
- security assumption
- performance trade-off
- protocol/external-system quirk
- migration hazard
- intentionally unusual code

Comment why/invariant, not what the line says.

### Performance mode

Activate only for explicit request, measured bottleneck, or clear hot path.

Rules:

1. State objective.
2. Preserve correctness and safety.
3. Improve algorithm/data structure before micro-optimization.
4. Keep complexity local and named.
5. Keep interfaces stable when possible.
6. Test/benchmark when practical.
7. Comment essential invariant or trade-off.
8. Report maintainability trade-off.

Allowed: local complexity, specialized data layout, caching, batching, explicit resource control.

Forbidden: invisible global state, untested concurrency, undocumented invariants, security/data shortcuts, unbounded cleverness.

## Blockers

Reject or revise code that introduces circular dependencies, hidden global state, duplicated business rules, framework leakage into domain logic, business rules in UI/SQL/SDK callbacks, unstable contracts, swallowed errors, unchecked boundary input, secrets, speculative abstraction, unrelated cleanup, single-use abstraction without a real change axis, unrequested flexibility, or unmeasured premature optimization.
