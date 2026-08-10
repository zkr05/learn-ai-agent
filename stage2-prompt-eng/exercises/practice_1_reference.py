# 练习 1 参考解答（先自己跑，卡住再看）
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 参考观察：
# 观察1：三个回答风格差异明显——律师版精准/长、老师版口语/短、JSON机器版是 {...} 结构
# 观察2：JSON 机器版可能夹带解释文字（如 "好的，以下是..."），最后一行的 {...} 才是合法 JSON；
#       也可能完全只回 JSON（gemma4 遵循度不如 Claude 严谨）
# 观察3："少于80字" 只是建议，模型经常超——这就是为什么重要约束要在 self-check 里验证

import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

SYSTEM_PROMPTS = {
    "严肃律师": "你是严谨的合约律师。回答要精准、引用法条编号、避免任何主观形容词。",
    "幼儿园老师": "你是温柔的幼儿园老师、要对 5 岁小孩说话。用比喻、口语、少于 80 字。",
    "JSON 机器": "你只回 JSON。schema: {\"answer\": string, \"confidence\": float}",
}
USER_MSG = "请帮我解释什么是租赁合约。"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=1000,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": USER_MSG},
        ],
    )
    outputs[label] = r.choices[0].message.content
    print(f"\n--- [{label}] ---")
    print(outputs[label])
    print(f"(长度: {len(outputs[label])} 字符)")

json_output = outputs["JSON 机器"]
print(f"\nJSON 机器输出长度: {len(json_output)} 字符")
last_line = json_output.strip().split("\n")[-1] if "\n" in json_output else json_output
try:
    parsed = json.loads(last_line)
    print("最后一行的 JSON 解析结果:", parsed)
except json.JSONDecodeError:
    print("最后一行的 JSON 解析失败——模型没遵守 schema")

print("\n✅ 练习 1 通过 — 同一个问题、3 种人格 / 格式 / 语气")
