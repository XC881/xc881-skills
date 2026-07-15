# Trigger

All xc881 skills are intent-routed. Direct `$skill-name` calls select that skill.
Implicit routing uses the minimum sufficient owner set.

```text
$xc881-solution-research
$xc881-requirement-analysis
$xc881-bugfix-research
$xc881-source-article-style
$xc881-porting-orchestration
```

Intent routing:

```text
调研技术方案 / 选技术栈 / 查官方资料 -> xc881-solution-research
分析需求 / 定范围 / 验收标准 / 分诊 issue / 拆 PRD -> xc881-requirement-analysis
接口 500 / 回归 / CVE / 日志报错 / 先定位原因 -> xc881-bugfix-research
写代码 / 重构 / 修复 / 验证 / 提交 / 推送 -> xc881-coding-skills
源码导读 / 函数级分析文章 / 调用链文章 / 我的文章风格 -> xc881-source-article-style
移植 / 迁移 / 跨语言 / 改写成另一种语言 -> xc881-porting-orchestration
```

Selection rules:

- Choose one primary owner from the user's requested final outcome, not every
  intermediate verb or noun in the prompt.
- Incidental errors, code, terms, languages, or research needs do not activate a
  second skill. The primary owner delegates one bounded subtask only when blocked.
- Ordinary explanations, generic writing, and simple exact/local/low-risk reads
  may use no xc881 skill.
- Ambiguity alone is not requirement intent. Use base-agent judgment when safe,
  or ask one blocking question when the final outcome truly cannot be inferred.
- A combined user request may chain skills, but only one owns the active phase;
  delegated skills return to that owner instead of becoming parallel owners.
- Do not run a full workflow merely because a skill was plausibly relevant. Run
  only the branch needed for the requested outcome.
