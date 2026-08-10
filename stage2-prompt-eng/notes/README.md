# Stage 2 — Prompt 设计（Prompt Engineering）

内容整理自 awesome-agentic-ai-zh 的 stages/02-prompt-engineering.zh-Hans.md。

## 完成本阶段后，你应该能做到

- 写出结构化 prompt（角色 + 任务 + 格式 + 示例）
- 应用 few-shot prompting，并知道什么时候有用
- 在推理任务上使用 chain-of-thought（CoT）
- 反复迭代修改 prompt 并衡量改善
- 看出什么时候 prompt 已经到极限（这时需要 tool / agent）

## 学习计划（每天约 1 小时，共 1-2 周）

```text
第 1 天：练习 1 — System Prompt（3 种人设，观察人格/格式变化）
第 2 天：练习 2 — Few-Shot（0-shot vs 3-shot 分类准确率对比）
第 3 天：练习 3 — CoT（数学题：纯 prompt vs "一步一步想" vs 推理范例）
第 4 天：练习 4 — Iterative Refinement（模糊 prompt 连改 5 版并记录）
第 5 天：Stage 2 出口考核（从零写 few-shot + CoT + refine，逐项验收）
```

## 检验机制（本阶段起启用）

每个练习完成后、进入下一天前，都要通过口头小测：

- **每日开头**：回顾上一天核心概念（2-3 题）
- **练习验收**：能解释关键代码 + 回答观察问题
- **阶段出口**：从零动手任务，按自检清单逐项验收

## 进 Stage 3 前的自我检查（出口标准）

- [ ] 写一个有 system message + user message + 3 个示例 message 的 prompt（few-shot）
- [ ] 示范 CoT 在某个推理任务上提升准确率
- [ ] 反复 refine 一个 prompt 5 次，每一版都留下记录
- [ ] 看出 prompt 不是对的工具的时候（这时要用 tool use）

## 环境

- 模型：gemma4:e4b（本机，$0）——小模型对 prompt 质量敏感，教学效果更好
- 坑：gemma4:e4b 是推理模型，max_tokens 需要 1000，200 会被思考吃光
- 云端对照（可选）：Anthropic 用 system= 参数，Ollama 用 messages 第一笔 role=system
