# xc881 Skills

Select skills autonomously from both **user intent** and **actual task readiness/direction**—not literal phrasing or keyword lists. Direct `$skill-name` calls remain valid.

Routing rules:

- Zero skill: ordinary Q&A, generic writing, or a simple exact/local/low-risk read stays direct.
- Ready execution -> `xc881-coding-skills` directly when target, scope, and cause are already concrete.
- Open prerequisites -> start in `xc881-analysis` (or `xc881-porting-orchestration` for cross-language/project parity) even when the user only says "build X" or "fix Y", if scope/AC is unspecified, root cause is unconfirmed, or external API/version facts block safe edits; once resolved and implementation was intended, chain automatically into `xc881-coding-skills` without asking for a second invocation.
- Mid-task shift: if Coding discovers contract conflicts, hidden scope decisions, or two failed fixes, pivot to `xc881-analysis` before further edits.

Skills:

- `xc881-analysis`: three internal branches (Requirement: scope/ER/IR/AC/risk/triage + `req-process`; Bugfix: repro/hypotheses/root cause/fix & verify plan; Solution: primary-source research). Internal branch switches never delegate. No code/test/commit.
- `xc881-coding-skills`: all project writes, complex/tracked reads, reviews, frontend UI, verification, and explicit git. Classify `instant|queue` then `read|change`; advance runnable queue items to task terminal without per-item continue prompts unless stepwise intent or a real blocker applies.
- `xc881-source-article-style`: Chinese source-reading articles; chain Coding for complex source traces and Analysis for external term/version facts.
- `xc881-porting-orchestration`: cross-language/project migration with behavioral equivalence (`req-process` + `cross-process`); chain Analysis for open scope/facts and Coding for edits/parity checks.

Default to compact plain-Chinese outputs. Preserve active owner and exact current window across context compaction; never commit/push implicitly.
