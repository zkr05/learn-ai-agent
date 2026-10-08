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

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal

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


# ---------------------------------------------------------------- 今日清单
# [ ] 1. 把 review_agent.py 里 main() 那段抽成 run_once(backend, days) -> dict
# [ ] 2. 跑 python review_agent.py --backend local 确认行为不变
# [ ] 3. 补完上面三个 TODO
# [ ] 4. uvicorn api_server:app --reload --port 8000 起服务
# [ ] 5. 浏览器打开 http://127.0.0.1:8000/docs 点着试
