# Frontend Motion And Performance

Load only for animation, scroll work or rendering-performance decisions. Continue
already-loaded frontend routes when the next concern arises.

- Motion communicates hierarchy, feedback, state change or narrative; a still
  interface is correct when motion has no job.
- Prefer CSS, IntersectionObserver or the installed motion library for simple
  transitions. Reserve GSAP/canvas for genuine scroll/choreography needs; isolate
  effects, clean up and avoid competing engines in a component tree.
- Honor reduced motion for nontrivial effects. Prefer transform/opacity; avoid
  raw per-frame scroll listeners, layout-property animation, broad blur/noise on
  scrolling content and arbitrary z-indexes.
- Reserve image/font/embed space to prevent layout shift. Load heavy below-fold
  or optional visuals only when supported by the current stack. Measure affected
  runtime behavior before making performance claims.
