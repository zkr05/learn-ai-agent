# Stage 6 出口考核（RAG + Memory）

规则：不抄练习，从零写/答。可以翻笔记。
环境：bge-m3 + qwen2.5:7b + Ollama。

---

## 任务 1：概念（30 分，注释回答）

1. 说出 RAG 流水线的 5 步（按顺序）
2. Retrieval 和 Memory 的区别？
3. 一个跨 session 的知识库 agent 用哪个 Pattern？为什么？

1.chunking -> embeding-> vector store -> retrieval -> LLM
2.Retrieval 是从向量库里面搜索相似度高的内容，memory是对过去内容的总结记忆，可以让下次运行记住用户习惯等等
3.跨session 应该用 vector store 和 retrieval，因为需要跨知识库需要用到向量存储等技术，retrieval可以检索内容
## 任务 2：动手（40 分）——从零写一个 RAG

写 `stage6_exam.py`：
- **自己设计知识库**（至少 5 段，主题自选——比如你的学习内容、菜谱、城市介绍）
- 完整流水线：chunk（分好段）→ embed → store → retrieve → generate
- 问 1 个问题，能从你的知识库正确回答
- 不许复制 practice_1_rag.py 的代码（可以看思路）

写在 stage6-exam.py里面了
## 任务 3：设计（30 分，注释回答）

给这个场景设计 Memory 方案：
"一个每周帮你做学习复盘的 agent（跨 session），你希望它记得你学到哪、哪些容易错、你的偏好。"

要求写出：
- 用哪种/哪几种 Pattern（混用怎么说）
- 记什么（对应三种内容类型各举 1 个例子）
- 怎么取回（什么时候查记忆）


1. 因为要用到跨session，所以要用到 Vector store + retrieval，production 通常混用：近期对话用 Pattern 2（摘要+近 N 轮），长期记忆用 Pattern 3"——课程强调这点
2. Episodic要结合我平时复盘的要求的经验记住，Semantic要记忆我的用户习惯、偏好，Procedural要记忆我要求的输出格式
3. 当我要求需要总结复盘时候，需要查记忆。
---

**提交**：`git commit -m "Stage6出口考核"`
**评分**：任务 1 全对、任务 2 跑通且自建知识库、任务 3 方案合理 → 通关进 Stage 7。
