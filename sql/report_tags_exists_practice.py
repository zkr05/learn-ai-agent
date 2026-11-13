"""用 NOT EXISTS 查周报。

填写 QUERY_1 和 QUERY_2。每次运行都使用新的 SQLite 内存库。
返回列为 week、content，行顺序不限。
在本文件所在目录运行 python report_tags_exists_practice.py。

状态：完成（2026-11-12，题 1 根据提示修改，两条查询均通过验收）
自述：去掉 rt.week = r.week 后，子查询会在整张标签表里找 SQLite。
只要表里有一条匹配，每份周报的 NOT EXISTS 都为假，外层返回零行。
"""

import sqlite3
import sys
from collections import Counter
from contextlib import closing

from report_tags_having_practice import SCHEMA_AND_DATA

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# 题 1。用 NOT EXISTS 找出没有任何标签的周报。
QUERY_1 = """
SELECT r.week, r.content
FROM reports AS r
WHERE NOT EXISTS(
    SELECT 1
    FROM report_tags AS rt
    WHERE rt.week = r.week);
"""

# 题 2。用 NOT EXISTS 找出没有 SQLite 标签的周报。
# 没有任何标签和只有其他标签的周报都符合条件。
QUERY_2 = """
SELECT r.week, r.content
FROM reports AS r
WHERE NOT EXISTS(
    SELECT 1
    FROM report_tags AS rt
    WHERE rt.week = r.week AND rt.tag = 'SQLite')
"""


def main() -> int:
    exercises = (
        ("题 1", QUERY_1, [("2026-W46", "日志分析")]),
        ("题 2", QUERY_2, [("2026-W46", "日志分析"), ("2026-W48", "Python 复习")]),
    )
    passed = 0
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.executescript(SCHEMA_AND_DATA)
        connection.execute("PRAGMA query_only = ON")
        for title, query, expected in exercises:
            if not query.strip():
                print(f"{title}：待填写 SQL")
                continue
            try:
                actual = connection.execute(query).fetchall()
            except sqlite3.Error as error:
                print(f"❌ {title}：{error}")
                continue
            if Counter(actual) == Counter(expected):
                print(f"✅ {title}通过")
                passed += 1
            else:
                print(f"❌ {title}\n   实际：{actual}\n   预期：{expected}")
    return 0 if passed == len(exercises) else 1


if __name__ == "__main__":
    raise SystemExit(main())
