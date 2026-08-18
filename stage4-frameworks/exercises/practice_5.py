# 练习 5：类型安全 agent（Pydantic AI）
# 需要：pip install pydantic-ai；前置：ollama pull qwen2.5:7b && ollama serve
#
# 核心：用 Pydantic model 强制 agent 返回结构化输出，运行时自动校验类型。
# 模型如果返回 confidence="高"（字符串）→ 校验失败 → 自动 retry 直到合法。
#
# 作业：跑完后在顶部注释回答：
# 观察1（agent 返回的结构是什么）：agent必须返回 {answer:str, confidence:float(0-1), sources:list[str]}——类型不符会被校验打回
# 观察2（类型校验怎么防"偷懒/编结构"）：校验失败自动重试(retries=5)，我遇到过一次连续5次失败(UnexpectedModelBehavior)——qwen小模型对structured output不稳定
# 观察3（换个题目，看 confidence 和 sources 怎么变）：换问题跑，confidence/sources会跟着变；模型知道就说高、不知道会说低并解释

import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

MODEL = os.environ.get("MODEL", "qwen2.5:7b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


# === Schema：agent 强制要回这个 shape ===

class AnswerWithConfidence(BaseModel):
    """Structured answer the agent must produce."""
    answer: str = Field(description="The actual answer text.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score 0-1.")
    sources: list[str] = Field(description="Sources or references used.")


def build_agent(model=None) -> Agent:
    if model is None:
        model = OpenAIChatModel(
            MODEL,
            provider=OpenAIProvider(base_url=OLLAMA_BASE, api_key="ollama"),
        )
    return Agent(
        model=model,
        output_type=AnswerWithConfidence,
        retries=5,
        system_prompt=(
            "You answer questions. ALWAYS return a structured answer with "
            "an 'answer' text, a 'confidence' float (0.0 to 1.0), and a list of 'sources'. "
            "If you don't know, set confidence low and explain in answer."
        ),
    )


def run(question: str, model=None) -> AnswerWithConfidence:
    agent = build_agent(model=model)
    result = agent.run_sync(question)
    return result.output


if __name__ == "__main__":
    question = "What is the population of Taipei?"
    print(f"❓ Q: {question}（using Pydantic AI + Ollama {MODEL}）")
    print("-" * 60)
    answer = run(question)
    print(f"  answer:     {answer.answer}")
    print(f"  confidence: {answer.confidence}")
    print(f"  sources:    {answer.sources}")

    # 类型校验：confidence 必须是 0-1 的 float，sources 必须是 list[str]
    assert isinstance(answer.confidence, float) and 0.0 <= answer.confidence <= 1.0
    assert isinstance(answer.sources, list)
    print("\n✅ 练习 5 通过 — Pydantic AI 结构化输出 + 类型校验、$0/run")
