# Solution Research Basis

Repository-level background, not runtime reference.

The Solution branch of `xc881-analysis` activates for standalone technical
research/comparison and when missing external API/standard/version facts block a
safe build, migration, or article claim.

Design rationale:

- normalize rough requests with the shared Spec fields before searching;
- derive explicit and inferred research questions only when they affect a decision or constraint;
- use papers first for principle-level claims and official docs/standards/changelogs/advisories for implementation facts;
- keep output compact (`xc881 调研`), cite only used sources, and emit `对比/推荐` only for real option decisions;
- return bounded evidence to the active branch/skill, or chain into Coding when an implementation request was waiting on that fact.
