# Function-Level Source Article

Use for one function/class/subsystem boundary/call chain.

## Evidence

- version/branch if cheap
- path + function/class
- caller + key callees
- state changes, side effects, thread/process context
- debug/log/breakpoint output if available

Map each claimed call edge to a call site, registration/build selection, or trace.
An unresolved dynamic target is a gap, not a complete call chain. Request only
evidence needed for that edge; debugger availability alone does not require a run.

## Spine

```text
现象/问题 -> 入口定位 -> 调用链 -> 关键源码 -> 调试验证 -> 本章结论
```

## Section Contract

```text
### 现象/问题
### 入口定位
### 调用链
### 关键源码
### 调试验证
### 本章结论
```

Rules:

- Explain why this entry is correct (registration, dispatch, or caller proof).
- When control crosses async queues, IPC/RPC, callbacks, vtables, or build-time
  selection, name the binding site, carrier struct/channel, and execution context
  (thread/process/phase); mark any unverified dynamic hop as a static gap.
- The debug section distinguishes observed runs from static inference or an unrun
  verification plan; do not invent runtime output to fill the section.
- Walk logical blocks, data ownership, and state invariants — never translate
  `if/for/call` line by line into Chinese.
- Explain non-obvious branches with "why this guard/indirection exists".
- `本章结论` extracts 3-5 non-obvious design invariants or lifecycle boundaries
  with `path:symbol` anchors, never restating section headings.
- Link previous/next lifecycle node and split oversized Mermaid graphs.
