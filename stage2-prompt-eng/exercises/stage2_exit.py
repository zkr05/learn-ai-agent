import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
#任务 1：Few-shot 分类（20 分）

#写函数 `classify(text) -> str`，要求：
#- 包含 **system message**（设定角色/规则）
#- 包含 **3 个示例**（few-shot）
#- 输入句子：「这个客服电话打了一小时都没人接。」
#- 输出：只返回 `正面` / `负面` / `中立` 之一
SYSTEM_PROMPTS = {
    "你是一个中文情绪分类器":"你要对中文的情绪进行分析，分为正面负面中立三种之一",
}
USER_MSG = "这个客服电话打了一小时都没人接。"

FEW_SHOT_EXAMPLES = """范例:
input:这个店的衣服漂亮价格实惠。
output:正面

input: 这个店排队让我排了很久。
output: 负面

input: 这个店处在汕头市潮阳区。
output: 中立
"""
TASK = "把下面的句子分类成“正面 / 负面 / 中立”其中一个，只输出这三个词其中之一，不要多余文字。\n\n"
def classify(text: str)->str:
    prefix = FEW_SHOT_EXAMPLES + "\n"
    prompt = f"{TASK}{prefix}input: {text}\noutput:"
    for attempt in range(3):
        r = client.chat.completions.create(
            model = "gemma4:e4b",
            max_tokens = 1000,
            messages = [{"role":"system","content":SYSTEM_PROMPTS["你是一个中文情绪分类器"]},
                        {"role":"user","content":prompt}],
        )
        content = (r.choices[0].message.content or "").strip()
        if content:
            return content.splitlines()[-1]
        print(f" (空响应,第{attempt+1}次重试)")
    return ""
print(classify(USER_MSG))


## 任务 2：CoT 解数学题（20 分）

#新题：「一个农场有 7 只鸭子和 5 只鸡。每只鸭子每天下 1 个蛋，每只鸡每天下 0.5 个蛋。请问 3 天后一共多少个蛋？」
#（正确答案 28.5：7×1×3 + 5×0.5×3）

#要求：写一个带 CoT 提示的 prompt，运行，输出里要有**推理步骤**和**最终答案**。

QUESTION = "一个农场有 7 只鸭子和 5 只鸡。每只鸭子每天下 1 个蛋，每只鸡每天下 0.5 个蛋。请问 3 天后一共多少个蛋？"
ANSWER = 28.5

COT_EXAMPLE = """范例:
Q: 一个果园有 4 棵苹果树和 3 棵梨树。每棵苹果树每天结 5 个果，每棵梨树每天结 3 个果。2天后一共多少个果？
A: 慢慢算，苹果4棵树 4×5=20,两天后20×2=40，梨三棵树 3×3=9，两天后9×2=18，总共 40+18=58。答案是 58。
"""

def ask(prompt: str) -> str:
    for attempt in range(3):
        r = client.chat.completions.create(
            model = "gemma4:e4b",
            max_tokens = 1000,
            messages=[{"role":"user","content":prompt}],
        )
        content = (r.choices[0].message.content or "").strip()
        if content:
            return content
        print(f" (空响应，第{attempt+1}次重试)")
    return ""

print(ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:"))


## 任务 3：Refine 5 版并记录（20 分）

#主题自选（例如：「向新同事介绍什么是 API」）。
#写 5 个版本，每版加一个约束/改进，**每版都跑一遍**，把每版输出贴进注释，最后写一句：哪版最好、为什么。


PROMPTS = {
    "v1 模糊":"写一段介绍API的文字。",
    "v2 加目标读者":"写一段介绍API的文字,给没有任何基础的人看。",
    "v3 加格式":"写一段介绍API的文字,给没有任何基础的人看。100字以内,用一个段落",
    "v4 加example要求":"写一段介绍API的文字,给没有任何基础的人看。100字以内,用一个段落,结尾举一个具体例子",
    "v5 加禁忌":"写一段介绍API的文字,给没有任何基础的人看。100字以内,用一个段落,结尾举一个具体例子,不要用空泛的词汇",
}

outputs = {}
for label,prompt in PROMPTS.items():
    text = ""
    for attempt in range(3):
        r = client.chat.completions.create(
            model = "gemma4:e4b",
            max_tokens = 1000,
            messages=[{"role":"user","content":prompt}],
        )
        text = (r.choices[0].message.content or "").strip()
        if text:
            break
        print(f" ({label}空响应,第{attempt+1}次重试)")
    outputs[label] = text
    print(f"\n--- [{label}]({len(text)} chars) ---")
    print(text)
#第四第五版比较好，内容变得比较简洁，也生动形象描绘了对象。

## 任务 4：判断 prompt 的极限（20 分，问答，不用跑代码）

#「让模型告诉我今天上海的气温」——为什么**纯 prompt** 做不到？需要什么？写进文件顶部注释。

#纯prompt没法让模型调用api去查询，需要用requests调用api去查询天气，再把结果返回。 