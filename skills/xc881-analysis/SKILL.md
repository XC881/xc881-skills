---
name: xc881-analysis
description: 'Primary owner for scope/AC/PRDs, issue/PR triage, bug/vulnerability diagnosis, and external research. Use for analysis outcomes OR before coding when a build/fix request lacks clear scope, confirmed root cause, or external facts, then chain Coding. Skip when scope and cause are already concrete.'
when_to_use: 'Use when intent or task gaps need scope/AC/triage, diagnosis, or external evidence—standalone or before underspecified builds/unconfirmed fixes (replaces requirement-analysis, bugfix-research, solution-research).'
display_name: "xc881分析"
version: "3.0.0"
category: "analysis"
tags:
  - intent-routing
  - analysis
  - requirements
  - bugfix
  - issue-triage
  - tracker
  - solution-research
  - root-cause
  - xc881
aliases:
  - xc881-analysis
  - xc881-requirement-analysis
  - xc881-bugfix-research
  - xc881-solution-research
  - xc881-issue-triage
  - xc881需求分析
  - xc881分诊
  - xc881拆issue
  - xc881漏洞与Bug诊断
  - xc881技术调研
---

# xc881 Analysis

Intent-routed analysis owner with three branches: Requirement (scope/AC/tracker),
Bugfix (diagnosis), Solution (external evidence). Direct calls select it.
Analysis-internal branch switches never delegate; no code.

## Reference Routes

Requirement:
- `./references/english-spec-first-policy.md`: normalize rough/mixed input.
- `./references/implicit-requirement-inference.md`: premise/IR gaps affecting AC.
- `./references/existing-project-feature-analysis.md`: existing behavior delta.
- `./references/issue-tracker-triage.md`: tracker state, Agent Brief, ops.
- `./references/requirement-process-artifact.md`: artifact reuse, gate, queue.
- `./references/design-system-artifact.md`: reusable visual contract.
- `./references/requirement-output-contract.md`: summary, tracker, blocker form.
- `./references/requirement-quality-rubric.md`: scope/AC review or risk.

Bugfix:
- `./references/bugfix-forensics-workflow.md`: uncertain cause/alternatives.
- `./references/reproducer-verification-plan.md`: repro/verification plan.
- `./references/web-research-policy.md`: external/version facts in diagnosis.
- `./references/vulnerability-triage-policy.md`: security severity/mitigation.
- `./references/bugfix-output-contract.md`: tracker or repair handoff fields.

Solution:
- `./references/english-spec-and-research-questions.md`: rough ask or missing RQ.
- `./references/source-priority-policy.md`: source/version/conflict or evidence.
- `./references/paper-first-policy.md`: principle/algorithm claims.
- `./references/tech-stack-feasibility-policy.md`: stack/library selection.
- `./references/solution-output-contract.md`: artifact or handoff fields.

Route each turn by user intent and actual task needs, not literal wording; chain
or switch skills when open scope, cause, facts, parity, or code work requires it.
Full supplied bodies count; names/paths/markers do not. Reuse in-context rules;
read missing/changed or reread-requested exact paths only. Higher-priority rules win.

## Workflow

1. Classify into one branch: Requirement / Bugfix / Solution; steps 3-5 are
   per-branch dispatch, not a sequence. Cross-branch work emits one contract
   for the requested artifact; other branches supply fields inside it,
   never a second contract (bug-issue triage: Requirement output carries Bugfix
   cause/fix/verify). Reuse supplied Spec/ER/IR, expected/actual+env, RQs and
   scope/version/freshness evidence; refresh only changed/conflicting inputs.
2. For missing project facts, perform a simple exact/local/low-risk read here (known target, 1-2 local files, no flow/risk/write), or delegate a complex/tracked `read` to `$xc881-coding-skills` using task+project complexity.
   Send question/evidence/permissions; receive needed anchors, uncertainty and
   next check; resume the same branch without repeating discovery. Gaps another
   branch covers (expected behavior, external facts, causal evidence) resolve
   inside Analysis by switching branch, not delegating; owner and handoff
   unchanged.
3. Requirement: resolve explicit/unambiguous artifacts, then gate. Falsify broken/XY
   premises against repo/platform facts first. Fill Spec/ER/IR/scope/AC (P0-P3 risks;
   decidable `input->outcome` + failure/non-regression). One blocking question max with
   recommendation/fallback — product-visible values (ratios/thresholds) warrant it
   under delegation; technical choices proceed as documented decisions. Then
   derive the complete linked write from template, apply one coherent patch; validators are
   audit/repair/CI tools, not normal authoring or handoff loops. Artifact maintenance stays in Requirement.
4. Bugfix: reuse valid repros; rank falsifiable explanations without quotas and pick
   the smallest distinguishing check. Cause + confidence needs evidence separating
   alternatives and upstream invariant corruption from crash site; stack/patch alone
   is not cause. Plan minimal root-invariant fix/risk/verify. Diagnosis-only stops
   with `下一步: 仅诊断` or missing evidence; reads never grant edits.
5. Solution: classify fact check / option decision with version-matched primary
   sources. Fact check: evidence/impact/risk/handoff; do not invent options.
   Decision filters disqualifiers (license, runtime/version, maintenance) on
   constraints before picking. `对比` and `推荐` are decision-only; omit them for a single-fact check.
6. Persist verification plans and queue state, never results/logs; write requested
   research under supplied `<artifact>/evidence/`. Outside artifact maintenance,
   hand every write and selected complex/tracked read to Coding with exact
   artifact/current/next/blockers. Hand repair/build to Coding when implementation intent is explicit, implied, or delegated; no second invocation.
7. Queued work runs to task terminal; compaction resumes the same owner/current.
   No per-item “continue” unless explicit stepwise/pause intent or a real blocker.
   Persisted progress outranks chat.

Start directly with the branch heading (no preamble); omit empty optional fields. Emit this contract when Analysis is the turn's terminal output or stops on a blocker; when chaining straight into Coding/Porting/Article in the same turn, pass bounded findings internally so the terminal skill emits the single user-facing contract.

Requirement output:

```text
需求结论: <一句话结论/决策>
这次会做:
完成标准:
需要注意:        # only when relevant
需要确认:        # only when blocked; include recommendation + fallback
下一步:
开发记录:
```

Tracker add-on: `事项状态` / `给开发的说明` / `平台操作` (executed | planned |
skipped). Persist Spec/ER/IR/Scope/FR/NFR/AC/Risk; summarize decisions in chat.
Chat-only output is self-contained.

Bugfix output:

```text
xc881 诊断: <故障对象一句话>
结论:
背景:
依据:
修复:
验证:
需要注意:
下一步:
```

Security adds `严重程度` / `编号` / `影响范围` / `可利用性` / `缓解措施`; no
exploit steps.

Solution output:

```text
xc881 调研: <查证对象一句话>
结论:
查证点:
依据:
对比:          # 仅真实决策
推荐:          # 仅真实决策
需要注意:
下一步:
```

Papers first for principles; cite used sources; fact ≠ inference ≠ recommendation.
