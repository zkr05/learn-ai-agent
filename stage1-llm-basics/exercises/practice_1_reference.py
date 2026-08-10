# 练习 1 参考解答（先自己写，卡住再看）
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 参考观察：
# 观察1（改 content）：换了问法后回答内容跟着变，token 数也会变。
# 观察2（max_tokens=10）：输出被截断，finish_reason 从 "stop" 变成 "length"，
#       回应不完整——这就是 max_tokens 上限生效的样子。
# 观察3（temperature=0）：连续跑 3 次答案几乎一样（每次采样都选最高概率）。

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

r = client.chat.completions.create(
    model="gemma4:e4b",
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)

text = r.choices[0].message.content
print("回应：", text)
print("usage:", r.usage)
print("finish_reason:", r.choices[0].finish_reason)

assert r.choices[0].finish_reason in ("stop", "length")
assert len(text) > 0
assert r.usage.completion_tokens > 0
print("✅ 练习 1 通过 — Ollama gemma4:e4b 已能本机回应、$0/次")
