# Porting Output Contract

Keep scope/stop boundary in req-process and magnitude, equivalence method and
progress in cross-process. Chat reports verification/equivalence evidence and
translates decisions; results/logs never enter either artifact.

```text
迁移结论: <plain decision and whether work may proceed>
本次迁移: <source, target, bounded scope>
如何确认成功: <observable parity/equivalence proof>
需要注意: <material user-relevant risk; omit when none>
需要确认: <blocking decision; omit when none>
当前进度: <status-based completed/current/remaining state>
下一步: <who does what next>
开发记录: <req-process + cross-process paths, or why absent>
```

Rules:

- Goal tasks still require linked req-process and cross-process artifacts before
  porting; human wording does not bypass the boundary gate.
- `如何确认成功` translates the equivalence method and stop criteria without
  copying the complete contracts into chat.
- `当前进度` uses status-based counts/state, never subjective percentages.
- `下一步` names automatic continuation only when implementation/queue execution
  was requested. Planning-only work names the bounded next decision or handoff.
- Chat-only/non-goal work omits `当前进度` and `开发记录`, skips durable ledgers even when shipping code, and includes enough scope, proof, assumptions, and next action to stand alone.
- In a single-turn Porting -> Coding chain, Porting emits one final `迁移结论` response; delegated Coding/Analysis steps return bounded evidence internally without emitting separate banners.
- Blocking questions include a recommendation and safe fallback/stop behavior.
- Omit irrelevant optional headings and do not repeat the full plan.
- No code here; delegate implementation and equivalence checks to `$xc881-coding-skills`.
- Keep each section evidence-backed; mark inference as inference.
