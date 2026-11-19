# Output

Keep structured Spec/ER/IR/Scope/FR/NFR/AC/Risk in req-process. Chat is a
decision summary for the user, not a dump of internal fields.

```text
需求结论: <one plain-language decision/result>
这次会做: <bounded included work>
完成标准: <observable user-facing result>
需要注意: <important risk/assumption; omit when none>
需要确认: <blocking decision; omit when none>
下一步: <who does what next>
开发记录: <path/state or why no document>
```

Do not print raw `Spec/ER/IR/FR/NFR/AC/Artifact/Handoff` headings to users when a
persisted artifact carries them. Omit irrelevant optional headings.

## Persisted mode

- Summarize; do not repeat the plan.
- Translate relevant AC into `完成标准` and material risk into `需要注意`.
- `开发记录` says whether the artifact was reused or created, then gives its exact
  path, current work, next work, and blockers in plain language.
- `下一步` states the agent's continuing action. Do not ask the user to say
  “continue” between runnable queue items unless stepwise control was requested.
- Keep bounded requirement research in linked evidence files. Verification output,
  pass/fail details, and logs remain in chat.

## Chat-only mode

The response is the only contract. Include enough plain-language scope,
completion criteria, risk/assumptions, and next action to stand alone.

## Acceptance form

Internal AC remains input/precondition -> observable output. User-facing
`完成标准` translates it without IDs or requirement-engineering jargon.

## Blocking decision

Ask only when blocked. One decision, with:

```text
需要确认: <plain question>
建议: <answer + why>
如果暂不确认: <safe default or stop>
```

## Tracker add-on
For issue/PR/PRD triage, use plain labels while preserving operation state:

```text
事项状态: <from -> to + why>
给开发的说明: <brief/issues>
平台操作: 已执行 | 待执行 | 未执行（原因）
```
