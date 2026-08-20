# 第 1 天：CLI agent 是什么 + AGENTS.md（CLAUDE.md 的 Codex 版）+ 探索你的 ~/.codex

> 对应 awesome-agentic-ai-zh Stage 5.1，用 Codex 对照学。

## 1. CLI agent 是什么（为什么用 CLI 不用 web）

| 界面 | 跑在哪 | 能做什么 |
|---|---|---|
| claude.ai / ChatGPT（web）| 浏览器 | 纯对话，无 file system 操作 |
| API（programmatic）| 你的脚本 | LLM call、自己包 agent loop |
| **CLI agent（Claude Code / Codex）** | 你的终端 | **完整 OS 级 agent**：读文件/改文件/跑命令/用 git |
| Agent SDK | Python/TS | 完整 agent runtime（Stage 4 学的那些）|

**核心差别**：CLI agent 有**完整的电脑权限**（file / shell / git / 子进程），能自主完成多步骤工作——**你现在用的 Codex 就是**。

## 2. CLAUDE.md ↔ AGENTS.md（给 agent 的"说明书"）

CLAUDE.md / AGENTS.md = 项目根目录的 markdown，agent 每次进项目都读，用来设定：
- 项目约定（命令、风格、结构）
- 该做什么不该做什么
- 规则（要可验证，不要空话）

**5 原则**（写 AGENTS.md 时用）：
1. **Legibility**：用 markdown header 分区、规则写具体（"2-space indent" 而不是 "format properly"）
2. **Progressive Disclosure**：< 200 行，拆到 `@-import` / 子文件
3. **System of Record**：AGENTS.md 当"入口地图"，细节指向 docs/
4. **Taste Invariants**：规则可验证（"commit 前跑 make lint"）而不是 "follow best practices"
5. **Transparency**：要求 agent 大改动前先 show plan

## 3. 命令对照（slash commands）

Claude Code 的 /plan /clear /compact /model /permissions 等 → Codex 里对应：
- plan mode（先规划再动手）
- 新会话（= /clear）
- 切换模型（= /model）

## 4. ~/.claude/ ↔ ~/.codex/（设置层）

课程：`~/.claude/` 有 settings.json（全局行为）、CLAUDE.md（全局 baseline）、skills/、agents/。
你的 `~/.codex/` 有：config.toml（=settings.json）、AGENTS.md（=CLAUDE.md）、skills/、auth.json、mcp 配置。

## 今日作业（探索你自己的 Codex）

1. 打开 `C:\Users\admin\.codex\config.toml`，找出：模型配置、sandbox 配置、MCP server 配置（各在哪一段）
2. 打开你项目里的 AGENTS.md（学习目录里有），看它写了什么规则
3. 口头回答：CLI agent 和 web 聊天有什么区别？AGENTS.md 是干嘛的？
