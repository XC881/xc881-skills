# Frontend Pattern Catalog

Open from routing, implementation, image workflow, or visual QA only when a
visual family, reusable block, or advanced pattern is needed. When the selected
pattern reaches code/layout/state work or screenshot-level verification,
automatically load the applicable implementation or visual-QA reference if it
has not already been opened; do not wait for another user request. A pattern is
a means to hierarchy, feedback, narrative, or workflow clarity, never a default
decoration.

If the visual family itself remains unresolved after project and brief evidence,
automatically load `./references/frontend-design-intelligence.md` before selecting a pattern.

## Visual Families

| Family | Use when | Guardrail |
| --- | --- | --- |
| Restrained minimal | product clarity, calm editorial, trust | use hierarchy and media intentionally; do not make it empty or generic |
| Editorial/brand | story, culture, portfolio, premium campaign | preserve scan order and readable content over visual surprise |
| Soft/material | tactile consumer or friendly product surface | use depth sparingly; do not nest containers for atmosphere |
| Industrial/brutalist | explicit technical, archival, or mechanical brief | use real data and semantics, not fake telemetry or status labels |
| Dense operational | repeated scanning, comparison, workflow controls | favor consistency and accessibility over marketing-page variation |
| Mobile-native | touch-first product flow | platform convention, safe area, and reachable navigation win |

Do not force a palette, font, card radius, serif/sans choice, or theme family
from a visual family onto an existing brand.

## Pattern Vocabulary

Choose only patterns whose purpose can be explained in one sentence.

| Area | Available vocabulary |
| --- | --- |
| Hero | asymmetric split, editorial manifesto, media mask, kinetic type, curtain reveal, scroll-pinned hero |
| Navigation | dock magnification, magnetic button, gooey menu, dynamic island, radial menu, speed dial, mega-menu reveal |
| Layout | bento, masonry, chroma grid, split-screen scroll, sticky stack, horizontal pan |
| Containers | parallax tilt, spotlight border, glass panel, holographic foil, swipe stack, morphing modal |
| Media | dome gallery, coverflow, drag-to-pan, accordion slider, hover trail, glitch treatment |
| Typography | kinetic marquee, text mask, scramble, circular path, gradient stroke, kinetic grid |
| Feedback | particle action, pull-to-refresh, skeleton shimmer, directional hover, ripple, line drawing, mesh, lens blur |

Use interaction-heavy patterns only when they carry state, feedback, or a real
story. Meet reduced-motion behavior, pointer/touch alternatives, keyboard
access, cleanup, and performance constraints before shipping them. Do not mix
multiple animation engines in the same component tree.

## Reusable Blocks

Create a reusable visual block only after demonstrated reuse or a confirmed
change axis. A block has a small semantic interface and documents:

- purpose and unsuitable contexts;
- responsive fallback and stable media/layout constraints;
- supported themes, accessibility, states, and visible content contract;
- optional motion levels plus reduced-motion behavior;
- source asset ownership and a test/screenshot target.

Do not add a generic component collection merely because a catalog exists.

## Honest Approximations

Web glass or "Liquid Glass" is a CSS approximation, not an Apple web package.
Use a contrast-safe solid fallback when transparency is reduced or unsupported.
Similarly, a visual effect inspired by a named product or design system must not
be described as an official implementation unless the project uses that system.

## Anti-Default Check

Before using a visually distinctive pattern, confirm it does not introduce a
fake dashboard, decorative status marker, unexplained logo wall, copied brand
asset, meaningless micro-label, repeated layout reflex, misleading metric, or
motion with no user benefit.
