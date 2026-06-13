# Evidence And Style Rules

## Voice

- Chinese practical source-reading tone.
- `笔者/读者/本章` allowed.
- Prefer "我们先看..." and "这里需要注意...".
- Use "可以观察到" only after evidence.

## Evidence

- Prefer local source, build files, debug output, and runtime behavior.
- Cite exact names: file, function, GN target, build arg, env var, process type.
- Mark inference: "从这里可以推断..." / "更准确地说...".
- If evidence conflicts with old prose, correct the prose.

## Structure

- Use tables for directory/file/variable meaning.
- Use Mermaid only for lifecycle/process/call chain; split large diagrams.
- Use question blocks for traps:

```text
> [!question]- 为什么...
> answer
```

- Use info/tip blocks only for prerequisite or navigation.
- End each major section with one takeaway.

## Token Rules

- Do not paste long code; quote symbol/path and summarize block intent.
- Do not restate obvious API behavior.
- Prefer numbered flow over paragraphs for call order.
- Full prose only when requested.

## Avoid

- long official-documentation summaries
- unverified historical claims
- API tutorial tone
- line-by-line narration when block-level intent is clearer
- vague words like "底层处理了一些逻辑" without naming the logic
