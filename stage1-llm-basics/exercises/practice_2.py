# 练习 2：Tokens（观察输出长度波动 + 中英文 token 差异）
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 作业：跑完后在文件顶部注释里回答：
# 1）中文和 English 的 input tokens 哪个多？多多少？
# 2）temperature=1.0 下 output 长度为什么会有波动？
# 3）把 N 从 10 改成 3 再跑一次，min/max 的差距是变大还是变小？为什么？
# 观察1：____________________________________
# 观察2：____________________________________
# 观察3：____________________________________

import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "中文": "用一句话描述一只猫在做什么。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # 本机慢、N 小一点
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=500,  # 推理模型思考也占额度，太小会全被截断
            temperature=1.0,
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === 自我验证 ===
assert max(output_tokens) > min(output_tokens), "temperature=1.0 下、output 长度应该有 variance"
print("\n✅ 练习 2 通过 — 本机跑 $0")
print("💡 中文 prompt 通常 input tokens 比 English 多（中文 token 化通常一字 ≈ 2 tokens）")
