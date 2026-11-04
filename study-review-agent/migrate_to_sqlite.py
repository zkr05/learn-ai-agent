# -*- coding: utf-8 -*-
"""把 reports/*.md 迁移进 SQLite。**幂等**，可以反复跑。

用法：
    python migrate_to_sqlite.py                 # 迁到默认 reports.db
    STUDY_DB_PATH=xx.db python migrate_to_sqlite.py

迁移完用 SQLite 后端启动：
    STUDY_STORE=sqlite python -m uvicorn api_server:app --port 8000
"""

import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from store import file_backend, sqlite_backend


def main() -> int:
    # 1) 建表
    sqlite_backend.init_db()

    # 2) 逐个文件比对：DB 里没有的才写（幂等靠这一步，不靠 UPSERT）
    weeks = file_backend.available_weeks()
    if not weeks:
        print("reports/ 里没有报告，什么也没做")
        return 0

    added, skipped = [], []
    for week in weeks:
        if sqlite_backend.read_report_text(week) is not None:
            skipped.append(week)
            continue
        text = file_backend.read_report_text(week)
        if text is None:                      # 理论不会发生，防御一下
            print(f"  ⚠️ 读不到 {week}，跳过")
            continue
        sqlite_backend.write_report(week, text)
        added.append(week)

    # 3) 报告
    db = sqlite_backend.DB_PATH
    size = db.stat().st_size if db.exists() else 0
    print(f"数据库：{db}（{size / 1024:.1f} KB）")
    print(f"新增 {len(added)} 篇" + (f"：{', '.join(added)}" if added else ""))
    print(f"已存在跳过 {len(skipped)} 篇" + (f"：{', '.join(skipped)}" if skipped else ""))

    # 4) 自检：DB 里的周次集合必须和文件一致
    db_weeks = sqlite_backend.available_weeks()
    if sorted(db_weeks) != sorted(weeks):
        print(f"⚠️ 不一致！文件 {len(weeks)} 篇，DB {len(db_weeks)} 篇")
        return 1
    print(f"✅ 校验通过：{len(db_weeks)} 篇，文件与 DB 周次一致")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())