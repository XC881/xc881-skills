# xc881 Quality Bar

## 1. Correctness

- Requested behavior is implemented.
- Existing unrelated behavior is not silently changed.
- Edge cases introduced by the change are considered.
- Claims match evidence.

## 2. Scope control

- Diff is limited to the task.
- No unrelated refactors, formatting churn, renames, or dependency additions.
- Abstractions exist only if needed by the current task or a real boundary.
- The solution is small and understandable.

## 3. Integration

- Existing project patterns are followed where valid.
- Interfaces, data contracts, and persistence behavior remain coherent.
- Adjacent tests, types, schemas, callers, and config are updated when required.
- Code looks like it belongs in the repository.

## 4. Boundary quality

- Each module has one main reason to change.
- Business rules are not mixed with framework, database, SDK, HTTP, UI, or filesystem details.
- Side effects are explicit and pushed toward the edges.
- There are no new circular dependencies.

## 5. Clarity and maintainability

- Main behavior is visible without excessive indirection.
- Names explain roles and intent.
- Important state transitions are clear.
- Concision does not rely on dense syntax or magical helpers.
- Local future changes are easier, not harder.

## 6. Testability

- Core logic can be tested without real infrastructure.
- Side effects can be isolated or faked.
- Error paths are testable.
- Unverified areas are called out.

## 7. Comment policy

- New or edited code has no comments unless an allowed exception applies.
- Explanation is placed in the response, not in the patch.
- Existing unrelated comments are preserved to avoid noisy churn.

## 8. Performance discipline

- Efficiency is adequate for the real workload.
- Performance-sensitive choices are justified by evidence or explicit constraints.
- Readability is not traded away for speculative optimization.

## 9. Honesty

- Assumptions are stated.
- Unknowns are surfaced.
- Verification limits are explicit.
- Success is not claimed beyond evidence.
