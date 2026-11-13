-- MySQL 第七课。每门课取最多两条已录成绩。
-- 每门课按成绩降序编号，同分时学号较小的排前面。
-- 先排除 NULL 并查看编号，再把编号查询放进第二个 CTE，从外层取前两条。
-- 返回 cno、sno、grade、rn，先按课程号、再按编号升序。
-- 预期结果为 (1, 101, 95, 1)、(1, 102, 88, 2)、
-- (2, 105, 96, 1)、(2, 101, 78, 2)、(3, 108, 82, 1)。
-- 观察：先用 sc_sample 给已录成绩编号，把带 rn 的结果放进 ranked_grades。
-- 外层查询 ranked_grades 时，rn 已经是一列，可以用 WHERE rn <= 2 筛选。

WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 95 AS grade
    UNION ALL SELECT 103, 1, 88
    UNION ALL SELECT 102, 1, 88
    UNION ALL SELECT 104, 1, NULL
    UNION ALL SELECT 101, 2, 78
    UNION ALL SELECT 105, 2, 96
    UNION ALL SELECT 106, 2, 70
    UNION ALL SELECT 108, 3, 82
    UNION ALL SELECT 107, 3, NULL
),
ranked_grades AS(
  SELECT cno, sno, grade,
         ROW_NUMBER() OVER (
             PARTITION BY cno
             ORDER BY grade DESC, sno ASC
         ) AS rn
  FROM sc_sample
  WHERE grade IS NOT NULL
)
SELECT cno, sno, grade, rn
FROM ranked_grades
WHERE rn <= 2
ORDER BY cno, rn;
