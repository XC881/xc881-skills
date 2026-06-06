# Engineering Quality Rubric

A good change is correct, data-safe, scoped, readable, locally consistent, modular, decoupled, testable, verified, and honest about assumptions.

Check:

- requested behavior encoded directly
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
- performance cleverness without requirement, measurement, or tests

Performance-mode checks:

- objective stated
- correctness preserved
- complexity localized
- trade-off reported
- tests/benchmarks/profiling provided when practical
