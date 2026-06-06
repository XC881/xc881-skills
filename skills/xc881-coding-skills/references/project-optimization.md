# Project Optimization

Use after requirements are clear.

## New project engineering

After `$xc881-requirement-analysis`:

1. identify change axes
2. define domain/use-case boundaries
3. keep infrastructure at edges
4. keep domain logic testable
5. avoid speculative abstractions
6. choose minimal stable contracts
7. define verification strategy

## Legacy optimization

1. inspect current behavior and entry points
2. find high-change/high-risk files
3. identify coupling, duplicated rules, framework/SDK leakage
4. identify blockers: hidden side effects, mixed responsibilities, unstable contracts, weak validation, untestable core
5. rank P0/P1/P2/P3
6. add/identify behavior tests
7. extract pure logic
8. isolate side effects
9. introduce interfaces only where they reduce coupling
10. keep each step reversible and verifiable

## Performance optimization

Enter performance mode only when requested, measured, or clearly hot-path.

Prefer algorithm/data-structure improvements before micro-optimization. Always state maintainability trade-off.
