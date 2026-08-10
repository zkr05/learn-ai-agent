# 练习 5：Error Handling（错误触发 + retry 包装）
# 完整版见 awesome-agentic-ai-zh/examples/stage-1/05-error-handling/
# 本文件是精简版：核心是 with_retry 这个 exponential backoff 包装器。
#
# 作业：
# 1）跑通 retry 演示（模拟 2 次失败后成功）
# 2）把 MAX_ATTEMPTS 改成 1，看它失败后直接 raise
# 3）回答：为什么 AuthenticationError 不应该 retry？
# 观察1：____________________________________
# 观察2：____________________________________
# 观察3：____________________________________

import random, sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import APIConnectionError, RateLimitError, OpenAI

RETRIABLE = (APIConnectionError, RateLimitError)
MAX_ATTEMPTS = 4
BASE_DELAY = 0.5  # 秒

def with_retry(fn, max_attempts=MAX_ATTEMPTS, base_delay=BASE_DELAY):
    """指数退避重试：可重试错误 → 等 base*2^n 秒再试；其他错误直接抛。"""
    last_exc = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except RETRIABLE as e:
            last_exc = e
            if attempt == max_attempts - 1:
                break
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.2)
            print(f"  ⚠ 第 {attempt+1}/{max_attempts} 次失败 ({type(e).__name__})，{delay:.1f}s 后重试")
            time.sleep(delay)
    raise last_exc

# === 演示：模拟一个"前 2 次网络错误、第 3 次成功"的调用 ===
attempts = {"n": 0}
def flaky_call():
    attempts["n"] += 1
    if attempts["n"] <= 2:
        raise APIConnectionError(request=None, message="simulated network drop")
    return "ok: 第 3 次成功了"

result = with_retry(flaky_call)
print("结果:", result)

# === 真实调用（如果 Ollama 在跑） ===
# client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# r = with_retry(lambda: client.chat.completions.create(
#     model="gemma4:e4b", max_tokens=20,
#     messages=[{"role": "user", "content": "hi"}]))
# print(r.choices[0].message.content)

# === 自我验证 ===
assert result == "ok: 第 3 次成功了", "retry 应该最终成功"
print("\n✅ 练习 5 通过 — retry 包装器能处理 transient 错误")
print("💡 400/401 这种“用户错误”不该 retry；429/网络错误才该 retry")
