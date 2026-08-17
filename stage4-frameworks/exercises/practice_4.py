# 练习 4：CodeAct vs JSON tool（Smolagents）
# 需要：pip install smolagents；前置：ollama pull qwen2.5:3b && ollama serve
#
# CodeAct pattern：agent 写【Python 代码】当 action（不是 JSON tool call）
#   - JSON tool（练习1/3）：LLM 回 {"name": "calculator", "arguments": {...}}
#   - CodeAct（本练习）：  LLM 回 ```python result = calculator(...) ``` 然后框架执行代码
#
# 作业：跑完后在顶部注释回答：
# 观察1（agent 怎么"写代码"调用工具的）：CodeAct让模型直接写Python代码调工具(lookup_fact→calculator)，框架执行并回传结果——2步完成
# 观察2（跟 JSON tool 路线比，输出长什么样）：CodeAct输出是代码(result=calculator(...))，JSON tool输出是结构化JSON——代码更灵活但对模型要求高
# 观察3（qwen 小模型写代码稳吗）：3b写错工具名失败；7b代码写对但工具只认英文查不到→加中文别名后正确(0.3121)——模型大小+工具设计都重要

import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from smolagents import CodeAgent, OpenAIServerModel, tool

MODEL = os.environ.get("MODEL", "qwen2.5:7b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


@tool
def calculator(expression: str) -> str:
    """Safe arithmetic calculator (whitelist + - * / parentheses).

    Args:
        expression: Arithmetic expression to evaluate, e.g. '2 + 3 * (4 - 1)'.
    """
    allowed = set("0123456789.+-*/() ")
    if any(c not in allowed for c in expression):
        return "error: only basic arithmetic allowed"
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"error: {e}"


@tool
def lookup_fact(query: str) -> str:
    """Look up a fact (population / physical constants, etc.).

    Args:
        query: Fact key to look up, e.g. 'taipei population' or 'speed of light'.
    """
    db = {
        "taipei population": "2602000", "taipei": "2602000", "台北人口": "2602000", "台北": "2602000",
        "new york population": "8336000", "new york": "8336000", "纽约人口": "8336000", "纽约": "8336000",
        "speed of light": "299792458",
    }
    return db.get(query.strip().lower(), f"unknown: {query}")


def build_agent(model=None) -> CodeAgent:
    model = model or OpenAIServerModel(
        model_id=MODEL, api_base=OLLAMA_BASE, api_key="ollama",
    )
    return CodeAgent(tools=[calculator, lookup_fact], model=model, max_steps=4)


def run(question: str, model=None) -> dict:
    agent = build_agent(model=model)
    result = agent.run(question)
    return {"final": str(result)}


if __name__ == "__main__":
    question = "先用 lookup_fact 查台北人口和纽约人口，再用 calculator 计算台北人口除以纽约人口的结果，必须给出最终数字。"
    print(f"❓ Question: {question}（Smolagents CodeAct + Ollama {MODEL}）")
    print("-" * 60)
    result = run(question)
    print(f"✅ Final: {result['final']}")
    assert result["final"], "expected non-empty result"
    print("\n✅ 练习 4 通过 — CodeAct agent 跑完、$0/run")
