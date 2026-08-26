# 练习 2：Eval（给 agent 写评估——"pytest for LLMs"）
# 需要：pip install openai；前置：ollama pull qwen2.5:7b && ollama serve
#
# 两种 evaluator：
#   1. String match：输出含关键词（简单、零成本）
#   2. LLM-as-judge：用 LLM 评分（灵活）
#
# 作业：跑完后在顶部注释回答：
# 观察1（哪些 case 挂了）：5/5 全过——数学/地理/诚实性都答对；ground_1 正确说"不知道"（不编造）
# 观察2（两种 evaluator 的差别）：字符串匹配便宜但死板（"4"和"四"算不同）；LLM裁判灵活但要花调用成本——生产通常混用
# 观察3（如果 production 没 eval 会怎样）：没 eval 的话，改坏 agent 没人知道；"肉眼看一下"不可靠，通过率下降=regression 能立刻发现

import os, sys
from typing import Any, Callable
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:7b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


# === Eval cases（评估用例） ===

EVAL_CASES = [
    {"id": "math_1", "input": "2 + 2 等于多少？", "expected_substring": "4"},
    {"id": "math_2", "input": "10 * 5 等于多少？", "expected_substring": "50"},
    {"id": "geo_1", "input": "日本的首都是哪里？", "expected_substring": "东京"},
    {"id": "geo_2", "input": "法国的首都是哪里？", "expected_substring": "巴黎"},
    {"id": "ground_1", "input": "什么是 flrgglemerk？",
     "expected_substring": "不知道", "instruction": "如果不知道就说不知道。"},
]


# === 被测 agent ===

def agent_answer(question: str, llm: Any = None, instruction: str = "") -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    system = "用中文简洁回答（1-2 句）。" + instruction
    resp = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": question}],
    )
    return resp.choices[0].message.content or ""


# === 两种 evaluator ===

def eval_substring(output: str, case: dict) -> bool:
    return case["expected_substring"].lower() in output.lower()


def eval_llm_as_judge(output: str, case: dict, judge_llm: Any = None) -> bool:
    judge_llm = judge_llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    prompt = f"""判断 AI 的回答是否正确。只回复 PASS 或 FAIL。

问题：{case['input']}
期望包含：{case['expected_substring']}
AI 回答：{output}

判定："""
    resp = judge_llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    verdict = (resp.choices[0].message.content or "").upper()
    return "PASS" in verdict and "FAIL" not in verdict


# === Eval 运行器 ===

def run_eval(cases: list[dict], agent_fn: Callable, eval_fn: Callable, **agent_kwargs) -> dict:
    results = []
    for case in cases:
        instruction = case.get("instruction", "")
        output = agent_fn(case["input"], instruction=instruction, **agent_kwargs)
        passed = eval_fn(output, case)
        results.append({"id": case["id"], "passed": passed, "output": output[:60]})
    passes = sum(1 for r in results if r["passed"])
    return {"results": results, "pass_count": passes, "total": len(results),
            "pass_rate": passes / len(results)}


if __name__ == "__main__":
    print(f"对 {len(EVAL_CASES)} 个用例跑 eval（模型 {MODEL}）...\n")

    print("=== Evaluator 1：字符串匹配 ===")
    out = run_eval(EVAL_CASES, agent_answer, eval_substring)
    for r in out["results"]:
        mark = "✅" if r["passed"] else "❌"
        print(f"   {mark} [{r['id']}] {r['output']}")
    print(f"   Pass: {out['pass_count']}/{out['total']} ({out['pass_rate']:.0%})")

    print("\n=== Evaluator 2：LLM-as-judge ===")
    out2 = run_eval(EVAL_CASES, agent_answer, eval_llm_as_judge)
    for r in out2["results"]:
        mark = "✅" if r["passed"] else "❌"
        print(f"   {mark} [{r['id']}] {r['output']}")
    print(f"   Pass: {out2['pass_count']}/{out2['total']} ({out2['pass_rate']:.0%})")

    assert out["total"] == 5
    print("\n✅ 练习 2 通过 — eval pipeline 跑通、$0/run")
    print("   观察：production 应该 pin baseline pass rate，每次 ship 前确认没 regression")
