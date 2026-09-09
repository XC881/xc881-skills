# Goal Boundary Contract

Use to classify the task and lock the anti-loop stop boundary.

## Magnitude

Judge magnitude from supplied or cheap source/target evidence, not language names:

- whole project
- subsystem / module
- single feature
- a slice of logic
- abstract architectural intent (borrow the design, not the code)

Delegate only missing complex repository evidence to `$xc881-coding-skills`;
Porting classifies from the return. Magnitude determines done-criteria. If ambiguity
changes the stop gate or proof obligation, ask one bounded question; do not silently
expand the requested scope to a larger magnitude.

## Classify

- non-goal: bounded, one-shot, single module/function/file. No standing loop.
- goal: long-horizon, whole-project or multi-module, iterative until "done".

Only goal tasks can loop forever, so only goal tasks need the hard gate.

## Hard gate (goal only)

Before goal porting, reuse a valid locked boundary or have
`$xc881-requirement-analysis` lock it:

- Done-criteria: measurable, checkable per iteration (e.g. "all N modules pass the parity suite").
- Exit conditions: what state ends the loop (success end, and give-up/escalate end).
- Out-of-scope: explicitly listed, so scope creep cannot re-open the loop.

Persist this contract in `dev-notes/req-process/<task>/index.md`. The linked
cross-process file references it and must not copy scope, AC, or done-criteria.

Rules:

- No locked boundary -> do not start porting.
- Vague or unmeasurable boundary -> ask one blocking question, do not loop.
- Re-check the boundary every iteration; report progress vs done-criteria + explicit done / not-done.
- Done-criteria must be observable, not "feels complete".
