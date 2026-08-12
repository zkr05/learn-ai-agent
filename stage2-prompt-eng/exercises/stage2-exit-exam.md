# Stage 2 出口考核（从零动手）

规则：**不参考任何模板/解答**，自己写。可以翻笔记，但不能抄代码。
写一个 `stage2_exit.py`，运行通过后把输出发我，我逐项验收（对照 Stage 2 自检清单）。

环境：Ollama + gemma4:e4b，模型是推理模型，记得 max_tokens 给够、空响应重试。

---
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
任务 1：Few-shot 分类（20 分）

写函数 `classify(text) -> str`，要求：
- 包含 **system message**（设定角色/规则）
- 包含 **3 个示例**（few-shot）
- 输入句子：「这个客服电话打了一小时都没人接。」
- 输出：只返回 `正面` / `负面` / `中立` 之一

TEST_SET = [
    ("这个客服电话打了一小时都没人接。","负面")
]

FEW_SHOT_EXAMPLES = """范例:
input: 这个店的衣服漂亮价格实惠。
output：正面

input：这个店排队让我排了很久。
output：负面

input：这个店处在汕头市潮阳区。
output：中立
"""
TASK = "把下面的句子分类成“正面 / 负面 / 中立”其中一个，只输出这三个词其中之一，不要多余文字。\n\n"
def classify(text: str, *, use_few_shot: bool)->str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{TASK}{prefix}input: {text}\noutput:"
    for attempt in range(3):
        r = client.chat.completions.create(
            model = "gemma4:e4b",
            max_tokens = 1000,
            messages = [{"role":"user","content":prompt}],
        )
        content = (r.choices[0].message.content or "").strip()
        if content:
            return content.splitlines()[-1]
        print(f" (空响应,第{attempt+1}次重试)")
    return ""

## 任务 2：CoT 解数学题（20 分）

新题：「一个农场有 7 只鸭子和 5 只鸡。每只鸭子每天下 1 个蛋，每只鸡每天下 0.5 个蛋。请问 3 天后一共多少个蛋？」
（正确答案 28.5：7×1×3 + 5×0.5×3）

要求：写一个带 CoT 提示的 prompt，运行，输出里要有**推理步骤**和**最终答案**。

## 任务 3：Refine 5 版并记录（20 分）

主题自选（例如：「向新同事介绍什么是 API」）。
写 5 个版本，每版加一个约束/改进，**每版都跑一遍**，把每版输出贴进注释，最后写一句：哪版最好、为什么。

## 任务 4：判断 prompt 的极限（20 分，问答，不用跑代码）

「让模型告诉我今天上海的气温」——为什么**纯 prompt** 做不到？需要什么？写进文件顶部注释。

## 提交（20 分）

`git commit -m "Stage2出口考核"`，把输出和观察发我。

**评分标准**：任务 1/2 能跑通且输出正确、任务 3 有 5 版记录和结论、任务 4 答到点子上 → 满分过关。
