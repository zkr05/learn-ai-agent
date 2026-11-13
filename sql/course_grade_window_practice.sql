-- MySQL 第六课。用窗口函数给每条成绩加上本课平均分。
-- 返回 sno、cno、grade、avg_grade，先按课程号、再按学号升序。
-- 预期结果为 (101, 1, 88, 80) 和 (105, 2, 78, 61.5)。
-- 观察：窗口函数保留全部六条成绩，并给每条加上本课平均分。
-- 如果再按课程号连回明细，1 号课的 88 分会重复四次，2 号课的 78 分会重复两次。

WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 102, 1, NULL
    UNION ALL SELECT 103, 1, 72
    UNION ALL SELECT 104, 1, 80
    UNION ALL SELECT 101, 2, 45
    UNION ALL SELECT 105, 2, 78
),
grade_with_avg AS (
    SELECT sno, cno, grade,
           AVG(grade) OVER (PARTITION BY cno) AS avg_grade
    FROM sc_sample
)
SELECT sno, cno, grade, avg_grade
FROM grade_with_avg
WHERE grade > avg_grade
ORDER BY cno, sno;
