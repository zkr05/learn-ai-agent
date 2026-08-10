# 练习 4：Cross-Provider 比较（同一 prompt 问多个模型）
# 需要：pip install openai；前置：ollama pull 两个模型（gemma4:e4b + qwen2.5:0.5b）
# 说明：本机没有 Claude/GPT/Gemini key 时，用两个不同的本地模型对比；
#       以后有 key 了，可以照 examples/stage-1/04-cross-provider 加云端对比。
#
# 作业：跑完回答：
# 1）两个模型对同一问题的回答风格有什么不同？
# 2）哪个更符合你的需求？为什么？
# 3）如果换成云端 Claude vs GPT，你预期差异会更大还是更小？
# 观察1：____________________________________
# 观察2：____________________________________
# 观察3：____________________________________

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPT = "用 3 句话解释什么是 Agent。"

for model in ["gemma4:e4b", "qwen2.5:0.5b"]:
    print(f"\n===== {model} =====")
    r = client.chat.completions.create(
        model=model,
        max_tokens=1000,  # gemma4:e4b 思考会吃 token，200 不够
        messages=[{"role": "user", "content": PROMPT}],
    )
    print(r.choices[0].message.content)

# === 自我验证 ===
print("\n✅ 练习 4 通过 — 你已体验 2 个不同的 LLM（达成 Stage 1 自检之一）")
