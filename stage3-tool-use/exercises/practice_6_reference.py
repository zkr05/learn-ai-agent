import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"

def convert_temperature(value: float, unit: str) -> str:
    if unit == "celsius":
        return f"{value * 9 / 5 + 32:.1f} 华氏度"
    elif unit == "fahrenheit":
        return f"{(value - 32) * 5 / 9:.1f} 摄氏度"
    return "error: 未知单位"

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

def react_loop(question: str, tools, max_iter: int = 4) -> dict:
    messages = [{"role": "user", "content": question}]
    trace = []
    for step in range(max_iter):
        resp = client.chat.completions.create(model=MODEL, tools=tools, messages=messages)
        msg = resp.choices[0].message
        thought = msg.content or ""
        tool_calls = msg.tool_calls or []
        assistant_entry = {"role": "assistant", "content": thought}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in tool_calls
            ]
        messages.append(assistant_entry)
        if not tool_calls:
            trace.append({"step": step, "thought": thought, "tool": None, "obs": None})
            return {"final": thought, "trace": trace, "steps": step + 1}
        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            try:
                obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
            except Exception as e:
                obs = f"error: 工具执行失败（{e}）"
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
            trace.append({"step": step, "thought": thought, "tool": tc.function.name, "tool_input": args, "obs": obs})
    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}

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
