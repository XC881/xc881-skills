# Frontend Image Reference Workflow

Open from routing or implementation when the user wants an art-directed result,
supplies visual references, asks for image-to-code, or a high-impact asset or
visual decision remains ambiguous. When this workflow reaches selected-frame
coding, post-implementation visual evidence, or a non-default pattern,
automatically load `./references/frontend-implementation-standard.md`,
`./references/frontend-redesign-and-visual-qa.md`, or `./references/frontend-pattern-catalog.md` and
continue without another user request.

If the supplied frame or asset still leaves its product/visual, type/color, or
mobile decision unresolved, automatically load `./references/frontend-design-intelligence.md`
before generating or selecting another reference. Use it only for that decision.

## Decide The Source

1. Prefer supplied references, existing brand assets, design files, real product
   screenshots, and the local component system.
2. When those do not resolve a high-impact visual decision and an image tool is
   available, generate a readable reference before freeform implementation.
3. Use one reference per distinct visual composition. Add a detail view only for
   unresolved text, media, spacing, controls, or responsive behavior. Do not
   create a fixed image count just because a page has many sections.
4. If a reference is unclear, generate a fresh focused view in the same system.
   Do not treat a cropped, unreadable fragment as a design specification.
5. Without a suitable tool or asset, use real local/supplied media where
   possible. Keep an honest asset gap rather than creating a fake screenshot or
   decorative placeholder that pretends to be the product.

## Build A Compact Art-Direction Brief

Before generating a reference, choose only what changes the result:

- surface, audience, conversion or workflow goal, and visual priority;
- brand/palette/type/radius/icon/media constraints from actual evidence;
- hero or first-screen hierarchy and a purposeful composition anchor;
- section rhythm, image treatment, and one coherent material language;
- mobile/platform mode and logical flow for mobile concepts.

Avoid randomization. A distinct choice must have a brief-based reason. Existing
brand identity wins, and references teach quality/rhythm rather than license
copying a logo, layout, slogan, or proprietary asset.

## Extract Before Coding

Treat a selected frame as a design specification. Record only the evidence
needed to implement it:

- readable copy, hierarchy, line count, type mood, and alignment;
- gutters, section cadence, component and media proportions, framing, radius,
  border, depth, color roles, and contrast treatment;
- primary and secondary actions, form/control states, visible navigation, and
  interaction cues;
- responsive collapse, safe areas, image crops, and constraints that must stay
  stable across the set.

Implement the visible logic faithfully. Resolve missing details by preserving
the same system, then favor the simplest accessible implementation. Do not
replace an intentional reference with a default template halfway through.

## Web, Mobile, And Brand Modes

### Web

Use meaningful media across visual storytelling surfaces. Keep the first
viewport clear, the main action obvious, and the page's composition varied only
where it improves hierarchy or narrative. Full-bleed media, gradients, glass,
textures, marquees, and artistic effects are conditional tools, not defaults.

### Mobile

Choose iOS-native, Android-native, or neutral conventions before drawing a
flow. Keep platform behavior, safe areas, navigation, type scale, media frames,
and device presentation consistent. A phone frame belongs to a requested visual
concept, never the implemented product screen.

### Brand

For an explicitly requested identity direction, infer category, audience,
promise, metaphor, trust needs, and exclusions before creating a brand board or
asset. Keep logo, palette, type, applications, and image direction coherent.
Do not silently replace an existing logo or fabricate credibility.

## Delivery Boundaries

- Follow host image-tool policy. Do not claim a generated reference is a local
  repository asset until it has actually been added through the project asset
  pipeline.
- Keep image generation, inspection, and implementation in the same visual
  system. Regenerate a weak reference instead of coding from guesswork.
- Use the visual QA reference after implementation. Tool-unavailable work still
  needs source-level checks and an explicit unverified boundary in the report.
