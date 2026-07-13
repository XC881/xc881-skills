# Goal Boundary Contract

Use to classify the task and lock the anti-loop stop boundary.

## Magnitude (read and judge first)

Porting intent is not only "port the whole project". On any cross-language / cross-project
work, read the actual code and judge which magnitude this is, with evidence:

- whole project
- subsystem / module
- single feature
- a slice of logic
- abstract architectural intent (borrow the design, not the code)

Deep reading is delegated to `$xc881-coding-skills`; the orchestrator only consumes the
verdict and classifies. Magnitude comes BEFORE the boundary: each magnitude has different
done-criteria. Grey area (feature vs logic-slice) -> round up to the larger scope.

## Classify

- non-goal: bounded, one-shot, single module/function/file. No standing loop.
- goal: long-horizon, whole-project or multi-module, iterative until "done".

Only goal tasks can loop forever, so only goal tasks need the hard gate.

## Hard gate (goal only)

Before any porting action, lock a stop-boundary contract via `$xc881-requirement-analysis`:

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
