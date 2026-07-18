# UI/UX Pro Max Integration

`xc881-coding-skills` uses UI/UX Pro Max as an upstream capability source, not
as an installed runtime skill. Its MIT license permits selective adaptation;
source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

## Runtime Decision

`frontend-design-intelligence.md` loads only after existing project/user/brand/
frame evidence leaves an active frontend decision unresolved. It selects one
concern and returns at most three candidates. Existing Coding routing remains
the only frontend owner.

## Adopt / Adapt / Reject

| Upstream capability | xc881 decision |
| --- | --- |
| Product, style, type/color, chart, platform, UX concern taxonomy | adapt as conditional branches |
| Compact candidate/rationale output | adapt with a three-candidate cap |
| Local product/style/type/chart/platform/UX lookup | adapt as an optional deterministic selector |
| Existing-system and evidence priority | retain and strengthen |
| Full searchable dataset, CLI install, Python path assumptions | reject as runtime dependency |
| Mandatory `--design-system` / `--persist` | reject |
| Reusable visual contract | adapt under `dev-notes/design-system/` and Requirement ownership |
| Vercel code-level UI QA | adapt selectively into current visual QA |
| Anthropic subject-led direction and Microsoft review pillars | adapt only where current refs lack coverage |

## Design-System Notes

No project-root `design-system/` directory is generated. Requirement may create
`dev-notes/design-system/<slug>/MASTER.md` only when its gate passes; Coding
receives an exact path and never discovers masters by scanning directories.

## Compact Selector

`scripts/select_frontend_design.py` contains a small attributable profile map for
product/visual, type-color, data, mobile, and UX concerns. It runs only after
the design-intelligence reference is already active and current evidence still
cannot rank candidates. It accepts one concern plus current terms, returns at
most three deterministic candidates, and has no network or filesystem-write path.
