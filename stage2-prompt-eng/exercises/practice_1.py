# 练习 1：System Prompt（同一个问题、3 种人设）
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 作业：跑完后在顶部注释回答：
# 观察1（风格差异）：律师版官方且较长，幼儿园老师易懂且较短，JSON机器版是机器式结构
# 观察2（JSON合法性）：JSON本身合法，\\n是字符串正常转义（json.loads后变换行）；但模型没遵守"不要代码块"，包了```json，原始输出看着乱
# 观察3（80字限制）：老师版做到了80字以内

import sys, json, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 同一个 user message、3 个不同 system prompt
SYSTEM_PROMPTS = {
    "严肃律师": "你是严谨的合约律师。回答要精准、引用法条编号、避免任何主观形容词。",
    "幼儿园老师": "你是温柔的幼儿园老师、要对 5 岁小孩说话。用比喻、口语、少于 80 字。",
    "JSON 机器": "你只输出一个 JSON 对象，不要代码块、不要任何解释。schema: {\"answer\": string, \"confidence\": float}",
}

USER_MSG = "请帮我解释什么是租赁合约。"

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    # Ollama 把 system 放 messages 第一笔（Anthropic 才用 system= 参数）
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=1000,  # 推理模型思考会吃 token，200 不够
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": USER_MSG},
        ],
    )
    outputs[label] = r.choices[0].message.content
    print(f"\n--- [{label}] ---")
    print(outputs[label])

# === 自我验证 ===
# 模型经常不老实遵守 system（可能夹解释、包代码块），所以要从输出里提取 JSON
json_output = outputs["JSON 机器"]
m = re.search(r"\{.*\}", json_output, re.DOTALL)   # 取第一个 { 到最后一个 }
assert m, f"JSON 机器版输出里没有找到 {{...}}，模型没遵守：{json_output[:100]}"
try:
    parsed = json.loads(m.group())
    assert "answer" in parsed, "JSON schema 应包含 answer 栏位"
    print(f"\n✅ JSON 机器版提取成功：{parsed}")
except json.JSONDecodeError as e:
    print(f"\n⚠️ 提取到的 JSON 无法解析（{e}）——模型输出不规范，真实场景要处理这种情况")
print(f"\n✅ 练习 1 通过 — 同一个问题、3 种人格 / 格式 / 语气")
print("💡 观察：律师长、老师短、JSON 机器要自己提取 {…}（模型不保证遵守 system）")
