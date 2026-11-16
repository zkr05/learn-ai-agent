-- MySQL 第十二课。计算每个学生在每门课最近三次学习的平均时长，含本次。
-- 当前组不足三次时，按已有记录求平均。把 avg_last_3 四舍五入到两位小数。
-- 返回 sno、cno、session_no、minutes_spent、avg_last_3，保留全部 10 行。
-- 按学号、课程号、学习次数升序。101 的 1 号课第 4 次平均值为 30.00。
-- 观察：第 4 次学习只取第 2、3、4 次，平均为 (35 + 15 + 40) / 3 = 30.00。
-- 组内不足三次时，按已有记录求平均。ROUND 对窗口平均值保留两位小数。

WITH study_sample AS (
    SELECT 101 AS sno, 1 AS cno, 1 AS session_no, 20 AS minutes_spent
    UNION ALL SELECT 101, 1, 3, 15
    UNION ALL SELECT 101, 1, 5, 25
    UNION ALL SELECT 102, 1, 2, 0
    UNION ALL SELECT 101, 2, 2, 10
    UNION ALL SELECT 101, 1, 2, 35
    UNION ALL SELECT 103, 1, 1, 25
    UNION ALL SELECT 102, 1, 1, 40
    UNION ALL SELECT 101, 1, 4, 40
    UNION ALL SELECT 101, 2, 1, 30
)
SELECT sno, cno, session_no, minutes_spent,
ROUND(AVG(minutes_spent) OVER(
    PARTITION BY sno, cno
    ORDER BY session_no
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
), 2) AS avg_last_3
FROM study_sample
ORDER BY sno, cno, session_no;
