## 任务 3：动手（30 分）——从零做一个 agent

#用 **LangGraph 或 CrewAI** 写一个**你自己设计**的小 agent（不许复制练习 1/2/3 的工具和任务）：
#- 自己发明一个工具（比如查书价、算折扣、查城市时差……）+ schema
#- 一个能触发它的任务
#- 跑通并给出正确结果

import os, sys
os.environ['CREWAI_TELEMETRY_OPT_OUT'] = 'true'
os.environ['OTEL_SDK_DISABLED'] = 'true'
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from crewai import Agent, Crew, Task
from crewai.tools import tool

MODEL = os.environ.get("MODEL", "ollama/qwen2.5:7b")  # LiteLLM 格式
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")


@tool("book_price")
def book_price(title: str) -> str:
    """查询一本书的价格。"""
    price = {"python入门":"¥59","算法导论":"¥99"}
    return price.get(title.strip().lower(),f"没有这本书{title}")

def build_crew(query:str) -> Crew:
    os.environ["OPENAI_API_BASE"] = f"{OLLAMA_BASE}/v1"
    os.environ["OPENAI_API_KEY"] = "ollama"

    researcher = Agent(
        role="Researcher",
        goal="找到书的价格",
        backstory="根据已有的价格查询",
        tools = [book_price],
        llm = MODEL,
        verbose=False,
    )
    task = Task(
        description=query,
        expected_output = "直接给出对应书名和价格。",
        agent=researcher,
    )
    return Crew(agents=[researcher],tasks=[task],verbose=False)

def run(query:str) -> dict:
    crew = build_crew(query)
    result = crew.kickoff()
    return {"final":str(result),"steps":None}

if __name__ == "__main__":
    query = "查询python入门和高等数学的书价。"
    print(f"❓ Query: {query}（using CrewAI + Ollama {MODEL}）")
    print("-" * 60)
    result = run(query)
    print(f"✅ Final: {result['final']}")