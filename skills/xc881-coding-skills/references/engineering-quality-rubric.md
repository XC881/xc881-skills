# Engineering Quality Rubric

A good change is correct, data-safe, scoped, readable, locally consistent, modular, decoupled, testable, verified, and honest about assumptions.

Check:

- requested behavior encoded directly
- assumptions surfaced only when behavior-changing
- one verifiable success target exists
- every changed line traces to request, bug evidence, verification need, or cleanup caused by this change
- no unrelated adjacent cleanup
- no unrequested feature/flexibility/configurability
- no single-use abstraction without real coupling/change/testability reason
- invalid states hard to represent
- state transitions explicit
- boundary inputs validated
- errors handled intentionally
- permission/security visible
- one main reason to change per module
- deep module shape: small interface, meaningful hidden behavior, clean seam
- tests exercise public seams and observable behavior, not internals
- infrastructure kept at edges
- core logic testable without real infrastructure
- comments limited to core difficulty

Low-quality signals:

- business rules in UI/controllers/SQL/SDK callbacks
- circular dependencies
- hidden side effects or global mutable state
- God object / 万能 service / 万能 utils
- shallow pass-through module with interface as complex as implementation
- tautological tests or mocks of internal collaborators
- unstable public contracts
- weak validation or swallowed errors
- speculative abstraction
- single-use abstraction without real change axis
- unrelated cleanup or adjacent refactor
- unrequested flexibility/configurability
- performance cleverness without requirement, measurement, or tests

Performance-mode checks:

- objective stated
- correctness preserved
- complexity localized
- trade-off reported
- tests/benchmarks/profiling provided when practical

Review mode:

- Standards axis: repo rules + xc881 quality smells.
- Spec axis: requested behavior / AC / issue / PRD.
- Keep axes separate; a standards-clean change can still implement the wrong thing.

Tracker/PR mode:

- Treat Agent Brief, issue AC, and out-of-scope as the implementation contract.
- For PR finish work, review the existing diff first; preserve correct contributor intent.
- Do not change labels/comments/close tracker items unless explicitly asked; report planned tracker ops separately.
