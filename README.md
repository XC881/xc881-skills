# xc881-skills

Token-compact agent skill library for the xc881 workflow.

It separates analysis from execution so the agent reads less, guesses less, and hands off cleanly between stages.

## Skills

```text
$xc881-solution-research     technical feasibility / web research; no code
$xc881-requirement-analysis  requirement analysis / scope / acceptance; no code
$xc881-bugfix-research       bug or vulnerability diagnosis; no code
$xc881-coding-skills         implementation / refactor / verify
$xc881-source-article-style  source-reading article writing
```

## Recommended flow

```text
idea / unfamiliar stack / external technical uncertainty
  → $xc881-solution-research
  → requirement only if the user asks for both solution + requirement in the same request, or invokes requirement after solution output

feature / PRD / scope / acceptance criteria
  → $xc881-requirement-analysis
  → auto bounded technical research via $xc881-solution-research when the requirement cannot be judged cleanly without it, then continue the same requirement run
  → $xc881-coding-skills

bug / vuln / regression
  → $xc881-bugfix-research
  → $xc881-coding-skills

source analysis article
  → $xc881-source-article-style
  → auto bounded term research via $xc881-solution-research when needed
```

## Rules

- Analysis and writing skills require explicit mention of `xc881` plus task intent. The agent chooses the exact skill by intent. Direct `$skill-name` calls also work. Examples: `用xc881调研`, `用xc881分析需求`, `用xc881修复`, `用xc881写作`.
- `xc881-solution-research` is for web-backed technical research only; it does not default into requirement analysis.
- `xc881-solution-research` enters requirement analysis only when the user asks for both in one request, or explicitly invokes requirement after solution output.
- `xc881-requirement-analysis` may automatically use bounded `xc881-solution-research` only when technical uncertainty affects requirement judgment, and then continues the same requirement run automatically.
- When `xc881-solution-research` was delegated by `xc881-requirement-analysis`, its result returns to that same requirement run automatically.
- `xc881-coding-skills` is the execution layer after scope is clear.
- `SKILL.md` is the fast path; `references/` are runtime-only support files.
- Keep outputs compact by default; expand only when the task or risk requires it.

## Install and validate

```bash
bash scripts/install.sh all
python scripts/validate_all.py
```
