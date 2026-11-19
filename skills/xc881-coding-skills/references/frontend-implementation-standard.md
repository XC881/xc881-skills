# Frontend Implementation Standard

Use for visible layout/component/state changes. Reuse inspected code and guidance;
automatically load only the next reached concern, with no user handoff:

- Layout, responsive geometry or mobile navigation -> `./references/frontend-layout-and-platform.md`.
- Palette, typography, content hierarchy or media -> `./references/frontend-visual-system-and-content.md`.
- Form/component states, semantics or accessibility -> `./references/frontend-states-and-accessibility.md`.
- Animation, scroll work or rendering performance -> `./references/frontend-motion-and-performance.md`.
- Unresolved design decision -> `./references/frontend-design-intelligence.md`.
- Supplied image/assets, redesign/visual QA, or special patterns -> the matching
  route in `./references/frontend-routing-and-design-read.md` already in context.

Paths resolve from the Coding skill root. These are branches, not a checklist of
files to read. Rules still in context remain active; a loaded marker alone is not
their content. Leaves do not restart this router; reacquire missing needed rules.
Scale verification to the affected states, viewports and themes.

## Architecture And Dependencies

- Inspect affected entry points, ownership, component boundaries, token/style
  source, data states and installed packages before editing; do not rediscover
  unchanged evidence.
- Views render supplied state and call narrow actions. Domain validation,
  permissions and data rules stay at application boundaries.
- In React/Next, keep static layout server-friendly. Isolate client input/browser
  APIs/animation in small leaves with cleanup; no React state per animation frame.
- Reuse the project's installed icon family or clean accessible inline SVG; never
  assume Lucide/Phosphor is installed, and map catalog icon names to the project's
  actual icon source. Keep weight, size, accessible names and labels consistent;
  never hand-draw familiar glyphs.
- Check the manifest before importing a package; assume no Motion, GSAP, Tailwind,
  font, design system or image library. No routine code comments.

## Pre-Flight

Preserve the existing system or its justified exception. Check truthful content,
unclipped controls, text fit, no overlap/overflow and stable media. Plan verification for affected
states, keyboard flow, responsive behavior, themes and reduced motion only.
