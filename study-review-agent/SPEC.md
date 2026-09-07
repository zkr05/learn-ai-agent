# study-review agent · 实现需求（SPEC）

> 这是你的 Stage 7 毕业设计：把 Stage 5 的 study-review skill 升级成每周自动跑的 production agent。
> 规则：参考 `reference-implementation` 分支只许在卡住超过 1 小时时偷看对应小节；写完删除该分支。
> 每完成一个 TODO 就 `git commit`（格式：`毕业设计第N天：xxx`）。

## 目标

每周自动扫描本仓库的学习动态，生成一份四板块复盘报告，由 GitHub Actions 每周一自动运行并 commit 回仓库。

## 每周报告格式（格式契约，标题必须逐字一致）

1. `## 本周学习进度回顾`
2. `## 易错点/踩坑提取`
3. `## 下周学习建议`
4. `## 作品集素材提醒`

诚实性规则写进 system prompt：数据里没有的必须写"本周无"，禁止编造。

## 功能需求（对应 6 个 TODO）

### TODO 1 · 后端解析 `resolve_backend(choice)`
- 三种模式：`local`（Ollama）/ `cloud`（OpenAI 兼容 API）/ `auto`（先探测本地，不通 fallback 云端）
- 配置全部走环境变量，空字符串视为未设置（GitHub Actions 未配 var 时会传空值）
- 参考环境变量：`REVIEW_BACKEND` / `LOCAL_BASE_URL` / `LOCAL_MODEL` / `CLOUD_API_KEY` / `CLOUD_BASE_URL` / `CLOUD_MODEL`

### TODO 2 · Tool registry（数据采集）
统一注册 5 个工具，**错误作为数据返回（`{"error":..., "retry_hint":...}`），不许 raise**（Stage 3 的教训）：
- `git_log(days)`：最近 N 天提交（`git log --since`）
- `scan_stages()`：各 stage 目录文件数 + 最近修改时间
- `read_pitfalls()`：LEARNING-ROUTE.md 的 `## 4.` 踩坑小节
- `read_selfcheck()`：LEARNING-ROUTE.md 的 `## 5.` 毕业自测小节
- `read_last_report()`：最近一期报告（跨 session 长期记忆，Memory Pattern）

### TODO 3 · LLM 调用包装（observability + cost）
- 包装 chat.completions 调用，记录 latency + input/output tokens
- 配置了 `CLOUD_PRICE_IN` / `CLOUD_PRICE_OUT`（每百万 token 单价）时自动算成本

### TODO 4 · 报告生成（retry recovery）
- system prompt：四板块格式契约 + 诚实性规则
- 生成后校验 4 个标题是否齐全；缺失则**带上缺失项反馈重试一次**

### TODO 5 · Eval harness（`--eval`）
至少 4 个用例：
- structure：报告包含全部 4 个标题
- honesty：空数据时输出含"本周无"类表述
- pitfall：给定含关键词的踩坑数据，报告必须提到（如 embedding）
- demo_fail：一个**故意挂**的用例——挂了才证明 eval 能发现错误（Stage 7 练习 2 的设计）
跑完输出通过率，结果追加写入 `reports/run_log.jsonl`

### TODO 6 · 主流程 + GitHub Actions
- `main()`：argparse（`--backend` / `--days` / `--eval`）→ 采集 → 生成 → 写 `reports/YYYY-WNN-review.md` → 打印 ✅ 和统计
- `.github/workflows/weekly-review.yml`：每周一北京时间 10:00（cron `0 2 * * 1`）+ 手动触发；注意 `fetch-depth: 0`（要读 git 历史）和报告 commit 回仓库

## 验收标准

- [ ] `python review_agent.py --backend local` 输出含 ✅，报告落在 `reports/`
- [ ] `python review_agent.py --eval` 通过率符合预期（demo_fail 挂才算 eval 有效）
- [ ] GitHub Actions 手动触发跑绿，报告自动 commit
- [ ] `reports/run_log.jsonl` 能查到每次运行的 latency / tokens / 通过率
- [ ] 每个 TODO 对应至少一个 commit，提交信息可读
