---
name: xc881-solution-research
description: 'Explicit-only skill. Use only when the user explicitly invokes $xc881-solution-research, says 使用 xc881-solution-research, or clearly asks to enable the xc881技术方案联网调研 Skill. It performs web-assisted solution/technology research before requirements or coding: English Spec First normalization, idea-to-research-question mapping, implicit technical dependency inference, tech stack hypothesis, paper-first principle research, official docs/standards/GitHub/developer-source exploration, feasibility comparison, trade-off analysis, and handoff to xc881-requirement-analysis or xc881-coding-skills. Do not auto-trigger from ordinary research/技术选型/联网调研 keywords.'
when_to_use: 'Use only on explicit invocation of this skill. Do not use implicitly for ordinary mentions of 联网调研, 技术选型, 方案分析, paper, GitHub, or 可行性. Once explicitly invoked, turn an idea into compact research questions, infer hidden technical dependencies, search authoritative sources, analyze feasible solution options, and produce a concise evidence-backed recommendation and handoff. Do not implement code.'
display_name: "xc881技术方案联网调研"
version: "1.0.0"
category: "solution-research"
tags:
  - explicit-only
  - web-research
  - solution-research
  - technology-selection
  - feasibility
  - papers
  - github
  - architecture
  - tech-stack
  - xc881
aliases:
  - xc881-solution-research
  - xc881-tech-research
  - xc881-research
  - xc881技术调研
  - xc881技术方案联网调研
---

# xc881 Solution Research

## Role

Explicit-only technology and solution research layer.

Activate only when the user explicitly invokes:

```text
$xc881-solution-research
```

or clearly says to use/enable `xc881-solution-research`.

Do not auto-trigger from ordinary research, technology selection, GitHub, paper, feasibility, or 联网调研 keywords.

Turn an idea into:

```text
normalized spec → research questions → inferred technical dependencies → authoritative evidence → feasible options → recommendation → handoff
```

Do not implement code. Do not turn output into product requirements unless handing off to `$xc881-requirement-analysis`.

## Load policy

`SKILL.md` is the fast path. Read references only when needed:

- `references/english-spec-and-research-questions.md`: rough/multilingual idea normalization and research-question mapping.
- `references/source-priority-policy.md`: source priority, authority, citations, and conflict handling.
- `references/paper-first-policy.md`: principle-level knowledge, algorithms, protocols, models, and academic grounding.
- `references/tech-stack-feasibility-policy.md`: stack inference, feasibility, trade-offs, option comparison.
- `references/solution-output-contract.md`: compact/detailed output contracts.

## Default output

Compact by default.

- 6-10 sections.
- Cite sources when web research is used.
- Compare only 2-4 viable options unless user asks.
- Expand only when principle knowledge is deep, evidence conflicts, or risk is high.

## Workflow

1. Confirm explicit invocation.
2. Normalize idea when needed:
   - `Standard English Research Spec: Goal / Inputs / Constraints / Unknowns / Output`
3. Derive research questions:
   - explicit questions
   - inferred questions from hidden dependencies, consequences, scale, security, cost, integration, data, compliance, deployment, maintainability
4. Infer technical stack candidates.
5. Research sources:
   - principle knowledge: papers first
   - implementation knowledge: official docs, standards/RFCs, vendor docs, benchmark repos, GitHub issues/PRs, release notes
   - operational/security knowledge: advisories, OWASP/CWE/CVE/GHSA/OSV, incident reports
   - community knowledge: maintainer discussions, high-quality forum posts, blogs only as support
6. Synthesize findings, options, and trade-offs.
7. Recommend one default only when evidence is strong enough.
8. Handoff to `$xc881-requirement-analysis` or `$xc881-coding-skills`.

## Compact output contract

```text
xc881 Solution Research:
Spec:
Research questions:
Inferred questions:
Source plan:
Findings:
Options:
Recommendation:
Risks:
Handoff:
```

## Rules

- Explicit invocation only.
- Do not implement code.
- Do not over-search; use targeted, high-authority sources.
- Prefer primary sources.
- Use papers first for principle-level claims.
- Separate evidence from inference.
- Mark uncertainty and version assumptions.
- Do not cite irrelevant sources.
- Do not produce a huge literature review unless requested.
