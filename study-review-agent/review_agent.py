# -*- coding: utf-8 -*-
"""study-review agent —— 每周学习复盘 agent（Stage 7 生产化毕业设计）

把 Stage 5 的 study-review skill 按 Harness 设计升级成 production agent：
- Tool registry：数据采集工具统一注册，错误作为数据返回（不 raise）
- 双后端：本地 Ollama（$0）/ 云端 OpenAI 兼容 API，auto 模式自动探测 + fallback
- Retry recovery：报告结构不完整时带反馈自动重试一次
- Observability：每次 LLM 调用记录 latency + token，追加写入 reports/run_log.jsonl
- Cost：按 token 记账，配置单价（每百万 token）后自动算成本
- Eval：--eval 跑评估用例（结构 / 诚实性 / 内容正确性 + 一个故意挂的用例）

用法：
    python review_agent.py                        # auto 后端，复盘最近 7 天
    python review_agent.py --backend cloud        # 强制云端
    python review_agent.py --days 14              # 复盘最近 14 天
    python review_agent.py --eval                 # 跑 eval（会产生真实 LLM 调用）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import argparse
import json
import os
import subprocess
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = AGENT_DIR / "reports"
RUN_LOG_PATH = REPORTS_DIR / "run_log.jsonl"

CST = timezone(timedelta(hours=8))  # 北京时间
MAX_TOKENS = 1500

SECTION_HEADERS = [
    "## 本周学习进度回顾",
    "## 易错点/踩坑提取",
    "## 下周学习建议",
    "## 作品集素材提醒",
]


def env(name: str, default: str = "") -> str:
    """读环境变量，空字符串视为未设置（GitHub Actions 未配置 var 时会传空值）。"""
    value = os.environ.get(name, "")
    return value if value else default


# ---------------------------------------------------------------------------
# 1. 后端解析：local / cloud / auto（自动探测 + fallback）
# ---------------------------------------------------------------------------

def resolve_backend(choice: str) -> dict:
    cloud_cfg = {
        "name": "cloud",
        "base_url": env("CLOUD_BASE_URL", "https://api.openai.com/v1"),
        "model": env("CLOUD_MODEL", "gpt-4o-mini"),
        "api_key": env("CLOUD_API_KEY"),
    }
    local_cfg = {
        "name": "local",
        "base_url": env("LOCAL_BASE_URL", "http://localhost:11434/v1"),
        "model": env("LOCAL_MODEL", "qwen2.5:7b"),
        "api_key": "ollama",
    }

    if choice == "local":
        return local_cfg
    if choice == "cloud":
        if not cloud_cfg["api_key"]:
            raise SystemExit("cloud 后端需要环境变量 CLOUD_API_KEY（GitHub 上配置为 secret）")
        return cloud_cfg

    # auto：本地通就用本地（$0），不通 fallback 到云端
    try:
        probe = OpenAI(base_url=local_cfg["base_url"], api_key=local_cfg["api_key"], timeout=3)
        probe.models.list()
        return local_cfg
    except Exception:
        if cloud_cfg["api_key"]:
            print("ℹ️ 本地 Ollama 不可达，fallback 到云端后端")
            return cloud_cfg
        raise SystemExit("auto 模式：本地 Ollama 不可达，且未配置 CLOUD_API_KEY，无法运行")


# ---------------------------------------------------------------------------
# 2. Tool registry：数据采集工具统一注册；错误作为数据返回，让上层自己恢复
# ---------------------------------------------------------------------------

TOOL_REGISTRY = {}


def register_tool(name: str, description: str):
    def deco(fn):
        TOOL_REGISTRY[name] = {"impl": fn, "description": description}
        return fn
    return deco


@register_tool("git_log", "读取仓库最近 N 天的 git 提交记录")
def get_git_log(days: int = 7) -> dict:
    since = (datetime.now(CST) - timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        result = subprocess.run(
            ["git", "log", f"--since={since}", "--pretty=%ad|%s", "--date=short"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            cwd=str(REPO_ROOT), timeout=30,
        )
    except Exception as exc:
        return {"error": f"git 命令执行失败: {exc}", "retry_hint": "确认本机 git 可用"}
    if result.returncode != 0:
        return {"error": result.stderr.strip(), "retry_hint": "确认在 git 仓库内运行"}
    commits = [line for line in result.stdout.splitlines() if line.strip()]
    return {"days": days, "commits": commits}


@register_tool("scan_stages", "扫描各 stage 目录，统计练习/笔记文件数量和最近修改时间")
def scan_stages() -> dict:
    stages = []
    for stage_dir in sorted(REPO_ROOT.glob("stage*")):
        files = [p for p in stage_dir.rglob("*") if p.suffix in (".py", ".md")]
        if not files:
            continue
        latest = max(p.stat().st_mtime for p in files)
        stages.append({
            "stage": stage_dir.name,
            "file_count": len(files),
            "last_modified": datetime.fromtimestamp(latest, CST).strftime("%Y-%m-%d"),
        })
    return {"stages": stages}


@register_tool("read_pitfalls", "读取 LEARNING-ROUTE.md 中的踩坑记录清单")
def read_pitfalls() -> dict:
    path = REPO_ROOT / "LEARNING-ROUTE.md"
    if not path.exists():
        return {"error": "LEARNING-ROUTE.md 不存在", "retry_hint": "检查仓库结构"}
    text = path.read_text(encoding="utf-8", errors="replace")
    if "## 4." not in text or "## 5." not in text:
        return {"error": "没找到踩坑记录小节", "retry_hint": "确认文档包含 '## 4.' 小节"}
    section = text.split("## 4.")[1].split("## 5.")[0]
    items = [line.strip() for line in section.splitlines() if line.strip() and line.strip()[0].isdigit()]
    return {"pitfalls": items}


@register_tool("read_selfcheck", "读取 LEARNING-ROUTE.md 中的毕业自测清单")
def read_selfcheck() -> dict:
    path = REPO_ROOT / "LEARNING-ROUTE.md"
    if not path.exists():
        return {"error": "LEARNING-ROUTE.md 不存在", "retry_hint": "检查仓库结构"}
    text = path.read_text(encoding="utf-8", errors="replace")
    if "## 5." not in text:
        return {"error": "没找到毕业自测小节", "retry_hint": "确认文档包含 '## 5.' 小节"}
    section = text.split("## 5.")[1]
    items = [line.strip() for line in section.splitlines() if line.strip().startswith("- [")]
    return {"selfcheck": items}


@register_tool("read_last_report", "读取最近一份复盘报告（跨 session 长期记忆）")
def read_last_report() -> dict:
    reports = sorted(REPORTS_DIR.glob("????-W??-review.md"))
    if not reports:
        return {"memory": None, "note": "还没有历史报告，这是第一期"}
    latest = reports[-1]
    return {"memory_file": latest.name, "memory": latest.read_text(encoding="utf-8", errors="replace")[:3000]}


def collect_context(days: int, stats: list) -> dict:
    """跑全部采集工具，组装成喂给模型的上下文。"""
    context = {"generated_at": datetime.now(CST).strftime("%Y-%m-%d %H:%M"), "days": days}
    for name, entry in TOOL_REGISTRY.items():
        start = time.perf_counter()
        result = entry["impl"](days) if name == "git_log" else entry["impl"]()
        stats.append({"tool": name, "latency_s": round(time.perf_counter() - start, 2),
                      "error": bool(result.get("error"))})
        context[name] = result
    return context


# ---------------------------------------------------------------------------
# 3. LLM 调用：包装 token / latency 记录（observability + cost）
# ---------------------------------------------------------------------------

@contextmanager
def timed(label: str, stats: list):
    start = time.perf_counter()
    try:
        yield
    finally:
        stats.append({"label": label, "latency_s": round(time.perf_counter() - start, 2)})


def call_llm(client: OpenAI, cfg: dict, system: str, user: str, stats: list) -> tuple[str, dict]:
    with timed("llm_call", stats):
        resp = client.chat.completions.create(
            model=cfg["model"],
            max_tokens=MAX_TOKENS,
            temperature=0.3,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
    usage = getattr(resp, "usage", None)
    tokens = {
        "input": getattr(usage, "prompt_tokens", None) if usage else None,
        "output": getattr(usage, "completion_tokens", None) if usage else None,
    }
    stats.append({"tokens": tokens})
    return resp.choices[0].message.content or "", tokens


def estimate_cost(cfg: dict, tokens: dict) -> float | None:
    """配置了每百万 token 单价（与币种无关的数字）才算成本。"""
    if cfg["name"] != "cloud" or tokens.get("input") is None:
        return None
    price_in = float(env("CLOUD_PRICE_IN", "0") or 0)
    price_out = float(env("CLOUD_PRICE_OUT", "0") or 0)
    return tokens["input"] / 1e6 * price_in + (tokens["output"] or 0) / 1e6 * price_out


# ---------------------------------------------------------------------------
# 4. 报告生成：system prompt（含诚实性规则）+ 结构校验 + 带反馈重试
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = f"""你是 kk 的学习复盘 agent，根据工具采集的真实数据写一份周度学习复盘报告（Markdown）。

硬性规则：
1. 报告必须且只能包含以下四个二级标题，按此顺序：
{chr(10).join(SECTION_HEADERS)}
2. 诚实性：数据里没有的内容必须写"本周无"，禁止编造提交、文件、事件或数字。
3. "易错点/踩坑提取"只能从给定的踩坑数据里选，不要自己发明新的坑。
4. 提到提交时保留原始提交信息，不要改写。
5. 全文简体中文，正文控制在 600 字以内，直接输出 Markdown，不要额外解释。"""


def check_structure(report: str) -> list:
    return [h for h in SECTION_HEADERS if h not in report]


def generate_report(client: OpenAI, cfg: dict, context: dict, stats: list) -> tuple[str, dict]:
    """生成报告；结构不完整时带上缺失项反馈重试一次（retry recovery）。"""
    user = "以下是本周采集的数据（JSON）：\n\n" + json.dumps(context, ensure_ascii=False, indent=1)
    report, tokens = call_llm(client, cfg, SYSTEM_PROMPT, user, stats)
    missing = check_structure(report)
    if missing:
        stats.append({"retry": True, "missing": missing})
        user_retry = (
            user
            + "\n\n你上一版报告缺少以下必需标题，请重新输出完整报告，标题必须逐字一致：\n"
            + "\n".join(missing)
        )
        report, tokens = call_llm(client, cfg, SYSTEM_PROMPT, user_retry, stats)
    return report, tokens


def report_filename(now: datetime | None = None) -> str:
    now = now or datetime.now(CST)
    iso = now.isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}-review.md"


def append_run_log(entry: dict) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    with RUN_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# 5. Eval harness：结构 / 诚实性 / 内容正确性 + 一个故意挂的用例
# ---------------------------------------------------------------------------

def empty_context() -> dict:
    return {"generated_at": "test", "days": 7, "git_log": {"days": 7, "commits": []},
            "scan_stages": {"stages": []}, "read_pitfalls": {"pitfalls": []},
            "read_selfcheck": {"selfcheck": []}, "read_last_report": {"memory": None}}


def pitfall_context() -> dict:
    ctx = empty_context()
    ctx["read_pitfalls"] = {"pitfalls": [
        "6. embedding 大小写敏感：ReAct≠React，查询要规范化",
        "7. 模型改数字：工具返回 6.7 模型可能用 6.7899——数据要校验",
    ]}
    return ctx


def build_eval_cases() -> list:
    return [
        {"id": "structure", "desc": "报告包含全部 4 个固定标题", "ctx": pitfall_context(),
         "check": lambda r: not check_structure(r), "expect_fail": False},
        {"id": "honesty", "desc": "空数据时必须说\"本周无\"（不许编造）", "ctx": empty_context(),
         "check": lambda r: any(w in r for w in ["本周无", "无提交", "没有提交", "无记录", "没有任何"]),
         "expect_fail": False},
        {"id": "pitfall", "desc": "踩坑提取必须包含数据中的关键词 embedding", "ctx": pitfall_context(),
         "check": lambda r: "embedding" in r.lower(), "expect_fail": False},
        {"id": "demo_fail", "desc": "故意写错的用例（期望出现'红烧肉'，应挂）——证明 eval 能发现错误",
         "ctx": pitfall_context(), "check": lambda r: "红烧肉" in r, "expect_fail": True},
    ]


def run_eval(client: OpenAI, cfg: dict) -> float:
    stats: list = []
    cases = build_eval_cases()
    results = []
    for case in cases:
        report, _ = generate_report(client, cfg, case["ctx"], stats)
        passed = case["check"](report)
        if case["expect_fail"]:
            passed = not passed  # demo 用例：挂了才算 eval 有效
        results.append({"id": case["id"], "passed": passed})
        mark = "✅" if passed else "❌"
        print(f"  {mark} [{case['id']}] {case['desc']}")
    pass_rate = sum(1 for r in results if r["passed"]) / len(results)
    print(f"Pass: {sum(1 for r in results if r['passed'])}/{len(results)} ({pass_rate:.0%})")
    append_run_log({"time": datetime.now(CST).isoformat(), "type": "eval",
                    "backend": cfg["name"], "model": cfg["model"],
                    "pass_rate": round(pass_rate, 3), "results": results})
    return pass_rate


# ---------------------------------------------------------------------------
# 6. 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="每周学习复盘 agent")
    parser.add_argument("--backend", choices=["auto", "local", "cloud"], default=env("REVIEW_BACKEND", "auto"))
    parser.add_argument("--days", type=int, default=7, help="复盘最近 N 天")
    parser.add_argument("--eval", action="store_true", help="跑 eval harness（产生真实 LLM 调用）")
    args = parser.parse_args()

    cfg = resolve_backend(args.backend)
    client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"], timeout=120)
    print(f"后端: {cfg['name']} | 模型: {cfg['model']}")

    if args.eval:
        run_eval(client, cfg)
        return

    stats: list = []
    context = collect_context(args.days, stats)
    report, tokens = generate_report(client, cfg, context, stats)

    missing = check_structure(report)
    if missing:
        print(f"⚠️ 重试后结构仍不完整，缺少: {missing}")

    REPORTS_DIR.mkdir(exist_ok=True)
    out_path = REPORTS_DIR / report_filename()
    out_path.write_text(
        f"# 学习复盘 · {report_filename().replace('-review.md', '')}\n\n{report}\n",
        encoding="utf-8",
    )
    print(f"✅ 报告已生成: {out_path.relative_to(REPO_ROOT)}")

    cost = estimate_cost(cfg, tokens)
    summary = {"time": datetime.now(CST).isoformat(), "type": "run",
               "backend": cfg["name"], "model": cfg["model"],
               "report": out_path.name, "tokens": tokens,
               "cost": round(cost, 6) if cost is not None else None,
               "tools": [s for s in stats if "tool" in s],
               "retried": any("retry" in s for s in stats)}
    append_run_log(summary)

    tool_errors = [s for s in stats if s.get("error")]
    print(f"tokens: {tokens} | 成本: {'$0（本地）' if cost is None else cost}")
    if tool_errors:
        print(f"⚠️ 有 {len(tool_errors)} 个采集工具返回错误，详情见 run_log.jsonl")


if __name__ == "__main__":
    main()
