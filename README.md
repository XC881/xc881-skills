# xc881-skills

一套面向编码 Agent 的**意图路由、渐进加载、证据优先、可断点续跑**的四技能系统。

设计目标只有四个：
- **低 Token 激活**：宿主平时只读 4 条 `description`（合计 ≤ 1,650 字符）；命中后先走 `SKILL.md` 快路径（≤ 5,000–7,000 字符），遇到具体关切才按需加载 `references/*.md`；`docs/` 仅用于仓库维护，永不进运行时。
- **职责单主责 + 同轮自动接力**：分析、编码、源码写作、跨语言移植边界分明；前置缺口收敛后同轮自动接力落地，且**整轮只由终态主控 skill 输出唯一一份大白话契约**，不连贴多套模板头。
- **硬核工程门禁**：证伪错误前提、区分脏状态产生点与崩溃点、选型一票否决、P0–P3 审查证据链、跨语言源端实跑 Golden 向量、源码文章反水文红线全部内建在快路径。
- **可恢复队列与安全底线**：复杂任务落盘 `dev-notes/`，只读有界热窗口即可跨压缩/跨会话无损续跑；**无显式指令绝不 `git commit` / `git push`**。

---

## 快速安装与使用

```bash
# 按宿主安装（支持：cursor | claude | codex | agents | cc-switch | grok | all）
bash scripts/install.sh cursor
```

`install.sh` 会把 4 个 `xc881-*` 技能拷入对应宿主目录（如 `~/.cursor/skills/`），并安全清理已退役的旧技能目录（仅替换含 `SKILL.md` 的真实技能目录，不动软链与其他第三方技能）。

**生效与日常用法**：
1. 安装或更新后**开新会话**（或重启宿主）即可自动发现。
2. **直接说人话提需求**，无需写 `$skill-name`，也无需手写“先分析再实现”——模型会按你的真实意图与当前缺口自动选零个、单个或串联多个 skill。需要强制指定时，`$xc881-analysis` 等显式调用及旧别名（`$xc881-requirement-analysis` / `$xc881-bugfix-research` / `$xc881-solution-research` / `$xc881-issue-triage`）依然兼容。

---

## 四个 Skills 与意图路由

| Skill | 主责边界 | 何时启用 / 自动接力 | 何时跳过 |
| --- | --- | --- | --- |
| `xc881-analysis` | 范围与验收标准（Requirement）、issue/PR 分诊、根因与漏洞诊断（Bugfix）、外部技术调研（Solution） | 纯分析/分诊/调研；或构建/修复请求的**范围、根因、外部事实尚未确认**时先启用，确认后同轮链入 Coding | 范围与根因已明确；绝不写生产代码 |
| `xc881-coding-skills` | 一切代码写入、复杂/追踪式代码读取（含代码库/模块走读讲解）、Code Review、前端设计与实现、测试验证、显式 Git | 目标与根因明确的改码、模块调用链/数据流走读、PR 审查、UI 实现或重设计；或承接 Analysis / Porting 交接 | 通用概念科普、普通润色、单文件精确常量读取 |
| `xc881-source-article-style` | 面向源码读者的中文技术文章（导读、函数级精读、调用链章节、文风改写） | 交付物是中文源码分析文章；缺复杂源码证据时自动链 Coding `read`，缺外部版本/术语事实时链 Analysis | 日常聊天解释代码（“讲讲这个模块怎么实现的，不用写文章”归 Coding `read`） |
| `xc881-porting-orchestration` | 跨语言 / 跨项目迁移与行为等价证明 | 跨语言/跨项目移植（规划边界或直接迁完）；缺边界/库事实链 Analysis，改码与跑等价验证链 Coding | 同语言常规重构、仅顺口提到其他语言 |

### 典型请求怎么走

```text
简单解释一下 Git rebase / 润色一段普通中文       -> 不启用任何 skill
看下 config.py 里 TIMEOUT 常量是多少             -> 简单精确本地读取，不启用 skill
讲解这个仓库 event bus 模块的实现思路，不写文章   -> xc881-coding-skills（instant + read）
帮我 review 一下这个 diff 有没有问题              -> xc881-coding-skills（instant + read）
把 login.ts 超时从 3s 改成 5s 并跑单测            -> xc881-coding-skills（instant + change）
线上订单偶发 500，原因还不清楚，帮我修好           -> xc881-analysis（定因）-> xc881-coding-skills（修复）
做一套会员积分系统，细节没想清，定完直接实现       -> xc881-analysis（问一次产品数值/落队列）-> xc881-coding-skills（queue）
基于我贴出的这段源码笔记写篇文章                  -> xc881-source-article-style（证据已足，不串 Coding）
写一篇当前仓库 Dispatcher 分发机制的源码文章       -> xc881-source-article-style -> 链 Coding 补追踪证据 -> 纯文章输出
把这个 Python 函数翻成 Go，行为一致               -> xc881-porting-orchestration（non-goal 免账本）-> 链 Coding 实跑 Golden
把订单/支付/库存三模块整体从 Python 迁到 Go        -> xc881-porting-orchestration（goal 双账本）-> 链 Analysis + Coding
```

---

## 各 Skill 核心防线与输出契约

所有面向用户的回复**直接以契约标题行开头**（无寒暄铺垫），空的可选段直接省略，内部流程术语不外泄；同轮多 skill 接力只输出终态主控的那一份契约。

### 1. `xc881-analysis`（Requirement / Bugfix / Solution 三分支合一）

分析内部按需切换分支不换 owner（如修 bug 缺预期行为切 Requirement、定范围缺外部版本事实切 Solution）。

- **Requirement 硬防线**：
  - **先证伪错误前提（XY 检查）**：锁范围前先核对仓库与平台事实（如浏览器沙箱限制、现有代码已满足等），绝不顺着不成立的前提硬写 AC。
  - **可判定验收标准**：禁止“体验友好 / 正常处理 / 性能良好”等模糊词，完成标准必须写成可观察的 `输入 -> 结果`，同时覆盖正常路径、异常拒绝与既有功能不回退。
  - **产品数值必问一次，纯技术决策不打断**：比例、阈值、限额、定价、有效期等产品可见数值未决时，哪怕用户说了“你定、直接做”，也必须发出**唯一一次**阻塞确认（附推荐值 + 不答复时的兜底默认值）；技术栈、目录结构等纯技术选择记入 `Decision:` 直接推进。
  - 含 issue / PR / PRD tracker 状态机（`needs-triage | needs-info | ready-for-agent | ready-for-human | wontfix`）、Agent Brief 与 `.out-of-scope/` 沉淀。
- **Bugfix 硬防线**：
  - **区分上游不变量破坏点（producer）与下游崩溃暴露点（consumer）**：禁止在消费端糊 `or {}` / `try-except` 静默吞掉脏状态，并顺手标出同路径邻近隐患。
  - 仅诊断请求（“查下哪坏了”）严格止步于 `下一步: 仅诊断`，不越权改代码；允许运行最小判别性复现实验，修复后验证计划交 Coding 执行。
- **Solution 硬防线**：
  - **一票否决门禁 + 版本锚定**：先核 License、目标运行时/OS 兼容与维护状态；一手官方源码/规范/公告优先，所有外部结论必须绑具体版本号；单事实查证不硬凑多方案对比表。

输出骨架（按分支三选一）：

```text
# Requirement 分支                      # Bugfix 分支                        # Solution 分支
需求结论: <一句话结论>                  xc881 诊断: <一句话主题>              xc881 调研: <一句话主题>
这次会做: <分点范围>                    结论: <根因与置信度>                  结论: <直接答案与版本前提>
完成标准: <可判定输入->结果>            背景: <复现条件与环境>                查证点: <核查的具体问题>
需要注意: <可选，边界与风险>            依据: <file:line 与判别证据>          依据: <一手来源与版本>
需要确认: <可选，问题+建议+暂不确认兜底> 修复: <最小修复方案>                  对比: <可选，仅真多方案决策时>
下一步: <执行或等待动作>                验证: <目标+非回归验证计划>           推荐: <可选，仅真多方案决策时>
开发记录: <工件路径或免建档原因>        需要注意: <可选，邻近隐患/语义取舍>   需要注意: <可选，兼容性与风险>
                                        下一步: <交接 Coding 或 仅诊断>       下一步: <后续动作>
```

---

### 2. `xc881-coding-skills`（读写门禁 + 双维分类 + 前端设计引擎）

打开任何项目文件或执行工件前，先完成两步独立分类：
1. **持久化维度 `instant | queue`**：无明确交接且无唯一活动队列时走 `instant`（不扫 `dev-notes`）；有精确交接或唯一活动窗口时走 `queue`（只读 `current.md` + 当前切片，禁预读前后切片与默认读 `index.md`）。
2. **动作维度 `read | change`**：只读走读/审查不获改码权；改码必须通过验证才算完成。

核心工程防线：
- **防调用方与线协议爆破**：改函数签名、序列化字段名或返回结构前，必须先追全量调用方、协议契约与测试。
- **边界校验与最小补丁**：导包前先核 manifest；系统边界做输入校验，严禁空 catch 吞错；验证必须同时覆盖目标行为与失败/非回归用例。
- **Code Review 牙齿**：按 `P0–P3` 严重度排序，每条必须给出 `file:line + 具体触发输入/并发交错 -> 被破坏的不变量`；报错前先查外层调用守卫；存在 P0–P2 缺陷时压制命名/排版类 nitpick。
- **内置前端设计引擎**：内置完整 UI/UX Pro Max 离线数据与本地检索生成引擎（`skills/xc881-coding-skills/scripts/frontend_design.py`，含产品推理、配色、字体、图表、22 个技术栈规则），数据留在磁盘按需检索，不塞进提示词；既有项目的组件、token、路由、表单契约与无障碍能力始终优先。

输出骨架：

```text
# change 模式（改码 / 显式 Git）        # read 模式（代码走读 / Review）
完成内容: <改动摘要；Git 含 Commit/Branch/Push/Left>   代码结论: <核心判断或合入建议>
验证: <实跑命令与结果>                                 依据: <带 file:line 的调用链或 P0-P3 清单>
需要注意: <可选，残余风险或默认取舍>                   需要注意: <可选，未覆盖边界>
下一步: <后续动作或队列终态>                           下一步: <建议动作>
```

---

### 3. `xc881-source-article-style`（深度中文源码文章）

- **证据分级**：用户已贴出的完整源码/笔记直接复用，不再空转进仓；缺口部分精准委派 Coding `read` 补齐。运行/调试器实测 > 静态推导，**未实际运行的验证必须明标为“推导/验证计划”，严禁伪造运行输出**。
- **反水文四条红线**：
  1. 禁逐行把代码翻译成中文（“先调 A 再 if B 最后返回 C”），必须讲数据所有权、状态不变量、为什么需要这层设计；
  2. 跨线程 / 异步 / IPC / 回调 / 虚表调用不断链，必须点名**注册绑定点、承载队列/结构体、执行线程/进程上下文**；
  3. 拉黑 AI 公文套话（`优雅地实现了`、`极大地提升了`、`综上所述`、`值得注意的是`、`不言而喻`）；
  4. `本章结论` 禁复读目录，3–5 条结论必须是读源码前猜不到、带 `path:symbol` 锚点的设计不变量或能力边界。

默认函数级章节骨架：`现象/问题 -> 入口定位 -> 调用链 -> 关键源码 ->（可选）调试验证 -> 本章结论`（完整章节可含 `前言 / 须知/背景 / 方向 / 常见疑问 / 下一步`）。

---

### 4. `xc881-porting-orchestration`（跨语言 / 跨项目等价移植）

- **按量级分流，拒绝杀鸡用牛刀**：
  - **有界 `non-goal` 迁移**（单函数、单文件、单逻辑切片的一次性移植，哪怕要落地写码跑测试）：保持 `chat-only`，**免建任何 `dev-notes` 账本**，直接委派 Coding `instant` 模式实现并跑通测试，输出省略 `当前进度` 与 `开发记录`。
  - **多模块 / 整仓 / 持续 `goal` 迁移**：先锁停止边界，建立 `req-process`（管范围/AC）+ `cross-process`（管量级/等价方法/模块进度）双账本后再逐切片推进。
- **源端实跑 Golden 向量**：只要源语言实现可运行，必须在源端实跑正常、边界与畸形输入采集真值，目标端逐条回放比对——**严禁靠模型心算凑测试期望值**。
- **四大静默语义陷阱必查清单**：
  - 数值：负数整除/取模符号（Python 向负无穷 vs Go/Rust/C 向零截断）、整数位宽溢出、浮点舍入（`round` 银行家舍入 vs 四舍五入）与 `NaN/-0.0`；
  - 文本与正则：UTF-8 字节 vs UTF-16 码元 vs Unicode 码点切片、正则 Unicode/ASCII 默认模式与行尾 `$`；
  - 序列化与协议：JSON 大小写、`null` vs 缺省字段（`omitempty`/`Option`）、签名场景 map 顺序、时间戳精度与时区；
  - 控制流与并发：值拷贝 vs 引用别名、异常栈展开 vs 错误返回值的半途状态修改、取消与超时传播。

输出骨架：

```text
迁移结论: <等价性与可推进判断>
本次迁移: <源 -> 目标映射范围>
如何确认成功: <Golden 实跑向量数与验证命令>
需要注意: <可选，已处理的语义陷阱与类型域边界>
需要确认: <可选，仅真实阻塞时>
当前进度: <仅 goal 任务保留>
下一步: <后续动作>
开发记录: <仅 goal 任务保留双账本路径>
```

---

## 持久化队列与低 Token 上下文设计

复杂多步任务通过 `dev-notes/` 落盘，每次续跑或上下文压缩恢复时只读**当前热窗口**，不重扫历史与全局规划：

```text
dev-notes/
  req-process/<YYYYMMDD>-<slug>/     # 需求队列（Analysis 建档维护，Coding 按窗口消费）
    index.md                         # 冷读契约（上限 20,000 字符）：ID: <id>，存 Scope/AC/风险，禁存 State
    current.md                       # 热读唯一状态权威（≤ 1,200 字符）：Task(=ID) / State / 路径指针 / 恢复摘要
    history.md                       # 追加式状态流转记录（Q-NNN: old -> new）
    queue/Q-NNN-<slug>.md            # 纵向可验证切片（非终态 ≤ 3,500 字符，内部链接用裸 Q-NNN）
    decisions/  evidence/            # 可选：决策档案与有界外部调研证据
  cross-process/<slug>.md            # 仅 goal 级移植使用（≤ 4,500 字符）：量级 / 等价方法 / 模块状态 / 风险
  design-system/<slug>/MASTER.md     # 仅跨多页或跨会话 UI 系统使用（≤ 3,000 字符，页面覆盖 ≤ 1,200 字符）
```

关键不变量：
- **单一可变真相源**：`current.md` 是任务状态与当前指针的唯一权威；队列项 `Status` 只用 `pending | ready | blocked | done | skipped`（严禁 `in-progress`），任务 `blocked` 时当前项必须同步为 `blocked`，终态（`done | cancelled | superseded`）置 `Current/Next: none`。
- **连续推进不停顿**：队列切片验证通过后，同一补丁更新 item status + `history.md` + `current.md` 并自动推进下一项直至终态；只有用户明确要求逐步暂停或遇到真实阻塞才停下。验证输出与日志只报聊天，不写进 `dev-notes`。
- **完整静态上下文预算定义**：见 [`docs/skill-context-budget.md`](docs/skill-context-budget.md)。

---

## 仓库验证与维护命令

```bash
# 全量校验（上下文预算、前端数据完整性、4 个 skill 校验器、路由与契约单测、账本校验器自测）
python3 scripts/validate_all.py

# 查看各 skill 快路径与描述字符预算报告
python3 scripts/validate_context_budgets.py --report

# 审计各场景冷启动/续跑的声明加载体积，或审计具体任务热窗口体积
python3 scripts/audit_skill_loads.py --baseline HEAD
python3 scripts/audit_context_sizes.py dev-notes/req-process/<active-task>

# 显式审计某个持久化账本（仅用于审计/修损/CI，常规执行不把校验器当试错循环）
python3 skills/xc881-analysis/scripts/validate_req_process.py dev-notes/req-process/<task>
python3 skills/xc881-porting-orchestration/scripts/validate_cross_process.py dev-notes/cross-process/<task>.md

# 核对本机已安装副本与仓库源码是否一致
python3 scripts/validate_installed_skills.py ~/.cursor/skills
```

维护约定：新增或调整路由/规则时，同步更新对应 `SKILL.md`、`references/`（登记至 `docs/reference-inventory.md`）、`evals/`、`agents/*.yaml` 与 `validate_skill.py` 防回退断言，确保 `python3 scripts/validate_all.py` 全绿后再提交安装。
