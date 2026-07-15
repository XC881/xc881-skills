---
name: xc881-source-article-style
description: 'Primary owner for Chinese source-code articles: source guides, function analysis, call-chain chapters, and rewrites. Generic writing or code-reading-only requests do not trigger it; reuse supplied evidence and delegate only blocking inspection or term research.'
when_to_use: 'Use for source-article prose, not generic code explanation. Reuse supplied evidence and delegate only blocking gaps.'
display_name: "xc881源码文章风格"
version: "1.4.0"
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
---

# xc881 Source Article Style

Intent-routed source-article owner. Direct calls select it; implicit use requires
article prose as the primary outcome. Generic writing and code-reading-only work
stay with the base/current owner. Run only the needed branch.

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

1. Ecosystem recon only when stack facts affect the article and are not already
   supplied: one line for language/build/package/debug/docs; expand only on a gap.
2. Reuse supplied evidence. Inspect only missing simple exact/local/low-risk facts;
   delegate missing complex/tracked evidence to `$xc881-coding-skills`, then resume.
3. Think hard before locating: entry-point and call-chain claims must carry a derivation path, never an assertion. Explain why each key branch exists.
4. Evidence tier: when a debugger/tracer is available, back entry/flow claims with breakpoint/call-stack/runtime output; when it is not, mark the claim as static inference and give the static basis (symbol, reference, build artifact).
5. Check unexplained terms or possibly-stale authoritative facts in the available context.
   - If a proprietary term, architecture concept, internal mechanism, acronym, domain term, or a version/API fact that may be outdated affects understanding, automatically use `$xc881-solution-research` against official docs / authoritative sources.
   - Research one fact/RQ with code path/function/context; do not start an option
     comparison or ask the user to invoke the research skill.
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
- Do not bypass Coding for complex/tracked source inspection; retain article ownership.
- After context compaction, preserve prose ownership, evidence paths, active section, and bounded delegation; resume automatically.
- Do not add decorative prose; keep the article source-reading oriented.
