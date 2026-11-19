# High-Constraint Coding Policy

Use for serious coding, bug fixes, refactors, reviews, production edits, surgical changes, minimal-diff requests, and anti-overengineering risk.

## Rules

1. Bound the task.
2. Read the real implementation path.
3. State current behavior before editing when useful.
4. Define one verifiable success target before editing.
5. If multiple interpretations change behavior, contract, data, permission, or migration, stop and ask or hand off.
6. Choose the smallest maintainable change.
7. Every changed line must trace to user request, bug evidence, verification need, or cleanup caused by this change.
8. Trace all callers, wire/serialization field names, config keys, and existing tests before changing a signature, payload shape, or error contract.
9. Check the project manifest/lockfile before importing any package; never assume an uninstalled dependency.
10. Validate untrusted inputs at boundaries; never swallow errors or mask broken invariants with blind `or {}` / bare catch.
11. Preserve local style; do not improve adjacent code, comments, formatting, names, or structure unless required.
12. Clean only orphans caused by this change; mention pre-existing dead code instead of removing it unasked.
13. Do not add abstraction, flexibility, configurability, feature flag, adapter, plugin system, or generic framework for one known use case unless it removes real coupling, protects a confirmed change axis, or makes core logic testable.
14. If the solution grows larger than the problem, simplify before patching.
15. Verify target behavior, negative/boundary inputs, and non-regression before success claims.
16. If two fixes fail, stop and hand root-cause diagnosis to `$xc881-analysis`.

## Non-trivial design gate (internal pre-edit check)

Before editing non-trivial/risky work, weigh two plausible designs internally across:
- change axis, verifiable target, module responsibilities, and dependency direction (`UI/Controller/Framework -> Use Case -> Domain/Core -> Ports <- Infrastructure`);
- coupling/overengineering risk, performance mode (`yes/no`), and seam test strategy.

Summarize only material design choices or trade-offs in plain Chinese inside `完成内容` / `需要注意`; never dump raw `xc881 设计门禁 / 变化轴 / 性能模式` labels into user-facing output.
