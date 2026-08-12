# Stage 3 — 工具使用与第一个 Agent（Tool Use & Hello Agent）

内容整理自 awesome-agentic-ai-zh 的 stages/03-tool-use-and-hello-agent.zh-Hans.md。
⭐ 全学习路线最关键的一站：**建过一个 agent 才算真懂 agent**。

## 学习目标

- 讲得出为什么 LLM 需要 tools（文字以外的事它都做不了）
- 定义一个 tool schema，并让 LLM 调用它
- 从零（不靠 framework）写出单步 ReAct agent
- 写出多步 ReAct agent，并让它自己判断何时该停
- 分得出哪种问题该用 tool use、哪种纯 prompt 就够

## 学习计划（2-3 周，约 10-20 小时）

```text
第 1 天：概念（AI/LLM/Agent 区别 + 3 部件）+ 环境（qwen2.5:3b）
第 2 天：练习 1 — Function Calling（一个工具、一次调用）
第 3 天：练习 2 — 多工具选择
第 4 天：练习 3 — 从零实现 ReAct（不用 framework）
第 5 天：练习 4 — 多步骤推理任务
第 6 天：练习 5 — 错误处理
第 7 天：练习 6 — Function schema 设计
第 8 天：Stage 3 出口考核（从零写单步 ReAct）
```

## 环境

- 模型：qwen2.5:3b（1.9GB，tool-use 支持稳定）——gemma4:e4b 工具调用不够用
- 坑：推理模型 max_tokens 要留足；工具调用输出在 tool_calls 字段而非 content

## 进 Stage 4 前的自我检查

- [ ] 讲得出 agent 的 3 个最小部件
- [ ] 定义一个 tool schema 并让 LLM 调用
- [ ] 从零写出单步 ReAct agent
- [ ] 写出多步 ReAct agent 并知道何时该停
