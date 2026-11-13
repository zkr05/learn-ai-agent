"""用 CASE WHEN 同时统计周报标签总数和非 SQLite 标签数。

填写 QUERY_1。每次运行都使用新的 SQLite 内存库。
返回列为 week、tag_count、other_tag_count，按 week 升序。
在本文件所在目录运行 python report_tags_case_practice.py。

状态：完成（2026-11-12，两种计数和排序均通过验收）
复盘：W46 的 rt.tag 是 NULL，WHEN 条件未成立，CASE 取 ELSE 0。
SUM 把 CASE 为每条记录产生的 0 或 1 加起来。
"""

import sqlite3
import sys
from contextlib import closing

from report_tags_having_practice import SCHEMA_AND_DATA

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# 每份周报输出一行，保留标签数为零的周报。
# 同时计算全部标签数，以及不等于 SQLite 的标签数。
# 用 SUM(CASE WHEN ... THEN 1 ELSE 0 END) 做条件计数。
QUERY_1 = """
SELECT r.week,
       COUNT(rt.tag) AS tag_count,
       SUM(CASE WHEN rt.tag != 'SQLite' THEN 1 ELSE 0 END) AS other_tag_count
FROM reports AS r
LEFT JOIN report_tags AS rt ON r.week = rt.week
GROUP BY r.week
ORDER BY r.week ASC
"""


def main() -> int:
    if not QUERY_1.strip():
        print("题 1：待填写 SQL")
        return 1
    expected = [
        ("2026-W44", 2, 1),
        ("2026-W45", 1, 0),
        ("2026-W46", 0, 0),
        ("2026-W47", 3, 2),
        ("2026-W48", 1, 1),
    ]
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
    print("✅ CASE WHEN 标签统计通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
