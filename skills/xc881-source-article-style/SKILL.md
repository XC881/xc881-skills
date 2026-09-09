---
name: xc881-source-article-style
description: 'Primary owner for Chinese source-code articles: source guides, function analysis, call-chain chapters, and rewrites. Generic writing or code-reading-only requests do not trigger it; reuse supplied evidence and delegate only blocking inspection or term research.'
when_to_use: 'Use for source-article prose, not generic code explanation. Reuse supplied evidence and delegate only blocking gaps.'
display_name: "xc881源码文章风格"
version: "1.4.1"
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

Intent-routed Chinese source-article owner; direct calls select it. Generic writing
and code-reading-only work stay with the current owner. Explain why from source,
not API tutorials. Article owns prose; Coding applies requested repository edits.

## Reference Routes

- `./references/function-level-source-article.md`: function/class/call-chain analysis.
- `./references/evidence-and-style-rules.md`: publishable prose, rewrite, or disputed evidence.
- `./references/article-output-contract.md`: full article/chapter/rewrite shape.

Route by intent each turn. Full supplied bodies count; names/paths/markers do not.
Reuse in-context rules; read needed exact paths automatically only for missing
rules, known changes or requested rereads. Higher-priority invocation rules win.
An outline needs no chapter template.

## Fast Path

1. Select outline / function analysis / requested full prose. Recon only for
   missing relevant stack facts.
2. Reuse supplied evidence when revision/config and claim scope match. Inspect only missing simple exact/local/low-risk facts;
   delegate missing complex/tracked evidence to `$xc881-coding-skills` with the
   claim/anchors. Receive path/symbol, derivation, evidence type, limits and next
   check; resume the same section.
3. Anchor claims/call edges/conclusions to source/observation. Call sites are fact;
   order may be inference. Scope traces by input/config; label unproved links.
   Runtime evidence requires a runtime-dependent gap or requested verification,
   not merely available tools.
4. A term/version gap blocking understanding automatically delegates one bounded
   RQ/code context to `$xc881-solution-research`. Reuse valid definitions/citations;
   skip explained terms. Receive cited context/uncertainty, not options or a restart.
5. Draft to supported depth; missing anchors narrow/qualify claims. Never invent
   branches or exceed user read boundaries. Default function-level spine:

```text
现象/问题 -> 入口 -> 调用链 -> 关键源码 -> 调试验证 -> 本章结论
```

6. Explain branch purpose, end major sections with one takeaway, and split large
   diagrams. Prefer tables/numbered flows and block summaries in a practical voice.

## Output Defaults

- Outline: title + 5-8 section bullets.
- Function analysis: path/function + call order + state/side effects + 3-5 conclusions.
- Full prose only when requested ("完整文章/章节/重写"); follow the output contract.
- Missing context: request only the exact path/function/log, not a broad paste.

## Hard Rules

- Do not present guessed call order as fact.
- Do not over-explain common programming concepts.
- Do not ask the user to manually invoke `$xc881-solution-research` for missing term context.
- Do not bypass Coding for complex/tracked source inspection; retain article ownership.
- After context compaction, preserve prose ownership, evidence paths, active section, and bounded delegation; resume automatically.
