# Stage 6 — 记忆 / RAG（Context Engineering）

内容整理自 awesome-agentic-ai-zh 的 stages/06-memory-rag.zh-Hans.md。
**核心**：agent 如何管理 context——RAG 解决"查资料"，Memory 解决"记住事"。

## 学习计划

```text
第 1 天：概念——两种 context 能力 + 名词切开（RAG/Embedding/VectorStore/Memory）
第 2 天：RAG 基础流水线（chunking → embedding → 向量库 → 检索）
第 3 天：Memory 模式
第 4 天：Stage 6 出口考核
```

## 名词速记（先背这张表）

| 名词 | 白话 |
|---|---|
| Retrieval | 找资料这个动作 |
| RAG | retrieve + generate 完整流程 |
| Embedding | 文本转向量（相似度搜索用）|
| Vector store | 存/搜向量的地方 |
| Chunking | 文档切成可搜索的片段 |
| Memory | agent 跨对话记住东西 |

## 关键认知

- RAG ≠ Vector DB（向量库只是 RAG 的一环）
- 什么时候用 RAG vs 长上下文 vs 微调（课程有对照）
- Context Engineering = 每次 LLM call 决定"塞哪些信息进窗口"
