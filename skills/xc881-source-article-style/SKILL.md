---
name: xc881-source-article-style
description: 'Explicit-only. Use only when the user explicitly invokes $xc881-source-article-style or writes the trigger phrase xc811文章规范. Provides the user''s Chinese source-code article style for Electron/Chromium/Node/V8 internals, function-level analysis, call-chain walkthroughs, build/debug/source-reading notes, article chapter drafts, diagrams, tables, conclusions, and reader-facing explanations.'
when_to_use: 'Only explicit invocation: $xc881-source-article-style or xc811文章规范. Use when producing article prose or outlines from source-code evidence, especially for function-level internals analysis. Do not use for code changes unless combined with xc881-coding-skills.'
display_name: "xc881源码文章风格"
version: "1.1.0"
category: "writing"
tags:
  - writing
  - source-analysis
  - function-level
  - electron
  - article-style
  - xc881
aliases:
  - xc881-source-article-style
  - xc881源码文章风格
  - xc811文章规范
---

# xc881 Source Article Style

Explicit only.

Write compact Chinese source-reading articles: problem -> evidence -> flow -> function -> conclusion.

Reference files live under `./references/`.

Reference Index:

- `./references/function-level-source-article.md`: use for function-level analysis chapters.
- `./references/evidence-and-style-rules.md`: use before publishable prose or rewrite.
- `./references/article-output-contract.md`: use when the user asks for a full article, chapter, or rewrite.

When opening reference files, always use the exact relative path shown above.
Do not assume reference files are located beside `SKILL.md`.

## Fast Path

1. Verify only needed evidence: version/path/function/callers/callees/debug note.
2. Use the function-level spine unless the user asks otherwise:

```text
现象/问题 -> 入口 -> 调用链 -> 关键源码 -> 调试验证 -> 本章结论
```

3. Strengthen article shape:
   - every section ends with one takeaway
   - big lifecycle diagrams split into small diagrams
   - conclusion is 3-5 evidence-backed bullets
4. Style: practical source guide, `笔者/读者/本章` allowed, no official-manual tone.
5. Mark inference when evidence is partial.

## Token Policy

- Load references only when the request needs them.
- Do not ask the model/user for broad pasted context; request exact path/function/log when missing.
- Default output: outline or section skeleton, not full chapter.
- Full prose only when user asks for "完整文章/章节/重写".
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
- Do not add decorative prose; keep the article source-reading oriented.
