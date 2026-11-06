# -*- coding: utf-8 -*-
"""study-reports MCP server —— 把周报只读暴露给任意 MCP host"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from datetime import datetime

from fastmcp import FastMCP

from reports_store import (available_weeks, normalize_week, read_report_text,
                           list_reports as store_list_reports)

mcp = FastMCP("study-reports")


@mcp.tool
def list_reports() -> dict:
    """列出所有周报的目录信息（周次、文件名、大小、修改日期），不返回正文。"""
    reports = []
    for m in store_list_reports():
        reports.append({
            "week": m.week,
            "file": f"{m.week}-review.md",
            "size_bytes": m.size_bytes,
            "modified": datetime.fromisoformat(m.modified).astimezone().strftime("%Y-%m-%d"),
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

    w = normalize_week(week)
    if w is None:
        return {"error": f"无法识别的周次：{week}", "retry_hint": "请用 2026-W39 这样的格式"}


    content = read_report_text(w)
    if content is None:
        return {"error": f"没有{w}的周报", "retry_hint": f"可选周次: {available_weeks()}"}
    return {"week": w, "content": content}


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
    for meta in store_list_reports():
        text = read_report_text(meta.week)
        if text is None:
            continue
        lines = text.splitlines()
        for lineno, line in enumerate(lines, 1):
            if kw in line.lower():
                total += 1
                if len(matches) < limit:
                    matches.append({
                        "week": meta.week,
                        "line": lineno,
                        "text": line.strip(),
                    })
    return {"matches": matches, "total": total, "truncated": total > len(matches)}


if __name__ == "__main__":
    mcp.run()
