# learn-ai-agent · AI Agent 学习仓库 & 作品集

从零到生产，跟完 **Track B — Agent Builder** 全路线（[WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)，Stage 0-7，2026-08 起）。

每个 stage 都是"概念 → 亲手写 → 自建 eval 验证 → 出口考核"的闭环，所有练习可运行、带观察记录。毕业设计是一个**真在 GitHub Actions 上每周自动跑的 production agent**（见下方亮点项目）。

## 🏆 毕业设计：study-review agent（每周自动学习复盘）✅

[![weekly-review](https://github.com/zkr05/learn-ai-agent/actions/workflows/weekly-review.yml/badge.svg)](https://github.com/zkr05/learn-ai-agent/actions/workflows/weekly-review.yml)

把 Stage 5 的 study-review skill 按 Stage 7 生产化设计升级成完整 agent：[`study-review-agent/`](study-review-agent/)（[需求文档 SPEC](study-review-agent/SPEC.md)）

**它真的在跑**：每周一北京时间 10:00，GitHub Actions 自动启动 → 采集仓库真实数据（git 历史 / stage 扫描 / 踩坑清单 / 上周报告）→ 调云端 LLM 生成报告 → 自动 commit 回仓库。→ [查看历次报告](study-review-agent/reports/)

Harness 元件（全部亲手实现）：

| 能力 | 实现 |
|---|---|
| 数据采集 | tool registry 管理 5 个工具，错误作为数据返回（`{"error", "retry_hint"}`）不 raise |
| 模型后端 | 本地 Ollama（$0）与云端 OpenAI 兼容 API 双后端；`auto` 模式 3s 探测 + fallback |
| Retry recovery | 报告缺标题时，把缺失项反馈给模型重试一次；重试计入 stats |
| Eval harness | 4 用例：结构完整性 / 诚实性（空数据必须说"无"）/ 内容正确性 / 故意挂掉的 demo → 通过率 3/4（demo 挂才证明 eval 有效）|
| Observability | 每次调用记录 latency + token，追加写入 `run_log.jsonl`（可查每次运行的耗时与用量）|
| 成本控制 | 按 token 记账 + 可配单价自动算成本；本地 $0、云端约 $0.008/次 |
| 自动化 | GitHub Actions 定时（cron）+ 手动触发，报告自动 commit（完整 CI/CD 闭环）|

**代码分层**：通用 harness 已抽成 [`agent_kit.py`](agent_kit.py)（8 个可复用零件：后端解析 / 计时 / LLM 记账 / 成本核算 / 遥测日志 / 工具注册 / 结构校验），`review_agent.py` 只留学习复盘专属逻辑（441 → 318 行）。

**运行实测**（数据来自 [`run_log.jsonl`](study-review-agent/reports/run_log.jsonl)）：累计 **39 次运行记录**（19 次 eval + 20 次报告）；本地后端 $0，云端后端 **$0.001~$0.027/次**（12 次计费运行合计 $0.134、中位数 $0.009）。单次成本波动 **27 倍**，来源是**推理模型的思考长度不稳定**（output token 662~6195），不是代码问题 —— **成本要按区间给，别给平均数**。

## 🔌 扩展：把周报接成 MCP server

[`study-review-agent/mcp_reports_server.py`](study-review-agent/mcp_reports_server.py) 把 `reports/` **只读**暴露成 3 个 MCP 工具 —— 任何 MCP 客户端挂载后都能直接问"我最近两周的复盘说了什么"。

| 工具 | 作用 | 设计要点 |
|---|---|---|
| `list_reports()` | 列出所有周报（周次/文件名/大小/修改日期） | 只给目录不给正文，让模型先知道"有哪些" |
| `read_report(week)` | 读某一周正文 | 周次**归一化**（`W39` / `2026-w39` / `2026-W39-review.md` 都认）；找不到时 `retry_hint` 里**动态**列出可选周次 |
| `search_reports(keyword, limit)` | 跨周报全文搜索，返回周次 + 行号 | 结果封顶但 `total` 仍是真实命中数（"封顶但不说谎"），避免 token 爆炸 |

**四个工程决策**：

- **只读** —— 无写文件、无 `subprocess`、无 `eval`。这是给外部 agent 调的 server，风险面压到最小
- **路径不硬编码** —— `Path(__file__).resolve().parent / "reports"`。host 可能在任意 cwd 启动它，写死相对路径必然找不到
- **`.local.md` 天然隔离** —— glob 模式 `????-W??-review.md` 不会匹配本地草稿，所以本地测试报告既不进列表，也不会被 agent 当成"上周报告"读进上下文
- **无路径穿越** —— 周次被正则锁死成 `YYYY-Www` 格式，拼不出 `../`

**验收**：[`test_mcp_reports.py`](study-review-agent/test_mcp_reports.py) 用 **stdio 端到端**（真起子进程、走真协议）跑 13 条断言。

> ⚠️ 这里踩过一个值得记的坑：最初用 in-process `Client(mcp)` 测，**13 条断言全绿**，但作为真 server 根本起不来 —— 漏了 `if __name__ == "__main__": mcp.run()`，客户端一连就 `Connection closed`。**in-process 测试测的是"零件"，用户用的是"整机"**；改成 stdio 之后它当场抓到了这个 bug。同类教训还有一条：docstring 里 `Args:` 与摘要之间少一个空行，**参数说明会静默变成 `null`**（不报错、不崩），已把"参数说明不为空"写成断言防复犯。

**已实测挂载**：WorkBuddy（MCP 客户端）+ `fastmcp call`（CLI 直调）。

> 📝 挂载到 Codex 时遇到过连不上的问题，完整的排障记录（读宿主 sqlite 日志 → 在边界插桩 → 换客户端交叉验证）见 [`notes/mcp-server-debugging.md`](notes/mcp-server-debugging.md)。

## 🧩 服务化：HTTP 接口层 + 容器化

CLI 只能人手动跑，MCP 只能给 MCP 客户端用。为了让**任何**程序都能触发和读取复盘，加了一层 HTTP 服务（[`api_server.py`](study-review-agent/api_server.py)），并把整套东西容器化 —— 四天施工记录与实测数字见 [`HTTP-PLAN.md`](study-review-agent/HTTP-PLAN.md)。

**同一个核心、多个适配器**：CLI / MCP / HTTP 共用一套业务逻辑，接口层自己**一条业务规则都没有**。分层是显式的：

| 层 | 文件 | 职责 |
|---|---|---|
| 接口层 | `api_server.py` / `mcp_reports_server.py` / `main()` | 把外部请求翻译成一次函数调用，再把结果翻译回外部语义（状态码 / JSON / 退出码） |
| 共享数据层 | `reports_store.py` | 报告在哪、叫什么名、怎么读 —— 三个上层共用（原本 4 处重复硬编码收敛为 1 处） |
| 业务层 | `review_agent.run_once()` | 采集 -> 生成 -> 落盘 |
| 核心层 | `agent_kit.py` | 后端解析 / 计时 / 记账 / 工具注册 |

判断一个文件属于哪层：**看它 import 了什么**。`api_server.py` 只 import 了 `reports_store` 和 `run_once`，自己没有业务规则 —— 所以它是接口层。

| 关键设计 | 为什么这么做 |
|---|---|
| `POST /report` 返回 **202 + task_id**，用 `GET /tasks/{id}` 轮询 | 一次复盘要跑 30 秒。同步接口会撞客户端和网关的超时，请求一断钱还白花。「登记 -> 后台跑 -> 轮询」之后**响应时间与任务耗时解耦** |
| 后台函数写 `def` 而不是 `async def` | `run_once` 里全是阻塞调用（同步 HTTP 客户端 + `git` 子进程），必须交给线程池；写成 `async` 会堵死整个事件循环 |
| 后台异常**捕获成数据**写回任务表 | 后台线程抛的异常不进任何响应体 —— 不捕获的话客户端只会永远看到 `running`（静默故障，和 Stage 3 的「错误是数据」是同一条原则） |
| `GET /reports/{week}` 区分 400 / 404 | 400 = 参数格式不合法（客户端该改）；404 = 格式对但服务器没有（资源不存在）。周次还做**归一化**：`2026-W41` / `W41` 都认 |

**实测数字**（全部真跑，不是估算）：`POST /report` 响应 **~20 秒 -> 23 ms**；构建上下文 **206 MB -> 53 kB**（`.dockerignore` 排掉 205 MB 的上游参考仓库）；镜像 **523 MB**；`docker compose up` 后 `/health` `/reports` 全通，容器 -> 宿主 Ollama 端到端跑出真实周报并落盘。

**容器化踩到的两个「只有真跑才暴露」的 bug**（当时静态检查全绿）：

1. `python:3.11-slim` 里**没有 `git`**，而 `git_log` 工具要 `subprocess` 跑 `git log` —— 静态检查在结构上看不出「缺一个系统二进制」
2. 本机代理（fake-ip 模式）把 `deb.debian.org` 解析成假地址：apt 走 http 得到 **502**、换 https 得到 **SSL EOF**，而 pip 走 443 却是通的 —— 症状自相矛盾，**代理会让「网络问题」伪装成「镜像问题」**

**已知缺陷（面试会问，自己先想清楚）**：`TASKS` 只增不减（内存泄漏）；任务表在内存里，进程重启就丢（要可靠得 Celery + Redis）；后台任务**没有并发上限**（10 个请求就真跑 10 次 LLM，成本失控）；**没有鉴权**（任何人都能烧钱）。

## 🌐 在线站点：周报静态网站

**https://zkr05.github.io/learn-ai-agent/**

每周定时任务生成报告 → bot 提交 → 自动触发站点重建 → 网站多出一期，**全流程零人工**。

| 关注点 | 实现 |
|---|---|
| 构建 | `build_reports_site.py` 是**装配式**构建：读 `site/index.html`（外壳）+ `reports/*.md`（正文）→ 产出 `_site/`。**它一行 HTML 都不生成** —— 渲染交给浏览器里的 docsify（零构建依赖、单一数据源） |
| 部署 | 独立的 `pages.yml`：build / deploy 两个 job（`needs` 依赖，构建失败就不发布）、最小权限（`contents: read` + `pages: write` + `id-token: write`）、`concurrency` 防止两个部署同时打架 |
| 触发 | 改 `reports/` 或模板时自动构建。**注意：bot 推送不会触发其他 workflow**（GitHub 的 `GITHUB_TOKEN` 防递归规则），所以周报 workflow 末尾主动 `gh workflow run` 一次 |
| 一个坑 | `.nojekyll` —— 不加的话 `_sidebar.md` 会被 Jekyll 吃掉（Jekyll 把 `_` 开头的文件当保留命名，一律不发布） |

## 技能清单

### Stage 0 — Python 基础 ✅
变量/函数/类、async/await、错误处理、文件+JSON、requests API、YAML 配置。产出：GitHub API 调用、带 token 的 API 认证。

### Stage 1 — LLM 基础 ✅
- Python 调用 LLM API（Ollama 本机 + OpenAI 兼容协议，全程 $0）
- 亲手验证 token / context window / temperature；跨模型对比（8B vs 0.5B）
- 成本与延迟估算：本机 vs 云端 trade-off
- 排坑：推理模型 max_tokens / reasoning 字段（思考会吃掉 token，content 为空）
- exponential backoff retry 包装器

### Stage 2 — Prompt 设计 ✅
- System prompt / Few-shot（0-shot vs 3-shot 对比）/ CoT / Iterative Refinement
- 核心经验：prompt 颗粒度匹配模型能力；"只回 JSON"要给 schema + 明确禁止项

### Stage 3 — Tool Use & 第一个 Agent ✅
- **从零手写 ReAct 循环**（不用框架）：function calling → loop → 收尾
- 踩过并总结 3 个经典坑：assistant 消息必须接回（否则死循环）/ tool 消息带 tool_call_id / max_iter 安全网
- 错误是数据：工具返回 `{"error":..., "retry_hint":...}` 让模型自己恢复，而不是 raise
- 出口考核：不依赖参考代码独立写出完整 agent（`stage3-exam.py`）

### Stage 4 — Agent 框架 ✅
- workflow vs agent 的判断标准；multi-agent 4 信号（都不满足就别硬上，3-10x token）
- 5 个 pattern：Routing / Sequential / Parallel / Supervisor-Worker / Debate
- LangGraph / CrewAI / Smolagents / Pydantic AI 对比
- 工具输入归一化（同一坑踩 3 次后总结：中英文别名 + .lower()）

### Stage 5 — CLI Agent 生态 ✅
- 用 FastMCP 写 MCP server（stdio 协议、@mcp.tool、错误重试提示），出口考核设计了 study-review skill
- 分清 MCP（能力）/ Skill（行为）/ Plugin（打包）/ Subagent（独立 worker）
- AGENTS.md 五原则：可读 / 短 / 单一源 / 可验证 / 透明

### Stage 6 — Memory & RAG ✅
- 完整 RAG 流水线：chunk → embed（bge-m3）→ store → retrieve（余弦相似度）→ generate
- embedding 大小写敏感坑（ReAct≠React）→ 查询规范化
- Memory 三 Pattern：全塞 / 摘要+近 N 轮 / 向量检索；生产混用 2+3
- 出口考核：从零写出 RAG + 设计跨 session 复盘 agent 的 Memory 方案

### Stage 7 — 生产化 ✅
- Harness 8 元件逐个落地：loop / tool registry / context manager / safety / retry / telemetry / eval / cost
- **multi-agent 辩论**：Critic 独立验收——自己检查会自我称赞
- **Eval harness**：EVAL_CASES → 跑通过率，故意留会挂的用例证明 eval 能发现错误
- **Observability**：latency / token / trace / errors（@contextmanager 自动计时）
- **Streaming** 与 **成本优化**（prompt caching 省 90% 输入成本）

## 项目亮点（面试可讲）

1. **不依赖框架手写 ReAct 循环**，并能说清 assistant 接回、tool_call_id 配对、max_iter 三个坑为什么存在
2. **eval 先行**：每个 agent 都有量化验收（通过率 + 故意挂的用例），不信"看起来能跑"
3. **独立验收意识**：用 multi-agent 辩论做 Critic，避免自我称赞
4. **9 条踩坑记录**沉淀成工程直觉（见 [LEARNING-ROUTE.md §4](LEARNING-ROUTE.md)）：推理模型吃 token、工具输入归一化、embedding 大小写敏感、模型改数字要校验……
   - 另有 [`notes/mcp-server-debugging.md`](notes/mcp-server-debugging.md)：把踩过的坑**按「错误的性质」分类**（shell 转义 / 解析器格式要求 / 依赖会变的数据 / 平台隐式规则 / 测试盲区），并记录了**用变异测试衡量测试强度**的方法 —— 以及它第一次跑就暴露出自己测试盲区的过程
5. **成本敏感**：全路线用本机 Ollama $0 跑通，需要云端时先算 token 账
6. **学习过程全部 git 留痕**，每个练习带自我验证（assert）和观察记录
7. **会做重构**：毕业设计跑通后把通用 harness 抽成独立模块 `agent_kit.py`（8 个可复用零件）。关键动作是**参数化**——日志路径、报告标题、工具表都改成参数注入，否则通用模块会把业务信息硬编码进去；全程坚持「行为不变」原则，本地 / eval / 云端 / CI 四项验证全绿才提交（业务层代码减少 28%）
8. **把能力接成 MCP server**：周报通过标准 MCP 协议暴露给任意客户端（已实测挂载 WorkBuddy）；并用 stdio 端到端测试抓出「in-process 测试全绿但真 server 起不来」的**测试盲区** —— 测试要测「用户怎么用它」，不是「零件对不对」
9. **会交付，不只是会写**：把周报接成 MCP server（跨客户端可用）、构建成静态站点自动部署（独立 workflow、最小权限、并发控制、`.nojekyll` 这类平台细节），形成「采集 → 生成 → 进版本库 → 自动发布」的完整闭环
10. **会做服务化和分层重构**：抽出 `run_once()` 与共享模块 `reports_store.py`（4 处重复硬编码收敛为 1 处），并显式分出接口层 / 共享数据层 / 业务层 / 核心层 —— 接口层不含任何业务规则，所以后来加 HTTP 入口时业务层一行未改。抽 `run_once()` 时用「`--eval` 通过率 + 本地后端 + MCP 端到端 + CI」四项验证确认行为不变才提交
11. **会容器化，而且只为真跑过的结果背书**：Dockerfile 分层（依赖在前、代码在后）吃到构建缓存；`.dockerignore` 把构建上下文从 206 MB 压到 53 kB；compose 管端口、环境变量和报告目录的持久化挂载。上面两个 bug 都是「静态检查全绿但真跑就炸」，改完重跑才提交 —— 这也反过来说明：**「应该能跑」不是结论，是猜测**

## 仓库结构

```text
learn-ai-agent/
├── README.md                    # 本文件（作品集）
├── agent_kit.py                 # 可复用 harness：后端解析/计时/LLM记账/成本/遥测/工具注册/结构校验
├── LEARNING-ROUTE.md            # Stage 0-7 复习地图 + 代码模板 + 踩坑记录
├── Dockerfile                   # 容器镜像配方：分层缓存 / 装 git / exec 形式 CMD
├── docker-compose.yml           # 运行编排：端口映射 / 环境变量 / 报告目录持久化挂载
├── .dockerignore                # 构建上下文 206MB -> 53kB
├── notes/                       # 工程笔记（MCP 跨宿主排障记录等）
├── study-review-agent/          # 🏆 毕业设计：自动复盘 agent + HTTP 服务层 + MCP server + 周报站点
├── stage1-llm-basics/           # API 调用 / token / retry
├── stage2-prompt-eng/           # system / few-shot / CoT / refine
├── stage3-tool-use/             # 从零手写 ReAct agent
├── stage4-frameworks/           # 框架对比 / multi-agent pattern
├── stage5-claude-code/          # MCP server / AGENTS.md / Skill
├── stage6-memory-rag/           # RAG 流水线 / Memory 方案
├── stage7-production/           # eval / observability / streaming / cost
└── awesome-agentic-ai-zh/       # 课程参考仓库（上游克隆）
```

## 环境

- Python 3.11+ · openai SDK · FastMCP
- 本机模型：Ollama（qwen2.5:7b + bge-m3 embedding）
- 云端：任意 OpenAI 兼容 API（复盘 agent 可配置切换）
- 容器：Docker Desktop 4.94 / Engine 29.8.2（WSL2 后端），`docker compose up -d` 即可起服务
