## 本周学习进度回顾

本周 13 次提交（2026-09-16～2026-09-21），主线是毕业设计逐日推进与 agent_kit 重构：

毕业设计第三天：tool registry 完成（5个采集工具 + collect_context + timed）；第四天：LLM调用包装 + token 记账；第五天：报告生成（prompt组装 + 结构校验 + 带反馈重试）；第六天：eval harness（4用例含故意挂的demo_fail）；第七天：main主流程（argparse + 端到端跑通）；第八天：Github Actions workflow(每周一自动跑)；workflow加入eval质量门禁(生成报告前先验证agent健康)；README:毕业设计标记为已完成(含action和实测数据)；chore: 周报 2026-09-18（两次）；重构：抽出agent_kit 通用模块（8个通用零件，review_agent减28%）；README: 补agent_kit 模块化说明 + 用run_log实测数据修正成本数字；chore: 周报 2026-09-21。

stage 扫描：7 个阶段目录最新更新均为 2026-09-21，文件数最多为 stage3（12 py/3 md）。

## 易错点/踩坑提取

1. 推理模型吃 token：max_tokens 要给 500+，否则 content 为空
2. 中文引号写进代码：字符串里别用 ASCII 引号当内容
3. 模型抢跑：多步任务别列工具清单
4. 模型漏步：3b 多步不稳，7b 更稳
5. 工具输入不匹配（踩 3 次）：中英文别名/归一化对齐
6. embedding 大小写敏感：ReAct≠React
7. 模型改数字：工具返回 6.7 可能写成 6.7899，需校验
8. 自己检查会自我称赞：验收要拆独立 agent
9. .codex 有敏感文件：auth.json 不能提交

## 下周学习建议

- 逐条对照 6 条自查清单：ReAct 循环＋3 个坑、RAG、agent eval 与通过率、MCP/Skill/AGENTS.md 区别、框架/手写/RAG/multi-agent 取舍、Harness 8 元件。
- 优先补坑 5（已踩 3 次）与坑 7；坑 8 尝试拆独立验收 agent。
- 按坑 9 确认 .codex/auth.json 等敏感文件未被提交。
- stage1~7 本周均有更新，安排回扫。

## 作品集素材提醒

本周无。