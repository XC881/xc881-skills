# Frontend Layout And Platform

Load only for layout, responsive geometry or platform navigation. Continue the
already-loaded frontend routes when the next concern arises.

- Use Grid for multi-track layouts when clearer than fragile flex percentages.
  Give fixed-format media, toolbars, tiles and controls stable constraints so
  dynamic content cannot shift them.
- Define each multi-column surface's small-screen behavior in its component.
  Check text fit, overflow, touch targets, order and focus at supported widths.
  Use dynamic viewport units when full-height mobile areas need them, not brittle
  browser-height assumptions.
- Touch views account for safe areas, system regions, reachable navigation,
  gesture space, readable type and believable screen-to-screen flow. Do not put a
  desktop landing page inside a phone-shaped website.
- Do not add decorative containers to frame containers. Cards need an actual
  hierarchy, interaction, grouping or surface boundary.
