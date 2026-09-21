# -*- coding: utf-8 -*-
"""study-review agent —— 每周学习复盘 agent（你的 Stage 7 毕业设计）

需求文档：同目录 SPEC.md（先读它）。6 个 TODO 全部实现后删除本注释上方一行提醒。
提示：卡住超过 1 小时可以偷看 reference-implementation 分支的对应小节（写完删分支）。

运行方式（写完 TODO 6 后可用）：
    python review_agent.py                        # auto 后端，复盘最近 7 天
    python review_agent.py --backend cloud        # 强制云端
    python review_agent.py --days 14              # 复盘最近 14 天
    python review_agent.py --eval                 # 跑 eval harness
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import argparse  
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

from openai import OpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agent_kit import (env, resolve_backend, timed, call_llm,
                       estimate_cost, append_run_log, check_structure, ToolRegistry)
AGENT_DIR = Path(__file__).resolve().parent
REPORTS_DIR = AGENT_DIR / "reports"
RUN_LOG_PATH = REPORTS_DIR / "run_log.jsonl"

CST = timezone(timedelta(hours=8))  # 北京时间
MAX_TOKENS = 1500
# 格式契约（SPEC：报告标题必须逐字一致，eval 也靠它校验）
SECTION_HEADERS = [
    "## 本周学习进度回顾",
    "## 易错点/踩坑提取",
    "## 下周学习建议",
    "## 作品集素材提醒",
]

registry = ToolRegistry()


@registry.register("git_log", "读取仓库最近 N 天的 git 提交记录")
def get_git_log(days: int = 7) -> dict:
    """subprocess 跑 git log --since=<N天前> --pretty=%ad|%s --date=short，cwd=REPO_ROOT。
    失败返回 {"error":..., "retry_hint":...}（想想 Stage 3 的'错误是数据'）。"""
    try:
        result = subprocess.run(
            ["git", "log", f"--since={days} days ago", "--pretty=%ad|%s", "--date=short"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            return {"error": f"git log失败: {result.stderr.strip()}", "retry_hint": "确认git仓库存在且cwd正确"}
        commits = [line for line in result.stdout.strip().splitlines() if line]
        return {"commits": commits, "count": len(commits)}
    except Exception as e:
        return {"error": f"错误原因{e}","retry_hint": "检查git命令是否正确"} 
@registry.register("scan_stages", "扫描各 stage 目录，统计练习/笔记文件数量和最近修改时间")
def scan_stages() -> dict:
    """遍历 REPO_ROOT.glob("stage*")，每个 stage 统计 .py/.md 文件数和最新 mtime。"""
    try:
        stages = []
        for d in sorted(REPO_ROOT.glob("stage*")):
            if not d.is_dir():
                continue
            py_count = len(list(d.rglob("*.py")))
            md_count = len(list(d.rglob("*.md")))
            files = list(d.rglob("*"))
            latest = max((f.stat().st_mtime for f in files if f.is_file()), default=0)
            if latest:
                latest = datetime.fromtimestamp(latest).strftime("%Y-%m-%d")
            else:
                latest = "无"
            stages.append({"name": d.name, "py_files": py_count, "md_files": md_count, "latest": latest})
        return {"stages": stages}
    except Exception as e:
        return {"error": f"遇到错误原因为：{e}", "retry_hint": "确认仓库目录存在且文件可读"}


@registry.register("read_pitfalls", "读取 LEARNING-ROUTE.md 中的踩坑记录清单")
def read_pitfalls() -> dict:
    """取 '## 4.' 到 '## 5.' 之间的数字开头的行。文档缺失/结构变了都要返回 error 数据。"""
    try:
        doc = REPO_ROOT / "LEARNING-ROUTE.md"
        text = doc.read_text(encoding="utf-8")
        start = text.find("## 4.")
        end = text.find("## 5.")
        if start == -1 or end == -1:
            return {"error": "LEARNING-ROUTE.md 里找不到 '## 4.'或'## 5.' 章节","retry_hint": "确认文档结构未变"}
        section = text[start:end]
        pitfalls = [line.strip() for line in section.splitlines()
                    if line.strip() and line.strip()[0].isdigit()]
        return {"pitfalls": pitfalls, "count": len(pitfalls)}
    except Exception as e:
        return {"error": f"错误原因{e}", "retry_hint": "检查文件是否存在"}


@registry.register("read_selfcheck", "读取 LEARNING-ROUTE.md 中的毕业自测清单")
def read_selfcheck() -> dict:
    """取 '## 5.' 之后的 '- [' 开头的行。"""
    try:
        doc = REPO_ROOT / "LEARNING-ROUTE.md"
        text = doc.read_text(encoding="utf-8")
        start = text.find("## 5.")
        if start == -1:
            return {"error": "LEARNING-ROUTE.md 里找不到 '## 5.'之后章节", "retry_hint": "检查文档结构"}
        section = text[start:]
        items = [line.strip() for line in section.splitlines()
                if line.strip().startswith("- [")]
        return {"selfcheck": items, "count": len(items)}
    except Exception as e:
        return {"error": f"错误原因：{e}", "retry_hint": "检查文件是否存在"}

@registry.register("read_last_report", "读取最近一份复盘报告（跨 session 长期记忆）")
def read_last_report() -> dict:
    """glob('????-W??-review.md') 取最新一份，读前 3000 字符。没有则返回 {"memory": None}。"""
    try:
        files = list(REPORTS_DIR.glob("????-W??-review.md"))
        if not files:
            return {"memory": None}
        latest = sorted(files)[-1]
        content = latest.read_text(encoding="utf-8")[:3000]
        return {"memory": content, "file": latest.name}
    except Exception as e:
        return {"error": f"错误原因{e}", "retry_hint": "检查文件是否存在"}


def collect_context(days: int, stats: list) -> dict:
    """跑全部采集工具组装上下文；顺手给每个工具记 latency（observability）。"""
    context = {}
    with timed("tool:git_log", stats):
        context["git_log"] = get_git_log(days)
    with timed("tool:scan_stages", stats):
        context["scan_stages"] = scan_stages()
    with timed("tool:read_pitfalls", stats):
        context["pitfalls"] = read_pitfalls()
    with timed("tool:read_selfcheck", stats):
        context["selfcheck"] = read_selfcheck()
    with timed("tool:read_last_report", stats):
        context["last_report"] = read_last_report()
    return context



SYSTEM_PROMPT = (
    "你是 kk 的学习复盘 agent，根据工具采集的真实数据写一份周度学习复盘报告（Markdown）。\n\n"
    "硬性规则：\n"
    "1. 报告必须且只能包含以下四个二级标题，按此顺序：\n"
    + "\n".join(SECTION_HEADERS)
    + "\n2. 诚实性：数据里没有的内容必须写\"本周无\"，禁止编造提交、文件、事件或数字。\n"
    "3. \"易错点/踩坑提取\"只能从给定的踩坑数据里选，不要自己发明新的坑。\n"
    "4. 提到提交时保留原始提交信息，不要改写。\n"
    "5. 全文简体中文，正文控制在 600 字以内，直接输出 Markdown，不要额外解释。"
)





def generate_report(client: OpenAI, cfg: dict, context: dict, stats: list) -> tuple[str, dict]:
    """生成报告；结构不完整时把缺失标题反馈给模型重试一次（retry recovery）。
    重试也要记进 stats（比如 {"retry": True, "missing": [...]}）。"""
    data_text = json.dumps(context, ensure_ascii=False, indent=2)
    user_prompt = f"""这是本周采集到的学习数据：

    {data_text}

    请根据这些数据写周报。"""
    report,tokens = call_llm(client, cfg, SYSTEM_PROMPT, user_prompt, stats)
    missing = check_structure(report, SECTION_HEADERS)
    if missing:
        retry_prompt = f"""你上次的输出缺少这些标题：{missing}
    请重新生成完整报告，必须包含全部4个标题。
    
    原始数据：
    {data_text}"""

        report2,tokens2 = call_llm(client, cfg, SYSTEM_PROMPT, retry_prompt, stats)
        report = report2
        tokens["input"] += tokens2["input"]
        tokens["output"] += tokens2["output"]
        stats.append({"retry": True, "missing": missing})

    return report, tokens


def report_filename(now: datetime | None = None) -> str:
    """按北京时间 isocalendar() 生成 '2026-W37-review.md' 这样的文件名。"""
    now = now or datetime.now(CST)
    iso = now.isocalendar()
    return f"{iso.year}-W{iso.week:02d}-review.md"





# ---------------------------------------------------------------------------
# TODO 5 · Eval harness（结构 / 诚实性 / 正确性 + 一个故意挂的用例）
# ---------------------------------------------------------------------------

def empty_context() -> dict:
    """所有工具返回空数据的上下文，测诚实性用。"""
    return {
        "git_log":    {"commits": [],"count": 0},
        "scan_stages":{"stages": []},
        "pitfalls":   {"pitfalls": [],"count": 0},
        "selfcheck":  {"selfcheck": [],"count": 0},
        "last_report":{"memory": None},
    }


def build_eval_cases() -> list:
    """至少 4 个用例：structure / honesty / pitfall / demo_fail（见 SPEC）。
    demo_fail 的期望是错的（应挂）——它挂了才证明 eval 能发现错误。"""
    def ctx_with_pitfall():
        c = empty_context()
        c["pitfalls"] = {"pitfalls": ["6. **embedding 大小写敏感**: ReAct≠React"], "count": 1}
        return c

    return [
        {
            "id": "structure",
            "context": collect_context(7,[]),
            "check": lambda r: not check_structure(r, SECTION_HEADERS),
        },
        {
            "id": "honesty",
            "context": empty_context(),
            "check": lambda r: any(w in r for w in ["本周无","无记录","暂无"]),
        },
        {
            "id": "pitfall",
            "context": ctx_with_pitfall(),
            "check": lambda r: "embedding" in r.lower(),
        },
        {
            "id": "demo_fail",
            "context": empty_context(),
            "check": lambda r: "绝不存在的词xyz" in r,
        },
    ]


def run_eval(client: OpenAI, cfg: dict) -> float:
    """逐个跑用例，打印 ✅/ 和通过率，结果追加进 run_log.jsonl。"""
    cases = build_eval_cases()
    results = []

    for case in cases:
        context = case["context"]
        stats = []
        report, tokens = generate_report(client,cfg,context,stats)
        passed = case["check"](report)
        print(f"{'✅' if passed else '❌'} [{case['id']}]")
        results.append({"id": case["id"],"passed": passed})
    pass_count = sum(1 for r in results if r["passed"])
    pass_rate = pass_count / len(results)
    print(f"通过率: {pass_count}/{len(results)} ({pass_rate: .0%})")
    print("  注：demo_fail 应该挂才证明eval有效")

    append_run_log({"event": "eval", "pass_rate": pass_rate, "results": results}, RUN_LOG_PATH)
    return pass_rate



def main() -> None:
    """argparse 解析参数 → resolve_backend → （--eval 则跑评估）→
    collect_context → generate_report → 写 reports/YYYY-WNN-review.md →
    打印 ✅ 报告路径 + tokens/成本统计 → 遥测写入 run_log.jsonl。"""
    parser = argparse.ArgumentParser(description = "每周学习复盘agent")
    parser.add_argument("--backend", default="auto", choices=["local","cloud","auto"],
                        help="模型后端")
    parser.add_argument("--days", type=int, default=7,help="复盘最近N天")
    parser.add_argument("--eval", action="store_true",help="只跑eval harness")

    args = parser.parse_args()
    cfg = resolve_backend(args.backend)
    client = OpenAI(base_url=cfg["base_url"], api_key=cfg["api_key"])

    if args.eval:
        run_eval(client,cfg)
        return
    
    stats = []
    context = collect_context(args.days, stats)
    report, tokens = generate_report(client, cfg, context, stats)

    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / report_filename()
    report_path.write_text(report, encoding="utf-8")

    cost = estimate_cost(cfg, tokens)
    append_run_log({
        "event": "report",
        "file": report_path.name,
        "days": args.days,
        "backend": cfg["name"],
        "tokens": tokens,
        "cost": cost,
        "stats": stats,
    }, RUN_LOG_PATH)

    print(f"✅ 报告已生成：{report_path}")
    print(f"    tokens: {tokens['input']} in / {tokens['output']} out")
    print(f"   成本：{cost if cost is not None else '$0 (本地)'}")

if __name__ == "__main__":
    main()