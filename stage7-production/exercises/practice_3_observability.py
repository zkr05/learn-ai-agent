# 练习 3：Observability（让 agent 的每一步"看得见"）
# 需要：pip install openai；前置：ollama pull qwen2.5:7b && ollama serve
#
# Production agent 必备 4 个 telemetry：
#   1. Latency（每次调用多久）
#   2. Token usage（花了多少 token → 成本）
#   3. Trace（多步 agent 的每一步）
#   4. Errors（异常 + 重试次数）
#
# 作业：跑完后在顶部注释回答：
# 观察1（trace summary 里有哪些指标）：trace summary 有 request_id/总耗时/span数/token数/错误数——每一步的耗时、成本、错误都能看到
# 观察2（如果没 observability，agent 出问题怎么查）：没 observability 的话，agent 出问题只能瞎猜（黑盒）——不知道卡在哪步、花了多少
# 观察3（这个跟 Stage 5 的 notify/hooks 什么关系）：这跟 Stage 5 的 notify/hooks 都是 harness 的 telemetry 元件——让 agent 运行可观测

import json, logging, os, sys, time
from contextlib import contextmanager
from typing import Any
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

MODEL = os.environ.get("MODEL", "qwen2.5:7b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("agent.observability")


# === 4 个 telemetry 原语 ===

class TraceContext:
    """每个请求的 trace 上下文（生产用 OpenTelemetry）。"""

    def __init__(self, request_id: str):
        self.request_id = request_id
        self.spans: list[dict] = []
        self.total_tokens = {"input": 0, "output": 0}
        self.errors: list[str] = []

    def add_span(self, name: str, latency_ms: float, **extras):
        span = {"name": name, "latency_ms": latency_ms, **extras}
        self.spans.append(span)
        logger.info(f"[{self.request_id}] span={name} ms={latency_ms:.1f} {json.dumps(extras)}")

    def add_tokens(self, input_t: int, output_t: int):
        self.total_tokens["input"] += input_t
        self.total_tokens["output"] += output_t

    def add_error(self, msg: str):
        self.errors.append(msg)
        logger.error(f"[{self.request_id}] error={msg}")

    def summary(self) -> dict:
        total_ms = sum(s["latency_ms"] for s in self.spans)
        return {
            "request_id": self.request_id,
            "total_latency_ms": total_ms,
            "span_count": len(self.spans),
            "input_tokens": self.total_tokens["input"],
            "output_tokens": self.total_tokens["output"],
            "error_count": len(self.errors),
        }


@contextmanager
def trace_span(ctx: TraceContext, name: str, **extras):
    """计时 + 记录 span（出错也会记 error）。"""
    t0 = time.perf_counter()
    err = None
    try:
        yield
    except Exception as e:
        err = str(e)
        ctx.add_error(f"{name}: {err}")
        raise
    finally:
        latency_ms = (time.perf_counter() - t0) * 1000
        ctx.add_span(name, latency_ms, error=err, **extras)


# === 插桩后的 agent ===

def observable_agent(question: str, ctx: TraceContext, llm: Any = None) -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")

    with trace_span(ctx, "llm_call", model=MODEL):
        resp = llm.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": question}],
        )

    usage = getattr(resp, "usage", None)
    if usage:
        ctx.add_tokens(
            input_t=getattr(usage, "prompt_tokens", 0),
            output_t=getattr(usage, "completion_tokens", 0),
        )

    return resp.choices[0].message.content or ""


def multi_step_agent(question: str, llm: Any = None) -> dict:
    """模拟 multi-step agent：search → reason → answer，每步都有 trace。"""
    ctx = TraceContext(request_id=f"req_{int(time.time()*1000)}")

    with trace_span(ctx, "search"):
        time.sleep(0.05)  # 模拟工具调用延迟
        search_result = "Fake search result for: " + question

    answer = observable_agent(f"Based on '{search_result}', answer: {question}", ctx, llm=llm)

    return {"answer": answer, "trace_summary": ctx.summary(), "spans": ctx.spans}


if __name__ == "__main__":
    print("运行插桩后的 agent...\n")
    result = multi_step_agent("2 + 2 等于多少？")
    print(f"\n📊 Trace summary:")
    for k, v in result["trace_summary"].items():
        print(f"   {k}: {v}")
    print(f"\n📝 Spans:")
    for s in result["spans"]:
        print(f"   {s['name']}: {s['latency_ms']:.1f}ms")

    assert result["trace_summary"]["span_count"] >= 2  # search + llm_call
    print(f"\n✅ 练习 3 通过 — 观察 4 个 telemetry primitive、$0/run")
