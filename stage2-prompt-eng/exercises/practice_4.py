# 练习 4：Iterative Refinement（5 轮迭代优化 prompt）
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 作业：跑完后在顶部注释回答：
# 观察1（v1 vs v5 差距）：v1的内容更加的空泛，而v5加了约束条件后变得更加精简
# 观察2（哪轮改动最有效）：v2到v3的改动最有效，加上了字数限制，用一个段落
# 观察3（为什么加约束能收敛）：约束越具体（不管是减法要求还是禁忌），输出越收敛。

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 5 个 iteration、每一轮 prompt 都比前一轮更具体
PROMPTS = {
    "v1 模糊": "写一段介绍 ReAct 的文字。",
    "v2 加目标读者": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。",
    "v3 加格式": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。100 字以内、用一个段落。",
    "v4 加example要求": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。100 字以内、用一个段落、结尾举一个具体例子（譬如查天气）。",
    "v5 加禁忌": "写一段介绍 ReAct 的文字、给写过 Python 的软件工程师看。100 字以内、用一个段落、结尾举一个具体例子（譬如查天气）。不要用「赋能」「驱动」「智能」这类空泛词汇。",
}

outputs = {}
for label, prompt in PROMPTS.items():
    # 推理模型思考会吃 token → 空响应重试
    text = ""
    for attempt in range(3):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = (r.choices[0].message.content or "").strip()
        if text:
            break
        print(f"  ({label} 空响应，第 {attempt+1} 次重试)")
    outputs[label] = text
    print(f"\n--- [{label}] ({len(text)} chars) ---")
    print(text)

# === 自我验证 ===
v1_len, v5_len = len(outputs["v1 模糊"]), len(outputs["v5 加禁忌"])
banned_words = ("赋能", "驱动", "智能")
v5_has_banned = [w for w in banned_words if w in outputs["v5 加禁忌"]]
assert v5_len > 0, "v5 必须有输出"
assert not v5_has_banned, f"v5 应该避免禁忌词、实际含: {v5_has_banned}"
print(f"\n✅ 练习 4 通过 — v1 长度 {v1_len}、v5 长度 {v5_len}、v5 无禁忌词（本机 $0）")
print("💡 观察：v1 通常比 v5「松」、加约束会逼 prompt 收敛")
