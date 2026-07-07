# Evidence And Style Rules

## Voice

- Chinese practical source-reading tone.
- `笔者/读者/本章` allowed.
- Prefer "我们先看..." and "这里需要注意...".
- Use "可以观察到" only after evidence.

## Evidence

- Prefer local source, build files, debug output, and runtime behavior.
- Cite exact names: file, function/symbol, plus the stack's own identifiers — e.g. GN target/build arg/process type for Chromium, crate/feature/cfg for Rust, package/build tag for Go, module/venv for Python. Instantiate per project, do not force one stack's vocabulary onto another.
- Evidence tier: debugger/tracer runtime evidence (breakpoint, call stack, log) outranks static inference. When you cannot run tooling, mark the claim as static inference and give the static basis (symbol, reference, build artifact).
- Doc supplementation: when a version/API/mechanism fact may be outdated or uncertain, back it with official docs or an authoritative source (via `$xc881-solution-research`) and mark it as cited, not recalled.
- Mark inference: "从这里可以推断..." / "更准确地说...".
- If evidence conflicts with old prose, correct the prose.

## Structure

- Use tables for directory/file/variable meaning.
- Use Mermaid only for lifecycle/process/call chain; split large diagrams.
- Ground specialized concepts before later sections depend on them. If the target reader is assumed to know one, name it as a prerequisite; otherwise introduce it before use.
- Grow long articles one block at a time from verified evidence. Re-read the target file before rewriting/appending so user edits are preserved.
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
- If raw notes/fragments are supplied, treat them as a quarry, not a script; preserve the source file unless the user asks to edit it.

## Avoid

- long official-documentation summaries
- unverified historical claims
- API tutorial tone
- line-by-line narration when block-level intent is clearer
- vague words like "底层处理了一些逻辑" without naming the logic
