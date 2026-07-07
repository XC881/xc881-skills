# Issue Tracker Triage

Use only for clear issue/PR/PRD tracker intent.

Canonical roles:

- `needs-triage`: classify
- `needs-info`: ask one blocking question
- `ready-for-agent`: behavior + interfaces + AC + out-of-scope + verify
- `ready-for-human`: needs human judgment/implementation
- `wontfix`: rejected/closed

Tracker:

- GitHub: `gh issue/pr view/list/comment/edit/close`, `gh pr diff`
- GitLab: `glab issue/mr view/list/note/update/close/diff`
- Local: `.scratch/<feature>/PRD.md`, `.scratch/<feature>/issues/NN-slug.md`
- Unknown: output planned mutation and ask convention

Agent Brief:

```text
Category / Summary / Current / Desired / Key interfaces / AC / Out of scope / Verification
```

Rules:

- Map canonical roles to real labels before editing.
- Public AI comments disclose AI assistance.
- Enhancement `wontfix` records/proposes `.out-of-scope/<concept>.md`; bugs never go there.
- PRD splits become vertical slices/tracer bullets with dependency order and blockers after items exist.
- Large/foggy work uses one map item: Destination, Notes, Decisions, Not yet specified, Out of scope; child tickets are research/prototype/grilling/task.
- Distinguish executed tracker ops from planned commands/files; never fake success when credentials/tooling are missing.
