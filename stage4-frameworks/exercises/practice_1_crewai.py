# 练习 1：同一个 agent、两个 framework —— CrewAI 版
# 需要：pip install crewai
# 前置：ollama pull qwen2.5:3b && ollama serve
#
# 作业：跑完后在顶部注释回答：
# 观察1（CrewAI 的代码风格 vs LangGraph）：CrewAI的代码风格更加简短，langgraph的代码风格会图示化
# 观察2（哪个更好理解？哪个藏了更多复杂度）：这个问题体现不出哪个更好理解，但是crewai隐藏了更多复杂度
# 观察3（CrewAI 对小模型 qwen 的表现）：CrewAI 封装越黑盒，小模型出错越难排查。

import os, sys
os.environ['CREWAI_TELEMETRY_OPT_OUT'] = 'true'
os.environ['OTEL_SDK_DISABLED'] = 'true'
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from crewai import Agent, Crew, Task
from crewai.tools import tool

MODEL = os.environ.get("MODEL", "ollama/qwen2.5:3b")  # LiteLLM 格式
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")


@tool("search")
def search(query: str) -> str:
    """Search a (fake, offline) knowledge base for a topic."""
    db = {
        "taipei": "Taipei is the capital of Taiwan, population ~2.6M, known for night markets.",
        "react agent": "ReAct (Reasoning + Acting) is an agent pattern: think -> act -> observe loop.",
    }
    return db.get(query.strip().lower(), f"no entry for {query}")


def build_crew(query: str) -> Crew:
    os.environ["OPENAI_API_BASE"] = f"{OLLAMA_BASE}/v1"
    os.environ["OPENAI_API_KEY"] = "ollama"

    researcher = Agent(
        role="Researcher",
        goal="Find and summarize the requested topic.",
        backstory="You search a knowledge base and give concise summaries.",
        tools=[search],
        llm=MODEL,
        verbose=False,
    )
    task = Task(
        description=query,
        expected_output="A 1-2 sentence summary based on search results.",
        agent=researcher,
    )
    return Crew(agents=[researcher], tasks=[task], verbose=False)


def run(query: str) -> dict:
    crew = build_crew(query)
    result = crew.kickoff()
    return {"final": str(result), "steps": None}


if __name__ == "__main__":
    query = "summarize what you know about Taipei"
    print(f"❓ Query: {query}（using CrewAI + Ollama {MODEL}）")
    print("-" * 60)
    result = run(query)
    print(f"✅ Final: {result['final']}")
    assert result["final"], "expected non-empty summary"
    print("✅ CrewAI 版本通过 — 同样任务、不同 framework、$0/run")
    print("   对照 practice_1.py（LangGraph）看代码风格差异")
