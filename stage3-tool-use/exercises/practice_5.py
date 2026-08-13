# 练习 5：错误处理（tool error 是 data、不是 exception）
# 需要：pip install openai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 任务：把你在练习 3/4 写的 react_loop 复制过来。
# 工具 fetch_weather 只会返回【结构化 dict】，从不 raise——错误也走 dict。
#
# 作业：跑完后在顶部注释回答：
# 观察1（模型遇到错误后怎么反应）：模型遇到错误后读了retry_hint，没有崩溃也没编数据
# 观察2（重试了吗/改参数了吗/放弃了吗）：它选择"告诉用户替代方案"而不是硬重试——合理恢复
# 观察3（如果工具直接 raise 会怎样）：如果工具raise异常，循环会直接中断、模型没机会恢复——所以错误要走dict
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"


# === 1. 工具：只会返回 dict，从不 raise ===

def fetch_weather(city: str) -> dict:
    known = {"taipei": ("rain", 24), "beijing": ("sunny", 30), "shanghai": ("cloudy", 28), "台北": ("rain", 24), "北京": ("sunny", 30), "上海": ("cloudy", 28)}
    key = city.strip().lower()
    if key in known:
        forecast, temp = known[key]
        return {"city": city, "forecast": forecast, "temperature_c": temp}
    # 错误也走 dict（关键！）
    return {"error": f"city not found: {city}", "retry_hint": "try one of: taipei / beijing / shanghai"}


TOOLS_SPEC = [
    {"type": "function", "function": {
        "name": "fetch_weather",
        "description": "查询城市天气。返回 dict：成功是 {city, forecast, temperature_c}；失败是 {error, retry_hint}。",
        "parameters": {"type": "object", "properties": {
            "city": {"type": "string", "description": "城市名"},
        }, "required": ["city"]}}},
]

TOOL_IMPL = {
    "fetch_weather": lambda i: json.dumps(fetch_weather(i["city"]), ensure_ascii=False),
}


# === 2. ★ 把你在练习 3/4 写的 react_loop 复制到这里 ===

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
    question = "悉尼现在天气怎么样？"
    print(f"❓ 问题：{question}")
    result = react_loop(question, max_iter=6)
    for entry in result.get("trace", []):
        print(f"[step {entry['step']}] tool: {entry.get('tool')} {entry.get('tool_input')} -> {entry.get('obs')}")
    print(f"✅ 最终答案：{result.get('final')}  （{result.get('steps')} 轮）")
    assert result.get("final") is not None or result.get("truncated"), "loop 应收尾或显式 truncate"
    print("✅ 练习 5 通过")
