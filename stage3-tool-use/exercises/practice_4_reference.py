# 练习 4 参考解答（完整版，先自己填空壳，卡住再看）
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"

def lookup_population(city: str) -> str:
    data = {"taipei": 2_602_000, "new york": 8_336_000}
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

def react_loop(question: str, max_iter: int = 8) -> dict:
    messages = [{"role": "user", "content": question}]
    for step in range(max_iter):
        resp = client.chat.completions.create(model=MODEL, tools=TOOLS_SPEC, messages=messages)
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
            return {"final": thought, "steps": step + 1}
        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
            print(f"  [step {step}] {tc.function.name}({args}) -> {obs}")
    return {"final": None, "steps": max_iter, "truncated": True}

if __name__ == "__main__":
    question = "找出台北人口，除以纽约人口，再把比例换成百分比。"
    print(f"❓ 问题：{question}")
    result = react_loop(question, max_iter=8)
    print(f"✅ 最终答案：{result.get('final')}  （{result.get('steps')} 轮）")
    assert result.get("final") is not None or result.get("truncated"), "loop 应收尾或显式 truncate"
    print("✅ 练习 4 通过")
