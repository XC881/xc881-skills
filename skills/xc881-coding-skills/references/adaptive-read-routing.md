# Adaptive Read Routing

Decide from requested-read complexity and relevant project complexity before
activating Coding. Project size alone is not enough; use coupling relevant to the
question.

## Direct Read

Allow only when every condition holds:

- the user names an exact file/symbol or the target is immediately obvious;
- the question is narrow and factual or a local explanation;
- evidence is confined to one/few clearly related files;
- no call/data/state flow, lifecycle, runtime/test reconstruction is required;
- no security, performance, concurrency, migration, or compatibility risk;
- no req-process/cross-process task and no likely follow-up code change.

The active analysis/writing skill may perform this read and retain ownership.

## Coding Read

Use Coding when explicitly invoked, when work is tracked, or when any trigger
applies:

- entry/path is unknown or evidence spans modules/languages/packages;
- call graph, data/state flow, architecture/lifecycle, runtime, tests, or debugging;
- security, performance, concurrency, migration, compatibility, generated code;
- plugin/framework magic, monorepo coupling, or project isolation is uncertain;
- the read supports a likely write, review decision, or verification claim.

Coding then classifies `instant | queue` before `read | change`. A delegated read
returns bounded evidence without granting change permission.
