# Frontend Redesign And Visual QA

Open from routing or implementation for visual review, redesign, modernization,
preservation risk, or screenshot-level confirmation. When asset/reference
ambiguity blocks the review or a proposed non-default pattern needs constraints,
automatically load `./references/frontend-image-reference-workflow.md` or
`./references/frontend-pattern-catalog.md` and continue without another user request.

When a concrete UX, data-display, mobile/platform, or visual-direction decision
is not resolved by the affected system or audit evidence, automatically load
`./references/frontend-design-intelligence.md`; do not use it for a general review checklist.

## Audit Before Editing

Read the affected route and its actual system before proposing visual changes:

- tokens, font loading, colors, theme strategy, icon family, components, and
  style ownership;
- information architecture, route IDs, navigation, conversion/workflow path,
  content hierarchy, and real assets;
- responsive behavior, keyboard/focus behavior, form validation, loading,
  empty, error, selected, and disabled states;
- metadata, structured content, analytics hooks, legal/cookie content, and
  existing accessibility or performance protections;
- visual debt: hierarchy, spacing, contrast, density, media, copy clarity,
  layout stability, duplicate patterns, and misleading mock data.

Classify the request as targeted preservation, approved visual overhaul, or
greenfield. If that distinction changes routes, content, brand, or acceptance
criteria and is not clear, ask one blocking question or return to Requirement.

## Preservation Contract

Never silently change route paths, anchor IDs, primary navigation labels, form
field names/order, logo/wordmark, legal copy, analytics identifiers, metadata,
structured data, accessibility behavior, or supported theme behavior. Preserve
working content and recognizable brand traits unless the user explicitly asks
to replace them.

Prefer the smallest high-value upgrade sequence:

1. Correct broken states, contrast, focus, text fit, responsive behavior, and
   accessibility regressions.
2. Reuse/refine tokens, typography hierarchy, spacing rhythm, and surface
   consistency.
3. Improve interaction feedback and media treatment.
4. Recompose only the affected high-value sections.
5. Replace a component or block only when it cannot meet the contract intact.

Do not use a redesign as a reason to migrate the framework, component library,
or information architecture.

## Visual Verification

When browser tooling exists, run the smallest relevant app path and inspect
screenshots at at least one desktop and one narrow mobile viewport. Also inspect
every theme and motion mode changed by the patch. Exercise the changed action
and relevant loading/error/empty or navigation states.

Check:

- first viewport hierarchy and CTA/action visibility where applicable;
- text fit, readable controls, no accidental overlap/overflow, stable media and
  fixed-format elements, and intended mobile collapse;
- color/focus/form/overlay contrast, keyboard reachability, semantic labels,
  and tap targets;
- real assets render, no fake preview or broken image fallback, and no invented
  data is presented as factual;
- reduced-motion fallback, cleanup of interactive effects, and visual behavior
  after resize/navigation;
- route, content, analytics/meta, and other preserved contracts remain intact.
- for changed forms, navigation, locale-sensitive values, or long content: clear
  labels/recovery, meaningful URL state, `Intl` formatting where applicable, and
  stable image dimensions/loading space.

For public-page performance work with a runnable tool and a relevant change,
measure the affected route or run an available audit. Do not claim web-vital
targets from style inspection alone.

If visual tooling is unavailable, inspect the rendered-code path, layout rules,
and responsive constraints, run available tests/build checks, and state exactly
which visual result remains unobserved. Never report screenshot or performance
verification that did not run.

## Review Output

Separate functional defects, visual defects, accessibility defects, performance
risks, and intentional scope exclusions. A polished screenshot does not prove a
usable workflow, and a passing unit test does not prove an unbroken layout.
