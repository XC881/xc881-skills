# Project Optimization Workflow

## New project

Goal: reduce engineering entropy from day one.

1. Define project boundary.
2. Identify likely change axes:
   - business rules
   - UI
   - auth and permissions
   - database schema
   - external providers
   - payments, messaging, search, AI providers
   - deployment environment
   - observability
3. Define dependency direction before directory structure.
4. Define core domain concepts and use cases.
5. Add ports only for real volatility, side effects, or testability.
6. Put infrastructure behind adapters.
7. Plan tests by layer.
8. Define error handling, validation, configuration, logging, and migration policy.
9. State what will not be built in the first version.

## Legacy project

Goal: reduce maintenance cost through small safe changes, not a blind rewrite.

1. Inspect entry points, call chains, and high-change files.
2. Identify large files/functions, circular dependencies, duplicated business rules, framework/database/SDK leakage, missing tests, and brittle configuration.
3. Rank issues as P0/P1/P2/P3.
4. Add or identify behavior protection tests before risky movement.
5. Extract pure logic.
6. Isolate side effects.
7. Introduce interfaces only where they reduce coupling.
8. Remove circular dependencies.
9. Clean naming, folders, and duplicated business rules.
10. Keep each step small, reversible, and verifiable.
