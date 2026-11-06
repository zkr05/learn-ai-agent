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
    out = []
    for path in report_files():
        st = path.stat()
        out.append(ReportMeta(
            week=week_of(path),
            # ⚠️ 不能用 st.st_size：Windows 上工作区文件是 CRLF，磁盘字节比内容字节多。
            #    契约定义是"正文的 UTF-8 字节数"，所以读出来按 LF 再算。
            size_bytes=len(path.read_text(encoding="utf-8").encode("utf-8")),
            modified=(
                datetime.fromtimestamp(st.st_mtime, tz=timezone.utc)
                .replace(microsecond=0)

                .isoformat()
            ),
        ))

    out.sort(key=lambda item: item.week)
    return out


def read_report_text(week: str) -> str | None:
    """读正文；文件不存在返回 None。"""
    path = report_path(week)
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def write_report(week: str, text: str, created_at: str | None = None) -> None:
    """写入/覆盖一周的报告。要求幂等。

    created_at 不为空时把文件修改时间改成它 —— 迁移/回填时用来保留历史时间。
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path(week).write_text(text, encoding="utf-8", newline="")
    if created_at:
        ts = datetime.fromisoformat(created_at).timestamp()
        os.utime(report_path(week), (ts, ts))


def available_weeks() -> list[str]:
    """只要周次，升序。"""
    return [week_of(p) for p in report_files()]
