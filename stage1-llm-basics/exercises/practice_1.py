# 练习 1：LLM API hello world（Path A — 本机 Ollama，$0）
# 需要：pip install openai（已装）
# 前置：ollama pull <MODEL> && ollama serve
#
# 作业：跑通后改 content / max_tokens / temperature 各试一次，
#       把观察写在文件顶部注释里。
# 观察1：___修改content后文本变长 token花费更多_________________________________
# 观察2：___限制max_token后文本输出不完整了 没办法完整表现__推理模型需要的max_token更多_______________________________
# 观察3：___修改temperature为1后发现结果更多变 为0时结果大致相同_________________________________

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

# 模型选择：今天先用小模型 qwen2.5:0.5b（gemma4:e4b 正在后台拉）
MODEL = "gemma4:e4b"  # gemma4:e4b 拉完后改回

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不检查、随便填
)

r = client.chat.completions.create(
    model=MODEL,
    max_tokens=1000,  # gemma4:e4b 是先思考再回答的推理模型，100 只够想不够答
    temperature=1,
    messages=[{"role": "user", "content": "简单用一句话30个字描述一下大语言模型。"}],
)

# === 自我验证 ===
text = r.choices[0].message.content
print("回应：", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"非预期 finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "回应不应为空"
assert r.usage.completion_tokens > 0, "output token 应 > 0"
print("✅ 练习 1 通过 — Ollama 已能本机回应、$0/次")
