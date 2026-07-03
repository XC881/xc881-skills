---
name: xc881-source-article-style
description: 'Explicit-only. Use when the user explicitly invokes $xc881-source-article-style or gives explicit xc881-scoped writing intent such as 用xc881写作. Provides the user''s Chinese source-code article style for internals of any language or stack (e.g. Electron/Chromium, Rust, Go, Python, JVM), function-level analysis, call-chain walkthroughs, build/debug/source-reading notes, article chapter drafts, diagrams, tables, conclusions, and reader-facing explanations. Automatically uses $xc881-solution-research for unexplained specialized terms or possibly-stale authoritative facts when needed.'
when_to_use: 'Use when producing article prose or outlines from source-code evidence, especially function-level internals analysis. Do not use for code changes unless combined with xc881-coding-skills.'
display_name: "xc881源码文章风格"
version: "1.1.0"
category: "writing"
tags:
  - writing
  - source-analysis
  - function-level
  - internals
  - article-style
  - xc881
aliases:
  - xc881-source-article-style
  - xc881源码文章风格
  - xc881写作
  - xc811文章规范
---

# xc881 Source Article Style

Explicit xc881-scoped intent only.

Write compact Chinese source-reading articles: problem -> evidence -> flow -> function -> conclusion.

Genre is explanation: show *why* the code behaves this way from source evidence. Not reference docs, not a tutorial, not API usage.

Reference files live under `./references/`.

Reference Index:

- `./references/function-level-source-article.md`: use for function-level analysis chapters.
- `./references/evidence-and-style-rules.md`: use before publishable prose or rewrite.
- `./references/article-output-contract.md`: use when the user asks for a full article, chapter, or rewrite.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

## Fast Path

1. Ecosystem recon (one line, every article): name the language, build system, package manager, debugger/trace tool, and authoritative doc source for this project. Keep it minimal; only expand when the stack is unfamiliar or a fact is uncertain.
2. Verify only needed evidence: version/path/function/callers/callees/debug note.
3. Think hard before locating: entry-point and call-chain claims must carry a derivation path, never an assertion. Explain why each key branch exists.
4. Evidence tier: when a debugger/tracer is available, back entry/flow claims with breakpoint/call-stack/runtime output; when it is not, mark the claim as static inference and give the static basis (symbol, reference, build artifact).
5. Check unexplained terms or possibly-stale authoritative facts in the available context.
   - If a proprietary term, architecture concept, internal mechanism, acronym, domain term, or a version/API fact that may be outdated affects understanding, automatically use `$xc881-solution-research` against official docs / authoritative sources.
   - Research only that point with code path/function/context; do not ask the user to invoke the research skill.
   - Treat researched facts as cited context, and mark remaining inference.
6. Use the function-level spine unless the user asks otherwise:

```text
现象/问题 -> 入口 -> 调用链 -> 关键源码 -> 调试验证 -> 本章结论
```

7. Strengthen article shape:
   - every section ends with one takeaway
   - big lifecycle diagrams split into small diagrams
   - conclusion is 3-5 evidence-backed bullets
8. Style: practical source guide, `笔者/读者/本章` allowed, no official-manual tone.
9. Mark inference when evidence is partial.

## Token Policy

- Load references only when the request needs them.
- Do not ask the model/user for broad pasted context; request exact path/function/log when missing.
- Default output: outline or section skeleton, not full chapter.
- Full prose only when user asks for "完整文章/章节/重写".
- Auto-research only terms that affect reader understanding; do not research ordinary programming words or repeated terms already introduced.
- Prefer compact tables/numbered flows over long paragraphs.
- Avoid repeating source code; cite path/function and summarize blocks.

## Output Defaults

- Outline: title + 5-8 section bullets.
- Function analysis: path/function + call order + state/side effects + 3-5 conclusions.
- Full chapter: follow `article-output-contract.md`.

## Hard Rules

- Do not write broad theory without code anchors.
- Do not present guessed call order as fact.
- Do not over-explain common programming concepts.
- Do not turn the article into API usage docs.
- Do not ask the user to manually invoke `$xc881-solution-research` for missing term context.
- Do not add decorative prose; keep the article source-reading oriented.
