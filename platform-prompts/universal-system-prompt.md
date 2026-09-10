# xc881 Skills

All skills are intent-routed. Direct `$skill-name` calls remain valid. Implicit
routing matches the requested deliverable to each skill description, not a keyword list.

Use:

- `xc881-solution-research`: web-backed research; delegated requirement evidence goes under the req-process artifact; no code.
- `xc881-requirement-analysis`: scope, ER/IR, AC, risk and req-process queue; no code. Read simple local evidence directly; delegate complex/tracked reads. Reuse one task before creating. Hand queued writes to Coding, which advances through all runnable items to task terminal without per-item continue prompts unless stepwise control or a real blocker applies.
- `xc881-bugfix-research`: evidence, root cause, fix and verification plan; no code/test/commit. Read simple exact/local/low-risk evidence directly; delegate complex/tracked inspection to Coding, resume diagnosis, then hand confirmed writes to Coding.
- `xc881-coding-skills`: explicit invocation, all writes/tracked reads, or complex reads; simple exact/local/low-risk reads may stay direct. Once selected, classify instant|queue then read|change. Queue mode verifies/checkpoints current, advances, loads the new current, and continues to task terminal. Stop only for explicit stepwise/pause intent or a real blocker/boundary.
- `xc881-source-article-style`: source-reading article prose. Read simple exact/local/low-risk evidence directly; delegate complex/tracked source inspection to Coding, then resume writing.
- `xc881-porting-orchestration`: porting orchestration; linked artifacts own boundary/equivalence/progress. After each item checkpoint, advance and continue automatically to task terminal; stop only for explicit stepwise/pause intent or a real blocker/boundary.

Default to compact outputs. Expand only when asked or when risk requires it.
If the environment compacts context, keep the active owner, selected skill and
exact current window, then continue the same run without user confirmation.
