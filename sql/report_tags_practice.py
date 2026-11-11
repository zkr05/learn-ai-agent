"""周报标签练习。

每题使用 SQLite 内存库。查询结果的行顺序不限，列顺序按题目要求。
在本文件所在目录运行：python report_tags_practice.py

状态：完成（2026-11-11，按讲解与骨架提示完成三条 SQL，结果验收通过）
自述：如果题 3 换成 COUNT(*)，W46 会得到 1，因为 LEFT JOIN 给它保留了一行。
补充：COUNT(rt.tag) 只数标签非 NULL 的行，因此没有标签的 W46 得到 0。

问答记录：
- 题 1 只返回带 SQLite 标签的周次时，直接查 report_tags 即可。
  题目还要求正文 content，需通过共同的 week 关联 reports，取出对应正文。
- SQLite 和 MySQL 都支持 SQL，JOIN、GROUP BY 等查询思路相通。
  SQLite 嵌入程序，可用文件或内存库；MySQL 单独运行数据库服务，程序连接它。
"""

import sqlite3
import sys
from collections import Counter
from contextlib import closing

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# 题 1：找带 SQLite 标签的周报。返回 week、content 两列。
QUERY_1 = """
SELECT r.week, r.content
FROM reports AS r
LEFT JOIN report_tags AS rt ON r.week = rt.week
WHERE rt.tag = 'SQLite'
"""

# 题 2：统计每种标签出现于多少份周报。返回 tag、report_count 两列。
QUERY_2 = """
SELECT tag, COUNT(*) AS report_count
FROM report_tags
GROUP BY tag;
"""

# 题 3：统计每份周报有几个标签，没标签也要返回 0。
# 返回 week、tag_count 两列。
QUERY_3 = """
SELECT r.week, COUNT(rt.tag) AS tag_count
FROM reports AS r
LEFT JOIN report_tags AS rt ON r.week = rt.week
GROUP BY r.week


"""

SCHEMA_AND_DATA = """
PRAGMA foreign_keys = ON;

CREATE TABLE reports (
    week TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE report_tags (
    week TEXT NOT NULL REFERENCES reports(week),
    tag TEXT NOT NULL,
    PRIMARY KEY (week, tag)
);

INSERT INTO reports (week, content, created_at) VALUES
    ('2026-W44', '接口和存储', '2026-10-26'),
    ('2026-W45', '存储契约', '2026-11-02'),
    ('2026-W46', '日志分析', '2026-11-09');

INSERT INTO report_tags (week, tag) VALUES
    ('2026-W44', 'FastAPI'),
    ('2026-W44', 'SQLite'),
    ('2026-W45', 'SQLite');
"""


def main() -> int:
    exercises = (
        ("题 1", QUERY_1, [("2026-W44", "接口和存储"), ("2026-W45", "存储契约")]),
        ("题 2", QUERY_2, [("SQLite", 2), ("FastAPI", 1)]),
        ("题 3", QUERY_3, [("2026-W44", 2), ("2026-W45", 1), ("2026-W46", 0)]),
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
