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
现象/问题 -> 入口 -> 调用链 -> 关键源码 -> 调试验证 -> 结论
```

## Section Contract

```text
### 现象/问题
### 入口定位
### 调用链
### 关键源码
### 调试验证
### 小结
```

Rules:

- Explain why this entry is correct.
- The debug section distinguishes observed runs from static inference or an unrun
  verification plan; do not invent runtime output to fill the section.
- Walk logical blocks, not every line.
- Explain confusing branches with "why it exists".
- Link previous/next lifecycle node.
- Prefer several small Mermaid graphs over one oversized graph.
