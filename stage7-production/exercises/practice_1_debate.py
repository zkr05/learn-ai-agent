# 练习 1：Multi-Agent 辩论（PRO / CON / Judge）
# 需要：pip install openai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 3 个 agent：正方 / 反方 / 裁判。目的：降低单一 LLM 的 bias（production 高赌注决策常用）。
#
# 作业：跑完后在顶部注释回答：
# 观察1（双方论点质量）：3b——PRO/CON 都没守住立场，CON 甚至站错边；7b——PRO 清晰，CON 仍偏框架
# 观察2（裁判怎么判的）：裁判——3b 奖励了站错边的，7b 判断清晰
# 观察3（多跑几次，裁判会不会变）：模型大小影响辩论质量——7b 明显比 3b 稳，但"反方"对 7b 也难（常识偏向框架）

import os, sys
from typing import Any
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:7b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


def llm_call(system: str, user: str, llm: Any = None) -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    resp = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return resp.choices[0].message.content or ""


def debate(question: str, llm: Any = None) -> dict:
    pro_argument = llm_call(
        system="You argue the PRO position on the user's question. Be concise (2-3 sentences).",
        user=question, llm=llm,
    )
    con_argument = llm_call(
        system="You argue the CON position on the user's question. Be concise (2-3 sentences).",
        user=question, llm=llm,
    )
    judge_verdict = llm_call(
        system="You are a neutral judge. Read both arguments below and pick the stronger one. "
               "Reply with: WINNER=PRO or WINNER=CON, then 1-sentence reasoning.",
        user=f"Question: {question}\n\nPRO: {pro_argument}\n\nCON: {con_argument}",
        llm=llm,
    )
    return {"question": question, "pro": pro_argument, "con": con_argument, "judge": judge_verdict}


if __name__ == "__main__":
    q = "小团队应该用框架（LangGraph/CrewAI）还是从零写 agent？"
    print(f"❓ 问题：{q}\n")
    result = debate(q)
    print(f"PRO（正方）：\n{result['pro']}\n")
    print(f"CON（反方）：\n{result['con']}\n")
    print(f"Judge（裁判）：\n{result['judge']}")
    assert "WINNER" in result["judge"].upper()
    print("\n✅ 练习 1 通过 — 3-agent debate 跑通、$0/run")
