-- MySQL 第十课。比较同一名学生在同一门课前后两次考试的成绩。
-- 第一步：用 LAG 给每次考试加上 previous_grade。
-- 第二步：把带上一场成绩的查询放进第二个 CTE，外层算 grade_change。
-- 返回 sno、cno、attempt_no、grade、previous_grade、grade_change。
-- 保留全部 8 行，按 sno、cno、attempt_no 升序。
-- 101 的 1 号课三次考试分差依次为 NULL、13、-3。
-- 观察：按学号和课程号分组后，每组的第一次考试没有上次成绩，分差为 NULL。
-- 102 的 1 号课两次都是 70 分，第二次有上次成绩，分差为 0。

WITH attempt_sample AS (
    SELECT 101 AS sno, 1 AS cno, 1 AS attempt_no, 65 AS grade
    UNION ALL SELECT 101, 1, 3, 75
    UNION ALL SELECT 101, 2, 2, 88
    UNION ALL SELECT 102, 1, 1, 70
    UNION ALL SELECT 101, 1, 2, 78
    UNION ALL SELECT 103, 1, 1, 82
    UNION ALL SELECT 101, 2, 1, 90
    UNION ALL SELECT 102, 1, 2, 70
),
diff_grade AS (
SELECT sno, cno, attempt_no, grade, LAG(grade) OVER (
                                        PARTITION BY sno, cno
                                        ORDER BY attempt_no) AS previous_grade
FROM attempt_sample
)
SELECT sno, cno, attempt_no, grade, previous_grade,
       grade - previous_grade AS grade_change
FROM diff_grade
ORDER BY sno, cno, attempt_no;
