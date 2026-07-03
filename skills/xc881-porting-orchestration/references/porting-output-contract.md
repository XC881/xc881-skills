# Porting Output Contract

Compact by default. Emit the sections that apply; goal tasks require the boundary before any porting.

```text
xc881 Porting:
Task class: goal / non-goal + why
Magnitude: whole-project / module / feature / logic-fragment / abstract-intent + evidence
Stop boundary: done-criteria / exit / out-of-scope
Understanding: language diff / architecture / library map
Risks: pre/post porting problems, prioritized (P0-P3)
Equivalence: method + consistent/inconsistent + evidence
Progress: vs done-criteria + done/not-done
Handoff:
```

Rules:

- Task class always first, then Magnitude (read and judge before locking the boundary).
- Stop boundary is required before porting on goal tasks; on non-goal tasks it may be a single line.
- Progress line appears on goal iterations.
- No code here; delegate implementation and equivalence checks to `$xc881-coding-skills`.
- Keep each section evidence-backed; mark inference as inference.
