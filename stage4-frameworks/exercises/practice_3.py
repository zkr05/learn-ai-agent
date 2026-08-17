# 练习 3：图式 workflow（LangGraph——分支 + 人类审核 + checkpoint）
# 需要：pip install langgraph；前置：ollama pull qwen2.5:3b && ollama serve
#
# 任务："研究 → 写稿 → 人类审核 → 发布"的 workflow
#  - classify 看 query 决定要不要 search（条件分支）
#  - respond 写稿
#  - 【HITL】发布前 interrupt 等人类批准（human-in-the-loop）
#  - final 根据 approved 决定 PUBLISHED / REJECTED
#
# 作业：跑完后在顶部注释回答：
# 观察1（条件分支怎么工作的）：should_search 看 needs_search（classify 检查query是否含"人口/天气"等关键词）→ 决定走search还是respond，图在classify后分叉
# 观察2（HITL 是怎么"暂停-等人-继续"的）：HITL三行——interrupt_before=["final"]暂停 → update_state改approved → invoke(None)从暂停处继续
# 观察3（checkpoint 是什么、thread_id 干嘛的）：InMemorySaver保存状态，thread_id标识"哪个对话"，所以invoke(None)能找到上次暂停的状态接着跑

import os, sys
from typing import Any, Literal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

MODEL = os.environ.get("MODEL", "qwen2.5:3b")


class State(TypedDict):
    query: str
    needs_search: bool
    search_result: str
    draft: str
    approved: bool
    final: str


# === 节点 ===

def classify_node(state: State) -> dict:
    """看 query 决定要不要 search：含"人口/天气/最新"就 search。"""
    q = state["query"].lower()
    needs = any(k in q for k in ["人口", "weather", "天气", "latest", "最新", "current"])
    return {"needs_search": needs}


def search_node(state: State) -> dict:
    db = {
        "taipei": "Taipei population ~2.6M (2024)",
        "台北": "Taipei population ~2.6M (2024)",
        "weather": "sunny 25°C",
        "天气": "sunny 25°C",
    }
    q = state["query"].lower()
    for k, v in db.items():
        if k in q:
            return {"search_result": v}
    return {"search_result": "no data"}


def respond_node(state: State) -> dict:
    if state.get("search_result"):
        return {"draft": f"Based on search: {state['search_result']}"}
    return {"draft": f"Direct answer to: {state['query']}"}


def final_node(state: State) -> dict:
    if state.get("approved"):
        return {"final": f"PUBLISHED: {state['draft']}"}
    return {"final": f"REJECTED (human said no): {state['draft']}"}


def should_search(state: State) -> Literal["search", "respond"]:
    return "search" if state["needs_search"] else "respond"


# === 构图 ===

def build_graph(checkpointer: Any = None) -> Any:
    g = StateGraph(State)
    g.add_node("classify", classify_node)
    g.add_node("search", search_node)
    g.add_node("respond", respond_node)
    g.add_node("final", final_node)

    g.add_edge(START, "classify")
    g.add_conditional_edges("classify", should_search, {"search": "search", "respond": "respond"})
    g.add_edge("search", "respond")
    g.add_edge("respond", "final")
    g.add_edge("final", END)

    # HITL：final 之前 interrupt，等人改 approved
    return g.compile(checkpointer=checkpointer, interrupt_before=["final"])


def run(query: str, approve: bool = True) -> dict:
    checkpointer = InMemorySaver()
    graph = build_graph(checkpointer=checkpointer)
    config = {"configurable": {"thread_id": "demo"}}

    state_before = graph.invoke({"query": query, "approved": False}, config=config)
    print(f"   draft（等待 approval）: {state_before.get('draft', '<none>')}")

    graph.update_state(config, {"approved": approve})   # HITL：人类审核

    state_after = graph.invoke(None, config=config)     # 继续跑完
    return state_after


if __name__ == "__main__":
    print(f"❓ Workflow: classify → [search?] → respond → [HITL] → final（using {MODEL}）")
    print("-" * 60)

    print("\n[Case 1] query 含「台北人口」→ 需要 search → 人类 approve=True")
    r1 = run("台北人口是多少？", approve=True)
    print(f"   final: {r1['final']}")
    assert "PUBLISHED" in r1["final"]

    print("\n[Case 2] query 不需要 search → 人类 approve=False")
    r2 = run("解释一下 Python 是什么", approve=False)
    print(f"   final: {r2['final']}")
    assert "REJECTED" in r2["final"]

    print("\n✅ 练习 3 通过 — LangGraph 图式 workflow + HITL checkpoint、$0/run")
