# 第 1 天：核心概念 + 环境搭建 + 练习 1（LLM hello world）

> 对应 awesome-agentic-ai-zh Stage 1（01-llm-basics.zh-Hans.md）。
> 学习方式：先读概念 → 装环境 → 复制练习代码自己跑 → 改参数观察变化。

## 0. Stage 1 要学什么

Stage 0 我们学会了"让 Python 去请求 API、处理 JSON、写 YAML"。Stage 1 开始进入 AI 本身：
第一次真正调用一个 LLM，并且搞懂三个贯穿所有后续阶段的核心词：

**token / context window / temperature**

学完这 6 天，你就能回答：
- "为什么中文比英文贵/慢？"（token 化）
- "为什么模型有时候胡说八道？"（temperature 采样）
- "为什么长对话会突然忘掉开头？"（context window 上限）
- "跑 1000 次调用要花多少钱？"（per-token 计价）

## 1. 三个核心概念

### token（词元）——LLM 计数的单位

LLM 不是按"字"或"字符"理解文字的，而是把文字切成 **token**（词元），
这是它计算长度、计费、判断"能看多少"的基本单位。

```text
"Hello, world!"  → 大约 3 个 token：["Hello", ",", " world!"]
"你好，世界"     → 大约 6-8 个 token（中文 1 个字 ≈ 1.5-2 token）
```

为什么中文更费 token？因为 tokenizer（分词器）是按常见字节/子词组合切分的，
英文单词重复率高、一个词一个 token；中文每个字都不同，很难压进一个 token。

> 验证方法（练习 2 会做）：同一个意思的中英文 prompt，看 `usage.prompt_tokens`，
> 中文通常明显更多。

### context window（上下文窗口）——模型一次能看多少

模型每次回答能"参考"的输入总量有上限，叫 context window：

| 模型 | context window | 大约能装 |
|---|---|---|
| Claude 旗舰 | 1M token | ~75 万中文字 |
| GPT 旗舰 | 1.05M token | ~80 万中文字 |
| Gemini 旗舰 | 2M token | ~150 万中文字 |
| 本机小模型（gemma4:e4b） | 通常 128k-256k | 少很多但够练习用 |

**超了会怎样？** 报错（练习 5 会故意触发），或者模型"忘了"对话开头。
所以长文档场景才需要 Gemini 那种超大窗口，日常聊天 128k 都绰绰有余。

### temperature（随机程度）——为什么同一个问题答案不一样

LLM 的核心动作是：**预测下一个 token**。它对"下一个字"算出一个概率分布，
然后从这个分布里**采样**一个。temperature 控制的是怎么采样：

- `temperature=0`：几乎永远选概率最高的那个 → 稳定、可复现、适合分类/提取
- `temperature=1`：更敢选概率低一点的冷门字 → 有创意、但容易跑题
- 建议：分类任务 0.0-0.3，写作/头脑风暴 0.7-1.0

```text
temperature 低 → 分布变"尖" → 每次都选最可能的 → 答案稳定
temperature 高 → 分布变"平" → 偶尔挑冷门的 → 答案多变
```

配套参数 `max_tokens`：最多采样几次就停，也就是输出长度上限。

## 2. 装环境（今天一次性搞定）

我们的路线（Path A，默认）：**Ollama 本机跑，$0/次**。
Stage 1 有 6 个练习要跑很多次，本机跑不花钱、还能离线。

```powershell
# 1. Python 包（用 OpenAI 兼容 SDK 跟 Ollama 通信）—— 今天已装好
python -m pip install openai

# 2. 装 Ollama —— 今天已装好
#    下载地址 https://ollama.com ，装完 Ollama 会自动在后台启动服务

# 3. 拉模型（约 7.5 GB，下载一次以后都能用）
ollama pull gemma4:e4b

# 4. 确认服务在跑（能看到 http://127.0.0.1:11434 之类的输出就行）
ollama serve
```

> 想对比云端高质量回答时，可以用 Path B（Anthropic，需要 API key，约 $0.001/次）。
> 今天先不用，把本机跑通最重要。

## 3. 练习 1：LLM hello world（你的第一个 AI 调用）

复制 `exercises/practice_1.py` 到 `C:\Users\admin\learn-py\stage1\exercises\`
然后运行。代码就 5 行核心逻辑，逐行拆解：

```python
from openai import OpenAI  # OpenAI 官方 SDK（Ollama 也兼容这个协议）

client = OpenAI(
    base_url="http://localhost:11434/v1",  # 指向本机 Ollama 的服务
    api_key="ollama",                       # Ollama 不校验 key，随便填
)

r = client.chat.completions.create(
    model="gemma4:e4b",                     # 用哪个模型（已 pull 的本机模型）
    max_tokens=100,                         # 输出最多 100 个 token
    messages=[{"role": "user", "content": "用一句话自我介绍。"}],
)
```

三个"第一次"：
- 第一次看到 `base_url` 指向 `localhost`——以前调 GitHub 都是公网，现在模型就在自己电脑上
- 第一次看到 `messages` 是"对话数组"——每个元素有 `role`（`user`/`assistant`）和 `content`
- 第一次看到响应里的 `usage`——它会告诉你这次调用花了多少 token

运行成功后你应该看到：

```text
回应： 我是 Gemma，一个由 Google 开发的开源 AI 助手……
usage: CompletionUsage(completion_tokens=xx, prompt_tokens=xx, total_tokens=xx)
✅ 练习 1 通过 — Ollama gemma4:e4b 已能本机回应、$0/次
```

## 4. 今天的作业（做完在 learn-py 里 git 提交一次）

1. 跑通 `practice_1.py`，确认 ✅ 输出
2. 改三处，观察变化：
   - 把 `content` 换成别的问法（比如"用 3 句话介绍你自己"）
   - 把 `max_tokens` 改成 `10`，看输出被截断时 `finish_reason` 变成什么
   - 把 `temperature` 改成 `0`，连续跑 3 次，对比答案是不是更接近
3. 把观察结果写进 `practice_1.py` 顶部的注释里（`# 观察：...`）
4. 提交：`git add . && git commit -m "第1天：LLM hello world"`

> 参考解答：`exercises/practice_1_reference.py`。先自己写，卡住再看。
