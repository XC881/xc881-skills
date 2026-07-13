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
8. Preserve local style.
9. Do not improve adjacent code, comments, formatting, names, or structure unless required.
10. Clean only orphans caused by this change.
11. Mention pre-existing dead code; do not remove it unless asked.
12. Avoid speculative abstraction.
13. Do not add abstraction, flexibility, configurability, feature flag, adapter, plugin system, or generic framework for one known use case unless it removes real coupling, protects a confirmed change axis, or makes core logic testable.
14. If the solution grows larger than the problem, simplify before patching.
15. Verify before success claims.
16. If two fixes fail, stop and diagnose root cause.

## Non-trivial design gate

Weigh two plausible designs, then report compactly:

```text
xc881 设计门禁:
变化轴 / 成功标准 / 职责拆分 / 边界与文件
依赖方向 / 代码质量风险 / 过度设计风险
性能模式: yes/no
测试策略:
```

Dependency direction:

```text
UI/Controller/Framework -> Application/Use Case -> Domain/Core -> Ports
Infrastructure implements ports.
```
