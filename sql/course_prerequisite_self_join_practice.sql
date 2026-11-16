-- MySQL 第十五课。查每门课的直接先修课，以及先修课的先修课。
-- cno 是课程号，cpno 是这一门课的直接先修课课程号，NULL 表示无先修课。
-- 保留全部 5 门课，缺少直接或间接先修课时，对应列显示 NULL。
-- 返回 cno、cname、direct_cno、direct_cname、indirect_cno、indirect_cname。
-- 按 cno 升序。可以先核对 40 → 30 → 20。
-- 观察：第二次连接沿 s1.cpno 继续找，所以 40 号课能沿 30 再找到 20。
-- 两次左连接保留全部课程，即使找不到直接或间接先修课。

WITH course_sample AS (
    SELECT 10 AS cno, '大学数学' AS cname, NULL AS cpno
    UNION ALL SELECT 20, '离散数学', 10
    UNION ALL SELECT 30, '数据结构', 20
    UNION ALL SELECT 40, '算法设计', 30
    UNION ALL SELECT 50, '计算机导论', NULL
)
-- 第一步：改下面的 SELECT，连接一次课程表，找直接先修课。
-- 第二步：再接一次课程表，找间接先修课。
SELECT c.cno, c.cname, c.cpno AS direct_cno, s1.cname AS direct_cname, s1.cpno AS indirect_cno, s2.cname AS indirect_cname
FROM course_sample AS c
LEFT JOIN course_sample AS s1 ON c.cpno = s1.cno
LEFT JOIN course_sample AS s2 ON s1.cpno = s2.cno
ORDER BY c.cno;
