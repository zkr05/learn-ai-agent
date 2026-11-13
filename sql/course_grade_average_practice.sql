-- MySQL 第三课。查出 1 号课中成绩高于本课平均分的学生。
-- 已完成（2026-11-12）。1 号课平均分为 80，结果为学生 101、88 分。
-- 自述：只删外层的课程限制时，2 号课的 96 分也会和 1 号课平均分比较，因此会出现在结果里。

WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 102, 1, NULL
    UNION ALL SELECT 103, 1, 72
    UNION ALL SELECT 104, 1, 80
    UNION ALL SELECT 101, 2, 45
    UNION ALL SELECT 105, 2, 96
)
SELECT s.sno, s.grade
FROM sc_sample AS s
WHERE s.cno = 1
  AND s.grade > (
    SELECT AVG(a.grade)
    FROM sc_sample AS a
    WHERE a.cno = 1
  )
ORDER BY s.sno;
