# xc881-skills

`xc881-skills` 是一组低 token、强边界、可交接的 agent skills。

这里的低 token 指**只补读当前任务缺少的最少充分信息，然后把事情做完整**：已有完整、仍适用的规则直接复用，不因新一轮对话再次读取。它不是删除知识、减少能力，也不是把完整资料库读进上下文。

核心思想：

- 分析和执行分离，先把问题说清楚，再让 coding 层改代码。
- `SKILL.md` 是 fast path，只放运行时必须读的内容。
- `references/` 是运行时按需读取的细节规则。
- `docs/` 是维护文档，不作为默认运行时上下文。
- 模型结合**用户意图 + 任务实际所需方向（前置缺口/就绪度）**自主选用零个、单个或按阶段串联的 skill，无需用户手写“先分析再实现”等流程词。
- 同一阶段只有一个主责 skill，其他 skill 只接受有界委派并把结果交回。
- 默认输出紧凑；大输出写文件，只在聊天里报告路径、进度和验证。
- `dev-notes/` 是首选开发笔记根目录；复杂需求使用 `dev-notes/req-process/` 持久化。
- 不隐式提交、不隐式推送。

## 支持的 skills

当前仓库支持 4 个 skills。`$xc881-analysis` 统一承接所有分析产物，内部三个分支按需启用：

| Skill | 触发 | 类型 | 用来做什么 | 不做什么 |
| --- | --- | --- | --- | --- |
| `$xc881-analysis` | 意图隐式 / 直接调用 | 分析 | requirement 分支：需求分析、范围、AC、PRD、issue/PR 分诊、PRD 拆 issue、Agent Brief；bugfix 分支：bug、回归、漏洞、性能问题的证据、复现、根因、修复计划、验证计划；solution 分支：联网技术调研、单事实查证、方案比较、可行性判断 | 不写代码，仅诊断时不自动改代码，不输出 exploit 步骤，不为单事实强造方案对比 |
| `$xc881-coding-skills` | 意图隐式 / 直接调用 | 读码/执行 | 读代码、入口/调用链/数据流分析、解释、review、实现、重构、修复、验证、提交/推送前检查 | 范围不清时不硬写代码 |
| `$xc881-source-article-style` | 意图隐式 / 直接调用 | 写作 | 源码导读、函数级分析、调用链文章、调试证据型中文技术文章 | 不改代码，不写泛泛教程 |
| `$xc881-porting-orchestration` | 意图隐式 / 直接调用 | 编排 | 跨语言/跨项目迁移，锁边界、写计划、识别风险、验证等价性 | 边界/规划请求不自动编码，不替代 specialist skills |

分析层内部的分支切换不产生委派：诊断中遇到 expected/scope 缺口、scope 中遇到外部事实缺口、分诊中需要根因，都在 Analysis 内部切到对应分支继续，不换 owner。旧名 `$xc881-requirement-analysis`、`$xc881-bugfix-research`、`$xc881-solution-research` 保留为 `$xc881-analysis` 的别名，直接调用仍有效。

## 触发规则

所有 skills 都支持意图隐式触发，也支持直接 `$skill-name` 调用。

路由由模型结合**用户的真实意图**与**任务当前实际所需方向（就绪度与缺口）**自主决定，既不要求出现 `xc881`，也不要求用户手写“先分析再实现”、“先定位再修复”之类的流程指令。

模型按两个维度自主选 skill（零个、单个、按阶段自动串联或中途切换）：

1. **用户意图是什么**：要结论/方案、要功能落地、要修好故障、要读懂/审查代码、要中文源码文章、还是要跨语言/项目迁移。
2. **任务当前实际缺什么**：
   - 范围、目标与根因**已明确** -> 直接进 `$xc881-coding-skills` 执行，不空转分析仪式；
   - 用户直接说“修好这个 500”或“做一套权限系统”，但**根因未证实、范围/验收未定或外部版本事实不明** -> 模型先选 `$xc881-analysis` 把根因/边界/事实收敛清楚，确认后自动串联 `$xc881-coding-skills` 落地，不要求二次调用；
   - 用户要**跨语言/跨项目迁移并合入** -> 先走 `$xc881-porting-orchestration` 锁行为等价与目标架构，再串 `$xc881-coding-skills` 改码与跑等价验证（缺边界或库事实时按需拉 `$xc881-analysis`）；
   - Coding 执行中途撞上**契约冲突、隐藏范围决策或两次修复失败** -> 主动切回 `$xc881-analysis` 补齐缺口后再继续，不硬猜硬改；
   - 顺带出现的名词（如文章里提到“代码”、改单行时提到语言名）只要不是任务实际需要的环节，绝不机械触发无关 skill。

直接调用示例：

```text
$xc881-analysis 分析这个功能
$xc881-analysis 调研这个技术方案
```

常用意图示例：

```text
帮我调研技术方案 -> $xc881-analysis（solution 分支）
帮我分析需求 -> $xc881-analysis（requirement 分支）
这个接口 500 帮我看看 -> $xc881-analysis（bugfix 分支）
把 login.ts 超时从 3000ms 改成 5000ms 并跑单测 -> 目标明确，直接 $xc881-coding-skills
线上订单偶发 500，原因还不清楚，帮我修好 -> 自主串联 $xc881-analysis（定因）-> $xc881-coding-skills（修复验证）
帮我做一套多租户权限系统，目前只有初步想法 -> 自主串联 $xc881-analysis（收敛范围/AC）-> $xc881-coding-skills（实现）
读取 src/version.ts 的 VERSION 常量 -> 简单读取，不启用 skill
简单解释 Git rebase / 润色普通中文 -> 不启用 xc881 skill
帮我读一下这个模块的入口和调用链，不要改代码 -> $xc881-coding-skills（read 模式）
把这个 Python 签名模块迁成 Rust 并合入当前仓库跑通测试 -> 自主串联 $xc881-porting-orchestration -> $xc881-coding-skills
按我的文章风格写一篇源码导读 -> $xc881-source-article-style（缺复杂调用链时自动拉 Coding read）
帮我把这个项目改写成另一种语言，先只定边界 -> $xc881-porting-orchestration
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

直接调用始终有效；隐式触发由模型根据“用户意图 × 任务实际缺口/方向”自主决策，不靠固定中文词表：

```text
用户意图 + 任务当前缺口 -> 零 skill | 单主责直达 | 前置 skill 收敛缺口后自动串联执行 skill
```

普通模型能力足以完成、且没有 xc881 特有合同的任务，不包装进 skill；目标与根因已明确的小改动也直达 Coding，只有范围、根因、外部事实或跨语言等价性确实未决时才先走前置 skill。

`$xc881-coding-skills` 负责所有项目写入和复杂工程读取。AI 会同时判断用户要读什么、需要多少证据，以及项目相关部分的耦合复杂度。只有目标明确、局部、低风险、无需调用链/运行时重建且不属于任务队列的读取，才可直接完成；路径未知、跨模块、调用/数据/状态流、架构生命周期、安全、性能、并发、生成代码、框架魔法、跨语言或后续可能改代码时，使用 Coding。项目大本身不是唯一理由，相关耦合才是。

## 能力取舍

主要收益：

- 用户不需要记住具体 skill 名，普通自然语言会按意图进入合适流程。
- 技术调研、需求分析、bug 诊断、代码执行、源码写作、移植编排的边界更清楚。
- 三个分析能力（scope/AC/分诊、bug 诊断、外部调研）合并进 `$xc881-analysis`，分析内部切分支不再产生委派，减少入口数量，保留 tracker 状态机、Agent Brief、PRD 拆 issue、out-of-scope 和 map/child tickets。
- eval、routing matrix 和 validator 会一起约束触发行为，降低文档和实际路由不一致的风险。
- 前端设计、视觉 review、重设计和 image-to-code 都在 Coding 内；只有现有证据无法决定当前设计 concern 时才自动加载设计情报 reference，随后按实际环节继续加载对应 reference，不等待用户再次请求，也不新增会误触发的审美 skill。
- 大输出默认写文件或分段 artifact，聊天里只报告路径、进度和验证，符合低 token 策略。
- 单事实、仅诊断、聊天内小需求、已有证据写作和仅迁移边界都有轻量分支，不会为形式完整跑满工作流。

主要代价：

- 隐式路由仍依赖意图判断；因此 description、routing eval 和单主责边界需要持续维护。
- 维护新增意图时必须同步 `skills-manifest.json`、`README.md`、`evals/cross-skill-routing.json`、skill 自身 trigger eval、agent prompts 和 validator。
- 分析/执行分离会让确实需要范围或根因的任务先分析再执行，但仅诊断或仅规划不会自动进入 Coding。
- 直接 `$skill-name` 仍然是兼容入口；当用户想绕开意图判断时，推荐显式指定。

## 开发笔记与 Req Process

需求分析不再默认只存在于聊天。Requirement 先判断这是不是已有需求的改动：优先使用用户给出的路径或当前对话唯一明确的任务；只有可能持久化或交给 Coding 执行、且上下文不足时，才从仓库根运行 `python scripts/find_req_process_candidates.py <root> <identity terms>` 返回最多 5 个候选路径，再只读取可能相关的 `index.md` 做语义比较。该入口转调 skill 内实现，不做语义匹配。明确的一轮聊天分析不扫描 `req-process`。唯一匹配就复用，多项匹配只问一个选择问题，不能按最新目录或关键词直接决定。

只有确认没有匹配后才进入文档 gate。用户未指定时，AI 在跨会话、3 个以上可验证任务、跨模块契约、迁移/数据/权限/安全风险、外部调研或长期实现等情况下，自动创建（由 Analysis 的 requirement 分支维护）：

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

复用已完成任务时，不重建目录或重写历史：新 queue ID 接在旧尾节点之后，任务重开为 `ready`，Requirement 把精确的 artifact、current、next 和 blockers 交给 Coding。Coding 只消费这个 handoff；直接读取发现损坏才回到 Requirement，正常路径不靠 validator 搜索候选或试错。

读请求先经过复杂度门槛：简单读取可由当前分析/写作流程直接完成；所有写入、任务读取和复杂读取进入 Coding。Coding 被选中后，在打开实际项目文件或执行 artifact 前，再判断临时还是任务：

| 持久化模式 | 识别条件 | Coding 行为 |
| --- | --- | --- |
| `instant` | 用户未提供 artifact/handoff，当前上下文也没有唯一明确的队列任务 | 不扫描、不读取 `dev-notes`，直接读代码或改代码 |
| `queue` | 用户明确给出 req-process/cross-process 路径或 handoff，或当前对话唯一明确指向一个活动任务 | 只读 `current.md` 和当前 queue item，不默认读 `index.md`、previous 或 next |

如果同时存在多个可能的 artifact，Coding 只问一个阻塞选择问题，不能扫描目录后猜“最新任务”。`read | change` 是另一条独立维度，因此四种组合都成立：即时读、即时改、队列读、队列改。队列项必须自带当前执行合同；previous 只有被当前项明确引用证据/依赖时才读，next 等推进为 current 后再读。

Analysis 或源码文章保留自己的分析/写作职责：简单精确局部证据可直接读取，复杂或任务化源码检查委派为 Coding 的 `read`。Coding 只返回约定证据，不会把只读请求自行升级成改动；requirement 分支自己维护 req-process 文档不触发 Coding，避免循环调用。

队列 checkpoint 是恢复点，不是默认确认点。Coding 完成当前项后会验证、更新 status/history/current，把 next 推进为 current，再只读取新的 current 窗口并继续，直到整个需求终态。只有用户明确要求逐项确认/每项暂停，或遇到输入、权限、审批、安全、范围变化等真实阻塞时才停止。

自动上下文压缩同样不是确认点。压缩完成后保留 active owner、被选 skill 和精确 current 窗口，自动继续同一次 Analysis、文章、Porting 或 Coding 流程，不要求用户说“继续”。

如果当前 queue item 信息不完整、与实际代码冲突、用户要求改变 Scope/AC，或队列需要重新规划，Coding 不自行读取 `index.md` 或改需求，而是返回 Requirement。Requirement 读取完整合同并生成新的 current 窗口后，再交回 Coding。

进度只使用 queue done/total、current 和 blocker，不使用主观百分比或验证结果计数。简单、单轮、单目标任务可以不创建文档，但 Requirement 必须在“开发记录”中说明为什么无需文档。若创建文档，完整工程字段留在文档中，聊天只用人话报告结论、当前工作、下一步和阻塞项。

上下文硬预算只卡每次恢复都要读的热文件：`current.md <= 1,200` 字符、当前 queue item `<= 3,500`（装不下说明切片该拆，不是上限该放大）。`index.md` 是冷读的稳定契约，只设 20,000 的失控天花板，稳定细节溢出去 `decisions/` 和 `evidence/`；`history.md`、`decisions/`、`evidence/` 不设字符上限。cross-process ledger `<= 4,500`（已完成模块可折叠汇总，item 状态禁止 `in-progress`）、design-system `MASTER.md <= 3,000`、surface override `<= 1,200` 同属按交接时读取设定的有界契约。有界技术调研可写入 evidence；验证命令输出、通过/失败详情和日志只在聊天报告，不写入 dev-notes。

视觉系统只有在用户明确要求，或新/重构视觉系统需要跨 2 个以上页面、跨会话复用、或指导队列任务时才创建。Requirement 把它写在 `dev-notes/design-system/<slug>/MASTER.md`，页面差异才追加 `surfaces/<surface>.md`；Coding 只在当前视觉 concern 到达后读取精确 handoff，绝不扫描目录。已有项目 tokens、组件和品牌始终优先，普通单页面设计不创建这类文档。

### Skill 上下文边界

安装多个 Skills 不等于每轮加载全部正文。按 Agent Skills 的分层设计，metadata 用来选择技能，`SKILL.md` 承载选中后的主流程，references/scripts 只在当前任务需要时读取或执行。具体客户端的发现方式和可用工具可能不同，不假定统一的上下文配额。

约束 skill 自己的读取：控制过宽的触发描述、过多主责、小任务被迫跑完整链路和无必要委派。

xc881 的约束是：每个 description 最多 320 字符、四个合计最多 1,650 字符；只选一个阶段主责；允许零 skill；references 按分支读取；Analysis 三个分支、Source、Porting 都有轻量分支；不存在“只要 1% 可能适用就必须调用”的全局启动器。

本仓库只优化自己能够控制的内容：skill 元数据、被选中的 `SKILL.md`、按需 reference/script、agent prompt，以及 req-process/cross-process 的当前窗口。核心方法是 progressive disclosure 和最小充分激活，而不是把所有说明一次性加载。

字符和行数预算只是防止仓库文件膨胀，用来约束入口体积，不代表模型上下文。

**每轮判断意图，不等于每轮重读正文。** 四个入口采用同一规则：

| 当前情况 | 行为 |
| --- | --- |
| 消息已提供完整正文，或所需规则仍在上下文且无已知变化 | 直接复用，不额外读一次文件 |
| 只有名字、路径、加载标记，或压缩后缺少必要规则 | 沿选中技能的精确路径补读缺失内容 |
| 做到新 concern，所需 ref 尚未提供 | 自动补读该 ref；返回已覆盖 concern 不重启路由 |
| 已知规则有相关更新，或用户明确要求重读 | 定向重新读取；更高优先级调用要求始终有效 |

新子任务必须在自己的上下文中得到足够的指令，不能继承父任务的“已加载”标记。返回原任务时复用仍有效的规则和有界证据；`current.md`、代码、外部证据和设计合同的新鲜度另行判断，不因静态规则可复用而省略必要检查。

不新增每轮加载登记文件、哈希轮询、必读公共 ref 或缓存代理。仓库修改也必须同步到实际使用的安装副本才会生效，核对内容而非仅核对版本号。

四个 skill 共用同一条执行原则：仍有效的证据与上下文内已有规则不重复读取；只补当前决定所缺的部分；委派只返回需要的证据、限制和下一步，然后继续原任务。不同角色/分支的强化点是：

| Skill / 分支 | 更有效的行为 |
| --- | --- |
| Coding | 按风险读取工程规则；机械改动不强制设计仪式；真实前端引擎按需执行 |
| Analysis · requirement | 补齐影响范围和验收的缺口，验收关联实际需求与可观察结果 |
| Analysis · solution | 按版本和时效复用证据，问题已足够支撑决定就停止扩搜 |
| Analysis · bugfix | 用最小区分性观察排除假设，不能把“看起来能修”当成根因 |
| Porting | 先确定输出、错误、状态和副作用如何等价，再迁移当前片段 |
| Source Article | 重要结论落到源码证据，区分调用存在与运行顺序，不为凑章节编造事实 |

维护时可运行 `python scripts/audit_skill_loads.py --baseline HEAD`，查看四个入口、典型分支体积及有明确前提的多轮预期读取。它报告字符数和声明路径，用来约束该读什么，不运行模型。已安装 tiktoken 时可用 `--encoding <编码名>` 单独测文本 token。

CI 默认不调用模型。

具体静态预算和审计方式见 `docs/skill-context-budget.md`。

官方依据：[OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)、[Anthropic Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)、[Anthropic Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)。

连续队列只规定恢复行为：如果运行环境压缩了上下文，从同一 active owner、`current.md` 和当前 queue item 恢复，然后自动继续，不要求用户说“继续”。

移植任务采用双真相源：`req-process` 负责 Scope/AC/边界，`cross-process` 只负责移植规模、行为等价方法和移植进度，两者通过路径关联，不复制同一字段。

## 推荐流程

### 1. 技术方案不确定

```text
idea / unfamiliar stack / external technical uncertainty
  -> $xc881-analysis
  -> $xc881-coding-skills
```

示例：

```text
用xc881调研 Supabase 和 Firebase 的技术方案差异
用xc881调研 React Server Components 在这个项目里是否适合
$xc881-analysis 查一下 GitHub Actions OIDC 部署 AWS 的官方做法
```

### 2. 功能、PRD、范围、验收标准

```text
feature / PRD / scope / acceptance criteria
  -> $xc881-analysis
  -> 外部事实缺口在 Analysis 内切 solution 分支做 bounded 调研
  -> $xc881-coding-skills
```

示例：

```text
用xc881分析这个登录功能的范围和验收标准
用xc881把这个想法整理成 PRD 和 AC
$xc881-analysis 分析现有会员系统要加优惠券，需要哪些 must-not-regress
```

### 3. issue / PR / PRD tracker 工作流

`xc881-issue-triage` 的能力已并入 `$xc881-analysis` 的 requirement 分支。

```text
issue / PR / PRD tracker workflow
  -> $xc881-analysis
  -> 需要 bug 根因诊断时在 Analysis 内切 bugfix 分支
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
  -> $xc881-analysis
  -> expected/scope 缺口在 Analysis 内切 requirement 分支
  -> $xc881-coding-skills 仅当用户要求修复/实现
```

示例：

```text
用xc881修复登录 500，先定位原因
$xc881-analysis 根据这段日志分析根因和验证计划
用xc881分析这个依赖 CVE 是否影响当前版本
只分析这个接口 500 的根因和修复方案，不改代码
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

前端设计任务同样直接进入 Coding。已有项目先复用组件、tokens 和品牌；新建或整体重做界面、且没有可复用设计系统时，自动调用 UI/UX Pro Max 引擎生成适合该项目的候选。局部缺口只查对应领域。工作推进到实现、图像、重设计/视觉验收或特殊模式时，再自动加载下一个需要的 reference，不等待用户手动调用，也不预加载整套规则。

已经引入 UI/UX Pro Max **完整开源数据、原生检索/生成引擎和 xc881 本地 CLI**，不是原来的少量固定候选。当前固定快照包含 192 类产品/配色/推理规则、79 个可检索风格、74 组字体配对、1,934 条字体记录、图标/图表/UX/动效资料，以及 22 个技术栈。数据留在磁盘，不作为提示词加载。

CLI 默认只返回 1 个结果，真实比较时最多 3 个；默认结果不超过 4,200 字符，需要代码或规则细节时通过精确记录 ID 展开完整字段，不截断代码。无匹配会明确返回空结果，生成器的补位建议会标明缺失来源。普通调用不联网、不安装依赖、不写文件；仅查询/生成需要 Python 3.9+。

以下命令从本仓库根目录执行；技能安装后由智能体使用该 skill 的实际路径，不要求用户手动输入：

```bash
python skills/xc881-coding-skills/scripts/frontend_design.py "time series trend" --domain chart
python skills/xc881-coding-skills/scripts/frontend_design.py "form accessibility react 18" --stack react
python skills/xc881-coding-skills/scripts/frontend_design.py "healthcare scheduling dashboard" --design-system --surface app
```

生成结果仍需检查任务适配、可访问性、中文字体覆盖和版本限制。应用界面不继承营销页结构，已有系统不被替换，推荐不等于合规证明。跨页面/会话需要复用的已确认系统由 Requirement 写到 `dev-notes/design-system/`；普通生成只是候选，不强制落文档。CLI 也支持显式 `--persist --project-root <项目> --slug <名称>` 导出 proposal，但不会覆盖旧文件，proposal 不能直接充当已确认执行合同。

上游 npm `uipro` 主要负责安装独立技能；xc881 通过自己的安装脚本分发完整引擎和数据，不另装一个竞争主责的 skill。来源、许可证、更新和验证方式见 [集成说明](docs/ui-ux-pro-max-integration.md)。

```text
给现有 React 产品页做可访问的视觉重设计，保留路由和业务行为
把设计参考图实现成响应式营销页，先提取视觉系统再写代码
检查营销页在手机上的文字溢出和暗色模式，不改代码
修复按钮点击事件，外观保持不变
```

只有视觉概念图、且明确不写代码时，不会为了生成图片而启动 Coding。

### 6. 源码阅读文章

```text
source evidence
  -> $xc881-source-article-style
  -> 需要解释专有术语时自动 bounded 委派 $xc881-analysis
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
  -> 必要时委派 $xc881-analysis 定义边界和风险
  -> 必要时委派 $xc881-analysis 调研语言/框架迁移坑
  -> 要求实现时委派 $xc881-coding-skills 执行 port + equivalence check
```

示例：

```text
用xc881移植这个 Go 服务到 Rust
$xc881-porting-orchestration 把这个 Python 模块迁移到 Go，先定边界
用xc881迁移这个 C++ 模块到 Rust，要求行为等价
```

## 详细说明

### `$xc881-analysis`

一个分析 owner，三个分支按请求产物选择，内部分支切换不产生委派。

requirement 分支用途：

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

bugfix 分支用途：

- bug / regression / stack trace / perf 问题分析
- dependency vuln / code vuln / CVE / GHSA / OSV / CWE / OWASP 判断
- 复现计划
- 根因定位
- 最小修复计划
- 验证计划

输出结构：

```text
xc881 诊断:
结论:
背景:
依据:
修复:
验证:
需要注意:
下一步:
```

安全问题附加：

```text
严重程度:
编号: CVE/GHSA/OSV/CWE/OWASP
影响范围:
可利用性:
缓解措施:
```

solution 分支用途：

- 技术路线调研
- 方案可行性判断
- 框架/库/协议/标准查证
- 多方案比较
- 论文、RFC、官方文档、security advisory 查证

输出结构：

```text
xc881 调研:
结论:
查证点:
依据:
需要注意:
下一步:
```

只有真实方案决策才附加：

```text
对比:
推荐:
```

规则：

- 不写代码、不 commit、不跑 exploit。
- IR 不能伪装成 ER；AC 必须可测试；事实、推断、推荐必须分开。
- 锁范围/写 AC 之前先用仓库与平台事实核验用户前提（XY 检查）；前提不成立先证伪并给出可行替代，不顺着错误假设写验收。
- 产品可见数值（比例/阈值/限额/定价/有效期等用户可能有偏好的取值）未决时，即使用户已授权实现，也问一次阻塞问题——带推荐答案与安全兜底，未答复按兜底推进；纯技术决策（栈、结构、持久化方式）记 `Decision:` 直接推进，不打断。除此一处阻塞问题外不问用户；能从仓库、文档、当前技术调研获得的事实，不问用户。
- 诊断区分上游不变量破坏点（producer）与下游崩溃暴露点（consumer）；不用 `or {}` 式静默兜底掩盖上游违约，并顺手标出同路径邻近隐患。诊断先建立 tight repro loop；假设要可证伪；最小化复现后再给根因。
- 三套输出共用大白话骨架：结论先行 → 依据 → 做法/对比 → 验证 → 需要注意 → 下一步；内部字段（Spec/RQ/Cause/AC 等）留在 artifact 或 handoff，不直接给用户看。
- 同一轮自动接力到底时，整轮只由终态/主控 skill 输出一份用户契约：Analysis→Coding 同轮修完只出 `完成内容`，Porting→Coding 同轮迁完只出 `迁移结论`，不连贴多套模板头；中间环节的根因与证据折进终态契约。
- 调研优先一手资料：官方文档、标准、论文、维护者 issue/PR、vendor advisory；单事实、标准或版本查证只输出证据、影响、风险和 handoff，不制造空的 对比/推荐；证据不足时输出 blocker 和下一步 research，不强行 推荐。
- 内部分支切换：expected/scope 缺口切 requirement，外部事实缺口切 solution，根因证据缺口切 bugfix，答案回到原分支，不换 owner。
- tracker 写操作必须区分已经执行、计划执行、因为权限/工具缺失而跳过。
- 简单精确局部证据可直接读取；复杂或任务化源码检查委派为 Coding 的 `read`；委派的只读证据不自动获得改动权限。
- 文档 gate 前先解析显式/对话中的已有任务；只有可能持久化或执行且身份不足时才搜索候选，聊天内小分析不扫描目录。
- 复用终态任务时追加 queue ID 并精确交接 artifact/current/next/blockers，Coding 不搜索任务目录。
- 复杂需求先通过 artifact gate；持久化时先按写前不变量一次性生成关联的 queue/current/history，不能把 req-process validator 当成试错工具。validator 只用于显式审计、已发现损坏后的修复和仓库/CI 维护。
- req-process 只保存验证计划和 queue/current/blocker 状态，实际验证结果只在聊天报告；委派调研写入 artifact 的 `evidence/`。
- Spec、ER/IR、Scope、FR/NFR/AC 和风险分级保存在 req-process，不作为聊天固定标题。
- 没有 artifact 时，聊天必须把范围、完成标准、需要注意和下一步说完整。
- bug issue 的 tracker brief 由 requirement 分支承接，bugfix 分支提供 evidence/cause/fix/verify。
- 仅诊断请求以 `下一步: 仅诊断` 或下一项所需证据结束，不自动进入 Coding change。

### `$xc881-coding-skills`

用途：

- 读取和解释真实代码
- 定位入口、调用链、数据流、配置和测试关系
- 只读 review / 架构与实现分析
- 实现功能
- 修复 bug
- 重构
- 工程质量优化
- 用户界面实现、视觉 review、重设计和 image-to-code
- 响应式布局、真实资产、交互状态、可访问性、动效和截图级验证
- review
- 测试和验证
- 显式提交/推送

最终回复（直接以标题行开头，空的可选项省略）：

改动 / 显式 git（`change`）：

```text
完成内容:
验证:
需要注意:
下一步:
```

复杂读取 / 代码审查 / 受托只读（`read`）：

```text
代码结论:
依据:
需要注意:
下一步:
```

规则：

- 每个改动行都要能追溯到请求、证据、验证或本次改动造成的清理。
- review 按 P0-P3 严重度排序，每条给出 `file:line` + 具体触发输入/交错与被破坏的不变量；存在 P0-P2 缺陷时压制纯排版 nit；报告前先查外层调用守卫，不凭猜测报 bug。
- 不做无关重构。
- 不加 speculative abstraction。
- 领域逻辑不泄漏到 UI、SQL、SDK callback、framework handler。
- 测 public seam，不测内部实现细节。
- 避免 tautological tests。
- mock 只放系统边界。
- 没有显式要求时不 commit、不 push。
- Coding 只在当前阶段是实现/复杂读取主责或收到有界委派时启用，不因别的 skill 顺带提到代码而并行抢占。
- AI 结合读取任务和相关项目耦合决定是否启用 Coding；简单精确局部读取可直接完成，复杂/任务读取和所有写入进入 Coding。
- Coding 被选中后，打开项目或 execution artifact 前先判定 `instant | queue`，再判定 `read | change`。
- 队列项完成后自动 checkpoint、推进并继续到任务终态；除非用户明确要求逐项确认或出现真实阻塞，不询问“是否继续”。
- Analysis/源码文章可直接完成简单读取；委派的复杂只读证据不自动获得改动权限。
- 没有明确路径/handoff 或唯一上下文时，不扫描 `dev-notes`，直接执行即时读/改任务。
- 收到明确 req-process/cross-process handoff 时，只读取 `current.md + 当前项`，不默认读取 `index.md`、previous 或 next；执行验证后只在聊天报告结果，dev-notes 同一 patch 只更新 status、history 和 current。
- 前端先读取真实页面、组件、token、资产和平台约束；无可复用系统的新建/整体重做 UI 默认生成项目候选，其他情况仅在当前决策缺少证据时查对应领域。实现、图像、视觉验收和特殊模式的 ref 仍按实际关切自动加载。外观不变的事件/数据绑定修复不加载前端规则。
- 可复用视觉系统不写入业务项目根目录：Requirement 仅在持久化 gate 通过时创建 `dev-notes/design-system/<slug>/MASTER.md` 和必要的页面 override；Coding 按 exact handoff 读取，不扫描、不开新全局默认，也不让上游建议覆盖现有系统。
- 既有设计系统、品牌、路由、表单、主题、可访问性、内容和用户范围优先于通用审美规则；不因“更好看”而自动安装包、换字体、加暗色模式或改信息架构。
- image-to-code 会把可靠的设计图当作实现证据，提取排版、间距、媒体和控件逻辑后再编码；缺图时不伪造 div 截图或虚构社交证明。
- 前端重设计先审计并保护路由、导航、表单契约、logo、legal、analytics/meta 和已有无障碍能力；有浏览器工具时检查桌面和窄屏截图，没有工具时明确未观察到的视觉边界。

### `$xc881-source-article-style`

用途：

- 中文源码导读
- 函数级源码分析
- 调用链解释
- 调试证据型文章
- 架构/生命周期章节

默认结构：

```text
现象/问题 -> 入口定位 -> 调用链 -> 关键源码 -> 调试验证 -> 本章结论
```

规则：

- 入口和调用链必须有推导路径。
- runtime/debugger/tracer 证据优先于静态推断。
- 静态推断必须标明依据；未实跑的验证只能写成验证计划，不伪造运行结果。
- 禁止逐行翻译代码；必须讲清数据所有权、状态不变量与分支/间接层存在的理由。跨异步/IPC/回调须点名注册点、承载结构与执行线程/进程上下文。
- 禁 AI 公文腔（如“优雅地实现了”“极大地提升了”“综上所述”“值得注意的是”“不言而喻”）；结论必须是读源码前猜不到、带 `path:symbol` 锚点的不变量或边界。
- 专有术语先介绍，再在后文依赖。
- 可能过期的 API/版本事实自动用 `$xc881-analysis` 查官方来源。
- 已提供的源码证据直接复用；只补缺失的简单局部证据，复杂或任务化检查才委派 Coding，返回证据后继续写作。

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
- goal/queue 任务必须同时链接 `dev-notes/req-process/<task>/` 和 `dev-notes/cross-process/<task>.md`；单函数/单文件/单切片的有界 non-goal 迁移（含落地实现+自测）保持 chat-only，免建双账本。
- req-process 保存 Scope/AC/边界；cross-process 只保存移植专有执行状态。
- goal/non-goal、规模、停止边界、技术差异、等价性证据保存在关联文档中，聊天不原样倾倒这些字段。
- 等价性看行为，不看结构相同；golden 期望值必须由源实现实跑采集，不靠心算；显式检查取模符号/整宽/浮点舍入/Unicode 单位/JSON null 与缺省/顺序/别名/错误传播/取消等静默语义陷阱。
- 目标项目已有架构时，迁入目标架构，不照搬源架构。
- 抽象意图移植时，用 intent fidelity，并记录 adopt/adapt/reject。
- 用户只要求边界/规划时不委派 Coding；只有明确实现意图或可执行队列才开始迁移。

## 安装和验证

安装到本机 skill 目录（目标：`agents|claude|codex|cursor|cc-switch|grok|all`）：

```bash
bash scripts/install.sh cursor
bash scripts/install.sh all
```

`install.sh` 把当前 `xc881-*` 技能拷到对应宿主目录，并安全清理已合并退役的旧 `xc881-*` 技能目录（仅当旧路径为含 `SKILL.md` 的真实目录时才清理；软链或非 skill 目录不会动）。目标根路径不能是空、`/` 或 `$HOME`。若目标技能目录已存在，只有它是含 `SKILL.md` 的目录才会被替换；不是 skill 目录的路径不会删除。这不是备份/还原，确认过的 xc881 目录仍会被覆盖。

验证仓库结构、frontmatter、trigger eval、behavior contract：

```bash
python scripts/validate_all.py
```

显式审计或修复已发现损坏的需求过程 artifact（常规创建/推进不运行）：

```bash
python skills/xc881-analysis/scripts/validate_req_process.py dev-notes/req-process/<task>
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
