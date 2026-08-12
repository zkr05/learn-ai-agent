# 练习 2：多工具选择（3 个工具，让模型自己挑）
# 需要：pip install openai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 作业：跑完后在顶部注释回答：
# 观察1（三个问题各挑了哪个工具）：算式题挑了calculator(对)，天气问题挑了calendar_lookup(错！)，日历问题直接文字回答没调工具(也错)
# 观察2（挑错了吗？为什么）：有挑错的——天气该用web_search却挑了calendar；模型选择不稳定，同一问题多次跑结果可能不同
# 观察3（把某个 description 改模糊，看模型会不会挑错）：description改模糊后模型更容易挑错；另外发现小模型有时会"忘记"自己有工具

import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

TOOLS = [
    {"type": "function", "function": {"name": "web_search",
        "description": "Search current or external info .",
        "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "calculator",
        "description": "Evaluate basic arithmetic with +, -, *, /, parentheses.",
        "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "calendar_lookup",
        "description": "Look up events for a specific date.",
        "parameters": {"type": "object", "properties": {"date": {"type": "string"}}, "required": ["date"]}}},
]

QUESTIONS = [
    "What is (19 * 42) - 8?",
    "今天上海天气怎么样？",
    "今天是 2026 年 8 月 12 日。我明天有什么安排？",
]

for q in QUESTIONS:
    resp = client.chat.completions.create(
        model="qwen2.5:3b",
        max_tokens=512,
        tools=TOOLS,
        messages=[{"role": "user", "content": q}],
    )
    msg = resp.choices[0].message
    if msg.tool_calls:
        tc = msg.tool_calls[0]
        print(f"问题: {q[:20]}... → 挑了 {tc.function.name}, args={json.loads(tc.function.arguments)}")
    else:
        print(f"问题: {q[:20]}... → 没调工具，直接答: {msg.content[:50]}")

# === 自我验证 ===
resp = client.chat.completions.create(
    model="qwen2.5:3b", max_tokens=512, tools=TOOLS,
    messages=[{"role": "user", "content": "What is (19 * 42) - 8?"}],
)
tc = resp.choices[0].message.tool_calls[0]
assert tc.function.name == "calculator", f"预期 calculator、实际 {tc.function.name}"
args = json.loads(tc.function.arguments)
assert "19 * 42" in args.get("expression", ""), f"预期表达式、实际 {args}"
print("\n✅ 练习 2 通过 — 模型对算式题正确挑了 calculator")
print("💡 观察：description 边界要互斥——写得太笼统会跟别的工具撞")
