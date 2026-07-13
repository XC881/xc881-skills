# Execution Checkpoint and Tool Policy

Coding owns execution checkpoints and the tools needed for the current read or
change. Environment context management is outside this skill.

## Queue checkpoint

Before each queue item, the exact artifact, `current.md`, and current item already
form the durable recovery anchor. Keep accepted contract impact, unresolved
blockers/approvals, changed paths, evidence paths, and remaining verification plan
recoverable. Do not persist raw command output or verification results.

After verification, update status/history/current atomically, advance, validate,
and continue. After context compaction, reload the exact current window, inspect
durable changed files when needed, and resume the same `read | change` action
without asking the user to continue.

Instant work does not create a queue merely for context management. The host must
retain a bounded continuation summary for the active request and changed paths.

## Tool selection

Load tools for the next action only:

- repository discovery/read tools for complex reads;
- edit/test/build tools for changes;
- git tools only for explicit checkpoint, commit, or push;
- source and target inspection tools for delegated porting work.

Use only tools needed for the next action. Batch independent mechanical reads,
request focused fields, and cap outputs.

## Tool-result retention

Keep a result only while it affects the current decision or verification. Before
it leaves active context, retain the relevant fact, decision impact, durable file
change, or evidence path. Then old search pages, command logs, repeated file
bodies, completed item text, and stale tool results may be removed by the host.

Never summarize secrets into a checkpoint or continuation summary.
