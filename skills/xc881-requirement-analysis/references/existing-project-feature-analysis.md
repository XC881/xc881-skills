# Existing Project Feature Analysis

Use when the user wants to add or change functionality in an existing product/codebase.

## Required focus

Before planning implementation, identify:

- current behavior
- affected user flows
- affected modules/screens/API endpoints
- existing data model and lifecycle states
- existing permissions
- external integrations
- compatibility constraints
- release and migration constraints
- tests that must protect current behavior
- must-not-regress behavior

## Existing project output must include

```text
1. Current project context
2. Feature goal
3. Explicit requirements
4. Inferred requirements
5. Affected areas
6. Existing behavior to preserve
7. Data/state/migration impact
8. Acceptance criteria
9. Regression test targets
10. Minimal safe implementation plan
```

## Special risks

Existing projects need extra care for:

- backward compatibility
- data migration
- feature flags
- phased rollout
- API contract changes
- permission model changes
- existing user data
- existing tests and CI
- hidden coupling
- production observability
