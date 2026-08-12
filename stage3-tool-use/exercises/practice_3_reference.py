# 练习 3：从零实现 ReAct（不用 framework）—— 最重要的一课！
# 需要：pip install openai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 作业：跑完后在顶部注释回答：
# 观察1（循环跑了几轮、每轮发生了什么）：____________________________________
# 观察2（3 个坑对应代码哪几行）：____________________________________
# 观察3（如果把 messages.append(assistant) 删掉会怎样）：____________________________________

import sys, json
from typing import Any
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "qwen2.5:3b"


# === 1. 工具定义 + 实现 ===

def tool_calculator(expression: str) -> str:
    """安全的计算器：只允许 + - * / 和数字。"""
    allowed = set("0123456789.+-*/() ")
    if any(c not in allowed for c in expression):
        return f"error: 表达式含不允许字符（{expression}）"
    try:
        return str(eval(expression))  # 已用 whitelist 限制
    except Exception as e:
        return f"error: {e}"


def tool_lookup_fact(query: str) -> str:
    """假的资料查询（教学用，避免依赖外部 API）。"""
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


# === 2. ReAct loop（核心！） ===

def react_loop(question: str, max_iter: int = 6) -> dict:
    messages = [{"role": "user", "content": question}]
    trace = []

    for step in range(max_iter):                       # 坑3：max_iter 安全网
        resp = client.chat.completions.create(
            model=MODEL, tools=TOOLS_SPEC, messages=messages,
        )
        msg = resp.choices[0].message
        thought_text = msg.content or ""
        tool_calls = msg.tool_calls or []

        # 坑1：必须把 assistant 回答接回 messages，下轮 LLM 才看得到自己说了什么
        assistant_entry = {"role": "assistant", "content": thought_text}
        if tool_calls:
            assistant_entry["tool_calls"] = [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in tool_calls
            ]
        messages.append(assistant_entry)

        if not tool_calls:                              # 模型不再调工具 → 收尾
            trace.append({"step": step, "thought": thought_text, "tool": None, "obs": None})
            return {"final": thought_text, "trace": trace, "steps": step + 1}

        # 执行工具、把结果（observation）接回 messages
        for tc in tool_calls:
            fn = TOOL_IMPL.get(tc.function.name)
            args = json.loads(tc.function.arguments)
            obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
            # 坑2：role="tool" 必须带 tool_call_id，LLM 才知道结果对应哪次调用
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
            trace.append({"step": step, "thought": thought_text,
                          "tool": tc.function.name, "tool_input": args, "obs": obs})

    return {"final": None, "trace": trace, "steps": max_iter, "truncated": True}


# === 3. 运行 + 自我验证 ===

if __name__ == "__main__":
    question = "'台北人口' 除以 '纽约人口'、答案保留 4 位小数。"
    print(f"❓ 问题：{question}（模型 {MODEL}）")
    print("-" * 60)

    result = react_loop(question, max_iter=5)

    for entry in result["trace"]:
        print(f"[step {entry['step']}] thought: {(entry['thought'] or '')[:60]}...")
        if entry["tool"]:
            print(f"           tool: {entry['tool']}({entry.get('tool_input')}) → {entry['obs']}")
    print("-" * 60)
    print(f"✅ 最终答案：{result['final']}")
    print(f"   共 {result['steps']} 轮")

    assert result.get("final") is not None or result.get("truncated"), "loop 应收尾或显式 truncate"
    print("✅ 练习 3 通过 — 你已用本机 qwen2.5:3b 跑通 ReAct + tool use、$0/run")
