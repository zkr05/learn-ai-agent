-- MySQL 第三十三课：用存储函数返回一名学生的 GPA。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 继续用第 31 课的四张 lab31 表。若表不存在，或 103 已有选课记录，
-- 先运行同目录 grade_point_range_gpa_practice.sql 的准备区，再回到本文件。

-- 【准备区】仅删除第 33 课的同名旧函数，便于重建。
USE db_lab;
DROP FUNCTION IF EXISTS lab33_student_gpa;

-- 【练习】
-- TODO：把第 32 课过程里的 GPA 查询改成存储函数。
-- 保留连接、学号筛选和分组。括号里的 SELECT 只输出 GPA 一列。
-- 选中完整 CREATE FUNCTION 运行，分号只写在 RETURN (...) 的外面。
-- CREATE FUNCTION lab33_student_gpa(p_sno INT)
-- RETURNS DECIMAL(4,2)
-- READS SQL DATA
CREATE FUNCTION lab33_student_gpa(p_sno INT)
RETURNS DECIMAL(4,2)
READS SQL DATA
RETURN(SELECT ROUND(SUM(c.credit * grade_point) / SUM(c.credit) , 2) AS gpa
FROM lab31_student AS s
LEFT JOIN lab31_sc AS sc ON sc.sno = s.sno
LEFT JOIN lab31_course AS c ON c.cno = sc.cno
LEFT JOIN lab31_grade_point AS g
    ON sc.grade BETWEEN g.min_grade AND g.max_grade
WHERE s.sno = p_sno
GROUP BY s.sno, s.sname
ORDER BY s.sno);

-- 【自测】函数创建后，分别运行下面的查询。
SELECT lab33_student_gpa(101) AS gpa; -- 一格，3.67
SELECT lab33_student_gpa(102) AS gpa; -- 一格，0.67
SELECT lab33_student_gpa(103) AS gpa; -- 一格，NULL
SELECT lab33_student_gpa(999) AS gpa; -- 一格，NULL

-- 对比 999：这次把函数放在一条从学生表出发的查询里。
SELECT s.sno, s.sname, lab33_student_gpa(s.sno) AS gpa
FROM lab31_student AS s
ORDER BY s.sno; -- 三行：101 为 3.67，102 为 0.67，103 为 NULL

-- 选做：在 WHERE 里用函数筛出 GPA 至少为 3.00 的学生，应该只有 101。
SELECT s.sno, s.sname, lab33_student_gpa(s.sno) AS gpa
FROM lab31_student AS s
WHERE lab33_student_gpa(s.sno) >= 3.00
ORDER BY s.sno;
-- 观察：103 和 999 都返回 NULL，但函数内的 SELECT 分别返回了几行？
-- 103的是存在，左连接保留一行，聚合结果为NULL；
-- 999的是不存在，筛选后没分组，返回零行，结果为NULL。