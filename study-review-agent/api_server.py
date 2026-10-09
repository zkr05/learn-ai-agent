# -*- coding: utf-8 -*-
"""study-review agent 的 HTTP 服务层：把复盘能力包成可调用的接口。

启动方式（在 study-review-agent 目录下执行）：
    uvicorn api_server:app --reload --port 8000

自动生成的接口文档（浏览器打开）：
    http://127.0.0.1:8000/docs
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from reports_store import (available_weeks, normalize_week, read_report_text,
                           report_files, week_of)
from review_agent import run_once

app = FastAPI(title="study-review agent API", version="0.1")


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


@app.post("/report")
def create_report(req: ReportRequest) -> dict:
    """跑一次复盘，生成报告，返回结果摘要。

    注意：这一步要调 LLM（本地后端约 20 秒），Day 3 会改成后台任务。
    """
    result = run_once(backend=req.backend, days=req.days)
    return result


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

