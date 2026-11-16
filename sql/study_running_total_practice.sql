-- MySQL 第十一课。计算每个学生在每门课的累计学习时长。
-- 在 SELECT 里添加 running_minutes，累加同组从第一次到当前这次的 minutes_spent。
-- 返回 sno、cno、session_no、minutes_spent、running_minutes。
-- 保留全部 8 行，按学号、课程号、学习次数升序显示。
-- 101 的 1 号课累计值依次为 20、55、70，换到 2 号课后依次为 30、40。
-- 观察：每个学生和课程的组合独立累计，窗口按学习次数从第一条加到当前这条。
-- 102 的 1 号课第二次用了 0 分钟，累计值仍是 40 分钟。

WITH study_sample AS (
    SELECT 101 AS sno, 1 AS cno, 1 AS session_no, 20 AS minutes_spent
    UNION ALL SELECT 101, 1, 3, 15
    UNION ALL SELECT 102, 1, 2, 0
    UNION ALL SELECT 101, 2, 2, 10
    UNION ALL SELECT 101, 1, 2, 35
    UNION ALL SELECT 103, 1, 1, 25
    UNION ALL SELECT 102, 1, 1, 40
    UNION ALL SELECT 101, 2, 1, 30
)
SELECT sno, cno, session_no, minutes_spent,
SUM(minutes_spent) OVER (
    PARTITION BY sno,cno
    ORDER BY session_no
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_minutes
FROM study_sample
ORDER BY sno, cno, session_no;
