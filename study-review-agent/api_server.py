# -*- coding: utf-8 -*-
"""study-review agent 的 HTTP 服务层：把复盘能力包成可调用的接口。

启动方式（在 study-review-agent 目录下执行）：
    uvicorn api_server:app --reload --port 8000

自动生成的接口文档（浏览器打开）：
    http://127.0.0.1:8000/docs
"""

import sys
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from datetime import datetime
from typing import Literal

from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from reports_store import (available_weeks, normalize_week, read_report_text,
                           report_files, week_of)
from review_agent import run_once

app = FastAPI(title="study-review agent API", version="0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReportRequest(BaseModel):
    """触发一次复盘的请求体。"""

    backend: Literal["local", "cloud", "auto"] = Field(
        "auto",
        description="模型后端：local 用本机 Ollama，cloud 用云端 API，auto 自动探测",
    )

    days: int = Field(
        7, ge=1, le=90,
        description="复盘最近多少天的数据（1~90）",
    )


@app.get("/health")
def health() -> dict:
    """健康检查：服务活着就返回 ok。"""
    return {"status": "ok"}


# ---------------------------------------------------------------- 后台任务
# 任务表：进程内的内存字典。
# 它的寿命 == 进程的寿命 —— 服务一重启，所有任务记录就没了。这就是要用 Celery/Redis 的原因。
TASKS: dict[str, dict] = {}

# 状态流转：pending（已登记）-> running（正在跑）-> done / error


def _run_report_task(task_id: str, backend: str, days: int) -> None:
    """真正干活的地方：跑一次复盘，把结果写回 TASKS。

    注意：这是**同步函数**（def）。run_once 里全是阻塞调用（OpenAI 同步客户端 + git 子进程），
         所以要让 FastAPI 把它丢进线程池。写成 async def 会堵死整个事件循环。
    """
    TASKS[task_id]["status"] = "running"
    try:
        result = run_once(backend=backend, days=days)
        TASKS[task_id].update(status="done", result=result)
    except Exception as e:
        # 后台线程抛出的异常不会进任何响应体 —— 不捕获的话客户端只会永远看到 running，
        # 只留一行 traceback 在控制台，这就是「静默失败」。所以异常也要当成数据存下来。
        TASKS[task_id].update(status="error", error=f"{type(e).__name__}: {e}")


@app.post("/report", status_code=202)
def create_report(req: ReportRequest, background: BackgroundTasks) -> dict:
    """登记一次复盘任务，**立刻**返回 202；进度用 GET /tasks/{task_id} 查。

    为什么是 202：HTTP 语义 =「请求我收到了，但还没做完」。
    和 200 的区别 —— 200 意味着内容已经躺在响应体里了。
    """
    task_id = uuid.uuid4().hex[:8]
    # 先登记、再丢后台。反过来的话，客户端可能在任务还没登记时就拿 id 来查，查不到。
    TASKS[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "backend": req.backend,
        "days": req.days,
        "result": None,
        "error": None,
    }
    background.add_task(_run_report_task, task_id, req.backend, req.days)
    return {"task_id": task_id, "status": "pending", "poll": f"/tasks/{task_id}"}


@app.get("/tasks/{task_id}")
def read_task(task_id: str) -> dict:
    """查询后台任务的状态和结果。"""
    task = TASKS.get(task_id)
    if task is None:
        # 404：服务重启过、或者 id 本来就拼错了
        raise HTTPException(
            status_code=404,
            detail=f"没有 {task_id} 这个任务（任务表在服务重启后会清空）",
        )
    return task


@app.get("/reports")
def list_reports() -> dict:
    """列出所有周报的目录信息（周次、文件名、大小、修改日期），不返回正文。

    只想看某一周的正文，用 GET /reports/{week}。
    """
    reports = []
    for f in report_files():
        stat = f.stat()
        reports.append({
            "week": week_of(f),
            "file": f.name,
            "size_bytes": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
        })
    return {"reports": reports}


@app.get("/reports/{week}")
def read_report(week: str) -> dict:
    """读取指定周次的周报正文。

    Args:
        week: 周次，形如 2026-W39（也接受 W39 / 2026-w39 等写法）。
    """
    w = normalize_week(week)
    if w is None:
        # 400：参数本身不合法 —— 客户端该改格式
        raise HTTPException(
            status_code=400,
            detail=f"无法识别的周次：{week}。请用 2026-W39 这样的格式。",
        )

    content = read_report_text(w)
    if content is None:
        # 404：参数合法，但服务器上确实没有这个资源
        raise HTTPException(
            status_code=404,
            detail=f"没有 {w} 的周报。可选周次: {available_weeks()}",
        )

    return {"week": w, "content": content}

