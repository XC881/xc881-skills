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
- infrastructure kept at edges
- core logic testable without real infrastructure
- comments limited to core difficulty

Low-quality signals:

- business rules in UI/controllers/SQL/SDK callbacks
- circular dependencies
- hidden side effects or global mutable state
- God object / 万能 service / 万能 utils
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
