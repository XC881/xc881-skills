# Execution Checkpoint and Tool Policy

Coding owns execution checkpoints and the tools needed for the current read or
change. Environment context management is outside this skill.

## Queue checkpoint

Before each queue item, the exact artifact, `current.md`, and current item already
form the durable recovery anchor. Keep accepted contract impact, unresolved
blockers/approvals, changed paths, evidence paths, and remaining verification plan
recoverable. Do not persist raw command output or verification results.

After verification, patch item status (never `in-progress`), one history
transition and current pointers/counts together; resume blocked items as `ready`.
Advance and continue without a process-validator call. After compaction, recover
the exact current window and resume the same `read | change` action automatically. Reuse
available required skill/ref instructions; acquire only missing or known-changed
rules from exact paths. A summary or loaded marker alone is not the rule body.
Project files, external evidence and mutable queue state retain their freshness
checks. If task identity is missing/ambiguous, ask once rather than guess.

Instant work does not create a queue for context management. Where the host
supports continuation summaries, preserve the active request and changed paths;
the skill cannot guarantee their retention.

## Tool selection

Load tools for the next action only:

- repository discovery/read tools for complex reads;
- edit/test/build tools for changes;
- git tools only for explicit checkpoint, commit, or push;
- source and target inspection tools for delegated porting work.

Use only tools needed for the next action. Batch independent mechanical reads,
request focused fields, and cap outputs.

## Tool-result retention

Before a supported checkpoint/compaction, preserve relevant facts, decisions,
durable changes and evidence paths. Do not copy old pages, logs or unchanged file
bodies into summaries. Context removal/retention is controlled by the host, not
this skill; never claim to have removed context merely by writing a summary.

Delegates need sufficient instructions in their own context, supplied or read;
they cannot inherit a parent's loaded marker. Return bounded evidence to the
original owner, which reuses its available rules without restarting discovery.

Never summarize secrets into a checkpoint or continuation summary.
