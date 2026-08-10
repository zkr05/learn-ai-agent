# Stage 1 — LLM 基础（LLM Basics）

内容整理自 awesome-agentic-ai-zh 的 [stages/01-llm-basics.zh-Hans.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/stages/01-llm-basics.zh-Hans.md)。

## 完成本阶段后，你应该能做到

- 解释 LLM、token、context window、temperature 等核心概念
- 用 Python 调用 LLM API（本机 Ollama 为主，可选 Anthropic）
- 比较不同 LLM 提供商（Claude / GPT / Gemini / Llama / 中文模型）
- 理解 per-token 定价模型并估算成本

## 如果下面这些你都会，可以直接跳到 Stage 2

- 写一个 5 行的 Python 脚本调用 LLM API
- 说出至少 2 个 token 例子（例如 "Hello" 是 1 个 token）
- 比较 Claude Sonnet vs Opus 的 per-token 价格
- 体验至少 2 个不同的 LLM

## 一周计划（每天约 1 小时，共 5-8 小时）

```text
第 1 天：核心概念（token / context window / temperature）+ 环境搭建 + 练习 1 hello world
第 2 天：练习 2 — tokens：跑 20 次观察输出长度波动、中英文 token 数差异
第 3 天：练习 3 — pricing / latency：算 1000 次调用的成本与耗时
第 4 天：练习 4 — cross-provider：对比不同模型对同一 prompt 的回答
第 5 天：练习 5 — error handling：错误触发 + exponential backoff retry
第 6 天：练习 6 — local LLM 收尾 + Stage 1 自我检查
```

## 学习进度

- 第 1 天（2026-08-07）✅：环境搭好（Ollama 0.32.6 + gemma4:e4b + qwen2.5:0.5b），练习 1 跑通并提交
  - 坑：gemma4:e4b 是推理模型，max_tokens 要 500 以上，100 会被思考吃光导致 content 为空
- 第 2 天（2026-08-10）✅：练习 2 tokens 实验——N=10 vs N=3 的 stdev 对比（样本量影响极值）
- 第 3 天（2026-08-10）✅：练习 3 定价/延迟——本机 1000 次 ## 学习进度 但 90 分钟 vs 云端 haiku ## 学习进度.25
- 第 4 天（2026-08-10）✅：练习 4 跨模型对比——8B 正确解释 Agent，0.5B 理解成"代理商"
- 第 5 天（2026-08-10）✅：练习 5 错误处理——exponential backoff retry 包装器
- 第 6 天（2026-08-10）✅：练习 6 本地 LLM 对比——8B 解释 ReAct 正确，0.5B 编造"Reactor"假库
- **Stage 1 自检通过（2026-08-10）→ 可进 Stage 2（Prompt Engineering）**

- 第 1 天（2026-08-07）✅：环境搭好（Ollama 0.32.6 + gemma4:e4b + qwen2.5:0.5b），练习 1 跑通并提交
  - 坑：gemma4:e4b 是推理模型，max_tokens 要 500 以上，100 会被思考吃光导致 content 为空
- 第 2 天（进行中）：练习 2 tokens 实验，`practice_2.py` 已就绪（N=10 全跑约 3-5 分钟）

## 6 个动手练习

| # | 文件 | 内容 |
|---|------|------|
| 1 | `exercises/practice_1.py` | 5 行代码调用 LLM，打印响应和 token 用量 |
| 2 | `exercises/practice_2.py` | 同一 prompt 跑 20 次，统计输出 token 波动 |
| 3 | `exercises/practice_3.py` | 测 latency、估算 1000 次调用成本 |
| 4 | `exercises/practice_4.py` | 同 prompt 对比多个模型的回答 |
| 5 | `exercises/practice_5.py` | 故意触发错误，写 retry 包装 |
| 6 | `exercises/practice_6.py` | 本机小模型（qwen2.5:3b）跑本地 LLM |

## 环境（第 1 天装好）

- Python 包：`pip install openai`（OpenAI 兼容 SDK，用来跟 Ollama 通信）✅ 已装
- Ollama：本机 LLM 运行时，下载模型后全程 $0
- 模型：`ollama pull gemma4:e4b`（~7.5 GB，第 1 天装）+ `ollama pull qwen2.5:3b`（第 6 天用）
- 可选：Anthropic API key（想看云端高质量回答时用，Path B）

## 关键名词速查

| 词 | 中文 | 一句话 |
|---|---|---|
| token | 词元 | 模型计算文字长度与费用的基本单位（中文 1 字 ≈ 1.5-2 token） |
| context window | 上下文窗口 | 模型一次能"看到"多少 token（Claude 1M / GPT 1.05M / Gemini 2M） |
| temperature | 随机程度 | 0 = 稳定可复现，1 = 更有创意；分类用 0.0-0.3，创作用 0.7-1.0 |
| max_tokens | 输出上限 | 最多采样多少次就停 |

## 使用说明

每天先看 `notes/day1-lesson.md`（或对应练习），把练习文件复制到
`C:\Users\admin\learn-py\stage1\exercises\` 下自己写，写完用 git 提交一次
（延续 Stage 0 的习惯）。

```powershell
cd C:\Users\admin\Documents\Codex\agent-learning\stage1\exercises
python practice_1.py
```
