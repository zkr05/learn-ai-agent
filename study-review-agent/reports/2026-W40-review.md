## 本周学习进度回顾

本周 git_log 采集到 14 条提交（2026-09-22～2026-09-29），较上一份报告（13 条）新增 1 条：

- 2026-09-29|修站点不自动更新：bot用GITHUB_TOKEN 推送不触发其他workflow.改为主动dispatch

其余 13 条上一份报告已覆盖。本周延续两条主线：一是周报静态站点（GitHub Pages 自动构建部署、pages.yaml/index.html、REPORTS_GLOB 收敛标注）；二是 MCP server 的测试与稳定性（3 个只读工具 list/read/search、stdio 端到端测试进 CI、修 CI push 失败、跨宿主排障笔记、fixture 驱动修 CI 误报）。

stage 扫描：7 个阶段目录最新更新均为 2026-09-29，合计 41 个 py、17 个 md；文件最多为 stage3-tool-use（12 py / 3 md），最少为 stage5-claude-code（1 py / 2 md）。

## 易错点/踩坑提取

1. 推理模型吃 token：max_tokens 要给 500+，否则 content 为空
2. 中文引号写进代码：字符串里别用 ASCII 引号当内容
3. 模型抢跑：多步任务别列工具清单，用"必须完成"短问题
4. 模型漏步：3b 多步不稳，7b 更稳；生产换大模型或多跑
5. 工具输入不匹配（踩 3 次）：工具和模型要对齐（中英文别名/归一化）
6. embedding 大小写敏感：ReAct≠React，查询要规范化
7. 模型改数字：工具返回 6.7 模型可能用 6.7899——数据要校验
8. 自己检查会自我称赞：验收要拆独立 agent（Debate/Critic）
9. .codex 有敏感文件：auth.json 不能提交

## 下周学习建议

- 对照 6 条自查清单逐项过：默写 ReAct 循环＋3 个坑、搭 RAG（embed→retrieve→generate）、给 agent 写 eval 并解释通过率、说清 MCP/Skill/AGENTS.md 区别、判断框架/手写/RAG/multi-agent 取舍、讲出 Harness 8 元件及自己做过的部分。
- 优先补坑 5（已踩 3 次）与坑 7 的数据校验；坑 8 试着拆独立验收 agent。
- 按坑 9 复查 .codex/auth.json 等敏感文件确未进入提交。
- 站点部署与 MCP 测试均已落地，可核对 REPORTS_GLOB 收敛后是否仍只有单一来源、fixture 驱动后 CI 是否稳定不再误报。

## 作品集素材提醒

本周无。