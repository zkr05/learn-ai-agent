# 练习 1：同一个 agent、两个 framework —— LangGraph 版
# 需要：pip install langgraph langchain-openai langchain-core
# 前置：ollama pull qwen2.5:3b && ollama serve
#
# 任务：搜索 + 摘要的小 agent（fake 知识库）。
# 作业：跑完后在顶部注释回答：
# 观察1（LangGraph 的代码风格）：LangGraph的代码风格是偏向于图表类型
# 观察2（跟手写 ReAct 比，它替你做了什么）：它让流程更加图示化了
# 观察3（debug 体验怎么样）：debug好修，能容易定位到问题的出处
import os, sys
from typing import Any
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

MODEL = os.environ.get("MODEL", "qwen2.5:3b")


@tool
def search(query: str) -> str:
    """Search a (fake, offline) knowledge base for a topic."""
    db = {
        "taipei": "Taipei is the capital of Taiwan, population ~2.6M, known for night markets.",
        "react agent": "ReAct (Reasoning + Acting) is an agent pattern: think -> act -> observe loop.",
    }
    return db.get(query.strip().lower(), f"no entry for {query}")


# LangGraph 的"状态"：消息列表
class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph(llm: Any) -> Any:
    llm_with_tools = llm.bind_tools([search])

    def agent_node(state: State):      # 节点 1：LLM 决定调不调工具
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    def tool_node(state: State):       # 节点 2：执行工具
        msg = state["messages"][-1]
        results = []
        for call in msg.tool_calls:
            obs = search.invoke(call["args"])
            results.append(ToolMessage(content=obs, tool_call_id=call["id"]))
        return {"messages": results}

    def should_continue(state: State) -> str:   # 条件边：有工具调用就回 agent，否则结束
        return "tools" if state["messages"][-1].tool_calls else END

    g = StateGraph(State)
    g.add_node("agent", agent_node)
    g.add_node("tools", tool_node)
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")
    return g.compile()


def run(query: str, llm: Any = None) -> dict:
    llm = llm or ChatOpenAI(
        base_url="http://localhost:11434/v1", api_key="ollama",
        model=MODEL, temperature=0,
    )
    graph = build_graph(llm)
    final_state = graph.invoke({"messages": [HumanMessage(content=query)]})
    return {"final": final_state["messages"][-1].content,
            "steps": len(final_state["messages"])}


if __name__ == "__main__":
    query = "summarize what you know about Taipei"
    print(f"❓ Query: {query}（using Ollama {MODEL}）")
    print("-" * 60)
    result = run(query)
    print(f"✅ Final: {result['final']}")
    print(f"   Steps: {result['steps']}")
    assert result["final"], "expected non-empty summary"
    print("✅ 练习 1 通过 — LangGraph + Ollama qwen2.5:3b、$0/run")
