# -*- coding: utf-8 -*-
"""把 reports/ 里的正式周报打包成一个 docsify 静态站点（输出到 _site/）。

构建=装配（不是把 md 翻成 html，翻译是浏览器里的 docsify 干的）。
诊断/构建产物目录 _site/ 可随时删掉重建，源数据始终只有 reports/ 一份。
"""

import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from reports_store import report_files, week_of

AGENT_DIR = Path(__file__).resolve().parent
SITE_DIR = AGENT_DIR / "site"
OUT_DIR = AGENT_DIR / "_site"


def build() -> None:
    # 1) 清空重建：构建必须幂等，否则上一轮的残留会跟着发布出去
    shutil.rmtree(OUT_DIR, ignore_errors=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 2) docsify 外壳
    shutil.copy2(SITE_DIR / "index.html", OUT_DIR / "index.html")

    # 3) .nojekyll：挡掉 Jekyll 的"_ 开头文件是保留命名"规则
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    # 4) 报告正文：复制进发布目录
    reports = sorted(report_files(), reverse=True)
    dest = OUT_DIR / "reports"
    dest.mkdir(parents=True, exist_ok=True)
    for path in reports:
        shutil.copy2(path, dest / path.name)

    # 5) 侧边栏：docsify 不会自己知道有哪些文件，得给它一份清单
    sidebar = "".join(f"* [{week_of(p)}](reports/{p.name})\n" for p in reports)
    (OUT_DIR / "_sidebar.md").write_text(sidebar or "* （暂无报告）\n", encoding="utf-8")

    # 6) 首页
    if reports:
        newest = reports[0]
        home = (
            "# 学习复盘周报\n\n"
            f"这是 `learn-ai-agent` 每周自动生成的学习复盘归档，目前共 **{len(reports)}** 篇，"
            "每周一由 GitHub Actions 自动更新。\n\n"
            f"最新一期：**[{week_of(newest)}](reports/{newest.name})**\n"
        )
    else:
        home = "# 学习复盘周报\n\n暂无报告。\n"
    (OUT_DIR / "_home.md").write_text(home, encoding="utf-8")

    # 7) 摘要（CI 日志里能看到）
    print(f"构建完成：{len(reports)} 篇报告 -> {OUT_DIR}")
    for path in reports:
        print(f"  - {week_of(path)}")


if __name__ == "__main__":
    build()
