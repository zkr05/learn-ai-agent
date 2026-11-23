-- MySQL 第三十一课：从成绩区间表查绩点，再算每位学生的 GPA。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 准备区只重建本课的四张 lab31 表。

-- 【准备区】
USE db_lab;

DROP TABLE IF EXISTS lab31_sc;
DROP TABLE IF EXISTS lab31_grade_point;
DROP TABLE IF EXISTS lab31_course;
DROP TABLE IF EXISTS lab31_student;

CREATE TABLE lab31_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE lab31_course (
    cno INT PRIMARY KEY,
    cname VARCHAR(50) NOT NULL,
    credit INT NOT NULL,
    CHECK (credit > 0)
) ENGINE=InnoDB;

CREATE TABLE lab31_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (sno, cno),
    FOREIGN KEY (sno) REFERENCES lab31_student(sno),
    FOREIGN KEY (cno) REFERENCES lab31_course(cno),
    CHECK (grade BETWEEN 0 AND 100)
) ENGINE=InnoDB;

CREATE TABLE lab31_grade_point (
    band_id INT PRIMARY KEY,
    min_grade DECIMAL(5,2) NOT NULL,
    max_grade DECIMAL(5,2) NOT NULL,
    grade_point INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO lab31_student (sno, sname) VALUES
    (101, '小林'), (102, '小陈'), (103, '小周');

INSERT INTO lab31_course (cno, cname, credit) VALUES
    (1, '数据库原理', 2), (2, '程序设计', 4);

INSERT INTO lab31_sc (sno, cno, grade) VALUES
    (101, 1, 89.99), (101, 2, 90.00),
    (102, 1, 59.99), (102, 2, 60.00);

INSERT INTO lab31_grade_point (band_id, min_grade, max_grade, grade_point) VALUES
    (1,  0.00,  59.99, 0),
    (2, 60.00,  69.99, 1),
    (3, 70.00,  79.99, 2),
    (4, 80.00,  89.99, 3),
    (5, 90.00, 100.00, 4);

-- 【练习】
-- 1. TODO：从选课表出发，连接绩点区间表。
--    输出 sno、cno、grade、grade_point，按 sno、cno 排序，先不算 GPA。
--    89.99、90.00、59.99、60.00 应分别匹配 3、4、0、1，各匹配一次。
--    按学校要求，从区间表查绩点，不用 CASE 或 IF 写死规则。
SELECT sno, cno, grade, grade_point
FROM lab31_sc AS sc
JOIN lab31_grade_point AS g
    ON sc.grade BETWEEN g.min_grade AND g.max_grade
ORDER BY sc.sno, sc.cno;
-- 2. TODO：给每位学生算 GPA。输出 sno、sname、gpa，按 sno 排序。
--    从学生表出发，保留没选课的学生；每条选课记录都要配上学分和绩点。
--    按学生分组，GPA = SUM(学分 × 绩点) / SUM(学分)，保留两位小数。
--    预期 101 为 3.67，102 为 0.67，103 为 NULL。
SELECT s.sno, s.sname, ROUND(SUM(c.credit * grade_point) / SUM(c.credit) , 2) AS gpa
FROM lab31_student AS s
LEFT JOIN lab31_sc AS sc ON sc.sno = s.sno
LEFT JOIN lab31_course AS c ON c.cno = sc.cno
LEFT JOIN lab31_grade_point AS g
    ON sc.grade BETWEEN g.min_grade AND g.max_grade
GROUP BY s.sno, s.sname
ORDER BY s.sno;

-- 选做：如果 103 选了 1 号课，且只考了 59.99，他的 GPA 会从 NULL 变成多少？
-- 从NULL 变成 0
-- 观察：为什么这个连接条件不能简单地把成绩写成等于区间下限？
-- 成绩等于下限只能匹配各档的起点。例如 89.99 属于 80.00～89.99，但不等于 80.00。区间没有重叠，BETWEEN 让每个成绩恰好匹配一档。