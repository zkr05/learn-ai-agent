#写 `stage7_exam.py`：
#- **自己设计知识库**（至少 5 段，主题自选——比如你的学习内容、菜谱、城市介绍）
#- 完整流水线：chunk（分好段）→ embed → store → retrieve → generate
#- 问 1 个问题，能从你的知识库正确回答
#- 不许复制 practice_1_rag.py 的代码（可以看思路）


import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
EMBED_MODEL = "bge-m3"      # 中文 embedding 模型
LLM_MODEL = "qwen2.5:7b"


KB = [
    "可乐鸡翅菜谱：先将鸡翅煎至表皮金黄，倒入可乐淹没鸡翅，加入生抽、老抽、蚝油、盐，开盖大火时刻小心收汁。",
    "西红柿炒鸡蛋菜谱：先把一颗番茄切大块，一颗切成小丁，鸡蛋打入搅匀备用，锅热下入鸡蛋，捞出备用，下入番茄丁炒出汁水，下入大块番茄和鸡蛋，出锅下白糖。",
    "辣椒炒肉菜谱：辣椒切好直接下锅煎出虎皮，捞出过，锅中加油下入腌制好的五花肉（用生抽老抽盐料酒），最后加入辣椒一起翻炒。",
    "水瓜汤：锅中加水煮开，加入腌制好的嫩肉片，烫熟后加入切好的水瓜，盖上锅盖，出锅加入盐，味精。",
]


def embed(text: str) -> list[float]:
    r = client.embeddings.create(model=EMBED_MODEL, input=text)
    return r.data[0].embedding

store = [(chunk,embed(chunk)) for chunk in KB]
print(f"已索引 {len(store)} 个chunk,每个向量维度 {len(store[0][1])}")


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    return dot / (na * nb) if na and nb else 0.0



def retrieve(question: str, top_k: int = 2) ->list[str]:
    q_vec = embed(question)
    scored = sorted(store, key=lambda item: cosine(q_vec, item[1]), reverse=True)
    return [chunk for chunk, _ in scored[:top_k]]


def ask_with_rag(question: str, top_k: int = 2) -> str:
    hits = retrieve(question, top_k)
    context = "\n".join(f"- {h}" for h in hits)
    prompt = f"""根据下面的资料回答问题。如果资料里没有，就说不知道。
    
资料:
{context}

问题:{question}
"""

    r = client.chat.completions.create(
        model=LLM_MODEL,max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content

EVAL_CASES = [
    {"id": "kb_1", "input": "可乐鸡翅怎么做？", "expected": "鸡翅"},     # 知识库内
    {"id": "kb_2", "input": "西红柿炒鸡蛋怎么做？", "expected": "鸡蛋"}, # 知识库内
    {"id": "kb_3", "input": "辣椒炒肉怎么做？", "expected": "辣椒"},     # 知识库内
    {"id": "outside", "input": "什么是机器学习？", "expected": "不知道"},  # 知识库外→测诚实
    {"id": "fail_demo", "input": "可乐鸡翅怎么做？", "expected": "红烧肉"}, # 故意写错→展示eval能发现
]

def run_eval(cases):
    results = []
    for case in cases:
        answer = ask_with_rag(case["input"])        # ① 调 agent 回答
        passed = case["expected"] in answer          # ② 检查是否包含期望词
        results.append({"id": case["id"], "passed": passed, "answer": answer[:50]})
    pass_count = sum(1 for r in results if r["passed"])   # 数一数有几个 True
    pass_rate = pass_count / len(results)                 # 通过数 / 总数
    return results, pass_rate, pass_count


if __name__ == "__main__":
    results,pass_rate,pass_count = run_eval(EVAL_CASES)
    for r in results:
        mark = "✅" if r["passed"] else "❌"
        print(f"   {mark} [{r['id']}] {r['answer']}")
    print(f"Pass: {pass_count}/{len(results)} ({pass_rate:.0%})")