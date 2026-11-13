-- MySQL 第一课。统计每门课程的选课人数，保留无人选的课程。
-- 运行整个语句，WITH 会为这一条查询提供两张小样例表。
-- 已完成（2026-11-12）。输出 cno、cname、student_count，按 cno 升序。
-- 自述：COUNT(s.grade) 跳过未录入的 NULL 成绩，数据库原理会从 2 人算成 1 人。

WITH course_sample AS (
    SELECT 1 AS cno, '数据库原理' AS cname
    UNION ALL SELECT 2, '计算机网络'
    UNION ALL SELECT 3, '操作系统'
),
sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 102, 1, NULL
    UNION ALL SELECT 101, 2, 76
)
SELECT c.cno, c.cname, COUNT(s.sno) AS student_count
FROM course_sample AS c
LEFT JOIN sc_sample AS s ON c.cno = s.cno
GROUP BY c.cno, c.cname
ORDER BY c.cno ASC;
