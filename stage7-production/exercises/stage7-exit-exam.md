# Stage 7 出口考核（收官）——Production Agent 综合

规则：不抄练习，从零写/答。可以翻笔记。这是整个学习路线的最后一关。

---

## 任务 1：Harness 概念（30 分，注释回答）

1. Harness 是什么？（一句话）
2. 8 个核心元件里，你在前面 stage 亲手做过哪 4 个以上？（列出来+哪个练习）
3. 反馈循环里最重要的一条是什么？为什么？（提示：独立验收）

1.Harness 是调用模型的外围程序
2.agent loop 是 、 tool registry是tool和mcp那一块、safety layer是权限管理那一块、retry recovery是写重试那里
3.反馈循环最重要的是要有多个agent，因为单个agent往往会对自己的成品有更高的评价。

## 任务 2：动手（30 分）——给 agent 写 eval

写 `stage7_exam.py`：给你 Stage 6 的 RAG agent 或 debate agent 写一个 eval：
- 定义至少 5 个测试用例（不同维度：正确性/诚实性）
- 跑出通过率（字符串匹配或 LLM 裁判都行）
- 故意留 1 个"会挂"的用例，展示 eval 能发现错误

## 任务 3：综合设计（40 分，注释回答）

"把 study-review skill 升级成 production agent（每周自动跑）"

写出设计方案：
- 加哪些 Harness 元件？为什么？（至少 3 个）
- 怎么 eval？（测什么、怎么算过）
- 怎么 observability？（看什么指标）
- 成本怎么控制？（模型选择/缓存）

1.要加Tool registry，因为需要用到调用我的一些学习资料，Eval harness，需要对内容进行评估，确保符合要求和正确，Observability，需要看agent是否有出现问题，方便排查
2.测试关于这个agent对我的学习内容的掌握程度，是否能够精准的说出我的一些典型错误
3.看latency，token看看成本，trace看看多agent的每一步骤，errors看异常改进
4.选择适合我自己的云端模型，选择缓存命中率高的

---

**提交**：`git commit -m "Stage7出口考核"`
**评分**：任务 1 概念清楚、任务 2 eval 跑通且能发现错误、任务 3 方案完整 → **整个学习路线通关！**
