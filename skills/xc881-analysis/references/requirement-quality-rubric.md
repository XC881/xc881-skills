# Rubric

Good: explicit, scoped, testable (`precondition/input -> observable outcome`), traceable, minimal, honest.

AC bar:
- Cover target behavior, key invalid/rejected/failure inputs, and non-regression guarantees on existing paths.
- Never accept untestable filler (`正常处理 / 体验友好 / 合理提示 / 性能良好`) without a concrete observable behavior or threshold.
- Falsify broken or XY user premises with repo/platform evidence before drafting FR/AC.

Good grilling: one decision at a time; repo facts researched first; user choices separated from agent inference; recommended answer + fallback supplied.

Good tracker triage: label transition justified; Agent Brief behavior-oriented; tracker mutations separated as executed/planned/skipped.

Bad: inferred as fact, vague AC, validating an infeasible premise, contradictory requirements, hidden dependency, scope creep, many questions, asking for discoverable facts, code before requirement.
