# -*- coding: utf-8 -*-
"""报告仓库的门面 —— 上层只认这里的函数名，不认存储方式。

选后端（环境变量）：
    STUDY_STORE=file     默认。reports/YYYY-Www-review.md，一文件一篇
    STUDY_STORE=sqlite   reports.db 一张表。首次使用先跑 migrate_to_sqlite.py

为什么要有这一层：
    以前 report_files() 直接返回 list[Path]，上层因此学会了
    path.read_text() / shutil.copy2() / path.name ——
    "存储是文件"这个决定被复制到了 3 个文件里，换存储就得改 3 处。
    现在上层只依赖本模块的函数名，具体存哪里由后端决定。

约束：本模块只允许依赖标准库 + store 包。
      不许 import fastapi / fastmcp —— 否则上层会被迫装上不需要的依赖。
"""

import os
import re

from store import file_backend, sqlite_backend
from store.base import ReportMeta

# 唯一保留的路径导出：review_agent 用它定位 run_log.jsonl 和本地草稿。
# 这属于"运行日志 / 临时产物"职责，不是"报告存储"职责。
# 报告本身的读写一律走上面的 5 个函数 —— 之前导出的 report_files / week_of /
# report_path 已经全部删除，上层再也拿不到 Path 了。
from store.file_backend import REPORTS_DIR  # noqa: F401

_BACKENDS = {"file": file_backend, "sqlite": sqlite_backend}


def _backend_name() -> str:
    """解析 STUDY_STORE；名字写错立刻报错，不静默降级。"""
    name = (os.environ.get("STUDY_STORE") or "file").strip().lower()
    if name not in _BACKENDS:
        raise ValueError(f"未知的 STUDY_STORE={name!r}，可选：{sorted(_BACKENDS)}")
    return name


def _backend():
    """按 STUDY_STORE 选后端。"""
    return _BACKENDS[_backend_name()]


def backend_name() -> str:
    """当前生效的后端名（file / sqlite）—— 给健康检查和日志用。"""
    return _backend_name()


# ---------------------------------------------------------------- 后端无关的接口

def list_reports() -> list[ReportMeta]:
    """全部报告元信息，按 week 升序（旧 -> 新）。"""
    return _backend().list_reports()


def read_report_text(week: str) -> str | None:
    """读某周报告全文；没有返回 None。

    注意：本函数不表达「错误」—— 是 None 就是事实，怎么报错由上层决定
         （MCP 层返回 error 字典，HTTP 层返回 404）。
    """
    return _backend().read_report_text(week)


def write_report(week: str, text: str, created_at: str | None = None) -> None:
    """写入/覆盖一周报告（幂等）。created_at 可选，用于迁移/回填保留历史时间。"""
    return _backend().write_report(week, text, created_at)


def available_weeks() -> list[str]:
    """当前可用的周次列表，例如 ["2026-W38", "2026-W39"]。"""
    return _backend().available_weeks()


# ---------------------------------------------------------------- 纯函数（与存储无关）

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
