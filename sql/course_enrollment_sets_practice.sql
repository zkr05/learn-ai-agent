-- MySQL 第十七课。用交集和差集比较两门课的学生名单。
-- 两道题各是一条独立的 SQL，各有自己的 WITH。可在 Navicat 运行整份脚本看两个结果。
-- 保留样例，两题都只返回 sno，按学号升序。未录成绩的选课记录仍算已选。
-- 观察：同一张表按不同的课程号筛选，得到两份只包含学号的名单。
-- 两份名单的交集为 101、105；从 1 号课名单里去掉 2 号课的人后只剩 102。

-- 题 1：找两门课都选了的学生。预期学号 101、105。
WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 101, 2, NULL
    UNION ALL SELECT 102, 1, 76
    UNION ALL SELECT 102, 3, 82
    UNION ALL SELECT 103, 2, 91
    UNION ALL SELECT 104, 3, 84
    UNION ALL SELECT 105, 1, 0
    UNION ALL SELECT 105, 2, 93
)
SELECT sno
FROM sc_sample
WHERE cno = 1
-- 在这里接上集合运算和 2 号课的名单。
INTERSECT
SELECT sno
FROM sc_sample
WHERE cno = 2
ORDER BY sno;

-- 题 2：找选了 1 号课但没选 2 号课的学生。预期学号 102。
WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 101, 2, NULL
    UNION ALL SELECT 102, 1, 76
    UNION ALL SELECT 102, 3, 82
    UNION ALL SELECT 103, 2, 91
    UNION ALL SELECT 104, 3, 84
    UNION ALL SELECT 105, 1, 0
    UNION ALL SELECT 105, 2, 93
)
SELECT sno
FROM sc_sample
WHERE cno = 1
-- 在这里接上集合运算和 2 号课的名单。
EXCEPT
SELECT sno
FROM sc_sample
WHERE cno = 2
ORDER BY sno;
