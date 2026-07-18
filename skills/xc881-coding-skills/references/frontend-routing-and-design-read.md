# Frontend Routing And Design Read

Open first for frontend design: UI creation, visual review/redesign, responsive
work, visible component/state work, asset work, or image-to-code translation.
An explicitly nonvisual UI behavior repair, backend, CLI, config, or
documentation task does not open a frontend reference.

## Just-In-Time Escalation

Automatically load the next reference and continue only when the current work
reaches its concern. Do not wait for another user request or handoff:

1. Unresolved product/visual, type/color, data-display, mobile/platform, or
   concrete UX decision after the First Read -> `frontend-design-intelligence.md`.
2. Code/layout/state implementation -> `frontend-implementation-standard.md`.
3. Supplied visual frame, image-to-code, art direction ambiguity, or asset
   decision -> `frontend-image-reference-workflow.md`.
4. Review/redesign, preservation risk, or screenshot-level confirmation ->
   `frontend-redesign-and-visual-qa.md`.
5. Deliberate visual family, reusable block, or advanced interaction ->
   `frontend-pattern-catalog.md`.

Each loaded reference automatically escalates again when a later listed concern
is reached. Do not preload the set merely because a task is frontend.

## First Read

Inspect only the evidence needed for the surface:

1. Existing routes/screens, components, tokens, styles, assets, and local UI
   conventions.
2. The user goal, audience, device/platform, brand and content constraints.
3. Supported themes, accessibility obligations, localization, and analytics or
   route identifiers that must remain stable.
4. Existing packages before proposing a design system, font, icon, motion, or
   asset dependency.
5. An exact Requirement handoff for `dev-notes/design-system/.../MASTER.md` only
   when its current visual concern needs it; never scan `dev-notes` for one.

For substantial greenfield visual work, redesign, or visual review, state a
compact Design Read before changing code:

```text
Surface / audience / task outcome / existing system or visual direction / key constraint
```

Use optional `variance`, `motion`, and `density` labels only when they resolve a
real design decision. They are not persistent settings and do not require a
ceremonial report for a narrow component change.

Ask one blocking question only when two plausible directions would materially
change the implementation. Otherwise infer from supplied references and project
evidence.

## Surface Branches

| Surface | What shapes the Design Read |
| --- | --- | --- |
| Existing system or product UI | current components, tokens, interaction model |
| Marketing, portfolio, editorial, consumer brand | task audience, brand, content and visual hierarchy |
| Image-to-code or visually underspecified greenfield work | supplied/generated visual source |
| Mobile or touch-dominant UI | platform conventions, safe areas and task flow |
| Existing-site visual review or redesign | preservation contract and observed baseline |
| Non-default visual mechanism | purpose, reduced-motion and performance limits |

This table determines which constraints carry most weight. Marketing composition
rules do not govern dense operational views; product comparability may
legitimately repeat grids, cards, tables, and compact controls when needed.

## System And Scope Rules

- Reuse an existing design system, component family, icon family, type tokens,
  supported theme model, and asset pipeline before introducing alternatives.
- A named platform or regulated context can justify an official design system.
  Inspect the manifest and use a bounded Solution delegate for current official
  guidance when selection is genuinely blocking. Do not hand-copy an official
  system or add a package speculatively.
- An aesthetic is not an official system. Describe web approximations honestly.
- Preserve the user's requested scope. Do not add a new theme, brand identity,
  route, feature, animation library, font, or asset pipeline as visual polish.
- Existing brand colors, typography, legal content, and accessibility wins
  override generic anti-default preferences.
- A handed-off design-system note is a bounded target contract, not proof that it
  overrides real project code; conflicts return to Requirement.

## No-Op And Handoff

If the task is an explicitly nonvisual UI repair, continue the ordinary Coding
path without a frontend reference. If the visual contract, scope, or acceptance
criteria are missing in queue mode, stop and return to Requirement rather than
inventing a redesign brief.
