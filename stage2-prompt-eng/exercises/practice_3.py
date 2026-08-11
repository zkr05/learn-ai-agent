# 练习 3：Chain-of-Thought（CoT）——数学文字题
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 作业：跑完后在顶部注释回答：
# 观察1（A/B/C 哪个答对）：A/B/C 全部答对(3/3)——A纯prompt也答对，gemma4是推理模型，内部思考就能解，还主动把步骤写进回答
# 观察2（gemma4 是推理模型的影响）：课程预期"普通chat模型A会答错"，但推理模型不适用——题目对8B推理模型太简单，三个条件看不出差异
# 观察3（什么时候别手写 CoT）：对内置思考的模型(推理模型)别硬塞手写CoT，可能干扰；手写CoT适用于无内置推理的普通模型(如0.5B那种)

import sys, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

QUESTION = "小明有 3 颗苹果。他给了小华 1 颗、又从妈妈那边拿到 5 颗、然后吃了 2 颗。请问现在剩几颗？"
ANSWER = 5  # 3 - 1 + 5 - 2 = 5

COT_EXAMPLE = """范例：
Q: 一只鸡有 2 只脚。3 只鸡跟 1 个人共有几只脚？
A: 让我一步一步算。3 只鸡 × 2 只脚 = 6 只脚。1 个人有 2 只脚。总共 6 + 2 = 8 只脚。答案是 8。
"""


def ask(prompt: str) -> str:
    # gemma4:e4b 是推理模型：思考可能吃光 token 导致 content 为空 → 重试
    for attempt in range(3):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=1000,  # 思考 + 步骤 + 答案都要 token
            messages=[{"role": "user", "content": prompt}],
        )
        content = (r.choices[0].message.content or "").strip()
        if content:
            return content
        print(f"  (空响应，第 {attempt+1} 次重试)")
    return ""


def extract_number(text: str) -> int | None:
    nums = re.findall(r"-?\d+", text)
    return int(nums[-1]) if nums else None


# A. 纯 prompt
out_a = ask(QUESTION); ans_a = extract_number(out_a)

# B. + Let's think step by step
out_b = ask(QUESTION + "\nLet's think step by step."); ans_b = extract_number(out_b)

# C. + CoT example
out_c = ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:"); ans_c = extract_number(out_c)

for label, out, ans in [("A 纯 prompt", out_a, ans_a), ("B +step-by-step", out_b, ans_b), ("C +CoT example", out_c, ans_c)]:
    print(f"\n--- [{label}] 答案={ans} {'✓' if ans == ANSWER else '✗'} ---")
    print(out[:200])

# === 自我验证 ===
correct = sum(1 for a in (ans_a, ans_b, ans_c) if a == ANSWER)
assert correct >= 1, f"3 种 prompt 至少要 1 种答对、实际 {correct}/3"
assert ans_b == ANSWER or ans_c == ANSWER, "B (step-by-step) 或 C (CoT example) 至少一种要答对"
print(f"\n✅ 练习 3 通过 — {correct}/3 答对（本机 $0）")
print("💡 gemma4:e4b 是推理模型（内置思考）——A 纯 prompt 也可能靠内部思考答对，跟课程预期的普通 chat 模型不同")
print("💡 对推理模型，硬塞'Let's think step by step' 不一定有帮助，甚至可能干扰——这正是课程警告框说的")
