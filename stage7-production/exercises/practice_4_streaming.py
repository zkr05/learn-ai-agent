# 练习 4：SDK 进阶（Streaming 流式输出）
# 需要：pip install openai；前置：ollama pull qwen2.5:7b && ollama serve
#
# Production 两个必备 SDK 进阶 feature：
#   1. Streaming：边生成边输出（用户体验：5秒→0.5秒就看到字）
#   2. Prompt caching：重复长上下文省 90% 成本（Anthropic 专属，本地只学概念）
#
# 作业：跑完后在顶部注释回答：
# 观察1（first_token 和 total 差多少）：first_token 39ms vs total 1014ms——差 25 倍；用户体验由"首个token"决定（39ms=秒回）
# 观察2（streaming 为什么让"感觉"更快）：streaming 边生成边输出(stream=True)，不用等全部生成完，用户看着字一个个出来，感觉快
# 观察3（prompt caching 为什么能省 90%）：prompt caching——重复的长上下文前缀被缓存，第二次调用同一前缀省 90% 输入成本（Anthropic 专属，本地无）

import os, sys, time
from typing import Any, Iterator
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:7b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")


def stream_response(prompt: str, llm: Any = None) -> Iterator[str]:
    """流式：每来一个 token 就 yield 出去。"""
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    stream = llm.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,          # ← 关键：流式
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def stream_to_string(prompt: str, llm: Any = None) -> dict:
    """消费流式生成器 + 统计延迟。"""
    t0 = time.perf_counter()
    first_token_at = None
    chunks = []
    for delta in stream_response(prompt, llm=llm):
        if first_token_at is None:
            first_token_at = time.perf_counter() - t0
        chunks.append(delta)
    total_latency = time.perf_counter() - t0
    return {
        "text": "".join(chunks),
        "first_token_ms": (first_token_at or 0) * 1000,
        "total_latency_ms": total_latency * 1000,
        "chunk_count": len(chunks),
    }


if __name__ == "__main__":
    prompt = "用 3 句话解释什么是 Python 列表推导式。"
    print(f"❓ {prompt}\n")
    print("(流式输出，一个字一个字出现...)\n")

    t0 = time.perf_counter()
    for delta in stream_response(prompt):
        print(delta, end="", flush=True)
    total = time.perf_counter() - t0
    print(f"\n\n⏱ 流式总耗时: {total*1000:.0f}ms")

    print("\n=== 统计数据 ===")
    info = stream_to_string(prompt)
    print(f"   首个 token: {info['first_token_ms']:.0f}ms（用户体验的关键）")
    print(f"   总耗时:     {info['total_latency_ms']:.0f}ms")
    print(f"   chunk 数:   {info['chunk_count']}")

    print("\n💡 Prompt caching 概念（Anthropic 专属）:")
    print("   重复的长上下文会被缓存——第二次调用同一前缀省 90% 输入成本")
    print("   Ollama 本地无此功能，概念先记下，云端 API 才有")
    print("\n✅ 练习 4 通过 — streaming + 统计、$0/run")
