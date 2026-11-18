-- MySQL 第二十六课。建立信息系学生视图，只显示学号和姓名。
-- 在 Navicat 选「数据库实验」和 db_lab，修改 CREATE VIEW 后面的查询。
-- 整份脚本会重建 lab26_is_students 视图和 lab26_student 练习表。
-- 结果 1 应只显示 101、103。向学生表加一行后，结果 2 应显示 101、103、105。
-- 观察：视图保存筛选规则，只返回信息系学生的学号和姓名。
-- 向学生表插入 105 后，再查同一视图就能读到 105，无需重新创建视图。

USE db_lab;

DROP VIEW IF EXISTS lab26_is_students;
DROP TABLE IF EXISTS lab26_student;

CREATE TABLE lab26_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL,
    dept VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

INSERT INTO lab26_student (sno, sname, dept) VALUES
    (101, '小林', 'is'),
    (102, '小陈', 'cs'),
    (103, '小周', 'is'),
    (104, '小吴', 'ma');

-- TODO：修改下面的 SELECT，只显示学号、姓名，只保留信息系（dept 为 'is'）。
CREATE VIEW lab26_is_students AS
SELECT sno, sname
FROM lab26_student
WHERE dept = 'is';

-- 结果 1：查视图，核对刚建好时的信息系名单。
SELECT * FROM lab26_is_students ORDER BY sno;

-- 向基础表再加一名信息系学生。
INSERT INTO lab26_student (sno, sname, dept) VALUES (105, '小许', 'is');

-- 结果 2：再次查同一视图，核对新学生是否出现。
SELECT * FROM lab26_is_students ORDER BY sno;
