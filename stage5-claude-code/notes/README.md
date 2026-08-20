# Stage 5 — Claude Code 生态（用 Codex 对照学）

内容整理自 awesome-agentic-ai-zh 的 stages/05-claude-code-ecosystem.zh-Hans.md。
**学习方式**：课程默认用 Claude Code，本学习用**你正在用的 Codex** 对照学（概念通用、免费、零安装）。

## 对照表（贯穿整个 stage）

| 课程概念（Claude Code）| Codex 对应物 | 你的真实例子 |
|---|---|---|
| CLAUDE.md（记忆层）| AGENTS.md | 学习目录、项目里的 AGENTS.md |
| slash commands（控制层）| Codex 命令 | `/help` 等 |
| `~/.claude/`（设置层）| `~/.codex/` | config.toml、skills、mcp_servers |
| settings.json（行为层）| `~/.codex/config.toml` | model、sandbox_mode 等 |
| Hooks（控制层）| Codex hooks/notify | config.toml 里的 notify |
| MCP | MCP | 你 Codex 里配了 node_repl MCP |
| Skills | Skills | ~/.codex/skills/ |
| Subagent | 多 agent | Codex 的 subagent |

## 学习计划

```text
第 1 天：CLI agent 是什么 + CLAUDE.md ↔ AGENTS.md + 探索你自己的 ~/.codex
第 2 天：MCP（你 Codex 里现成的 node_repl MCP 当例子）
第 3 天：Skills + Subagent
第 4 天：Stage 5 出口考核（对照自检）
```

## 进 Stage 6 前的自我检查（对照版）

- [ ] 讲得出 CLI agent 和 web/API 的区别（为什么用 CLI 不用 web）
- [ ] 说得出 AGENTS.md / ~/.codex / config.toml 各自的作用
- [ ] 看得懂 MCP 是什么、你 Codex 里怎么配的
- [ ] 说得出 skills 和 subagent 是干嘛的
