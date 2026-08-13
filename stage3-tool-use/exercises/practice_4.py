# 练习 4：多步骤推理任务（3-5 步 tool 调用）
# 需要：pip install openai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 任务：把你练习 3 写的 react_loop 复制/搬过来，换下面的工具和题目。
# 题目：找出台北人口，除以纽约人口，再把比例换成百分比。（需要 3-4 次工具调用）
#
# 作业：跑完后在顶部注释回答：
# 观察1（跑了几轮、每轮调了什么）：多步任务=同一个ReAct循环，跑久一点（max_iter=8）——3轮完成查人口→计算→收尾
# 观察2（模型漏步了吗？哪步容易漏）：模型会漏步/编数据/抢跑/传垃圾参数——try/except把错误变observation让模型自纠错；工具支持中英文；prompt短+必须完成
# 观察3（多跑几次，看稳不稳定）：qwen2.5:3b 多步成功率低（我实测2/5），不稳定是模型能力边界
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"


# === 1. 4 个工具（已给你） ===

def lookup_population(city: str) -> str:
    data = {"taipei": 2_602_000, "台北":2_602_000, "new york": 8_336_000,"纽约": 8_336_000}
    return str(data.get(city.strip().lower(), 0))

def divide(a: float, b: float) -> str:
    b = float(b)
    return "0" if b == 0 else str(float(a) / b)

def to_percentage(ratio: float) -> str:
    return f"{float(ratio) * 100:.2f}"

def round_int(x: float) -> str:
    return str(round(float(x)))

TOOLS_SPEC = [
    {"type": "function", "function": {"name": "lookup_population",
        "description": "Return the population for a known city.",
        "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}},
    {"type": "function", "function": {"name": "divide",
        "description": "Divide a by b. Returns 0 instead of crashing when b is zero.",
        "parameters": {"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}, "required": ["a", "b"]}}},
    {"type": "function", "function": {"name": "to_percentage",
        "description": "Convert a ratio to a percentage string.",
        "parameters": {"type": "object", "properties": {"ratio": {"type": "number"}}, "required": ["ratio"]}}},
    {"type": "function", "function": {"name": "round_int",
        "description": "Round a number to the nearest integer.",
        "parameters": {"type": "object", "properties": {"x": {"type": "number"}}, "required": ["x"]}}},
]

TOOL_IMPL = {
    "lookup_population": lambda i: lookup_population(i["city"]),
    "divide": lambda i: divide(i["a"], i["b"]),
    "to_percentage": lambda i: to_percentage(i["ratio"]),
    "round_int": lambda i: round_int(i["x"]),
}


# === 2. ★ 把你在练习 3 写的 react_loop 复制到这里（改 max_iter=8） ===

def react_loop(question: str, max_iter: int = 8) -> dict:
    messages = [{"role": "user","content":question}]
    trace = []

    for step in range(max_iter):
        resp = client.chat.completions.create(
            model = MODEL,tools = TOOLS_SPEC,messages = messages)
        msg = resp.choices[0].message
        thought = msg.content or ""
        tool_calls = msg.tool_calls or []
        assistant_entry = {"role": "assistant","content":thought}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {"id": tc.id, "type":"function",
                "function":{"name": tc.function.name,"arguments": tc.function.arguments}}
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        if not tool_calls:
            trace.append({"step": step, "thought":thought, "tool":None, "obs":None})
            return{"final": thought, "trace" : trace, "steps": step + 1}

        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            try:
                obs = fn(args) if fn else f"error: unknown tool {tc.function.name}" #加上try格式
            except Exception as e:
                obs = f"error: 工具执行失败（{e}），请检查参数重新调用"   # ← 错误变成 observation
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
            trace.append({"step": step,"thought":thought,
                          "tool": tc.function.name,"tool_input": args,"obs": obs})

    return {"final": None, "trace": trace, "steps": max_iter,"truncated": True}
# === 3. 运行 ===

if __name__ == "__main__":
    question = "台北人口是纽约人口的百分之几？先查数据，再用工具计算，必须给出最终百分比答案，不要提前结束。"
    print(f"❓ 问题：{question}")
    result = react_loop(question, max_iter=8)
    for entry in result.get("trace", []):
        print(f"[step {entry['step']}] tool: {entry.get('tool')} {entry.get('tool_input')} -> {entry.get('obs')}")
    print(f"✅ 最终答案：{result.get('final')}  （{result.get('steps')} 轮）")
    assert result.get("final") is not None or result.get("truncated"), "loop 应收尾或显式 truncate"
    print("✅ 练习 4 通过")
