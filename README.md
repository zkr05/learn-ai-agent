# learn-ai-agent · AI Agent 学习仓库 & 作品集

从零到生产，跟完 **Track B — Agent Builder** 全路线（[WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)，Stage 0-7，2026-08 起）。

每个 stage 都是"概念 → 亲手写 → 自建 eval 验证 → 出口考核"的闭环，所有练习可运行、带观察记录。毕业设计是一个**真在 GitHub Actions 上每周自动跑的 production agent**（见下方亮点项目）。

## 🏆 毕业设计：study-review agent（每周自动学习复盘，开发中）

把 Stage 5 的 study-review skill 按 Stage 7 生产化设计升级成完整 agent：[`study-review-agent/`](study-review-agent/)（[需求文档 SPEC](study-review-agent/SPEC.md)）

设计中的 Harness 元件：

| 能力 | 设计 |
|---|---|
| 数据采集 | tool registry 管理 git log / 练习扫描 / 踩坑提取 / 上周报告记忆，错误作为数据返回（不 raise） |
| 模型后端 | 本地 Ollama（$0）与云端 OpenAI 兼容 API 双后端，`auto` 模式自动探测 + fallback |
| Eval harness | 结构完整性 / 诚实性（数据为空时必须说"无"）/ 内容正确性用例，含故意挂掉的 demo 用例 |
| Observability | 每次 LLM 调用记录 latency + token 用量，追加写入 `run_log.jsonl` |
| 成本控制 | 按 token 记账，可配置单价自动算成本；本地后端 $0 |
| 自动化 | GitHub Actions 每周一自动运行，报告自动 commit 回仓库（CI/CD 闭环） |

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
5. **成本敏感**：全路线用本机 Ollama $0 跑通，需要云端时先算 token 账
6. **学习过程全部 git 留痕**，每个练习带自我验证（assert）和观察记录

## 仓库结构

```text
learn-ai-agent/
├── README.md                    # 本文件（作品集）
├── LEARNING-ROUTE.md            # Stage 0-7 复习地图 + 代码模板 + 踩坑记录
├── study-review-agent/          # 🏆 毕业设计：每周自动复盘 agent（GitHub Actions）
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
