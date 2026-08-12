# 第 1 天：AI / LLM / Agent 三者怎么分 + Agent 的 3 个最小部件

> 对应 awesome-agentic-ai-zh Stage 3 开场框景。纯概念，不需要模型。

## 1. 一张阶层图（先建立认知）

AI 是整棵大树（学科）；ML/DL/LLM 是树上的分类；**Agent 不在树上**——它是跨层抽象：
把 LLM 当作一个零件，接上工具和循环，组成一个能独立干活的系统。

> **Agent 不是"比 LLM 更厉害的模型"。** Cursor / Claude Code / 各种 agent 内部
> 用的还是同一批 LLM（Claude / GPT / Gemini）——差别是**怎么把 LLM 包进工具调用循环里**。

## 2. 三行对照

| 词 | 是什么 | 你给它什么、它回什么 | 例子 |
|---|---|---|---|
| AI | 整个学科 | 太抽象、不能直接用 | ML / DL / LLM 都是子领域 |
| LLM | 文字→文字的单一模型 | 给 prompt → 回字 | GPT、Claude、gemma4、Qwen |
| Agent | LLM + 工具 + loop 的系统 | 给任务 → 自己多步完成 | Cursor、Claude Code |

**一句话**：LLM 是"理解并生成文字的大脑"；Agent 是"大脑 + 手 + 心跳"组成能完成多步任务的系统。

## 3. Agent 的 3 个最小必要部件（是不是 agent 的判准）

| 部件 | 角色 | 在哪学 |
|---|---|---|
| 🧠 LLM（brain）| 推理 / 决策 / 自然语言 | Stage 1 已学 |
| 🔧 Tools（hands）| 对世界做事（call API、跑 code、查数据）| **本 stage** |
| 🔁 Loop（heartbeat）| 想 → 做 → 看结果 → 再想（ReAct）| **本 stage 练习 3** |

**3 个合在一起 = agent 的最低定义。** 没有 tools / loop，那只是 "LLM + 你写 retry"，不算 agent。

## 4. Agent 怎么想：4 种经典范式

| 范式 | 是什么 | 在哪学 |
|---|---|---|
| CoT | 先写推理再给答案（prompting 技巧）| Stage 2 已学 |
| ReAct | Loop 里套 CoT：Thought→Action→Observation→Thought | 本 stage 练习 3 |
| Reflection | 跑完自我批改、根据 feedback 重答 | 本 stage 反思节 |
| Planning | 大任务拆子任务、可分给多个 agent | Stage 4 |

## 5. ⚠️ 风险意识（先记住）

给 agent 工具 = 给它一个**攻击面**。LLM 分不清"你下的指令"和"不可信数据里夹带的指令"
——这就是 **prompt injection**。先有这个意识，具体防法后面 stage 学。

## 今日作业

1. 用自己的话回答（口头）：
   - LLM 和 Agent 的本质区别是什么？
   - Agent 的 3 个部件是什么？缺一个行不行？
   - 为什么"给模型配 retry"不算 agent？
2. 等 qwen2.5:3b 拉完，确认 `ollama list` 能看到它
