# -*- coding: utf-8 -*-
"""报告仓库的读写 —— 本项目内共享模块。

这里的知识是「本项目的报告长什么样、放在哪、怎么读」。
三个上层共用它：
    api_server.py          （HTTP 接口）
    mcp_reports_server.py  （MCP 工具）
    build_reports_site.py  （站点构建）

约束：本模块只允许依赖标准库。
      不许 import fastapi / fastmcp —— 否则上层会被迫装上自己不需要的依赖。
"""

import os
import re
from pathlib import Path

# ------------------------------------------------------------------ 目录与命名

_DEFAULT_REPORTS_DIR = Path(__file__).resolve().parent / "reports"
# 报告目录可被环境变量覆盖（测试用来指向临时 fixture 目录）；不设则用默认目录
REPORTS_DIR = Path(os.environ.get("STUDY_REPORTS_DIR") or _DEFAULT_REPORTS_DIR)

REPORTS_GLOB = "????-W??-review.md"


def report_files() -> list[Path]:
    """正式报告文件列表，按周次排序（旧 -> 新）。"""
    return sorted(REPORTS_DIR.glob(REPORTS_GLOB))


def week_of(path: Path) -> str:
    """'2026-W39-review.md' -> '2026-W39'"""
    return path.name.removesuffix("-review.md")


def available_weeks() -> list[str]:
    """当前可用的周次列表，例如 ["2026-W38", "2026-W39"]。"""
    return [week_of(p) for p in report_files()]


def normalize_week(raw: str) -> str | None:
    """把各种写法的周次归一化成 2026-W39；认不出来返回 None。

    能认这些写法：2026-W39 / 2026-w39 / W39 / 2026-W39-review.md
    """
    s = raw.strip().upper()
    s = s.removesuffix("-REVIEW.MD")
    m = re.fullmatch(r"(\d{4})-W(\d{1,2})", s)
    if m:
        year, week = m.group(1), m.group(2)
    else:
        m2 = re.fullmatch(r"W(\d{1,2})", s)
        if not m2:
            return None
        year, week = None, m2.group(1)
    if year is None:
        weeks = available_weeks()
        if not weeks:
            return None
        year = max(w[:4] for w in weeks)
    return f"{year}-W{int(week):02d}"


# ------------------------------------------------------------------ 读取

def report_path(week: str) -> Path:
    """周次 -> 报告文件路径（不判断文件是否存在）。"""
    return REPORTS_DIR / f"{week}-review.md"


def read_report_text(week: str) -> str | None:
    """读某周报告的全文；文件不存在则返回 None。

    注意：本函数不表达「错误」—— 是 None 就是事实，怎么报错由上层决定
         （MCP 层返回 error 字典，HTTP 层返回 404）。
    """

    path = report_path(week)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")
