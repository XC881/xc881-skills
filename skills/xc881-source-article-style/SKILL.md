---
name: xc881-source-article-style
description: 'Primary owner for Chinese source-code articles: guides, function/call-chain deep dives, and prose rewrites (chaining Coding for complex source traces and Analysis for external term/version gaps). Ordinary chat explanations and generic writing skip it.'
when_to_use: 'Use when the deliverable is Chinese source-article prose, not ordinary code chat; chain Coding for complex source traces and Analysis for external term/version gaps.'
display_name: "xc881源码文章风格"
version: "3.0.0"
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

Route each turn by user intent and actual task needs, not literal wording; chain
or switch skills when open scope, cause, facts, parity, or code work requires it.
Full supplied bodies count; names/paths/markers do not. Reuse in-context rules;
read missing/changed or reread-requested exact paths only. Higher-priority rules win.
An outline needs no chapter template.

## Fast Path

1. Select outline / function analysis / requested full prose. Recon only for
   missing relevant stack facts.
2. Reuse supplied evidence when revision/config and claim scope match. Inspect only missing simple exact/local/low-risk facts (known target, 1-2 local files, no flow/risk/write);
   delegate missing complex/tracked evidence to `$xc881-coding-skills` with the
   claim/anchors. Receive path/symbol, derivation, evidence type, limits and next
   check; resume the same section.
3. Anchor claims/call edges/conclusions to source/observation. Call sites are fact;
   order may be inference. Scope traces by input/config; label unproved links.
   Runtime evidence requires a runtime-dependent gap or requested verification,
   not merely available tools.
4. A term/version gap blocking understanding automatically delegates one bounded
   RQ/code context to `$xc881-analysis`. Reuse valid definitions/citations;
   skip explained terms. Receive cited context/uncertainty, not options or a restart.
5. Draft to supported depth; missing anchors narrow/qualify claims. Never invent
   branches or exceed user read boundaries. Default function-level spine:

```text
现象/问题 -> 入口定位 -> 调用链 -> 关键源码 -> 调试验证 -> 本章结论
```

6. Explain data ownership, state invariants, and why each branch/indirection
   exists — never paraphrase `if/for/call` line by line. For async/IPC/callback/vtable
   hops, name the registration site, carrier struct/queue, and thread/process context.
   End major sections with one takeaway, split large diagrams, and avoid hollow AI
   filler (`优雅地/极大地/综上所述/值得注意的是`).

## Output Defaults

- Start directly with `# 标题` or the first contract heading (no chat preamble); delegated Coding/Analysis checks feed prose internally and never prepend `代码结论`/`xc881 调研` banners.
- Outline: `# 标题` + 5-8 section bullets (do not open with chapter headings).
- Function analysis: use the `### 现象/问题 ... ### 本章结论` spine above (`调试验证` optional when purely static); `本章结论` gives 3-5 non-obvious architectural invariants anchored to `path:symbol`, never restating section titles. Skip headings only when the user explicitly asks for a brief/non-sectioned note.
- Full prose ("完整文章/章节/重写"): follow `article-output-contract.md`.
- Missing context: request only the exact path/function/log, not a broad paste.

## Hard Rules

- Do not present guessed call order as fact.
- Do not over-explain common programming concepts.
- Do not ask the user to manually invoke `$xc881-analysis` for missing term context.
- Do not bypass Coding for complex/tracked source inspection; retain article ownership.
- After context compaction, preserve prose ownership, evidence paths, active section, and bounded delegation; resume automatically.
