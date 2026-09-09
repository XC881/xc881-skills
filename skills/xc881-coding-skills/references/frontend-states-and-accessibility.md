# Frontend States And Accessibility

Load for component/form states or semantics. Continue already-loaded frontend
routes only when another concern is reached.

- Prefer semantic landmarks and native controls. Preserve keyboard order,
  visible focus, labels above inputs, contextual errors and meaningful image
  alternatives.
- Implement applicable loading, empty, error, disabled, selected, hover, active,
  focus, validation and recovery states. Skeletons match final structure when
  loading shape matters. Do not add unused states just to satisfy a checklist.
- Keep action, form, image-overlay and focus contrast usable. Verify changed
  interaction and keyboard paths; visual review uses the existing QA route.
- A remaining specific platform/UX gap may use design intelligence; known project
  state conventions do not require a catalog lookup or new visual system.
