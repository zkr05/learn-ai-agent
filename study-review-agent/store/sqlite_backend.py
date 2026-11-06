# -*- coding: utf-8 -*-
"""SQLite 后端：一张表存全部报告。

为什么值得存在（面试会问）：
    文件后端的瓶颈不是"读得慢"，而是"没有事务、没有并发控制、没法按条件查"。
    一旦要支持多用户 / 并发写入 / 查询某段时间，文件就不够用了。

为什么默认不用它（面试也会问）：
    单用户、无并发写、报告是静态产物 —— 文件更简单，还能被 git 追踪、
    直接被静态站点复制。**默认用简单的，需要时才换。**
"""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from contextlib import closing

from store.base import ReportMeta

_DEFAULT_DB = Path(__file__).resolve().parent.parent / "reports.db"
DB_PATH = Path(os.environ.get("STUDY_DB_PATH") or _DEFAULT_DB)


def _connect() -> sqlite3.Connection:
    """开一个连接。

    ⚠️ 每次操作都新开连接：sqlite3 的连接默认不能跨线程使用，
       而 FastAPI 会把同步端点丢进线程池 —— 全局共享一个连接会炸。
       SQLite 开连接很便宜（本地文件），不用连接池。
    """
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row      # 让结果能 row["week"] 这样取值
    return conn


def init_db() -> None:
    """建表（幂等，可以重复调用）。"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS reports (
                week       TEXT PRIMARY KEY,
                content    TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


# ---------------------------------------------------------------- 后端契约 4 件套

def available_weeks() -> list[str]:
    """只要周次，升序。

    这是已经写好的样例 —— 看它怎么"开连接 / 执行 / 取列"，
    下面三个 TODO 都是同一个套路。
    """
    with closing(_connect()) as conn:
        rows = conn.execute("SELECT week FROM reports ORDER BY week").fetchall()
    return [r["week"] for r in rows]


def read_report_text(week: str) -> str | None:
    """读正文；没有这一周返回 None。"""
    with closing(_connect()) as conn:
        row = conn.execute(
            "SELECT content FROM reports WHERE week = ?",
            (week,),
        ).fetchone()
    if row is None:
        return None
    return row["content"]


def write_report(week: str, text: str, created_at: str | None = None) -> None:
    """写入/覆盖一周的报告。要求幂等。

    created_at 不为空时用它当时间戳（迁移/回填），否则用当前 UTC 时间。
    """
    init_db()
    stamp = created_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    with closing(_connect()) as conn, conn:
        conn.execute(
            """
            INSERT INTO reports (week, content, created_at) VALUES (?, ?, ?)
            ON CONFLICT(week) DO UPDATE SET
                content    = excluded.content,
                created_at = excluded.created_at
            """,
            (week, text, stamp),
        )

def list_reports() -> list[ReportMeta]:
    """全部报告元信息，按 week 升序。"""
    with closing(_connect()) as conn:
        rows = conn.execute(
            "SELECT week, content, created_at FROM reports ORDER BY week"
        ).fetchall()

    return [
        ReportMeta(
            week=r["week"],
            size_bytes=len(r["content"].encode("utf-8")),
            modified=r["created_at"],
        )
        for r in rows
    ]
