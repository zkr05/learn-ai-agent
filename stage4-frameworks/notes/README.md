# Stage 4 — Agent 框架（Agent Frameworks）

内容整理自 awesome-agentic-ai-zh 的 stages/04-agent-frameworks.zh-Hans.md。

## 学习目标

- 比较 5 个主流 agent framework（LangGraph、AutoGen、CrewAI、Smolagents、OpenAI Agents SDK）
- 替任务挑出对的 framework
- 用两个 framework 各做一次同样的 agent，亲身感受差异
- 看出什么时候该丢掉 framework、自己写

## 进入条件（你已满足）

- ✅ Stage 3 全部完成（从零写过 ReAct）
- ✅ async Python 基础（Stage 0 第 12 天学过 async/await）

## 学习计划

```text
第 1 天：概念——workflow vs agent、single vs multi、什么时候才需要 multi-agent
第 2 天：练习 1——同一个 agent、两个 framework（LangGraph vs 另一个）
第 3 天：练习 2——多 agent 角色分配
第 4 天：练习 3——图式 workflow
第 5 天：练习 4——CodeAct vs JSON tool
第 6 天：练习 5——类型安全 agent
第 7 天：Stage 4 出口考核
```

## 核心概念速记

- **workflow** = 你写死的 code path；**agent** = LLM 动态决定下一步
- **single-agent** = 一个 LLM + ReAct loop（Stage 3 你写的）
- **multi-agent** = 2+ LLM 各司其职，orchestrator 协调
- ⚠️ 大多数任务**不需要** multi-agent——别硬上（token 成本 3-10x、debug 难）

## 进 Stage 5 前的自我检查

- [ ] 比较 5 个 framework 的定位
- [ ] 替一个具体任务选出对的 framework
- [ ] 用两个 framework 各做一个同样的 agent
- [ ] 说出什么时候该丢掉 framework 手写
