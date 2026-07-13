# xc881-skills

`xc881-skills` 是一组低 token、强边界、可交接的 agent skills。

核心思想：

- 分析和执行分离，先把问题说清楚，再让 coding 层改代码。
- `SKILL.md` 是 fast path，只放运行时必须读的内容。
- `references/` 是运行时按需读取的细节规则。
- `docs/` 是维护文档，不作为默认运行时上下文。
- 默认输出紧凑；大输出写文件，只在聊天里报告路径、进度和验证。
- `dev-notes/` 是首选开发笔记根目录；复杂需求使用 `dev-notes/req-process/` 持久化。
- 不隐式提交、不隐式推送。

## 支持的 skills

当前仓库支持 6 个 skills：

| Skill | 触发 | 类型 | 用来做什么 | 不做什么 |
| --- | --- | --- | --- | --- |
| `$xc881-solution-research` | 意图隐式 / 直接调用 | 分析 | 联网技术调研、方案比较、可行性判断、权威资料查证 | 不写代码，不默认进入需求分析 |
| `$xc881-requirement-analysis` | 意图隐式 / 直接调用 | 分析 | 需求分析、范围、AC、PRD、issue/PR 分诊、PRD 拆 issue、Agent Brief | 不写代码，不做 bug 根因诊断 |
| `$xc881-bugfix-research` | 意图隐式 / 直接调用 | 分析 | bug、回归、漏洞、性能问题的证据、复现、根因、修复计划、验证计划 | 不直接修代码，不输出 exploit 步骤 |
| `$xc881-coding-skills` | 意图隐式 / 直接调用 | 读码/执行 | 读代码、入口/调用链/数据流分析、解释、review、实现、重构、修复、验证、提交/推送前检查 | 范围不清时不硬写代码 |
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
读取 src/version.ts 的 VERSION 常量 -> 简单读取，可不启用 skill
帮我读一下这个模块的入口和调用链，不要改代码 -> $xc881-coding-skills
先分析登录需求，明确后直接读取代码并实现 -> $xc881-requirement-analysis + $xc881-coding-skills
先定位接口 500 根因，明确后直接修复 -> $xc881-bugfix-research + $xc881-coding-skills
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

`$xc881-coding-skills` 负责所有项目写入和复杂工程读取。AI 会同时判断用户要读什么、需要多少证据，以及项目相关部分的耦合复杂度。只有目标明确、局部、低风险、无需调用链/运行时重建且不属于任务队列的读取，才可直接完成；路径未知、跨模块、调用/数据/状态流、架构生命周期、安全、性能、并发、生成代码、框架魔法、跨语言或后续可能改代码时，使用 Coding。项目大本身不是唯一理由，相关耦合才是。

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

## 开发笔记与 Req Process

需求分析不再默认只存在于聊天。每次准备持久化前，Requirement 先判断这是不是已有需求的改动：优先使用用户给出的路径或当前对话唯一明确的任务；上下文不足时，用机械脚本最多返回 5 个候选路径，再只读取可能相关的 `index.md` 做目标和权责范围的语义比较。唯一匹配就复用，多项匹配只问一个选择问题，不能按最新目录或关键词直接决定。

只有确认没有匹配后才进入文档 gate。用户未指定时，AI 在跨会话、3 个以上可验证任务、跨模块契约、迁移/数据/权限/安全风险、外部调研或长期实现等情况下，自动创建：

```text
dev-notes/req-process/<YYYYMMDD>-<task-slug>/
  index.md       # 稳定需求、范围、ER/IR、AC、风险
  current.md     # 唯一 previous/current/next 指针
  history.md     # 重要状态变更
  queue/         # 可独立验证的纵向任务切片
  decisions/     # 可选，重要决策追加记录
  evidence/      # 可选，bounded 技术调研
```

`index.md` 默认存在，但按角色读取：Requirement 在识别/复用任务、恢复需求分析、修改 Scope/AC/Out-of-scope、全局审计或状态修复时读取；Coding 正常执行不读取。`current.md` 是唯一可变任务状态和活动指针，`index.md` 不重复保存 `State`。

复用已完成任务时，不重建目录或重写历史：新 queue ID 接在旧尾节点之后，任务重开为 `ready`，Requirement 把精确的 artifact、current、next 和 blockers 交给 Coding。Coding 只验证并消费这个 handoff，不负责搜索候选任务。

读请求先经过复杂度门槛：简单读取可由当前分析/写作流程直接完成；所有写入、任务读取和复杂读取进入 Coding。Coding 被选中后，在打开实际项目文件或执行 artifact 前，再判断临时还是任务：

| 持久化模式 | 识别条件 | Coding 行为 |
| --- | --- | --- |
| `instant` | 用户未提供 artifact/handoff，当前上下文也没有唯一明确的队列任务 | 不扫描、不读取 `dev-notes`，直接读代码或改代码 |
| `queue` | 用户明确给出 req-process/cross-process 路径或 handoff，或当前对话唯一明确指向一个活动任务 | 机械校验后只读 `current.md` 和当前 queue item，不默认读 `index.md`、previous 或 next |

如果同时存在多个可能的 artifact，Coding 只问一个阻塞选择问题，不能扫描目录后猜“最新任务”。`read | change` 是另一条独立维度，因此四种组合都成立：即时读、即时改、队列读、队列改。队列项必须自带当前执行合同；previous 只有被当前项明确引用证据/依赖时才读，next 等推进为 current 后再读。

Requirement、Bugfix 或源码文章保留自己的分析/写作职责：简单精确局部证据可直接读取，复杂或任务化源码检查委派为 Coding 的 `read`。Coding 只返回约定证据，不会把只读请求自行升级成改动；Requirement 自己维护 req-process 文档不触发 Coding，避免循环调用。

队列 checkpoint 是恢复点，不是默认确认点。Coding 完成当前项后会验证、更新 status/history/current，把 next 推进为 current，再只读取新的 current 窗口并继续，直到整个需求终态。只有用户明确要求逐项确认/每项暂停，或遇到输入、权限、审批、安全、范围变化等真实阻塞时才停止。

自动上下文压缩同样不是确认点。真正的 token 检测、原生/客户端压缩、历史替换和 agent loop 继续由 Codex、Claude Code、API session 或其它宿主负责，不属于 Coding 或任何单一 skill。压缩完成后保留 active owner、被选 skill 和精确 current 窗口，自动继续同一次 Requirement、Solution、Bugfix、文章、Porting 或 Coding 流程，不要求用户说“继续”。

如果当前 queue item 信息不完整、与实际代码冲突、用户要求改变 Scope/AC，或队列需要重新规划，Coding 不自行读取 `index.md` 或改需求，而是返回 Requirement。Requirement 读取完整合同并生成新的 current 窗口后，再交回 Coding。

进度只使用 queue done/total、current 和 blocker，不使用主观百分比或验证结果计数。简单、单轮、单目标任务可以不创建文档，但 Requirement 必须在“开发记录”中说明为什么无需文档。若创建文档，完整工程字段留在文档中，聊天只用人话报告结论、当前工作、下一步和阻塞项。

上下文硬预算：`current.md <= 1,200` 字符、未完成 queue item `<= 3,500`、`index.md <= 10,000`、cross-process ledger `<= 3,000`。有界技术调研可写入 evidence；验证命令输出、通过/失败详情和日志只在聊天报告，不写入 dev-notes。

### Skill 上下文边界

本仓库只优化自己能够控制的内容：skill 元数据、被选中的 `SKILL.md`、按需 reference/script、agent prompt，以及 req-process/cross-process 的当前窗口。核心方法是 progressive disclosure，而不是把所有说明一次性加载。

字符和行数预算只是防止仓库文件膨胀，不代表真实 token 或模型上下文。运行客户端内部机制不属于 xc881-skills，也不在本仓库中模拟或验证。

具体静态预算和审计方式见 `docs/skill-context-budget.md`。

连续队列只规定恢复行为：如果运行环境压缩了上下文，从同一 active owner、`current.md` 和当前 queue item 恢复，然后自动继续，不要求用户说“继续”。

移植任务采用双真相源：`req-process` 负责 Scope/AC/边界，`cross-process` 只负责移植规模、行为等价方法和移植进度，两者通过路径关联，不复制同一字段。

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
- requirement 委派且提供 req-process Artifact 时，bounded 调研写入其 `evidence/`，并返回同一次需求分析。

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

用户看到的输出：

```text
需求结论:
这次会做:
完成标准:
需要注意:      # 有实际风险时
需要确认:      # 只有阻塞决策时
下一步:
开发记录:
```

tracker 场景补充：

```text
事项状态:
给开发的说明:
平台操作: 已执行 | 待执行 | 未执行（原因）
```

规则：

- 不写代码。
- IR 不能伪装成 ER。
- AC 必须可测试。
- 只问一个阻塞问题。
- 能从仓库、文档、当前技术调研获得的事实，不问用户。
- tracker 写操作必须区分已经执行、计划执行、因为权限/工具缺失而跳过。
- 文档 gate 前先解析已有任务；唯一语义匹配就复用，多项匹配只问一次，没有匹配才考虑新建。
- 复用终态任务时追加 queue ID 并精确交接 artifact/current/next/blockers，Coding 不搜索任务目录。
- 复杂需求先通过 artifact gate；持久化后必须生成可验证 queue 并运行 req-process validator。
- req-process 只保存验证计划和 queue/current/blocker 状态，实际验证结果只在聊天报告。
- Spec、ER/IR、Scope、FR/NFR、AC 和风险分级保存在 req-process，不作为聊天固定标题。
- 没有 artifact 时，聊天必须把范围、完成标准、风险/假设和下一步说完整。

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

- 读取和解释真实代码
- 定位入口、调用链、数据流、配置和测试关系
- 只读 review / 架构与实现分析
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
- AI 结合读取任务和相关项目耦合决定是否启用 Coding；简单精确局部读取可直接完成，复杂/任务读取和所有写入进入 Coding。
- Coding 被选中后，打开项目或 execution artifact 前先判定 `instant | queue`，再判定 `read | change`。
- 队列项完成后自动 checkpoint、推进并继续到任务终态；除非用户明确要求逐项确认或出现真实阻塞，不询问“是否继续”。
- Requirement/Bugfix/源码文章可直接完成简单读取；委派的复杂只读证据不自动获得改动权限。
- 没有明确路径/handoff 或唯一上下文时，不扫描 `dev-notes`，直接执行即时读/改任务。
- 收到明确 req-process/cross-process handoff 时，只读取 `current.md + 当前项`，不默认读取 `index.md`、previous 或 next；执行验证后只在聊天报告结果，dev-notes 同一 patch 只更新 status、history 和 current。

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
- 简单精确局部源码证据可直接读取；复杂或任务化源码检查委派 Coding，返回证据后继续写作。

### `$xc881-porting-orchestration`

用途：

- 跨语言移植
- 跨项目迁移
- 抽象架构意图移植
- 长任务 stop boundary
- plan file
- behavior equivalence

用户看到的输出：

```text
迁移结论:
本次迁移:
如何确认成功:
需要注意:      # 有实际风险时
需要确认:      # 只有阻塞决策时
当前进度:
下一步:
开发记录:
```

规则：

- goal 任务必须先锁 stop boundary。
- 必须同时链接 `dev-notes/req-process/<task>/` 和 `dev-notes/cross-process/<task>.md`。
- req-process 保存 Scope/AC/边界；cross-process 只保存移植专有执行状态。
- goal/non-goal、规模、停止边界、技术差异、等价性证据保存在关联文档中，聊天不原样倾倒这些字段。
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

验证一个需求过程 artifact：

```bash
python skills/xc881-requirement-analysis/scripts/validate_req_process.py dev-notes/req-process/<task>
```

审计 fast path 和具体任务上下文：

```bash
python scripts/validate_context_budgets.py --report
python scripts/audit_context_sizes.py dev-notes/req-process/<active-task>
```

安装到 cc-switch 后校验仓库与安装副本一致：

```bash
python scripts/validate_installed_skills.py ~/.cc-switch/skills
```

## 维护约束

- 新增 skill 必须同步 `skills-manifest.json`、`README.md`、`evals/cross-skill-routing.json`、skill 自身 evals 和 agent prompts。
- 运行时 reference 要登记到 `docs/reference-inventory.md`。
- 所有 skill 保持 intent-routed；直接 `$skill-name` 调用是兼容入口，不是唯一入口。
- req-process 协议只在 requirement reference 中定义；其它 skill 只维护自己的消费规则，禁止复制完整协议。
- 大能力优先吸收到现有 skill 的 `references/`，不要轻易新增入口。
- README 只描述当前真实能力，不写未实现承诺。
