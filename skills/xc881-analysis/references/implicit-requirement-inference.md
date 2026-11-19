# IR

Infer only needs whose omission changes scope, AC, or material risk. Check relevant
prerequisites/dependencies, consequences, state, permissions, data/failure paths,
audit, notification, migration, NFRs and abuse cases, not every category.

Fact vs premise vs decision:

- Premise / XY check first: verify user assumptions against repo contracts and platform/protocol capabilities. If a requested mechanism cannot achieve the user's real goal (or already exists / breaks an invariant), surface that evidence and re-anchor Goal/AC on the real outcome instead of locking scope around a broken premise.
- Reuse applicable repo/docs/research evidence; inspect only missing or conflicting facts.
- If it is a product/domain decision, ask at most one blocking question with the recommended answer + safe fallback. Delegation does not waive it for product-visible values users may prefer differently (ratios, thresholds, limits, pricing): ask once with a default recommendation, then proceed on the fallback if unanswered. Technical/structural-only choices (stack, module layout, persistence) may proceed as documented `Decision:` records instead of a question.
- Challenge vague or conflicting terms; propose one canonical term when it affects AC/scope.
- Tie each IR to its triggering evidence and affected AC/risk. An inference does
  not authorize scope growth; unresolved consequential choices block Coding handoff.

```text
IR-*:
why:
confidence: H|M|L
confirm: yes|no
```
