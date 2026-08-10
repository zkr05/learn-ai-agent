# 练习 6：Local LLM（本机小模型收尾）——两个模型同台对比
# 需要：pip install openai；前置：ollama pull gemma4:e4b qwen2.5:0.5b && ollama serve
#
# 作业：
# 1）跑通本机模型调用，确认 $0
# 2）对比 0.5B 和 8B 对同一问题的回答：质量差在哪？差多少？
# 3）什么场景适合本机小模型？什么场景必须上云端大模型？
# 观察1：____________________________________
# 观察2：____________________________________
# 观察3：____________________________________

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查、随便填
)

PROMPT = "用 3 句话介绍什么是 ReAct。"

texts = []
for model in ["gemma4:e4b", "qwen2.5:0.5b"]:
    print(f"\n===== {model} =====")
    r = client.chat.completions.create(
        model=model,
        max_tokens=1000,  # 推理模型思考会吃 token
        messages=[{"role": "user", "content": PROMPT}],
    )
    text = r.choices[0].message.content
    texts.append(text)
    print("回应：", text)
    print(f"(本次用了 {r.usage.completion_tokens} tokens)")

# === 自我验证 ===
assert all(len(t) > 10 for t in texts), "回应太短、Ollama 可能没跑起来"
print("\n✅ 练习 6 通过 — 本机两个模型都能跑，全程 $0")
print("💡 观察 0.5B 是不是又把 ReAct 当成 React 了？")
