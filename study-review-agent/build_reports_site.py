# -*- coding: utf-8 -*-
"""把报告打包成一个 docsify 静态站点（输出到 _site/）。

构建=装配（不是把 md 翻成 html，翻译是浏览器里的 docsify 干的）。
诊断/构建产物目录 _site/ 可随时删掉重建，源数据始终只有存储层一份。

⚠️ 站点需要**真实文件**：docsify 用 XHR 去拉 .md。
    所以不管存储层是 file 还是 sqlite，这里都统一「读内容 -> 写出文件」。
"""

import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from reports_store import list_reports, read_report_text

AGENT_DIR = Path(__file__).resolve().parent
SITE_DIR = AGENT_DIR / "site"
OUT_DIR = AGENT_DIR / "_site"


def build() -> None:
    # 1) 清空重建：构建必须幂等，否则上一轮的残留会跟着发布出去
    shutil.rmtree(OUT_DIR, ignore_errors=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 2) docsify 外壳（这是站点资源，不是报告数据）
    shutil.copy2(SITE_DIR / "index.html", OUT_DIR / "index.html")

    # 3) .nojekyll：挡掉 Jekyll 的"_ 开头文件是保留命名"规则
    (OUT_DIR / ".nojekyll").write_text("", encoding="utf-8")

    # 4) 报告正文：从存储层读出来，写成 docsify 能拉的文件（新 -> 旧）
    dest = OUT_DIR / "reports"
    dest.mkdir(parents=True, exist_ok=True)
    weeks: list[str] = []
    for meta in reversed(list_reports()):
        text = read_report_text(meta.week)
        if text is None:                      # 理论上不会发生，防御一下
            print(f"  ⚠️ 读不到 {meta.week}，跳过")
            continue
        (dest / f"{meta.week}-review.md").write_text(text, encoding="utf-8", newline="")
        weeks.append(meta.week)

    # 5) 侧边栏：docsify 不会自己知道有哪些文件，得给它一份清单
    sidebar = "".join(f"* [{w}](reports/{w}-review.md)\n" for w in weeks)
    (OUT_DIR / "_sidebar.md").write_text(sidebar or "* （暂无报告）\n", encoding="utf-8")

    # 6) 首页
    if weeks:
        home = (
            "# 学习复盘周报\n\n"
            f"这是 `learn-ai-agent` 每周自动生成的学习复盘归档，目前共 **{len(weeks)}** 篇，"
            "每周一由 GitHub Actions 自动更新。\n\n"
            f"最新一期：**[{weeks[0]}](reports/{weeks[0]}-review.md)**\n"
        )
    else:
        home = "# 学习复盘周报\n\n暂无报告。\n"
    (OUT_DIR / "_home.md").write_text(home, encoding="utf-8")

    # 7) 摘要（CI 日志里能看到）
    print(f"构建完成：{len(weeks)} 篇报告 -> {OUT_DIR}")
    for w in weeks:
        print(f"  - {w}")


if __name__ == "__main__":
    build()