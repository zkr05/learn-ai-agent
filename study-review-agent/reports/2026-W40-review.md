## 本周学习进度回顾

本周 git_log 采集到 11 条提交（2026-09-22～2026-09-28），其中 2026-09-28 新增 3 条：

- 2026-09-28|build_reports_site:标注REPORTS_GLOB的重复位置与收敛时机
- 2026-09-28|新增GitHub Pages：周报自动构建静态站点并部署
- 2026-09-28|提交pages.yaml,index.html

其余 8 条日期为 09-22～09-24（上一份报告已覆盖其中 6 条）。本周主线是把周报做成静态站点：接上 GitHub Pages 自动构建与部署，并标注 REPORTS_GLOB 的重复位置与收敛时机。

stage 扫描：7 个阶段目录最新更新均为 2026-09-28，合计 41 个 py、17 个 md；文件最多为 stage3-tool-use（12 py / 3 md），最少为 stage5-claude-code（1 py / 2 md）。

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

- 对照 6 条自查清单逐项过：ReAct 循环＋3 个坑、搭 RAG（embed→retrieve→generate）、给 agent 写 eval 并解释通过率、MCP/Skill/AGENTS.md 区别、框架/手写/RAG/multi-agent 取舍、Harness 8 元件。
- 优先补坑 5（已踩 3 次）与坑 7 的数据校验；坑 8 试着拆独立验收 agent。
- 按坑 9 复查 .codex/auth.json 等敏感文件确未进入提交。
- 7 个 stage 本周均有更新，安排一次回扫；站点部署刚落地，可核对 REPORTS_GLOB 收敛后是否仍只有单一来源。

## 作品集素材提醒

本周无。