# 练习 3：Pricing / Latency（成本敏感的工作必修）
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 作业：跑完回答：
# 1）本机跑 1000 次要多久？（min/1000 次）
# 2）同样 1000 次用云端 haiku 大约多少钱？为什么 trade-off 存在？
# 3）把 max_tokens 改成 50 再跑，latency 变了吗？为什么？
# 观察1：____________________________________
# 观察2：____________________________________
# 观察3：____________________________________

import sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

latencies = []
for _ in range(5):
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": "你好！自我介绍一下。"}],
    )
    latencies.append(time.time() - t0)

avg_latency = sum(latencies) / len(latencies)
out_tok_avg = r.usage.completion_tokens
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b (本机)")
print(f"5 次 latency (sec): min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens、约 {tps:.1f} tokens/sec")
print(f"\n1000 次成本: $0 (本机)、预计时长: {avg_latency * 1000 / 60:.1f} 分钟")

# === 自我验证 ===
assert avg_latency > 0, "latency 应 > 0"
assert out_tok_avg > 0, "output token 应 > 0"
print(f"\n✅ 练习 3 通过 — 本机 model $0 但要花 {avg_latency * 1000 / 60:.0f} 分钟跑 1000 次")
print("💡 对照 Path B Anthropic：1000 次只要 ~10-20 分钟但要 $0.25（haiku）")
