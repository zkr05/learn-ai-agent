# study-review agent · 每周自动学习复盘

把 Stage 5 的 study-review skill 按 Stage 7 Harness 设计升级成的 production agent。
**每周一自动运行**（GitHub Actions），扫描仓库本周动态，生成四板块复盘报告并自动 commit 回仓库。

## 每周报告四个板块

1. **本周学习进度回顾** — git log + 各 stage 文件扫描
2. **易错点/踩坑提取** — 从 LEARNING-ROUTE.md 的踩坑记录里选高频相关的
3. **下周学习建议** — 结合毕业自测清单
4. **作品集素材提醒** — 把本周产出整理成作品集语言

诚实性规则写死在 system prompt：数据里没有的必须写"本周无"，禁止编造。

## 本地运行

```bash
cd study-review-agent
pip install -r requirements.txt

python review_agent.py                # auto：先探测本地 Ollama，不通 fallback 云端
python review_agent.py --backend cloud
python review_agent.py --days 14
python review_agent.py --eval         # 跑 eval harness（4 个用例，含 1 个故意挂的）
```

报告输出到 `reports/YYYY-WNN-review.md`，运行遥测追加到 `reports/run_log.jsonl`。

## 环境变量

| 变量 | 说明 | 默认 |
|---|---|---|
| `REVIEW_BACKEND` | `auto` / `local` / `cloud` | `auto` |
| `LOCAL_BASE_URL` / `LOCAL_MODEL` | 本地 Ollama 地址 / 模型 | `http://localhost:11434/v1` / `qwen2.5:7b` |
| `CLOUD_API_KEY` | 云端 API key（GitHub 上配成 secret） | 无 |
| `CLOUD_BASE_URL` / `CLOUD_MODEL` | OpenAI 兼容端点 / 模型 | `https://api.openai.com/v1` / `gpt-4o-mini` |
| `CLOUD_PRICE_IN` / `CLOUD_PRICE_OUT` | 每百万 token 单价，配置后自动算成本 | 不计费 |

## GitHub Actions 自动化

工作流在 `.github/workflows/weekly-review.yml`：**每周一北京时间 10:00** 自动运行，也支持手动触发（Actions 页面 → weekly-review → Run workflow）。

仓库设置（Settings → Secrets and variables → Actions）：

| 类型 | 名字 | 内容 |
|---|---|---|
| Secret | `LLM_API_KEY` | 云端 API key |
| Variable（可选） | `LLM_BASE_URL` / `LLM_MODEL` | 指向任意 OpenAI 兼容服务 |
| Variable（可选） | `LLM_PRICE_IN` / `LLM_PRICE_OUT` | 单价，启用成本记账 |

## 对应 Stage 7 Harness 设计

| Harness 元件 | 落地 |
|---|---|
| Tool registry | `TOOL_REGISTRY` 统一注册 5 个采集工具，错误作为数据返回 |
| Retry recovery | 报告结构不完整 → 带缺失标题反馈自动重试一次 |
| Safety（诚实性） | system prompt 硬性规则 + eval 诚实性用例把关 |
| Observability | 工具/LLM 各自记录 latency，token 用量写入 `run_log.jsonl` |
| Cost | token 记账 + 可选单价自动算成本；本地后端 $0 |
| Eval | `--eval`：结构 / 诚实性 / 内容正确性 + 1 个故意挂的 demo 用例 |
| Memory | 自动读上一期报告作为上下文（跨 session） |
| Automation | GitHub Actions 定时触发 + 报告自动 commit（CI/CD 闭环） |
