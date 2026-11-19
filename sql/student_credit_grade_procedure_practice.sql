-- MySQL 第二十八课：用带输入参数的存储过程查询一名学生的学绩分。
-- 连接 Navicat 的「数据库实验」，选中 db_lab。先选中并运行准备区。
-- 准备区仅重建本课的练习表，删除本课同名旧过程。

-- 【准备区】
USE db_lab;

DROP PROCEDURE IF EXISTS lab28_get_student_credit_grade;
DROP TABLE IF EXISTS lab28_sc;
DROP TABLE IF EXISTS lab28_course;

CREATE TABLE lab28_course (
    cno INT PRIMARY KEY,
    cname VARCHAR(50) NOT NULL,
    credit INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE lab28_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (sno, cno),
    FOREIGN KEY (cno) REFERENCES lab28_course(cno)
) ENGINE=InnoDB;

INSERT INTO lab28_course (cno, cname, credit) VALUES
    (1, '数据库原理', 2),
    (2, '程序设计', 4);

INSERT INTO lab28_sc (sno, cno, grade) VALUES
    (101, 1, 90), (101, 2, 75),
    (102, 1, 60), (102, 2, 96);

-- 【练习】
-- 1. TODO：先写普通 SELECT，计算 101 号学生的学绩分，预期为 80.00。
--    通过 cno 连接两张表，分别汇总「成绩 × 学分」和「学分」，两者相除。
--    只输出 credit_grade 一列，保留两位小数。
SELECT ROUND((SUM(c.credit * sc.grade) / SUM(c.credit)), 2) AS credit_grade
FROM lab28_sc AS sc
LEFT JOIN lab28_course AS c ON c.cno = sc.cno
WHERE sc.sno = 101;

-- 2. TODO：把刚才的 SELECT 放在 CREATE PROCEDURE 下面，改用参数 p_sno 筛学号。
--    本课过程体只有一条 SELECT；把创建过程的整条语句选中运行。
--    如果已经建过，要重建时先单独运行上面的 DROP PROCEDURE 那一行。
CREATE PROCEDURE lab28_get_student_credit_grade(IN p_sno INT)
SELECT ROUND((SUM(c.credit * sc.grade) / SUM(c.credit)), 2) AS credit_grade
FROM lab28_sc AS sc
LEFT JOIN lab28_course AS c ON c.cno = sc.cno
WHERE sc.sno = p_sno;

-- 【自测】创建过程后，分别选中并运行下面两句。
CALL lab28_get_student_credit_grade(101); -- 预期 80.00
CALL lab28_get_student_credit_grade(102); -- 预期 84.00

-- 选做：调用一个没有选课记录的学号 999。你的查询会得到什么？
CALL lab28_get_student_credit_grade(999);
-- 显示NULL
-- 观察：为什么过程只创建一次，却能查到两个人不同的学绩分？
-- 因为创建了一次之后，就可以让别的反复调用了