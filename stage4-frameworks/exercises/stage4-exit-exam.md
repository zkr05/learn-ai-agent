# Stage 4 出口考核（框架判断 + 动手）

规则：不抄练习答案，从零写/答。可以翻笔记。
环境：已装 langgraph / crewai / smolagents / pydantic-ai，模型 qwen2.5:7b。

---

## 任务 1：框架定位（25 分，写进文件顶部注释）

用一句话说出 4 个框架各自的定位（你用过/见过的）：
- LangGraph：针对简单的任务，复杂度比较低，可以将整个流程用图表示出来。
- CrewAI：比较复杂的任务，对模型的要求比较高，难以排查错误。
- Smolagents：是模型通过写代码来调用工具，对模型的要求较高，但是步骤较少
- Pydantic AI：类型安全校验，可以让输出的文本符合要求，对错误会打会重试，适合要求规定输出的客户，小模型不好跑。

任务 1 修正：
- LangGraph：图式工作流框架——擅长复杂流程、状态管理、checkpointing、human-in-the-loop
  （不是"简单任务"；它恰恰是处理复杂的，控制流全在图上看得见）
- CrewAI：角色式多 agent 框架——上手快、适合快速雏形（researcher→writer→critic），
  但把复杂度藏起来了（黑盒、难 debug）；"对模型要求高"不是它的定位
- Smolagents：CodeAct——模型写代码当 action，灵活但对模型能力要求高
- Pydantic AI：类型安全结构化输出——输出必须符合 schema，校验失败自动重试

## 任务 2：替任务选框架（25 分，注释回答）

给下面 3 个任务各选一个方案（LangGraph / CrewAI / Smolagents / Pydantic AI / 直接手写），并说一句为什么：
1. "一个客服分流系统：销售问题转 A、技术问题转 B"
crewAI，可以用多agent分流问题。
2. "一个要严格返回 {答案, 置信度, 来源} 的问答 API"
用Pydantic AI 因为要求严格回答 可以用 AnswerwithConfidence
3. "模型要自己写代码算一个复杂公式"
用Smolagents 因为要自己写代码算，可以把任务交给ai。

任务 2 修正（客服分流那道）：
客服分流（销售→A、技术→B）：标准做法是 Routing/Handoff pattern——
LangGraph 的条件边 或 OpenAI Agents SDK 的 handoff（CrewAI 也能做，但不是它的招牌）
## 任务 3：动手（30 分）——从零做一个 agent

用 **LangGraph 或 CrewAI** 写一个**你自己设计**的小 agent（不许复制练习 1/2/3 的工具和任务）：
- 自己发明一个工具（比如查书价、算折扣、查城市时差……）+ schema
- 一个能触发它的任务
- 跑通并给出正确结果

写在stage4-exam里面了
## 任务 4：何时手写（20 分，注释回答）

"什么时候该丢掉 framework、自己写 agent？"列出至少 2 个理由（用你的真实经验）。
1.当面对比较简单的问题
2.且需要排错的时候
---

**提交**：`git commit -m "Stage4出口考核"`
**评分**：任务 1/2/4 答到点、任务 3 跑通且自创工具 → 通关进 Stage 5。
