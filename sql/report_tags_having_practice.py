"""WHERE 与 HAVING 练习。

只填写下面的 QUERY_1 和 QUERY_2。每次运行都会新建 SQLite 内存库。
返回列的顺序均为 week、tag_count，结果行的顺序不限。
在本文件所在目录运行：python report_tags_having_practice.py

状态：完成（2026-11-11，按讲解与提示完成两条 SQL，结果验收通过）
自述：题 2 删掉 WHERE 后，W44 会出现，标签数为 2。
原因：FastAPI 也参与分组计数，W44 的两个标签满足 HAVING 条件。
复盘：WHERE 决定哪些输入记录参与统计，HAVING 根据统计结果筛选分组。
"""

import sqlite3
import sys
from collections import Counter
from contextlib import closing

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# 题 1：找出标签数至少为 2 的周报，返回 week、tag_count。
# 先自己写 SQL。需要时可以借鉴第一课的“每份周报标签数”查询。
QUERY_1 = """
SELECT r.week, COUNT(rt.tag) AS tag_count
FROM reports AS r
LEFT JOIN report_tags AS rt ON r.week = rt.week
GROUP BY r.week
HAVING COUNT(rt.tag) >= 2;
"""

# 题 2：先排除 FastAPI 标签，再找出至少有两个剩余标签的周报。
# 例如 W44 排除后只剩 SQLite，W47 排除后剩 SQLite、Pandas。
# 返回 week、tag_count。想清楚这里的标签数应该包含哪些输入记录。
QUERY_2 = """
SELECT r.week, COUNT(rt.tag) AS tag_count
FROM reports AS r
LEFT JOIN report_tags AS rt ON r.week = rt.week
WHERE rt.tag <> 'FastAPI'
GROUP BY r.week
HAVING COUNT(rt.tag) >= 2;
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
    ('2026-W46', '日志分析', '2026-11-09'),
    ('2026-W47', '数据处理', '2026-11-16'),
    ('2026-W48', 'Python 复习', '2026-11-23');

INSERT INTO report_tags (week, tag) VALUES
    ('2026-W44', 'FastAPI'),
    ('2026-W44', 'SQLite'),
    ('2026-W45', 'SQLite'),
    ('2026-W47', 'FastAPI'),
    ('2026-W47', 'SQLite'),
    ('2026-W47', 'Pandas'),
    ('2026-W48', 'Python');
"""


def main() -> int:
    exercises = (
        ("题 1", QUERY_1, [("2026-W44", 2), ("2026-W47", 3)]),
        ("题 2", QUERY_2, [("2026-W47", 2)]),
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
