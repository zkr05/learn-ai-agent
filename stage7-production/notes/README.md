# Stage 7 — 多 Agent 与生产化（Harness Engineering）

内容整理自 awesome-agentic-ai-zh 的 stages/07-multi-agent-production.zh-Hans.md。
**本阶段 = 把 agent 从 prototype 推到"能稳定给人用"**。

## 三层工程分工（贯穿全程的框架）

| 层级 | 核心问题 | 对应 stage |
|---|---|---|
| Prompt Engineering | 这次怎么问？ | Stage 2 ✅ |
| Context Engineering | 这次给哪些信息？ | Stage 6 ✅ |
| **Harness Engineering** | 整个流程怎么跑起来？ | **本 stage** |

**怎么分辨自己在做哪层**：
- 改的是字符串本身？→ Prompt
- 改的是塞进窗口的信息？→ Context
- 改的是调用模型的外围程序？→ **Harness**

## Harness 的 8 个核心元件

1. **Agent loop**（循环）
2. **Tool registry**（工具注册表 + 权限）
3. **Context manager**（上下文管理）
4. **Safety layer**（安全层）
5. **Retry / recovery**（重试恢复）
6. **Telemetry / Observability**（可观测性）
7. **Eval harness**（评估）
8. **Cost / Latency optimization**（成本/延迟）

## 核心 insight：反馈循环

**agent 变强靠的是"把反馈送回循环"，不是把 prompt 写得更完美。**

反馈的 4 个时机：
1. 工具返回值（错误信息写清楚）
2. 执行中插话（steering）
3. 单轮结束的独立验收（evaluator 而不是自己打分）
4. 外层 loop（对着目标反复重跑）

> ⚠️ 第 3 点最重要：让 agent 自己检查成品，它几乎都"自我称赞"——必须拆"做的 agent"和"验收的 agent"。

## 学习计划

```text
第 1 天：概念——三层分工 + 8 元件 + 反馈循环
第 2 天：练习 1 multi-agent 辩论 + 练习 2 Eval
第 3 天：练习 3 Observability + Cost
第 4 天：Stage 7 出口考核
```
