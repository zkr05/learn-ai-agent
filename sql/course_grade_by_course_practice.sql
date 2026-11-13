-- MySQL 第四课：找出每门课中成绩高于本课平均分的选课记录。
-- 返回 sno、cno、grade，先按 cno 升序，再按 sno 升序。
-- 在 Navicat 里保留 WITH 样例，修改末尾的查询，再运行整条语句。
-- 预期结果：(101, 1, 88)、(105, 2, 78)。
-- 观察：a.cno = s.cno 让内层只计算当前成绩所属课程的平均分。

WITH sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 102, 1, NULL
    UNION ALL SELECT 103, 1, 72
    UNION ALL SELECT 104, 1, 80
    UNION ALL SELECT 101, 2, 45
    UNION ALL SELECT 105, 2, 78
)
SELECT s.sno, s.cno, s.grade
FROM sc_sample AS s
WHERE s.grade > (
    SELECT AVG(a.grade)
    FROM sc_sample AS a
    WHERE a.cno = s.cno
  )
ORDER BY s.cno ASC, s.sno ASC;
