# 练习 2：多 agent 角色分配（CrewAI 3-agent 流水线）
# 需要：pip install crewai；前置：ollama pull qwen2.5:3b && ollama serve
#
# 3 个 agent 各有角色：
# - Researcher 查资料（用 search 工具）
# - Writer 写稿（拿 researcher 的结果写 blog）
# - Critic 审稿（检查 factual + tone）
#
# 作业：跑完后在顶部注释回答：
# 观察1（每个 agent 的产出是什么）：Researcher查到ReAct原始资料→Writer写了带夸大的初稿→Critic逐条挑出5个问题(夸大/归因/loop描述不符/无证据)
# 观察2（sequential 流程怎么交接的）：context=[research_task]让Writer拿到研究结果；critic的context同时含research+write才能核对
# 观察3（跟 single agent 比，多 agent 的代价/收益）：代价=3次独立LLM调用(token≈3x)；收益=Critic能独立挑错，防止同一个模型自我辩护

import os, sys
os.environ['CREWAI_TELEMETRY_OPT_OUT'] = 'true'
os.environ['OTEL_SDK_DISABLED'] = 'true'
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from crewai import Agent, Crew, Process, Task
from crewai.tools import tool

MODEL = os.environ.get("MODEL", "ollama/qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")


@tool("search")
def search(query: str) -> str:
    """Search a (fake, offline) knowledge base."""
    db = {
        "react": "ReAct (Reasoning+Acting, Yao et al. 2022) is the foundational agent pattern: think→act→observe loop.",
        "langgraph": "LangGraph is a graph-based agent orchestration framework by LangChain, focuses on state + checkpointing.",
        "crewai": "CrewAI is a role-based multi-agent framework — define Agent/Task/Crew, run with kickoff().",
    }
    return db.get(query.strip().lower(), f"no entry for {query}")


def build_crew(topic: str, llm_model: str = MODEL) -> Crew:
    os.environ["OPENAI_API_BASE"] = f"{OLLAMA_BASE}/v1"
    os.environ["OPENAI_API_KEY"] = "ollama"

    researcher = Agent(
        role="Researcher",
        goal=f"Find concise factual info about {topic} from the knowledge base.",
        backstory="You search a knowledge base and return raw factual entries.",
        tools=[search],
        llm=llm_model,
        verbose=True,
        allow_delegation=False,
    )
    writer = Agent(
        role="Writer",
        goal=f"Write a 2-sentence blog intro about {topic}.",
        backstory="You take the researcher's findings and write engaging blog copy.",
        llm=llm_model,
        verbose=True,
        allow_delegation=False,
    )
    critic = Agent(
        role="Critic",
        goal="Verify the writer's blog intro is factually grounded in the researcher's data + check tone.",
        backstory="You're a strict editor who flags hallucinations and tone issues.",
        llm=llm_model,
        verbose=True,
        allow_delegation=False,
    )

    research_task = Task(
        description=f"Search for `{topic}` and report what you find.",
        expected_output="A 1-2 sentence factual entry from the knowledge base.",
        agent=researcher,
    )
    write_task = Task(
        description="Write a 2-sentence blog intro using the researcher's findings.",
        expected_output="A 2-sentence intro paragraph.",
        agent=writer,
        context=[research_task],
    )
    critic_task = Task(
        description="Check if the writer's intro is factually grounded in the researcher's data. "
                    "Report PASS or list issues.",
        expected_output="Either 'PASS: [intro]' or 'ISSUES: [list]'.",
        agent=critic,
        context=[research_task, write_task],
    )

    return Crew(
        agents=[researcher, writer, critic],
        tasks=[research_task, write_task, critic_task],
        process=Process.sequential,
        verbose=True,
    )


def run(topic: str, llm_model: str = MODEL) -> dict:
    crew = build_crew(topic, llm_model=llm_model)
    result = crew.kickoff()
    return {"final": str(result), "topic": topic}


if __name__ == "__main__":
    topic = "react"
    print(f"❓ Topic: {topic}（using CrewAI + Ollama {MODEL}）")
    print(f"   3 agents: Researcher → Writer → Critic（sequential）")
    print("-" * 60)
    result = run(topic)
    print(f"✅ Final (critic's verdict):\n{result['final']}")
    assert result["final"], "expected critic to produce a verdict"
    print("\n✅ 练习 2 通过 — 3-agent crew 跑完、$0/run")
