-- MySQL 第二十九课：用存储过程把指定学生的学绩分写回学生表。
-- 在 Navicat 连接「数据库实验」并选中 db_lab。按区块选中运行。
-- 准备区会重建本课的三张 lab29 表，并删除本课旧过程。

-- 【准备区】
USE db_lab;

DROP PROCEDURE IF EXISTS lab29_save_student_credit_grade;
DROP TABLE IF EXISTS lab29_sc;
DROP TABLE IF EXISTS lab29_course;
DROP TABLE IF EXISTS lab29_student;

CREATE TABLE lab29_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL,
    credit_grade DECIMAL(5,2) DEFAULT NULL
) ENGINE=InnoDB;

CREATE TABLE lab29_course (
    cno INT PRIMARY KEY,
    cname VARCHAR(50) NOT NULL,
    credit INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE lab29_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (sno, cno),
    FOREIGN KEY (sno) REFERENCES lab29_student(sno),
    FOREIGN KEY (cno) REFERENCES lab29_course(cno)
) ENGINE=InnoDB;

INSERT INTO lab29_student (sno, sname) VALUES
    (101, '小林'), (102, '小陈'), (103, '小周');

INSERT INTO lab29_course (cno, cname, credit) VALUES
    (1, '数据库原理', 2), (2, '程序设计', 4);

INSERT INTO lab29_sc (sno, cno, grade) VALUES
    (101, 1, 90), (101, 2, 75),
    (102, 1, 60), (102, 2, 96);

-- 【练习】
-- 1. TODO：先查 lab29_student，确认三人的 credit_grade 目前都是 NULL。
--    复用上一课的普通 SELECT，改成本课表名，先确认能算出 101 的 80.00。
SELECT ROUND((SUM(c.credit * sc.grade) / SUM(c.credit)), 2) AS credit_grade
FROM lab29_sc AS sc
LEFT JOIN lab29_course AS c ON c.cno = sc.cno
WHERE sc.sno = 101;


-- 2. TODO：把加权查询作为子查询放进 UPDATE 的 SET 右侧。
--    过程体是一条 UPDATE；内层选这次计算的选课记录，外层指定要更新的学生行。
--    两层都用参数 p_sno，不写死 101。把完整 CREATE PROCEDURE 选中运行。
CREATE PROCEDURE lab29_save_student_credit_grade(IN p_sno INT)
UPDATE lab29_student
SET credit_grade = (
    SELECT ROUND((SUM(c.credit * sc.grade) / SUM(c.credit)), 2) AS credit_grade
    FROM lab29_sc AS sc
    LEFT JOIN lab29_course AS c ON c.cno = sc.cno
    WHERE sc.sno = p_sno
)
WHERE sno = p_sno;



-- 3. 自测：先 CALL 101，再看全表。应该只有 101 变成 80.00。
CALL lab29_save_student_credit_grade(101);
SELECT sno, sname, credit_grade FROM lab29_student ORDER BY sno;

-- 再 CALL 102。应该得到 101 为 80.00、102 为 84.00、103 仍为 NULL。
CALL lab29_save_student_credit_grade(102);
SELECT sno, sname, credit_grade FROM lab29_student ORDER BY sno;

-- 选做：分别传 103（没选课）和 999（没有这名学生），再查学生表。
CALL lab29_save_student_credit_grade(103);
CALL lab29_save_student_credit_grade(999);
SELECT sno, sname, credit_grade FROM lab29_student ORDER BY sno;
-- 观察：内外两层的 WHERE 各管什么？如果漏掉外层 WHERE 会发生什么？
-- 内层管的是学分权重是加的谁的权重，外层是管给哪个学生置权重，如果漏掉，第一次调用则全都变成101的权重。