# xc881-skills

`xc881-skills` 是一组低 token、强边界、可交接的 agent skills。

核心思想：

- 分析和执行分离，先把问题说清楚，再让 coding 层改代码。
- `SKILL.md` 是 fast path，只放运行时必须读的内容。
- `references/` 是运行时按需读取的细节规则。
- `docs/` 是维护文档，不作为默认运行时上下文。
- 默认输出紧凑；大输出写文件，只在聊天里报告路径、进度和验证。
- 不隐式提交、不隐式推送。

## 支持的 skills

当前仓库支持 6 个 skills：

| Skill | 触发 | 类型 | 用来做什么 | 不做什么 |
| --- | --- | --- | --- | --- |
| `$xc881-solution-research` | 意图隐式 / 直接调用 | 分析 | 联网技术调研、方案比较、可行性判断、权威资料查证 | 不写代码，不默认进入需求分析 |
| `$xc881-requirement-analysis` | 意图隐式 / 直接调用 | 分析 | 需求分析、范围、AC、PRD、issue/PR 分诊、PRD 拆 issue、Agent Brief | 不写代码，不做 bug 根因诊断 |
| `$xc881-bugfix-research` | 意图隐式 / 直接调用 | 分析 | bug、回归、漏洞、性能问题的证据、复现、根因、修复计划、验证计划 | 不直接修代码，不输出 exploit 步骤 |
| `$xc881-coding-skills` | 意图隐式 / 直接调用 | 执行 | 实现、重构、修复、验证、工程质量控制、提交/推送前检查 | 范围不清时不硬写代码 |
| `$xc881-source-article-style` | 意图隐式 / 直接调用 | 写作 | 源码导读、函数级分析、调用链文章、调试证据型中文技术文章 | 不改代码，不写泛泛教程 |
| `$xc881-porting-orchestration` | 意图隐式 / 直接调用 | 编排 | 跨语言/跨项目迁移，锁边界、写计划、识别风险、验证等价性 | 不直接编码，不替代 specialist skills |

## 触发规则

所有 skills 都支持意图隐式触发，也支持直接 `$skill-name` 调用。

路由由用户意图决定，不再要求必须出现 `xc881`。`xc881` 仍然是有效的命名空间/风格信号，适合在用户想明确指定本技能库时使用。

直接调用示例：

```text
$xc881-requirement-analysis 分析这个功能
$xc881-solution-research 调研这个技术方案
```

常用意图示例：

```text
帮我调研技术方案 -> $xc881-solution-research
帮我分析需求 -> $xc881-requirement-analysis
这个接口 500 帮我看看 -> $xc881-bugfix-research
写代码实现登录 -> $xc881-coding-skills
按我的文章风格写一篇源码导读 -> $xc881-source-article-style
帮我把这个项目改写成另一种语言 -> $xc881-porting-orchestration
```

带 `xc881` 的自然语言仍然有效：

```text
用xc881调研
用xc881分析需求
用xc881分诊
用xc881拆issue
用xc881修复
用xc881写代码
用xc881写作
用xc881移植
```

`$xc881-coding-skills` 是执行层。只要用户明确要实现、修复、重构、验证、提交或推送，它可以按编码意图触发；但如果需求、权限、生命周期、数据迁移或验收标准不清楚，应先按意图走 `$xc881-requirement-analysis`。

## 能力取舍

主要收益：

- 用户不需要记住具体 skill 名，普通自然语言会按意图进入合适流程。
- 技术调研、需求分析、bug 诊断、代码执行、源码写作、移植编排的边界更清楚。
- issue/PR/PRD 分诊能力并入 `$xc881-requirement-analysis`，减少入口数量，保留 tracker 状态机、Agent Brief、PRD 拆 issue、out-of-scope 和 map/child tickets。
- eval、routing matrix 和 validator 会一起约束触发行为，降低文档和实际路由不一致的风险。
- 大输出默认写文件或分段 artifact，聊天里只报告路径、进度和验证，符合低 token 策略。

主要代价：

- 隐式路由依赖意图判断，模糊请求可能误入分析、调研或 bugfix 流程。
- 维护新增意图时必须同步 `skills-manifest.json`、`README.md`、`evals/cross-skill-routing.json`、skill 自身 trigger eval、agent prompts 和 validator。
- 更严格的分析/执行分离会让部分请求先进入 requirement 或 bugfix，再交给 coding，链路更稳但不一定最短。
- 直接 `$skill-name` 仍然是兼容入口；当用户想绕开意图判断时，推荐显式指定。

## 推荐流程

### 1. 技术方案不确定

```text
idea / unfamiliar stack / external technical uncertainty
  -> $xc881-solution-research
  -> $xc881-requirement-analysis 仅在用户同时要求方案+需求，或后续要求需求分析时进入
  -> $xc881-coding-skills
```

示例：

```text
用xc881调研 Supabase 和 Firebase 的技术方案差异
用xc881调研 React Server Components 在这个项目里是否适合
$xc881-solution-research 查一下 GitHub Actions OIDC 部署 AWS 的官方做法
```

### 2. 功能、PRD、范围、验收标准

```text
feature / PRD / scope / acceptance criteria
  -> $xc881-requirement-analysis
  -> 必要时自动做 bounded $xc881-solution-research
  -> $xc881-coding-skills
```

示例：

```text
用xc881分析这个登录功能的范围和验收标准
用xc881把这个想法整理成 PRD 和 AC
$xc881-requirement-analysis 分析现有会员系统要加优惠券，需要哪些 must-not-regress
```

### 3. issue / PR / PRD tracker 工作流

`xc881-issue-triage` 的能力已并入 `$xc881-requirement-analysis`。

```text
issue / PR / PRD tracker workflow
  -> $xc881-requirement-analysis
  -> $xc881-bugfix-research 当需要 bug 根因诊断
  -> $xc881-coding-skills 当 ready-for-agent
```

支持内容：

- canonical tracker 状态：`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human`、`wontfix`
- GitHub / GitLab / local markdown tracker 操作计划
- Agent Brief
- PRD 拆 issues
- blocker / dependency 表达
- `.out-of-scope/<concept>.md` 知识库
- 大任务 map / child tickets
- executed / planned / skipped tracker ops 区分

示例：

```text
用xc881分诊 GitHub issue #42，判断能不能给 agent 做
用xc881把这个 PRD 拆成 tracker issues，并建立阻塞关系
用xc881分诊这个 PR，判断是 ready-for-agent 还是 ready-for-human
用xc881分析这个 enhancement 是否应该进入 .out-of-scope
```

### 4. bug / vuln / regression

```text
bug / vuln / regression
  -> $xc881-bugfix-research
  -> $xc881-coding-skills
```

示例：

```text
用xc881修复登录 500，先定位原因
$xc881-bugfix-research 根据这段日志分析根因和验证计划
用xc881分析这个依赖 CVE 是否影响当前版本
```

### 5. 代码实现、重构、验证

```text
clear scope
  -> $xc881-coding-skills
  -> patch
  -> verify
```

示例：

```text
用xc881写代码实现登录
按 xc881 代码规范重构这个 service
修这个 bug，根因明确，最小 diff
提交并推送
```

### 6. 源码阅读文章

```text
source evidence
  -> $xc881-source-article-style
  -> 需要解释专有术语时自动 bounded $xc881-solution-research
```

示例：

```text
用xc881写作 BrowserWindow 创建流程
$xc881-source-article-style 写一篇 NodeBindings::CreateEnvironment 的函数级分析
用xc881写作，分析 tokio runtime 的任务调度入口
```

### 7. 跨语言 / 跨项目移植

```text
cross-language / cross-project porting
  -> $xc881-porting-orchestration
  -> goal task 先锁 stop boundary
  -> $xc881-requirement-analysis 定义边界和风险
  -> $xc881-solution-research 调研语言/框架迁移坑
  -> $xc881-coding-skills 执行 port + equivalence check
```

示例：

```text
用xc881移植这个 Go 服务到 Rust
$xc881-porting-orchestration 把这个 Python 模块迁移到 Go，先定边界
用xc881迁移这个 C++ 模块到 Rust，要求行为等价
```

## 详细说明

### `$xc881-solution-research`

用途：

- 技术路线调研
- 方案可行性判断
- 框架/库/协议/标准查证
- 多方案比较
- 论文、RFC、官方文档、security advisory 查证

输出结构：

```text
xc881 Solution:
Spec:
RQ:
Evidence:
Options:
Pick:
Risk:
Handoff:
```

规则：

- 事实、推断、推荐必须分开。
- 优先一手资料：官方文档、标准、论文、维护者 issue/PR、vendor advisory。
- 证据不足时不强行 Pick，输出 blocker 和下一步 research。
- 大调研写成 Markdown artifact，聊天里只报告路径和决策影响。

### `$xc881-requirement-analysis`

用途：

- 需求分析
- PRD/MVP/范围定义
- 显式需求 ER、隐含需求 IR
- FR/NFR/AC
- 风险 P0-P3
- issue/PR/PRD tracker 分诊
- PRD 拆 issues
- Agent Brief

输出结构：

```text
xc881 Req:
Spec:
ER:
IR:
Scope:
FR/NFR:
AC:
Risk:
Q:
Handoff:
```

tracker add-on：

```text
Tracker:
State: from -> to + why
Brief/Issues:
Tracker Ops: executed | planned | skipped
```

规则：

- 不写代码。
- IR 不能伪装成 ER。
- AC 必须可测试。
- 只问一个阻塞问题。
- 能从仓库、文档、当前技术调研获得的事实，不问用户。
- tracker 写操作必须区分已经执行、计划执行、因为权限/工具缺失而跳过。

### `$xc881-bugfix-research`

用途：

- bug / regression / stack trace / perf 问题分析
- dependency vuln / code vuln / CVE / GHSA / OSV / CWE / OWASP 判断
- 复现计划
- 根因定位
- 最小修复计划
- 验证计划

输出结构：

```text
xc881 BugFix:
Context:
Evidence:
Cause:
Fix:
Verify:
Risk:
Handoff:
```

安全问题附加：

```text
Severity:
CVE/GHSA/OSV/CWE/OWASP:
Affected:
Exploitability:
Mitigation:
```

规则：

- 先建立 tight repro loop。
- 复现应能抓到用户描述的具体症状。
- 最小化复现后再给根因。
- 假设要可证伪。
- 不输出 exploit 步骤。
- bug issue 的 tracker brief 由 requirement-analysis 承接，bugfix 提供 evidence/cause/fix/verify。

### `$xc881-coding-skills`

用途：

- 实现功能
- 修复 bug
- 重构
- 工程质量优化
- review
- 测试和验证
- 显式提交/推送

默认最终回复：

```text
完成内容:
验证:
风险/假设:
```

规则：

- 每个改动行都要能追溯到请求、证据、验证或本次改动造成的清理。
- 不做无关重构。
- 不加 speculative abstraction。
- 领域逻辑不泄漏到 UI、SQL、SDK callback、framework handler。
- 测 public seam，不测内部实现细节。
- 避免 tautological tests。
- mock 只放系统边界。
- 没有显式要求时不 commit、不 push。

### `$xc881-source-article-style`

用途：

- 中文源码导读
- 函数级源码分析
- 调用链解释
- 调试证据型文章
- 架构/生命周期章节

默认结构：

```text
现象/问题 -> 入口 -> 调用链 -> 关键源码 -> 调试验证 -> 本章结论
```

规则：

- 入口和调用链必须有推导路径。
- runtime/debugger/tracer 证据优先于静态推断。
- 静态推断必须标明依据。
- 专有术语先介绍，再在后文依赖。
- 可能过期的 API/版本事实自动用 `$xc881-solution-research` 查官方来源。

### `$xc881-porting-orchestration`

用途：

- 跨语言移植
- 跨项目迁移
- 抽象架构意图移植
- 长任务 stop boundary
- plan file
- behavior equivalence

输出结构：

```text
xc881 Porting:
Magnitude:
Task class:
Stop boundary:
Understanding:
Risks:
Equivalence:
Progress:
Handoff:
```

规则：

- goal 任务必须先锁 stop boundary。
- 必须写 `dev-notes/cross-process/<task>.md` 作为进度源。
- 等价性看行为，不看结构相同。
- 目标项目已有架构时，迁入目标架构，不照搬源架构。
- 抽象意图移植时，用 intent fidelity，并记录 adopt/adapt/reject。

## 安装和验证

安装到本机 skill 目录：

```bash
bash scripts/install.sh all
```

验证仓库结构、frontmatter、trigger eval、behavior contract：

```bash
python scripts/validate_all.py
```

## 维护约束

- 新增 skill 必须同步 `skills-manifest.json`、`README.md`、`evals/cross-skill-routing.json`、skill 自身 evals 和 agent prompts。
- 运行时 reference 要登记到 `docs/reference-inventory.md`。
- 所有 skill 保持 intent-routed；直接 `$skill-name` 调用是兼容入口，不是唯一入口。
- 大能力优先吸收到现有 skill 的 `references/`，不要轻易新增入口。
- README 只描述当前真实能力，不写未实现承诺。
