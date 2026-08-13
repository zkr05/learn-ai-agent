#Agent 的 3 个最小部件是什么？缺一个行不行？
# LLM（大脑）+  Tools（手）+ Loop（心跳）；缺一不可，缺了 Tools/Loop 就只是"会说话的模型"
#多步 ReAct 什么时候该停？
# 模型不再返回 tool_calls（不打算再调工具）时就停；另外 max_iter 是强制安全网，防止无限循环
#为什么工具错误要 return dict 而不是 raise？
# raise 会中断整个循环，模型没机会恢复；返回 {"error": ..., "retry_hint": ...} 让错误变成数据喂回模型，模型自己决定重试/改参数/放弃

import sys,json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"


RATES = {
    "USD":1.0,
    "CNY":6.7,
    "EUR":0.89,
    "JPY":159.0,
}

def exchange_rate(from_currency: str,to_currency: str) -> dict:
    f = from_currency.upper()
    t = to_currency.upper()
    if f not in RATES or t not in RATES:
        return {"error": f"不支持的币种: {from_currency} -> {to_currency}",
                "retry_hint": f"支持的币种: {list(RATES.keys())}"}
    rate = RATES[t] / RATES[f]
    return {"from": from_currency, "to": to_currency,"rate": rate}

def calculator(expression: str) -> dict:
    allowed = set("0123456789.+-*/() ")
    if any(c not in allowed for c in expression):
        return {"error": f"表达式含不允许字符: {expression}",
                "retry_hint": "只用数字和+-*/()"}
    try:
        return {"result": str(eval(expression))}
    except Exception as e:
        return {"error": f"计算失败: {e}",
                "retry_hint": "检查表达式是否正确"}

TOOLS_SPEC = [
    {"type": "function","function":{
        "name": "exchange_rate",
        "description": "Use when user ask to exchange rate between different currency.",
        "parameters": {"type":"object","properties":{
            "from_currency": {"type": "string"},
            "to_currency": {"type": "string"}},
            "required": ["from_currency","to_currency"]}}},
    {"type": "function","function":{
        "name": "calculator",
        "description": "做基本算术运算（加减乘除）。输入是表达式字符串。",
        "parameters": {"type":"object","properties":{
            "expression": {"type":"string","description": "算术表达式，如 10 * 7.2"},
        },"required": ["expression"]}}}
]

TOOL_IMPL = {
    "exchange_rate": lambda i: json.dumps(exchange_rate(i["from_currency"],i["to_currency"]),ensure_ascii=False),
    "calculator": lambda i: json.dumps(calculator(i["expression"]),ensure_ascii=False),
}


def react_loop(question: str, max_iter: int = 4) -> dict:
    messages = [{"role":"user","content":question}]
    trace = []

    for step in range(max_iter):
        resp = client.chat.completions.create(
            model = MODEL,tools = TOOLS_SPEC,messages = messages)
        msg = resp.choices[0].message
        thought = msg.content or ""
        tool_calls = msg.tool_calls or []
        assistant_entry = {"role":"assistant","content":thought}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {"id":tc.id, "type":"function",
                "function":{"name":tc.function.name,"arguments":tc.function.arguments}}
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        if not tool_calls:
            trace.append({"step": step,"thought":thought,"tool":None,"obs":None})
            return{"final": thought,"trace": trace,"step": step + 1}

        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            try:
                obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
            except Exception as e:
                obs = f"error: 工具执行失败({e}),请检查参数重新调用"
            messages.append({"role":"tool","tool_call_id": tc.id, "content": obs})
            trace.append({"step": step, "thought":thought,
                          "tool": tc.function.name,"tool_input": args,"obs": obs})

    return{"final":None,"trace":trace,"step": max_iter,"truncated":True}

if __name__=="__main__":
    question1 = "查一下 USD 兑 JPY 的汇率是多少"
    r1 = react_loop(question1,max_iter=4)
    for e in r1.get("trace",[]):
        print(f"[step{e['step']}] tool: {e.get('tool')} {e.get('tool_input')} -> {e.get('obs')}")
    print(f"答案: {r1.get('final')}")
    question2 = "查一下 USD 兑 CNY 的汇率，然后用 calculator 工具计算 100 USD 能换多少 CNY，必须给出最终答案，不要提前结束。"
    r2 = react_loop(question2,max_iter=4)
    for e in r2.get("trace",[]):
        print(f"[step{e['step']}] tool: {e.get('tool')} {e.get('tool_input')} -> {e.get('obs')}")
    print(f"答案: {r2.get('final')}")
    question3 = "BTC 兑 CNY 的汇率是多少"
    r3 = react_loop(question3,max_iter=4)
    for e in r3.get("trace",[]):
        print(f"[step{e['step']}] tool: {e.get('tool')} {e.get('tool_input')} -> {e.get('obs')}")
    print(f"答案: {r3.get('final')}")       