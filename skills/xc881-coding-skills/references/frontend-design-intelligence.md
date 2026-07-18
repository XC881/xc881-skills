# Frontend Design Intelligence

Frontend routing automatically loads this reference only after it finds that the
active decision cannot be made from the user request, existing project system,
brand, supplied frame, or local surface evidence. It is a bounded decision aid,
not a second frontend owner, design default, or full catalog.

## Evidence First

Existing tokens, components, assets, content, product workflow, platform, and
user constraints win. If they settle the decision, do not open this reference.
Never replace an existing design system, add a package, or invent an identity
because this reference exists.

## Select One Concern

Load only the branch that is unresolved, then return a compact choice: no more
than three candidates, the evidence/reason for each, the rejected default, and
the current decision. Do not read another branch without its concern.

| Concern | Decide | Continue to |
| --- | --- | --- |
| Product or visual direction | hierarchy, density, material, signature, anti-default | implementation, image, pattern, or QA as reached |
| Type or color role | semantic roles, contrast, readable hierarchy | implementation |
| Data display | comparison, trend, composition, distribution, relationship, or status | implementation; pattern only if non-default |
| Mobile/platform | native convention, navigation, safe area, touch flow | implementation or QA |
| UX/QA gap | action hierarchy, feedback, form/recovery, accessibility detail | redesign/visual QA |

The current decision records why a candidate fits this surface, not a universal
style recipe. A source category may inform a choice; it cannot force Tailwind,
Motion, GSAP, a font, icon family, palette, chart library, or product pattern.

If this active branch still cannot rank candidates, run the local selector once:
`scripts/select_frontend_design.py <concern> "<current terms>"`. Its concern is
`product`, `type-color`, `data`, `mobile`, or `ux`; aliases are accepted for
visual, data-display, platform, and QA. It returns at most three candidates and
never writes files; order is deterministic. Do not retry with synonyms or run it when
project/user evidence already decides the choice.

## Durable Visual Contract

When the selected decision must coordinate two or more surfaces, survive a
session, or the user explicitly asks, automatically delegate a bounded visual
contract request to Requirement. If its design-system gate passes, Requirement
writes the master and hands back an exact
`dev-notes/design-system/<slug>/MASTER.md` path. Do not wait for a user handoff,
scan the directory, write a project-root `design-system/`, or create a contract
for a one-surface decision.

With an exact master path, load it only when its current concern is reached.
Load `surfaces/<surface>.md` only if the handoff/current contract names it; it
overrides only its stated fields. An implementation/code conflict returns to
Requirement instead of silently changing the master.

## Source Boundary

This compact taxonomy adapts UI/UX Pro Max concern categories and selected
Vercel, Anthropic, and Microsoft review ideas. The upstream packages, scripts,
full datasets, global triggers, and mandatory design-system generation are not
runtime dependencies. Maintenance provenance is recorded in
`docs/ui-ux-pro-max-integration.md`.
