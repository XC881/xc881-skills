# Matt Pocock Skills Porting Map

Source inspected: `/home/xia/AMyCode/Projects/Other/skills/mattpocock_skills`.

Porting mode: abstract-intent. The goal is to preserve useful capabilities while keeping xc881's core shape: intent-routed analysis, compact fast paths, runtime references, coding as execution, no implicit commit/push.

## Adopted or adapted

| Source capability | xc881 landing point | Porting decision |
| --- | --- | --- |
| Predictable skill writing: invocation load, progressive disclosure, leading words, pruning | `docs/skill-authoring-standard.md` | Adopt as maintenance standard, not runtime bloat. |
| Grilling discipline: ask one decision at a time, discover facts instead of asking, stop before acting | `xc881-requirement-analysis` references | Adapt to xc881's one-blocking-question and intent-routed analysis model. |
| Primary-source research and cited findings | `xc881-solution-research` references | Adopt; large findings become a bounded Markdown artifact, not a huge chat response. |
| Tight bug feedback loop before hypothesis | `xc881-bugfix-research` references | Adopt as diagnosis policy; bugfix skill still plans only and hands coding to execution. |
| TDD seam discipline, anti-tautology, mock only at system boundaries | `xc881-coding-skills` quality standard | Adopt into coding execution and semantic rubric. |
| Deep module vocabulary: module/interface/seam/adapter/depth/leverage/locality | `xc881-coding-skills` quality standard and project optimization | Adopt, but keep xc881 dependency-direction rules. |
| Throwaway prototype as design evidence | `xc881-coding-skills` project optimization | Adapt as optional exploration for uncertain UI/logic, never default production code. |
| Handoff/resume artifacts instead of giant responses | coding default policy, solution output, docs handoff contract | Adopt using existing compact-output and plan-file habits. |
| Abstract-intent equivalence | `xc881-porting-orchestration` equivalence reference | Adopt as guarded downgrade only when no source code is transliterated. |

## Rejected

| Source capability | Reason |
| --- | --- |
| Claude plugin/docs publishing rules | Out of scope for xc881 skill runtime and install format. |
| Personal Obsidian and article-editing setup | User-specific source workflow; not generally useful to xc881. |
| Deprecated source skills | Superseded by stronger source skills or conflicts with xc881 compactness. |
| User-invoked router that hides all skill choices | xc881 now uses intent-routed skill selection plus manifest/evals; no separate router skill is needed. |

## Source skill coverage

| Source skill(s) | Disposition |
| --- | --- |
| `writing-great-skills` | Adopted into `docs/skill-authoring-standard.md`. |
| `grilling`, `grill-me`, `grill-with-docs` | Adapted into requirement fact-vs-decision, one-question, and term-clarity rules. |
| `to-prd`, `to-issues` | Adapted into requirement AC, handoff, vertical-slice, and tracer-bullet breakdown rules. |
| `domain-modeling`, `codebase-design`, `improve-codebase-architecture` | Adapted into term/decision handoff, deep-module vocabulary, seam discipline, and project optimization. |
| `diagnosing-bugs` | Adopted into bugfix tight-loop, minimization, hypothesis, and instrumentation cleanup rules. |
| `tdd`, `code-review`, `implement` | Adapted into coding seam tests, anti-tautology, boundary mocks, two-axis review, and final verification rules. |
| `research` | Adopted into primary-source and bounded artifact research rules. |
| `prototype` | Adapted into optional throwaway evidence for uncertain UI/logic questions. |
| `handoff` | Already aligned with xc881 handoff; strengthened through artifact/plan-file discipline. |
| `teach`, `writing-beats`, `writing-fragments`, `writing-shape` | Partly adapted into writing grounding, one-block growth, and raw-material handling; full teaching workspace rejected as out of scope. |
| `setup-matt-pocock-skills`, `triage`, `ask-matt` | `triage` and tracker setup are adapted into `xc881-requirement-analysis`; `ask-matt` router remains rejected because xc881 uses native intent routing. |
| `wayfinder`, `loop-me`, `wizard`, `claude-handoff` | `wayfinder` map/ticket ideas are adapted into `xc881-requirement-analysis`; the other direct workflows remain rejected. |
| `scaffold-exercises`, `git-guardrails-claude-code`, `migrate-to-shoehorn`, `setup-pre-commit`, `obsidian-vault`, `edit-article` | Rejected as project/personal/tool-specific. |
| `design-an-interface`, `qa`, `request-refactor-plan`, `ubiquitous-language` | Rejected as deprecated source skills; useful parts are covered by newer adapted capabilities. |

## Equivalence check

- Preserved intent: source skills' useful constraints now appear as xc881 docs/references/evals.
- Deliberate departure: no Claude-specific hook behavior and no broad automatic analysis trigger.
- Verification target: `python scripts/validate_all.py` plus diff audit against this map.
