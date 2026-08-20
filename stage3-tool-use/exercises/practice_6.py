# 练习 6：Function schema 设计（坏 schema 修到好）
# 需要：pip install openai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 任务：同一个温度转换工具，BAD schema 和 GOOD schema 各跑一遍，看模型表现差多少。
# 把你在练习 3/4 写的 react_loop 复制过来。
#
# 作业：跑完后在顶部注释回答：
# 观察1（BAD schema 下模型的表现）：BAD时模型调了convert(不存在)、value传了字符串'100'——工具报unknown tool，模型退回路算没算完
# 观察2（GOOD schema 下模型的表现）：GOOD时一次调用convert_temperature(value=100, unit='fahrenheit')→37.8℃，答案正确
# 观察3（4 个改进点分别起什么作用）：名字具体化让模型调对工具；type=number让value传数字；enum限死unit只能celsius/fahrenheit；required确保参数齐全

import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"


# === 1. 工具实现 ===

def convert_temperature(value: float, unit: str) -> str:
    if unit == "celsius":
        return f"{value * 9 / 5 + 32:.1f} 华氏度"
    elif unit == "fahrenheit":
        return f"{(value - 32) * 5 / 9:.1f} 摄氏度"
    return "error: 未知单位"


# === 2. 两种 schema ===

BAD_TOOLS = [
    {"type": "function", "function": {
        "name": "convert",
        "description": "Convert a value.",
        "parameters": {"type": "object", "properties": {
            "value": {"type": "string"},
            "unit": {"type": "string"}}}}},
]

GOOD_TOOLS = [
    {"type": "function", "function": {
        "name": "convert_temperature",
        "description": "Use when user asks to convert temperatures between Fahrenheit and Celsius.",
        "parameters": {"type": "object", "properties": {
            "value": {"type": "number", "description": "Temperature value"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}},
            "required": ["value", "unit"]}}},
]

TOOL_IMPL = {"convert_temperature": lambda i: convert_temperature(i["value"], i["unit"])}


# === 3. ★ 你的 react_loop（改成接收 tools 参数） ===

def react_loop(question: str, tools, max_iter: int = 4) -> dict:
    # ✍️ 你的代码：把练习 4 的 react_loop 复制过来，把 TOOLS_SPEC 换成 tools 参数
    messages = [{"role": "user","content":question}]
    trace = []
    
    for step in range(max_iter):
        resp = client.chat.completions.create(
            model = MODEL,tools = tools,messages = messages)
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
    


# === 4. 运行对比 ===

if __name__ == "__main__":
    question = "100 华氏度是多少摄氏度？"
    print("=" * 30, "BAD schema", "=" * 30)
    r1 = react_loop(question, BAD_TOOLS, max_iter=4)
    for e in r1.get("trace", []):
        print(f"[step {e['step']}] tool: {e.get('tool')} {e.get('tool_input')} -> {e.get('obs')}")
    print(f"答案：{r1.get('final')}")

    print("=" * 30, "GOOD schema", "=" * 30)
    r2 = react_loop(question, GOOD_TOOLS, max_iter=4)
    for e in r2.get("trace", []):
        print(f"[step {e['step']}] tool: {e.get('tool')} {e.get('tool_input')} -> {e.get('obs')}")
    print(f"答案：{r2.get('final')}")
