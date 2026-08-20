# 第 1 天：workflow vs agent、single vs multi、什么时候才要 multi-agent

> 对应 awesome-agentic-ai-zh Stage 4 开头概念。纯概念，不需要模型。

## 1. 两个正交维度

**维度 A：workflow vs agent**（谁决定下一步）
- **Workflow** = 你写死的 code path（if A 走这条路、if B 走那条路）
- **Agent** = LLM 动态决定下一步（Stage 3 的 ReAct loop）

**维度 B：single vs multi**（几个 LLM）

四个象限：

| | Workflow（代码决定）| Agent（LLM 决定）|
|---|---|---|
| Single LLM | 线性 pipeline | 一个 LLM + ReAct loop ← **Stage 3 你写的** |
| Multi LLM | 预设 routing | 多 agent 协作 ← **Stage 4 主题** |

## 2. 什么时候才真的需要 multi-agent？（4 个信号）

Multi-agent **不是默认、是 last resort**。Anthropic 和 Cognition 都写过：**90% 用例不该用 multi-agent**。

硬上会付 3 个代价：**3-10x token、debug 痛苦、context fragmentation**（上下文被切散，各 agent 看不到全貌）。

需要 multi-agent 的 4 个信号：
1. **任务天然分解**：大任务有清楚子步骤 → Sequential / Planner-Executor
2. **Token explosion**：single agent 塞不下所有工具/上下文 → Supervisor-Worker
3. **角色冲突**：同一个 LLM 既当 writer 又当 critic 会 self-justify → Debate
4. **并行加速**：多个独立子任务同时跑 → Parallel

**4 个信号都不在？** → single agent + 好 prompt + tool use 就够。

## 3. Multi-agent 经典 pattern（按复杂度）

1. **Routing/Handoff**（⭐）：agent 之间 1:1 交接（客服分流）
2. **Sequential**（⭐⭐）：Planner 规划 + Executor 执行
3. **Parallel**（⭐⭐⭐）：N 个 agent 并行跑、结果汇总
4. **Supervisor-Worker**（⭐⭐⭐）：1 主 + N worker，主分配整合
5. **Debate**（⭐⭐⭐⭐）：多 agent 互相 critique（研究、判断任务）

## 4. Framework 帮你做什么

multi-agent 的协调、交接、状态管理、样板代码——让你不用从零写整套协作流程。

## 今日作业

1. 用自己的话回答：
   - workflow 和 agent 的本质区别？
   - 为什么 90% 的任务不该用 multi-agent？（3 个代价）
   - 4 个信号里，哪个对应"让两个 agent 互相挑错"？
2. （可选）看 Anthropic "Building Effective Agents" 文章前 10 分钟
