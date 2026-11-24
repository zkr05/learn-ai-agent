-- MySQL 第三十二课：用带参存储过程查询一名学生的 GPA。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 继续用第 31 课的四张 lab31 表。若表不存在，或 103 已被加了选课，
-- 先运行同目录 grade_point_range_gpa_practice.sql 的准备区，再回到本文件。

-- 【准备区】仅删除第 32 课的同名旧过程，便于重建。
USE db_lab;
DROP PROCEDURE IF EXISTS lab32_get_student_gpa;

-- 【练习】
-- 1. TODO：复制第 31 课的 GPA 查询，先让它只返回 101 的学号、姓名和 GPA。
--    保留原有 LEFT JOIN 和加权公式。在 GROUP BY 前按学生表的学号筛选。
CREATE PROCEDURE lab32_get_student_gpa(IN p_sno INT)
SELECT s.sno, s.sname, ROUND(SUM(c.credit * grade_point) / SUM(c.credit) , 2) AS gpa
FROM lab31_student AS s
LEFT JOIN lab31_sc AS sc ON sc.sno = s.sno
LEFT JOIN lab31_course AS c ON c.cno = sc.cno
LEFT JOIN lab31_grade_point AS g
    ON sc.grade BETWEEN g.min_grade AND g.max_grade
WHERE s.sno = p_sno
GROUP BY s.sno, s.sname
ORDER BY s.sno;

-- 2. TODO：把刚才的 SELECT 放入存储过程，把写死的 101 换成 p_sno。
--    这里的过程主体只有一条 SELECT。选中整条 CREATE PROCEDURE 运行。
-- CREATE PROCEDURE lab32_get_student_gpa(IN p_sno INT)


-- 【自测】创建过程后，分别运行下列 CALL，再比较行数和 GPA。
CALL lab32_get_student_gpa(101); -- 一行，GPA 为 3.67
CALL lab32_get_student_gpa(102); -- 一行，GPA 为 0.67
CALL lab32_get_student_gpa(103); -- 一行，GPA 为 NULL
CALL lab32_get_student_gpa(999); -- 零行

-- 观察：为什么传入 103 能看到一行 NULL，而传入 999 一行也没有？
-- 因为999没有这个学生，而103有这个学生，只是没有成绩，果茶里的分组也能分上。