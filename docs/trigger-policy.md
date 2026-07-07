# Trigger

All xc881 skills are intent-routed. Direct `$skill-name` calls still work, but
ordinary wording may also trigger a skill when the task intent is clear.

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

When intent is ambiguous, prefer requirement analysis before coding. Do not fan
out to multiple skills unless the user asks for a combined workflow or a skill
delegates a bounded subtask.
