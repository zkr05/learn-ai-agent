# 练习 3：从零实现 ReAct（不用 framework）——循环部分你自己写！
# 需要：pip install openai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 规则：工具定义和 TOOL_IMPL 已经给你（样板）；【react_loop 函数体】必须你自己写。
# 卡住可以看 practice_3_reference.py（参考解答），先试 15 分钟再看。
#
# 作业：跑通后填观察：
# 观察1（循环跑了几轮、每轮发生了什么）：2轮完成——第1轮同时查了台北/纽约人口，第2轮算除法收尾
# 观察2（3 个坑：assistant接回 / tool_call_id / max_iter 在哪）：assistant接回(第91~98行)、tool_call_id(第105~111行)、max_iter(for循环那行 85行)——3个坑都在
# 观察3（删掉 assistant 接回那行会怎样）：删掉assistant接回会失忆→重复查人口→死循环
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"


# === 1. 工具定义 + 实现（已给你，样板） ===

def tool_calculator(expression: str) -> str:
    allowed = set("0123456789.+-*/() ")
    if any(c not in allowed for c in expression):
        return f"error: 表达式含不允许字符（{expression}）"
    try:
        return str(eval(expression))
    except Exception as e:
        return f"error: {e}"


def tool_lookup_fact(query: str) -> str:
    facts = {
        "台北人口": "2602000",
        "纽约人口": "8336000",
        "光速": "299792458",
    }
    return facts.get(query.strip(), f"unknown: {query}")


TOOLS_SPEC = [
    {"type": "function", "function": {
        "name": "calculator",
        "description": "做基本算术运算（加减乘除）。输入是表达式字符串。",
        "parameters": {"type": "object", "properties": {
            "expression": {"type": "string", "description": "算术表达式"},
        }, "required": ["expression"]}}},
    {"type": "function", "function": {
        "name": "lookup_fact",
        "description": "查询一个事实（人口 / 物理常数等）。",
        "parameters": {"type": "object", "properties": {
            "query": {"type": "string", "description": "查询关键字"},
        }, "required": ["query"]}}},
]

TOOL_IMPL = {
    "calculator": lambda inp: tool_calculator(inp["expression"]),
    "lookup_fact": lambda inp: tool_lookup_fact(inp["query"]),
}


# === 2. ReAct loop（★ 你自己写这里 ★） ===

def react_loop(question: str, max_iter: int = 6) -> dict: 
    """
    要求：
    1. messages 从 [{"role": "user", "content": question}] 开始
    2. 循环 max_iter 次：
       a. 调 client.chat.completions.create(model=MODEL, tools=TOOLS_SPEC, messages=messages)
       b. 取 msg = resp.choices[0].message；thought = msg.content or ""；tool_calls = msg.tool_calls or []
       c. 【坑1】把 assistant 的回答接回 messages（有 tool_calls 时要带上 tool_calls 字段）
       d. 如果 tool_calls 为空 → 返回 {"final": thought, "steps": 第几轮}
       e. 否则对每个 tc：
          - 从 TOOL_IMPL 取函数，json.loads(tc.function.arguments) 拿参数
          - 执行得到 obs
          - 【坑2】把 {"role": "tool", "tool_call_id": tc.id, "content": obs} 接回 messages
    3. 循环走完没返回 → 返回 {"final": None, "truncated": True}
    """
    # ✍️ 你的代码从这里开始：
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
                {"id": tc.id, "type": "function",
                "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        if not tool_calls:
            trace.append({"step": step, "thought": thought, "tool": None, "obs": None})
            return{"final": thought, "trace": trace, "steps": step + 1}


        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
            messages.append({"role": "tool","tool_call_id": tc.id,"content": obs})
            trace.append({"step": step,"thought": thought,
                          "tool": tc.function.name,"tool_input": args, "obs": obs})

    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}
# === 3. 运行 + 自我验证 ===

if __name__ == "__main__":
    question = "'台北人口' 除以 '纽约人口'、答案保留 4 位小数。"
    print(f"❓ 问题：{question}（模型 {MODEL}）")
    result = react_loop(question, max_iter=5)
    print(f"✅ 最终答案：{result.get('final')}  （{result.get('steps')} 轮）")
    assert result.get("final") is not None or result.get("truncated"), "loop 应收尾或显式 truncate"
    print("✅ 练习 3 通过 — 你的 ReAct 循环跑通了！")
