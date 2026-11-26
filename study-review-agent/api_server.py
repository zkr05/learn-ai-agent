# -*- coding: utf-8 -*-
"""study-review agent 的 HTTP 服务层：把复盘能力包成可调用的接口。

启动方式（在 study-review-agent 目录下执行）：
    uvicorn api_server:app --reload --port 8000

自动生成的接口文档（浏览器打开）：
    http://127.0.0.1:8000/docs
"""

import logging
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from contextlib import asynccontextmanager
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from datetime import datetime
from typing import Literal

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from reports_store import (available_weeks, normalize_week, read_report_text,
                           list_reports as store_list_reports, backend_name)
from review_agent import run_once
from task_store import TaskStore

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 一个任务库只对应一个 API 进程；启动时把上次中断的任务归为失败。
    store = TaskStore.from_env()
    store.initialize()
    app.state.task_store = store
    yield


app = FastAPI(title="study-review agent API", version="0.1", lifespan=lifespan)

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


class ReportSummary(BaseModel):
    """单份周报的目录信息（/reports 列表里的一项）。"""

    week: str
    file: str
    size_bytes: int
    modified: str


class ReportList(BaseModel):
    """GET /reports 的响应体：外面套一层对象，以后加 total/cursor 不破坏兼容。"""

    reports: list[ReportSummary]


@app.get("/health")
def health() -> dict:
    """健康检查：服务活着就返回 ok，并报出当前用的是哪个存储后端。

    把 store 报出来是为了能一眼确认 STUDY_STORE 生效了 —— 否则切完后端
    服务照样能起，你分不清到底是切成功了还是根本没读环境变量。
    """
    return {"status": "ok", "store": backend_name()}


# ---------------------------------------------------------------- 后台任务
def _run_report_task(store: TaskStore, task_id: str, backend: str, days: int) -> None:
    """跑一次复盘，保存终态。模型调用期间不持有 SQLite 写事务。

    注意：这是**同步函数**（def）。run_once 里全是阻塞调用（OpenAI 同步客户端 + git 子进程），
         所以要让 FastAPI 把它丢进线程池。写成 async def 会堵死整个事件循环。
    """
    if not store.start(task_id):
        return
    try:
        result = run_once(backend=backend, days=days)
    except Exception as exc:
        # 原始异常可能带有模型服务的请求信息，不把它写进持久库或接口。
        error = f"{type(exc).__name__}: 复盘任务失败。"
        logger.error("复盘任务 %s 失败 (%s)", task_id, type(exc).__name__)
        store.fail(task_id, error)
    else:
        store.complete(task_id, result)


@app.post("/report", status_code=202)
def create_report(req: ReportRequest, background: BackgroundTasks, request: Request) -> dict:
    """登记一次复盘任务，**立刻**返回 202；进度用 GET /tasks/{task_id} 查。

    为什么是 202：HTTP 语义 =「请求我收到了，但还没做完」。
    和 200 的区别 —— 200 意味着内容已经躺在响应体里了。
    """
    store: TaskStore = request.app.state.task_store
    task_id = store.create(req.backend, req.days)
    background.add_task(_run_report_task, store, task_id, req.backend, req.days)
    return {"task_id": task_id, "status": "pending", "poll": f"/tasks/{task_id}"}


@app.get("/tasks/{task_id}")
def read_task(task_id: str, request: Request) -> dict:
    """查询后台任务的状态和结果。"""
    store: TaskStore = request.app.state.task_store
    task = store.read(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"没有 {task_id} 这个任务",
        )
    return task


@app.get("/reports", response_model=ReportList)
def list_reports() -> dict:
    """列出所有周报的目录信息（周次、文件名、大小、修改日期），不返回正文。

    只想看某一周的正文，用 GET /reports/{week}。
    """
    reports = []
    for m in store_list_reports():
        reports.append({
            "week": m.week,
            "file": f"{m.week}-review.md",
            "size_bytes": m.size_bytes,
            # 契约里 modified 是 ISO(UTC)；展示要转回本地时区，否则凌晨写的报告会差一天
            "modified": datetime.fromisoformat(m.modified).astimezone().strftime("%Y-%m-%d"),
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

