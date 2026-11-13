-- MySQL 第八课。找出每门课排名第 1 或第 2 的已录成绩，同分并列。
-- 第一步：给已录成绩加上 grade_rank。1 号课的名次应是 1、2、2、4。
-- 第二步：把排名查询放进第二个 CTE，再从外层筛选。
-- 返回 cno、sno、grade、grade_rank，按课程号、名次、学号升序。
-- 预期共 6 行。1 号课保留 101、102、103，2 号课保留 105、101，3 号课保留 108。
-- 观察：窗口内按成绩排，两个 88 分并列第 2，72 分排第 4。
-- 外层按名次筛选时，两个并列第 2 的学生都会保留。

WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 95 AS grade
    UNION ALL SELECT 103, 1, 88
    UNION ALL SELECT 102, 1, 88
    UNION ALL SELECT 109, 1, 72
    UNION ALL SELECT 104, 1, NULL
    UNION ALL SELECT 101, 2, 78
    UNION ALL SELECT 105, 2, 96
    UNION ALL SELECT 106, 2, 70
    UNION ALL SELECT 108, 3, 82
    UNION ALL SELECT 107, 3, NULL
),
rank_grade AS (
SELECT sno,cno, grade, RANK() OVER(
                            PARTITION BY cno
                            ORDER BY grade DESC
                            ) AS grade_rank
FROM sc_sample
WHERE grade IS NOT NULL

)
SELECT cno, sno, grade, grade_rank
FROM rank_grade
WHERE grade_rank <= 2
ORDER BY cno, grade_rank, sno;
