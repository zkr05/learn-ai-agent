# 练习：RAG 基础流水线（从零搭，不装向量库）
# 需要：pip install openai；前置：ollama pull bge-m3 qwen2.5:7b && ollama serve
#
# 两条流水线：
#   预处理（一次）：chunk → embed → store
#   检索生成（每次）：retrieve → generate
#
# 作业：跑通后在顶部注释回答：
# 观察1（检索到了哪几个 chunk）：MCP问题检索到"MCP标准协议"chunk(精确命中) + "AGENTS.md"chunk(语义相关，无共同关键词也被捞到)——语义搜索 vs 关键词搜索的区别
# 观察2（如果知识库里没有相关 chunk，模型会怎么答）：知识库里没有相关chunk时，模型按prompt要求说"不知道"（不编造）
# 观察3（把 top_k 改成 1 或 4，回答质量怎么变）：top_k=1和4结果都准确简洁(知识库小、区分度高)；但把"ReAct"改成"React"后检索失配——embedding对大小写/拼写敏感，真实系统要查询规范化+混合搜索

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "bge-m3"      # 中文 embedding 模型
LLM_MODEL = "qwen2.5:7b"


# === 1. 知识库（chunk 已经分好——每段是一个可搜索的片段） ===

KB = [
    "ReAct 是一种 agent 模式：思考(Thought)→行动(Action)→观察(Observation)的循环。",
    "MCP（Model Context Protocol）是让 LLM 使用外部工具的标准协议，写一次 server 任何 host 都能用。",
    "LangGraph 是图式工作流框架，擅长复杂流程、状态管理和 checkpointing。",
    "CrewAI 是角色式多 agent 框架，适合快速搭建 researcher→writer→critic 流水线。",
    "Skill 是特定情境的行为包，description 匹配时自动加载，教 agent 遇到什么情况走什么流程。",
    "AGENTS.md 是给 agent 看的项目说明书，每个会话都会加载，写的是项目约定和可验证规则。",
    "Context window 是模型一次能看到的 token 上限，Claude 1M / GPT 1.05M / Gemini 2M。",
]


# === 2. Embed：把文本转成向量 ===

def embed(text: str) -> list[float]:
    r = client.embeddings.create(model=EMBED_MODEL, input=text)
    return r.data[0].embedding


# === 3. Store：向量 + 原文一起存（学习用 in-memory） ===

store = [(chunk, embed(chunk)) for chunk in KB]
print(f"已索引 {len(store)} 个 chunk，每个向量维度 {len(store[0][1])}")


# === 4. Retrieve：问题向量化 → 余弦相似度 → top-k ===

def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


def retrieve(question: str, top_k: int = 2) -> list[str]:
    q_vec = embed(question)
    scored = sorted(store, key=lambda item: cosine(q_vec, item[1]), reverse=True)
    return [chunk for chunk, _ in scored[:top_k]]


# === 5. Generate：检索结果拼进 prompt → LLM 回答 ===

def ask_with_rag(question: str, top_k: int = 2) -> str:
    hits = retrieve(question, top_k)
    context = "\n".join(f"- {h}" for h in hits)
    prompt = f"""根据下面的资料回答问题。如果资料里没有，就说不知道。

资料：
{context}

问题：{question}
"""
    r = client.chat.completions.create(
        model=LLM_MODEL, max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


if __name__ == "__main__":
    q = "什么是 ReAct？"
    print(f"\n❓ 问题：{q}")
    print(f"检索到的 chunks：{retrieve(q, 2)}")
    print("-" * 50)
    print(ask_with_rag(q))
    print("\n✅ RAG 流水线跑通 — chunk→embed→store→retrieve→generate、$0/run")
