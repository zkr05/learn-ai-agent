-- MySQL 第五课：用 GROUP BY 和 JOIN 查出每门课中高于本课平均分的成绩。
-- 返回 sno、cno、grade、avg_grade，按 cno、sno 升序。
-- 预期结果：(101, 1, 88, 80)、(105, 2, 78, 61.5)。
-- 观察：按课程号连接后仍有六条成绩，每条都带上本课平均分。
-- 用 WHERE 保留严格高于平均分的成绩，最后剩两条。

WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 102, 1, NULL
    UNION ALL SELECT 103, 1, 72
    UNION ALL SELECT 104, 1, 80
    UNION ALL SELECT 101, 2, 45
    UNION ALL SELECT 105, 2, 78
),
cno_avg AS (
    SELECT cno, AVG(grade) AS avg_grade
    FROM sc_sample
    GROUP BY cno
)
SELECT s.sno, s.cno, s.grade, a.avg_grade
FROM sc_sample AS s
LEFT JOIN cno_avg AS a ON a.cno = s.cno
WHERE s.grade > a.avg_grade
ORDER BY s.cno, s.sno;
