import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")


time_tool = {
    "type": "function",
    "function": {
        "name":"get_time",
        "description": "查询城市目前时间。",
        "parameters": {
            "type": "object",
            "properties":{
                "city": {"type": "string", "description": "城市名称(如[东京])"},
            },
            "required": ["city"],
        }
    }
}

resp = client.chat.completions.create(
    model = "qwen2.5:3b",
    max_tokens = 512,
    tools = [time_tool],
    messages=[{"role":"user","content":"东京现在几点？"}],
)

msg = resp.choices[0].message
print("finish_reason:",resp.choices[0].finish_reason)
print("tool_calls:",msg.tool_calls)

assert msg.tool_calls,"预期 LLM 会选择调用 tool（而非直接回答）"
tc = msg.tool_calls[0]
assert tc.function.name == "get_time",f"预期调用get_time,实际{tc.function.name}"
args = json.loads(tc.function.arguments)
assert args.get("city"),"预期 city 参数有值"
print(f"✅ 练习 1.5 通过 — qwen2.5:3b 正确选了 get_time、带 city='{args['city']}' 参数")