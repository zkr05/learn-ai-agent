-- MySQL 第九课。取每门课最高的两个不同分数，同分的学生都保留。
-- 排除未录成绩，先查看 DENSE_RANK 编出的分数档次，再用外层 WHERE 筛选。
-- 返回 cno、sno、grade、score_tier，按课程号、分数档次、学号升序。
-- 预期 7 行。1 号课保留 101、102、103、109，2 号课保留 105、101，3 号课保留 108。
-- 观察：1 号课两个 95 分同属第 1 档，两个 88 分同属第 2 档，所以这四条都保留。
-- 窗口内只按分数排，外层再让同一分数档次的学生按学号升序显示。

WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 95 AS grade
    UNION ALL SELECT 103, 1, 88
    UNION ALL SELECT 102, 1, 95
    UNION ALL SELECT 109, 1, 88
    UNION ALL SELECT 110, 1, 72
    UNION ALL SELECT 104, 1, NULL
    UNION ALL SELECT 101, 2, 78
    UNION ALL SELECT 105, 2, 96
    UNION ALL SELECT 106, 2, 70
    UNION ALL SELECT 108, 3, 82
    UNION ALL SELECT 107, 3, NULL
),
rank_grade AS (
SELECT sno, cno, grade, DENSE_RANK() OVER (
                            PARTITION BY cno
                            ORDER BY grade DESC
                            ) AS score_tier
FROM sc_sample
WHERE grade IS NOT NULL
)
SELECT cno, sno, grade, score_tier
FROM rank_grade
WHERE score_tier <= 2
ORDER BY cno, score_tier, sno ASC;
