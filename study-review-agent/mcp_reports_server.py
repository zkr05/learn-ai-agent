# -*- coding: utf-8 -*-
"""study-reports MCP server —— 把周报只读暴露给任意 MCP host"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import re
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP




REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORTS_GLOB = "????-W??-review.md"


mcp = FastMCP("study-reports")


def _report_files() -> list[Path]:
    """正式报告文件列表，按周次排序"""
    return sorted(REPORTS_DIR.glob(REPORTS_GLOB))


def _week_of(path: Path) -> str:
    """'2026-W39-review.md' -> '2026-W39'"""
    return path.name.removesuffix("-review.md")


def _available_weeks() -> list[str]:
    return [_week_of(p) for p in _report_files()]


def _normalize_week(raw: str) -> str | None:
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
        weeks = _available_weeks()
        if not weeks:
            return None
        year = max(w[:4] for w in weeks)
    return f"{year}-W{int(week):02d}"



@mcp.tool
def list_reports() -> dict:
    """列出所有周报的目录信息（周次、文件名、大小、修改日期），不返回正文。"""
    reports = []
    for f in _report_files():
        stat = f.stat()
        reports.append({
            "week": _week_of(f),
            "file": f.name,
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
        })
    if not reports:
        return {"reports": [], "note": "报告为空"}
    return {"reports": reports}


@mcp.tool
def read_report(week: str) -> dict:
    """阅读指定周报的正文。
    
    Args:
        week: 周次，形如2026-W39
    """
    w = _normalize_week(week)
    if w is None:
        return {"error": f"无法识别的周次：{week}", "retry_hint": "请用 2026-W39 这样的格式"}

    path = REPORTS_DIR / f"{w}-review.md"
    if not path.exists():
        return {"error": f"没有{w}的周报", "retry_hint": f"可选周次: {_available_weeks()}"}

    return {"week": w, "content": path.read_text(encoding="utf-8")}


@mcp.tool
def search_reports(keyword: str, limit: int = 30) -> dict:
    """遍历所有报告，搜关键词，返回关键词的周次和行数

    Args:
        keyword: 关键词，如 embedding
        limit: 关键词的限制，超出后只返回前N条，但 total 为真实命中数
    """
    kw = keyword.strip().lower()
    if not kw:
        return {"error": "未找到可读取内容", "retry_hint": "重新输入关键词"}

    matches = []
    total = 0
    for f in _report_files():
        lines = f.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, 1):
            if kw in line.lower():
                total += 1
                if len(matches) < limit:
                    matches.append({
                        "week": _week_of(f),
                        "line": lineno,
                        "text": line.strip(),
                    })
    return {"matches": matches, "total": total, "truncated": total > len(matches)}

if __name__ == "__main__":
    mcp.run()