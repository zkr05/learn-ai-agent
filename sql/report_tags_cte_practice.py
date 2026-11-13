"""用 WITH 找出需要补标签的周报。

填写 QUERY_1。每次运行都使用新的 SQLite 内存库。
返回列为 week、tag_count，验收会检查行顺序。
在本文件所在目录运行 python report_tags_cte_practice.py。

状态：完成（2026-11-12，根据提示调整连接、筛选和排序后通过验收）
自述：外层 WHERE 使用的 tag_count 来自 CTE week_count。
复盘：COUNT(rt.tag) AS tag_count 定义了 CTE 的输出列，外层读取这列进行筛选。
"""

import sqlite3
import sys
from contextlib import closing

from report_tags_having_practice import SCHEMA_AND_DATA

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# 用 WITH week_counts AS (...) 统计每份周报的标签数，包含 0。
# 外层筛出标签数不超过 1 的周报，返回 week、tag_count。
# 先按 tag_count 升序，再按 week 升序。
QUERY_1 = """
WITH week_count AS (
    SELECT r.week, COUNT(rt.tag) AS tag_count
    FROM reports AS r
    LEFT JOIN report_tags AS rt ON r.week = rt.week
    GROUP BY r.week
)
SELECT week, tag_count
FROM week_count
WHERE tag_count <= 1
ORDER BY tag_count ASC, week ASC;
"""


def main() -> int:
    if not QUERY_1.strip():
        print("题 1：待填写 SQL")
        return 1
    expected = [("2026-W46", 0), ("2026-W45", 1), ("2026-W48", 1)]
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
    print("✅ WITH 周报标签查询通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
