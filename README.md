# AI Agent 学习记录（AI Agent Learning）

学习路线：**Track B — Agent Builder**（[WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)）
当前进度：**Stage 2 — Prompt 设计**（进行中，2026-08-10 开始）

## 仓库结构

```text
learn-ai-agent/
├── README.md                    # 本文件（学习路线 + 技能清单）
├── stage1-llm-basics/           # Stage 1：LLM 基础（已完成）
│   ├── exercises/               # 6 个练习（含观察记录）
│   └── notes/                   # 课程笔记
├── stage2-prompt-eng/           # Stage 2：Prompt 设计（进行中）
│   ├── exercises/
│   └── notes/
├── awesome-agentic-ai-zh/       # 课程参考仓库（上游克隆）
└── ...
```

## 技能清单

### ✅ Stage 1 — LLM 基础（已完成）

- 用 Python 调用 LLM API（Ollama 本机 + OpenAI 兼容协议，全程 $0）
- 理解 token / context window / temperature 并亲手验证
- 估算成本与延迟：本机 vs 云端 trade-off
- 跨模型对比（8B vs 0.5B 的质量差距）
- 错误处理：exponential backoff retry 包装器
- 排坑：推理模型 max_tokens / reasoning 字段

### 🔄 Stage 2 — Prompt 设计（进行中）

- [x] System Prompt（人设 / 格式 / 输出限制）
- [ ] Few-Shot（0-shot vs 3-shot 准确率对比）
- [ ] Chain-of-Thought
- [ ] Iterative Refinement

## 学习方式

每天约 1 小时：读笔记 → 完成练习 → 填观察 → git 提交。
每个练习带自我验证（assert），每课通过口头验收。

## 环境

- Python 3.11 + openai SDK
- Ollama（本机）：gemma4:e4b（8B）、qwen2.5:0.5b
