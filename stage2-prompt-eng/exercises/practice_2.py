# 练习 2：Few-Shot（0-shot vs 3-shot 情绪分类）
# 需要：pip install openai；前置：ollama pull gemma4:e4b && ollama serve
#
# 作业：跑完后在顶部注释回答：
# 观察1（准确率）：0-shot 6/6(100%)，3-shot 5/6(83%)——3-shot 反而少对1题（"第一集…崩了"判成中立）
# 观察2（输出格式）：两边输出都是干净标签（这组句子太简单，0-shot 也够干净）——跟准确率比，格式差异这次不明显
# 观察3（为什么few-shot有用）：单次结果受采样随机性影响，6题差1题=噪声级别；few-shot 不保证每次更准，要多跑几次取平均才能评估

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 中文情绪分类（正面 / 负面 / 中立）
TEST_SET = [
    ("这部电影超赞、看完想再看一次！", "正面"),
    ("剧情无聊、演员演技尴尬。", "负面"),
    ("这是一部 2019 年的电影。", "中立"),
    ("我不确定喜不喜欢、可能再想想。", "中立"),
    ("第一集很不错但第二集就崩了。", "负面"),
    ("看完心情很好、推荐！", "正面"),
]

FEW_SHOT_EXAMPLES = """范例：
input: 这家餐厅的牛排好吃到让我哭出来。
output: 正面

input: 服务生态度很差、我再也不会来了。
output: 负面

input: 这家店位于新北市三重区。
output: 中立
"""

# 两种条件共用同一段“任务说明”；few-shot 只多加范例——对比才干净
TASK = "把下面的句子分类成“正面 / 负面 / 中立”其中一个，只输出这三个词其中之一、不要多余文字。\n\n"


def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{TASK}{prefix}input: {text}\noutput:"
    # gemma4:e4b 是推理模型：思考可能吃光 token 导致 content 为空 → 重试
    for attempt in range(3):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=1000,  # 推理模型思考会吃 token，10 不够
            messages=[{"role": "user", "content": prompt}],
        )
        content = (r.choices[0].message.content or "").strip()
        if content:
            return content.splitlines()[-1]
        print(f"  (空响应，第 {attempt+1} 次重试)")
    return ""


def evaluate(use_few_shot: bool) -> tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f"  {'✓' if ok else '✗'} [{label}] {text[:26]}... → '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)


print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"正确 {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"正确 {c3}/{n} = {c3/n:.0%}")

# === 自我验证 ===
assert n == 6 and 0 <= c0 <= n and 0 <= c3 <= n, "两种条件都要各跑完 6 题"
print(f"\n✅ 练习 2 通过 — 0-shot {c0}/{n}、3-shot {c3}/{n}；few-shot 净提升 {c3 - c0} 题（可能为 0 甚至负，都算正常）（本机 $0）")
print("💡 观察：即使准确率一样，0-shot 输出通常更啰嗦，3-shot 更干净——few-shot 的价值在钉住输出格式 + 示范判准")
