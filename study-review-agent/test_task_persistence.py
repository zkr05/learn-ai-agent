# -*- coding: utf-8 -*-
"""使用临时 SQLite 和替代的复盘函数，验证任务接口以及跨进程持久化。"""

import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi.testclient import TestClient

import api_server
from task_store import INTERRUPTED_MESSAGE, TaskStore


def check_restart(path: Path) -> None:
    result = {
        "backend": "local",
        "file": "2026-W48-review.local.md",
        "tokens": {"input": 120, "output": 50},
        "cost": None,
        "stats": [{"stage": "生成周报", "elapsed": 0.2}],
    }
    request = {"backend": "local", "days": 7}
    with TestClient(api_server.app) as client:
        task_store = api_server.app.state.task_store
        with patch.object(api_server, "run_once", return_value=result) as run_once:
            started = client.post("/report", json=request)
            invalid = client.post("/report", json={"days": 0})
        assert started.status_code == 202 and invalid.status_code == 422
        run_once.assert_called_once_with(**request)
        task_id = started.json()["task_id"]
        poll = f"/tasks/{task_id}"
        assert started.json() == {"task_id": task_id, "status": "pending", "poll": poll}
        successful = {"task_id": task_id, **request, "status": "done", "result": result, "error": None}
        assert client.get(poll).json() == successful

        with patch.object(api_server, "run_once", side_effect=RuntimeError("simulated private detail")):
            failure = client.post("/report", json=request)
        assert failure.status_code == 202
        failed = failure.json()["task_id"]
        failed_body = client.get(f"/tasks/{failed}").json()
        assert failed_body["status"] == "error" and failed_body["result"] is None
        assert "RuntimeError" in failed_body["error"] and "private detail" not in failed_body["error"]
        assert task_store.path == path
        assert client.get("/tasks/missing").status_code == 404

        # 模拟上次进程退出时尚未结束的两类任务。
        pending_id = task_store.create("auto", 14)
        running_id = task_store.create("auto", 14)
        assert task_store.start(running_id)

    # 用新的 Python 进程和同一个数据库文件，证明不是应用内存留下的结果。
    urls = [poll, f"/tasks/{failed}", f"/tasks/{pending_id}", f"/tasks/{running_id}"]
    program = """
import json
import sys
from fastapi.testclient import TestClient
from api_server import app
with TestClient(app) as client:
    print(json.dumps([client.get(path).json() for path in sys.argv[1:]]))
"""
    proc = subprocess.run(
        [sys.executable, "-X", "utf8", "-B", "-c", program, *urls],
        cwd=Path(__file__).resolve().parent,
        capture_output=True, text=True, encoding="utf-8", timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    restored, failed_again, pending, running = json.loads(proc.stdout)
    assert restored == successful and failed_again == failed_body
    for task in (pending, running):
        assert task["status"] == "error" and task["error"] == INTERRUPTED_MESSAGE
        assert task["result"] is None


def check_transition(path: Path) -> None:
    store = TaskStore(path)
    store.initialize()
    task_id = store.create("auto", 7)
    assert store.read(task_id)["status"] == "pending"
    # 独立连接竞争同一个任务，只允许其中一个线程领取。
    with ThreadPoolExecutor(max_workers=4) as executor:
        assert sum(executor.map(store.start, [task_id] * 4)) == 1
    assert store.read(task_id)["status"] == "running"
    assert store.complete(task_id, {"ok": True})
    assert not store.fail(task_id, "重复完成不应覆盖原结果")
    assert store.read(task_id)["result"] == {"ok": True}


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as temp:
        db_path = Path(temp) / "api.db"
        with patch.dict(os.environ, {"STUDY_TASK_DB_PATH": str(db_path)}):
            check_restart(db_path)
        print("✅ 任务接口、错误状态和跨进程恢复检查通过")
        check_transition(Path(temp) / "transition.db")
        print("✅ 并发领取仅成功一次，已完成任务不可被覆盖")
