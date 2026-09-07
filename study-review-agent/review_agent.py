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

import argparse  # TODO 6: 用它解析 --backend / --days / --eval
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

# 格式契约（SPEC：报告标题必须逐字一致，eval 也靠它校验）
SECTION_HEADERS = [
    "## 本周学习进度回顾",
    "## 易错点/踩坑提取",
    "## 下周学习建议",
    "## 作品集素材提醒",
]


def env(name: str, default: str = "") -> str:
    """读环境变量。注意：空字符串要视为未设置（Actions 未配 var 会传空值）。"""
    # TODO 1: 实现
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 1 · 后端解析（local / cloud / auto）
# ---------------------------------------------------------------------------

def resolve_backend(choice: str) -> dict:
    """返回 {"name", "base_url", "model", "api_key"} 字典。

    - local:  Ollama，默认 http://localhost:11434/v1 + qwen2.5:7b
    - cloud:  OpenAI 兼容 API，必须配置 CLOUD_API_KEY，否则报错退出
    - auto:   用 client.models.list() 带 3s 超时探测本地；不通则 fallback 云端
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 2 · Tool registry：错误作为数据返回，不许 raise
# ---------------------------------------------------------------------------

TOOL_REGISTRY = {}


def register_tool(name: str, description: str):
    """装饰器：把函数注册进 TOOL_REGISTRY（name -> {"impl": fn, "description": ...}）。"""
    # 提示：和 Stage 4 的 @tool 一个思路，但这里给你自己的采集流水线用
    def deco(fn):
        ...
    return deco


@register_tool("git_log", "读取仓库最近 N 天的 git 提交记录")
def get_git_log(days: int = 7) -> dict:
    """subprocess 跑 git log --since=<N天前> --pretty=%ad|%s --date=short，cwd=REPO_ROOT。
    失败返回 {"error":..., "retry_hint":...}（想想 Stage 3 的'错误是数据'）。"""
    raise NotImplementedError


@register_tool("scan_stages", "扫描各 stage 目录，统计练习/笔记文件数量和最近修改时间")
def scan_stages() -> dict:
    """遍历 REPO_ROOT.glob("stage*")，每个 stage 统计 .py/.md 文件数和最新 mtime。"""
    raise NotImplementedError


@register_tool("read_pitfalls", "读取 LEARNING-ROUTE.md 中的踩坑记录清单")
def read_pitfalls() -> dict:
    """取 '## 4.' 到 '## 5.' 之间的数字开头的行。文档缺失/结构变了都要返回 error 数据。"""
    raise NotImplementedError


@register_tool("read_selfcheck", "读取 LEARNING-ROUTE.md 中的毕业自测清单")
def read_selfcheck() -> dict:
    """取 '## 5.' 之后的 '- [' 开头的行。"""
    raise NotImplementedError


@register_tool("read_last_report", "读取最近一份复盘报告（跨 session 长期记忆）")
def read_last_report() -> dict:
    """glob('????-W??-review.md') 取最新一份，读前 3000 字符。没有则返回 {"memory": None}。"""
    raise NotImplementedError


def collect_context(days: int, stats: list) -> dict:
    """跑全部采集工具组装上下文；顺手给每个工具记 latency（observability）。"""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 3 · LLM 调用包装（observability + cost）
# ---------------------------------------------------------------------------

@contextmanager
def timed(label: str, stats: list):
    """Stage 7 练习 3 的老朋友：计时 contextmanager，结束把 latency 写进 stats。"""
    raise NotImplementedError


def call_llm(client: OpenAI, cfg: dict, system: str, user: str, stats: list) -> tuple[str, dict]:
    """调用 chat.completions，返回 (回复文本, {"input": n, "output": n})。
    token 数从 resp.usage 里拿；把 tokens 也写进 stats。"""
    raise NotImplementedError


def estimate_cost(cfg: dict, tokens: dict) -> float | None:
    """仅 cloud 后端且配置了 CLOUD_PRICE_IN/OUT（每百万 token 单价）才算，否则 None。"""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 4 · 报告生成（诚实性 system prompt + 带反馈重试）
# ---------------------------------------------------------------------------

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


def check_structure(report: str) -> list:
    """返回缺失的标题列表（空列表 = 结构完整）。"""
    raise NotImplementedError


def generate_report(client: OpenAI, cfg: dict, context: dict, stats: list) -> tuple[str, dict]:
    """生成报告；结构不完整时把缺失标题反馈给模型重试一次（retry recovery）。
    重试也要记进 stats（比如 {"retry": True, "missing": [...]}）。"""
    raise NotImplementedError


def report_filename(now: datetime | None = None) -> str:
    """按北京时间 isocalendar() 生成 '2026-W37-review.md' 这样的文件名。"""
    raise NotImplementedError


def append_run_log(entry: dict) -> None:
    """把运行遥测追加写入 reports/run_log.jsonl（一行一个 JSON）。"""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 5 · Eval harness（结构 / 诚实性 / 正确性 + 一个故意挂的用例）
# ---------------------------------------------------------------------------

def empty_context() -> dict:
    """所有工具返回空数据的上下文，测诚实性用。"""
    raise NotImplementedError


def build_eval_cases() -> list:
    """至少 4 个用例：structure / honesty / pitfall / demo_fail（见 SPEC）。
    demo_fail 的期望是错的（应挂）——它挂了才证明 eval 能发现错误。"""
    raise NotImplementedError


def run_eval(client: OpenAI, cfg: dict) -> float:
    """逐个跑用例，打印 ✅/❌ 和通过率，结果追加进 run_log.jsonl。"""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 6 · 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    """argparse 解析参数 → resolve_backend → （--eval 则跑评估）→
    collect_context → generate_report → 写 reports/YYYY-WNN-review.md →
    打印 ✅ 报告路径 + tokens/成本统计 → 遥测写入 run_log.jsonl。"""
    raise NotImplementedError


if __name__ == "__main__":
    main()
