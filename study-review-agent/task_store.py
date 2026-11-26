# -*- coding: utf-8 -*-
"""用本地 SQLite 保存 HTTP 复盘任务，独立于周报正文存储。"""

import json
import os
import sqlite3
import uuid
from contextlib import closing
from pathlib import Path
from typing import Literal


DEFAULT_DB = Path(__file__).resolve().parent / ".local" / "tasks.db"
INTERRUPTED_MESSAGE = "服务重启前任务未结束，请重新提交。"
TaskStatus = Literal["pending", "running", "done", "error"]


class TaskStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    @classmethod
    def from_env(cls) -> "TaskStore":
        return cls(Path(os.environ.get("STUDY_TASK_DB_PATH") or DEFAULT_DB).expanduser())

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        """单实例启动：保留已结束任务，将前次未完成的任务标记为失败。"""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as conn, conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id     TEXT PRIMARY KEY NOT NULL,
                    status      TEXT NOT NULL CHECK (status IN ('pending', 'running', 'done', 'error')),
                    backend     TEXT NOT NULL,
                    days        INTEGER NOT NULL,
                    result_json TEXT,
                    error       TEXT,
                    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                UPDATE tasks SET status = 'error', error = ?, updated_at = CURRENT_TIMESTAMP
                WHERE status IN ('pending', 'running')
                """,
                (INTERRUPTED_MESSAGE,),
            )

    def create(self, backend: str, days: int) -> str:
        """提交待处理任务后，再允许调用方把它交给后台线程。"""
        with closing(self._connect()) as conn, conn:
            for _ in range(5):
                task_id = uuid.uuid4().hex[:8]
                cursor = conn.execute(
                    """
                    INSERT INTO tasks (task_id, status, backend, days) VALUES (?, 'pending', ?, ?)
                    ON CONFLICT(task_id) DO NOTHING
                    """,
                    (task_id, backend, days),
                )
                if cursor.rowcount == 1:
                    return task_id
        raise RuntimeError("无法分配新的任务 ID")

    def read(self, task_id: str) -> dict | None:
        with closing(self._connect()) as conn:
            row = conn.execute(
                "SELECT task_id, status, backend, days, result_json, error FROM tasks WHERE task_id = ?",
                (task_id,),
            ).fetchone()
        if row is None:
            return None
        task = dict(row)
        result_json = task.pop("result_json")
        task["result"] = json.loads(result_json) if result_json is not None else None
        return task

    def _transition(
        self, task_id: str, previous: TaskStatus, status: TaskStatus,
        *, result_json: str | None = None, error: str | None = None,
    ) -> bool:
        # 把状态检查和修改合并成一条 SQL，避免两个线程同时领取同一任务。
        with closing(self._connect()) as conn, conn:
            cursor = conn.execute(
                """
                UPDATE tasks SET status = ?, result_json = ?, error = ?, updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ? AND status = ?
                """,
                (status, result_json, error, task_id, previous),
            )
            return cursor.rowcount == 1

    def start(self, task_id: str) -> bool:
        return self._transition(task_id, "pending", "running")

    def complete(self, task_id: str, result: dict) -> bool:
        return self._transition(task_id, "running", "done", result_json=json.dumps(result, ensure_ascii=False))

    def fail(self, task_id: str, error: str) -> bool:
        return self._transition(task_id, "running", "error", error=error)
