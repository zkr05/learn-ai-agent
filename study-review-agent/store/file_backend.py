# -*- coding: utf-8 -*-
"""文件后端：reports/YYYY-Www-review.md 一个文件一篇。

这是项目的默认后端 —— 报告天然是静态产物，一个文件就是一次发布单元，
git 能追踪每次变化，静态站点直接复制即可。
"""

import os
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from store.base import ReportMeta

_DEFAULT_REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
REPORTS_DIR = Path(os.environ.get("STUDY_REPORTS_DIR") or _DEFAULT_REPORTS_DIR)

REPORTS_GLOB = "????-W??-review.md"


def report_files() -> list[Path]:
    """文件后端的私有细节：按周次排序的 md 文件列表。

    ⚠️ 只给「必须有文件」的地方用（例如 build_reports_site 要 copy2）。
       业务逻辑请用 list_reports()，别用这个。
    """
    return sorted(REPORTS_DIR.glob(REPORTS_GLOB))


def week_of(path: Path) -> str:
    """'2026-W39-review.md' -> '2026-W39'"""
    return path.name.removesuffix("-review.md")


def report_path(week: str) -> Path:
    return REPORTS_DIR / f"{week}-review.md"


# ---------------------------------------------------------------- 后端契约 4 件套

def list_reports() -> list[ReportMeta]:
    """全部报告元信息，按 week 升序。"""
    # TODO 1：遍历 report_files()，为每个文件造一个 ReportMeta
    #   1) week = week_of(path)
    #   2) st = path.stat()
    #   3) size_bytes 用 st.st_size（文件字节数）
    #   4) modified 用 datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
    #        .replace(microsecond=0).isoformat()
    #      注意：.isoformat() 的输出要能被 fromisoformat() 读回来，
    #      否则契约测试里"两个后端 time 字段格式一致"这条会挂。
    #   ---
    #   或者更省事：直接复用磁盘上的真实值，别自己编时间。
    raise NotImplementedError("file_backend.list_reports")


def read_report_text(week: str) -> str | None:
    """读正文；文件不存在返回 None。"""
    path = report_path(week)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def write_report(week: str, text: str) -> None:
    """写入/覆盖一周的报告。要求幂等。"""
    # TODO 2：写文件
    #   1) REPORTS_DIR.mkdir(parents=True, exist_ok=True)   # 目录可能不存在
    #   2) report_path(week).write_text(text, encoding="utf-8")
    #   幂等性由"覆盖写"天然满足 —— 想想为什么文件后端不需要 UPSERT 这种语法。
    raise NotImplementedError("file_backend.write_report")


def available_weeks() -> list[str]:
    """只要周次，升序。"""
    return [week_of(p) for p in report_files()]