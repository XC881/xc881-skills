# Frontend Implementation Standard

Open from frontend routing for user-visible layout, component, responsive, or
state implementation. Apply only the rules relevant to the changed UI and its
observable states. When an active product/visual, type/color, data-display,
mobile/platform, or UX decision remains unresolved after local evidence,
automatically load `frontend-design-intelligence.md`. When work reaches a visual
source/asset decision, redesign or screenshot confirmation, or a deliberate
non-default pattern, automatically load `frontend-image-reference-workflow.md`,
`frontend-redesign-and-visual-qa.md`, or `frontend-pattern-catalog.md` and
continue without another user request.

## Architecture And Dependencies

- Inspect real entry points, route ownership, component boundaries, theme/token
  source, styles, data states, and installed dependencies before editing.
- Keep domain decisions outside views. Components render supplied state and call
  narrow actions; validation, permission, and data rules remain at their proper
  application boundaries.
- In React/Next, keep static layout server-friendly. Isolate client-only input,
  animation, browser APIs, and continuous pointer/scroll values in small leaf
  components with cleanup. Do not update React state every animation frame.
- Reuse the existing icon family. If none exists, use Lucide for familiar UI
  glyphs. Keep weight, size, labels, and accessible names consistent. Do not
  draw familiar icon paths by hand.
- Check the manifest before importing a package. Do not assume Motion, GSAP,
  Tailwind, a design system, a font, or an image library exists.

## Structure, Responsive Behavior, And Platforms

- Prefer semantic landmarks and native controls. Preserve keyboard order,
  visible focus, form labels above inputs, contextual errors, and meaningful
  image alternatives.
- Use Grid for multi-track layouts when it expresses the structure more clearly
  than fragile flex percentage calculations. Give fixed-format media, toolbars,
  tiles, and controls stable constraints so dynamic content cannot shift them.
- Define each multi-column surface's small-screen behavior in the component.
  Check text fit, overflow, touch targets, order, and focus at the actual
  supported viewport sizes. Use dynamic viewport units for full-height mobile
  areas when needed, not brittle browser-height assumptions.
- For touch-dominant views, account for safe areas, system regions, reachable
  navigation, gesture space, readable type, and believable screen-to-screen
  flow. Do not turn a desktop landing page into a phone-shaped website.
- Do not add decorative containers merely to frame other containers. Use a
  card only when it communicates hierarchy, interaction, grouping, or a real
  surface boundary.

## Visual System And Content

- Preserve existing semantic tokens. For new visual work, choose a coherent
  palette, radius, border, shadow, type, spacing, and media-frame system before
  adding local exceptions. Keep supported theme hierarchy and contrast intact.
- Favor clear hierarchy, readable copy, intentional line breaks, and concise
  labels over oversized type, micro-label clutter, decorative status marks, or
  repeated eyebrow treatments. Do not manufacture precision, testimonials,
  customer logos, names, metrics, or product claims.
- Marketing/editorial pages need a clear first viewport, one primary next
  action, visible contrast, relevant visual media, and varied section rhythm.
  Do not repeat the same split or equal-card layout mechanically. Product UIs
  may repeat structures when comparison and scanning benefit from consistency.
- Use project, supplied, licensed, or appropriately generated visual assets.
  Never substitute div rectangles for a purported product screenshot. A real
  live component preview is valid when it is the actual component. Do not put
  labels over imagery unless they convey necessary information.
- Keep media aspect ratios, crop behavior, alt text, and loading space stable.
  Use genuine logos only when authorized; invented social proof is not a visual
  asset strategy.

## States, Motion, Accessibility, And Performance

- Implement applicable loading, empty, error, disabled, selected, hover,
  active, focus, validation, and recovery states. Skeletons should match the
  final structure when loading shape matters.
- Add motion only when it communicates hierarchy, feedback, state change, or
  narrative. A still interface is correct when motion has no job.
- Prefer CSS, IntersectionObserver, or the project's motion library for simple
  transitions. Reserve GSAP or canvas work for genuine scroll/choreography
  needs, isolate it, clean it up, and avoid competing animation engines in one
  component tree.
- Honor reduced-motion preferences for nontrivial motion. Animate transform and
  opacity where possible; avoid raw per-frame scroll listeners, layout-property
  animation, broad blur/noise on scrolling content, and arbitrary z-indexes.
- Keep CTA, form, image-overlay, and focus contrast usable. Reserve space for
  images, fonts, and embeds to prevent layout shift. Load heavy below-fold or
  optional visual work only when the local stack supports it.

## Compact Pre-Flight

- The changed route has a coherent visible hierarchy and no clipped/wrapped
  controls, accidental overflow, overlapping text, or broken media frame.
- The change preserves the existing system or declares the justified exception.
- Relevant states, keyboard behavior, responsive layout, supported themes, and
  reduced motion have a verification plan.
- Copy, labels, alternatives, data, assets, and claims are truthful and useful.
