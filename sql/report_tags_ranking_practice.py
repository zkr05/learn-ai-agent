"""标签排行榜练习。

填写 QUERY_1。沿用第二课的内存数据库，每次运行重新建库。
本题要求结果行的先后顺序一致。
在本文件所在目录运行：python report_tags_ranking_practice.py

状态：完成（2026-11-12，补上分组后通过顺序验收）
复盘：先按标签分组计数，再排序和限制行数。省略分组会把全表记录合为一组。
"""

import sqlite3
import sys
from contextlib import closing

from report_tags_having_practice import SCHEMA_AND_DATA

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# 找使用最多的三个标签，返回 tag、report_count 两列。
# 先按次数从大到小排。同次数按标签名升序，再取前 3 行。
QUERY_1 = """
SELECT rt.tag, COUNT(rt.tag) AS report_count
FROM report_tags AS rt
GROUP BY rt.tag
ORDER BY report_count DESC, tag ASC
LIMIT 3
"""


def main() -> int:
    if not QUERY_1.strip():
        print("题 1：待填写 SQL")
        return 1
    expected = [("SQLite", 3), ("FastAPI", 2), ("Pandas", 1)]
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.executescript(SCHEMA_AND_DATA)
        connection.execute("PRAGMA query_only = ON")
        try:
            actual = connection.execute(QUERY_1).fetchall()
        except sqlite3.Error as error:
            print(f"❌ 查询报错：{error}")
            return 1
    if actual != expected:
        print(f"❌ 结果或顺序不符\n   实际：{actual}\n   预期：{expected}")
        return 1
    print("✅ 标签排行榜查询通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
