-- MySQL 第三十课：写一个返回单个学绩分的存储函数。
-- Navicat 新建连接「数据库实验－函数」：127.0.0.1，端口 3308，
-- 用户 lab，密码同原「数据库实验」连接，选中 db_lab。
-- 准备区仅重建本课的 lab30 表，删除本课的旧函数。

-- 【准备区】
USE db_lab;

DROP FUNCTION IF EXISTS lab30_student_credit_grade;
DROP TABLE IF EXISTS lab30_sc;
DROP TABLE IF EXISTS lab30_course;
DROP TABLE IF EXISTS lab30_student;

CREATE TABLE lab30_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE lab30_course (
    cno INT PRIMARY KEY,
    cname VARCHAR(50) NOT NULL,
    credit INT NOT NULL
) ENGINE=InnoDB;

CREATE TABLE lab30_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (sno, cno),
    FOREIGN KEY (sno) REFERENCES lab30_student(sno),
    FOREIGN KEY (cno) REFERENCES lab30_course(cno)
) ENGINE=InnoDB;

INSERT INTO lab30_student (sno, sname) VALUES
    (101, '小林'), (102, '小陈'), (103, '小周');

INSERT INTO lab30_course (cno, cname, credit) VALUES
    (1, '数据库原理', 2), (2, '程序设计', 4);

INSERT INTO lab30_sc (sno, cno, grade) VALUES
    (101, 1, 90), (101, 2, 75),
    (102, 1, 60), (102, 2, 96);

-- 【练习】
-- TODO：创建 lab30_student_credit_grade。传入学号 p_sno，返回该生的学绩分。
-- 复用上一课的加权 SELECT，改用 lab30 表，在内层按 p_sno 筛选。
-- 把这条 SELECT 放在 RETURN 后的括号内，分号写在最外面的右括号之后。
CREATE FUNCTION lab30_student_credit_grade(p_sno INT)
RETURNS DECIMAL(5,2)
READS SQL DATA
RETURN (
    SELECT ROUND((SUM(c.credit * sc.grade) / SUM(c.credit)), 2) AS credit_grade
    FROM lab30_sc AS sc
    LEFT JOIN lab30_course AS c ON c.cno = sc.cno
    WHERE sc.sno = p_sno
);


-- 【自测】函数创建后，再分别运行以下查询。
SELECT lab30_student_credit_grade(101) AS credit_grade; -- 一行，80.00

SELECT sno, sname, lab30_student_credit_grade(sno) AS credit_grade
FROM lab30_student
ORDER BY sno; -- 三行：101 为 80.00，102 为 84.00，103 为 NULL

-- 选做：在 WHERE 里调用函数，筛出学绩分至少为 82 的学生。
SELECT sno, sname, lab30_student_credit_grade(sno) AS credit_grade
FROM lab30_student
WHERE lab30_student_credit_grade(sno) >= 82;
-- 观察：名单里传的是 sno。为什么同一条 SELECT 能得到三个不同结果？
-- 因为传的sno，但是从lab30_student得到有三个学生，所以会有三个结果。
