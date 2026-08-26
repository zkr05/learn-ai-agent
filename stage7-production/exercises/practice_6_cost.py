# 练习 6：Cost Optimization（量成本 + 算缓存省多少）
# 需要：pip install openai；前置：ollama pull qwen2.5:7b && ollama serve
#
# Ollama 本地 $0，但我们可以量 token 数 + 用云端定价模拟"如果上云要花多少"，
# 再演示 prompt caching 能省多少（串起 Stage 1 的定价课）。
#
# 作业：跑完后在顶部注释回答：
# 观察1（一次回答花了多少 token、模拟成本）：一次回答 89 token（40输入+49输出），模拟云端成本 $0.000019——量级很小
# 观察2（1000 次调用要多少钱）：1000 次 $0.02——便宜模型 1000 次才 2 分钱（对比 Stage 1 学的 haiku 1000 次 $0.25）
# 观察3（prompt caching 后能省多少）：prompt caching 让重复的输入前缀只花 10% 价——80% 命中时输入侧省 72%

import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:7b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")

# 模拟云端定价（每 1M token，美元）——按 qwen API 量级
PRICING = {"input": 0.14, "output": 0.28}   # 便宜的开源模型价格


def one_call(question: str) -> dict:
    client = OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": question}],
    )
    usage = resp.usage
    return {"input": usage.prompt_tokens, "output": usage.completion_tokens,
            "text": resp.choices[0].message.content[:50]}


def cost_usd(input_t: int, output_t: int) -> float:
    return (input_t * PRICING["input"] + output_t * PRICING["output"]) / 1_000_000


if __name__ == "__main__":
    print(f"测量 agent 的 token 成本（模型 {MODEL}，定价 $0.14/$0.28 per 1M）\n")

    question = "用 3 句话解释什么是 RAG。"
    r = one_call(question)
    print(f"❓ {question}")
    print(f"   input={r['input']} tokens, output={r['output']} tokens")
    cost_one = cost_usd(r["input"], r["output"])
    print(f"   单次成本: ${cost_one:.6f}")

    # 1000 次调用
    cost_1k = cost_one * 1000
    print(f"\n1000 次调用: ${cost_1k:.2f}")

    # 假设 80% 输入 token 被 prompt caching 命中（省 90% 的缓存部分价格）
    cacheable = r["input"] * 0.8
    cached_price = PRICING["input"] * 0.1   # 缓存命中的输入只要 10% 价格
    normal_input_cost = r["input"] * PRICING["input"]
    cached_input_cost = cacheable * cached_price + (r["input"] - cacheable) * PRICING["input"]
    saving = (normal_input_cost - cached_input_cost) / normal_input_cost

    print(f"\n💡 Prompt caching 模拟（80% 输入命中缓存、缓存价 10%）:")
    print(f"   未缓存输入成本: ${normal_input_cost/1e6:.6f}")
    print(f"   缓存后输入成本: ${cached_input_cost/1e6:.6f}")
    print(f"   输入侧节省: {saving:.0%}")

    assert r["input"] > 0 and r["output"] > 0
    print(f"\n✅ 练习 6 通过 — token 成本可量化、caching 能省约 {saving:.0%} 输入成本、$0/run")
