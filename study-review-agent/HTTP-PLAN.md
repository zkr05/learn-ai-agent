# HTTP 服务层 · 四天施工图

> 目标：把 study-review agent 从「命令行脚本」变成「任何程序都能调用的服务」。
> 每一步都有实测数字 —— 这是简历里「后端服务化」那一块的原始记录。

## 为什么做（不是为做而做）

CLI 只能人手动跑，MCP 只能给 MCP 客户端用。要让**任何**程序（网页 / 别的服务 / 定时任务）
都能触发和读取复盘，就需要一个通用的 HTTP 接口。
顺带把项目里本来就存在的分层**显式化**（见下表）。

## 分层（Day 2 的成果）

| 层 | 文件 | 职责 |
|---|---|---|
| 接口层 | `api_server.py` / `mcp_reports_server.py` / `review_agent.py` 的 `main()` | 把外部请求翻译成一次函数调用，再把结果翻译回外部语义（状态码 / JSON / 退出码） |
| 共享数据层 | `reports_store.py` | 报告在哪、叫什么名、怎么读 —— 三个上层共用 |
| 业务层 | `review_agent.run_once()` | 采集 -> 生成 -> 落盘 |
| 核心层 | `agent_kit.py` | 后端解析 / 计时 / 记账 / 工具注册 |

判断一个文件属于哪层：**看它 import 了什么**。
`api_server.py` 只 import 了 `reports_store` 和 `run_once`，自己没有一条业务规则 —— 所以它是接口层。

## 四天

| 天 | 内容 | 验收标准 | 状态 |
|---|---|---|---|
| Day 1 | 抽 `run_once()` + FastAPI 最小服务（`/health`、`/report`） | `--eval` 仍是 3/4（与抽取前一致）；`/report` 跑通 | ✅ |
| Day 2 | 抽 `reports_store.py`（4 处重复 -> 1 处）+ `GET /reports`、`GET /reports/{week}` | 硬编码收敛为 1 处；`W41` 归一化生效；400 与 404 分别触发 | ✅ |
| Day 3 | `POST /report` 改后台任务（`BackgroundTasks` + 202 + `GET /tasks/{id}`） | 响应从 ~20 秒降到毫秒级；轮询能看到 `running` -> `done`；失败能被客户端读到 | ✅ |
| Day 4 | Dockerfile + compose | `docker run` 起来后 `/health`、`/reports` 可用 | 未开始 |

## 关键数字（简历可用）

- `POST /report` 响应：**~20 秒 -> 23 ms**（202 + task_id，实测）
- 一次复盘任务实际要跑 **30 秒**，但**响应时间已经和它解耦**
- 周次归一化：`2026-W41` 和 `W41` 两种写法都命中同一份报告

## 已知缺陷（面试会问，自己先想清楚）

1. `TASKS` 只增不减 -> 内存泄漏。生产要么加时间戳定期清理，要么用 `cachetools.TTLCache`。
2. 任务表在内存里 -> **进程一重启，任务记录和任务本身都丢**。要可靠就得上 Celery/RQ + Redis。
3. `BackgroundTasks` 没有并发上限 -> 10 个请求同时来就真跑 10 次 LLM 调用，成本失控。
4. **没有鉴权** —— 任何人都能 `POST /report` 烧你的钱。
