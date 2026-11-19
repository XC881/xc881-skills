# Changelog

## 3.0.0

- Consolidate `xc881-requirement-analysis`, `xc881-bugfix-research`, and `xc881-solution-research` into unified `xc881-analysis` (Requirement / Bugfix / Solution internal branches; legacy names retained as aliases and safely pruned on `install.sh` upgrade).
- Upgrade routing across all 4 skills, agent shims, and platform prompts to autonomous two-axis selection (`User Intent × Task Readiness/Direction`) with Coding pre-edit readiness checks and automatic Analysis/Porting -> Coding chaining.
- Unify user-facing output contracts onto plain-Chinese structures (`需求结论` / `xc881 诊断` / `xc881 调研` / `完成内容` / `代码结论` / `迁移结论`) and align `xc881-source-article-style` chapter and function-level headings.
- Separate hot per-resume artifact caps (`current.md <= 1,200`, non-terminal queue slice `<= 3,500`) from cold ceilings (`index.md <= 20,000`, `cross-process <= 4,500` with completed-slice roll-up and no item `in-progress`).
- Add machine validation for shared routing passages, namespace-guarded aliases, cross-file `decisions/`/`evidence/`/`cross-process` link integrity, manifest handoffs, reference inventory parity, and installed-skill staleness.

## 2.1.0

- Compress all runtime prompts.
- Integrate Karpathy guardrail into coding.
- Enforce compact validators and trigger policies.
