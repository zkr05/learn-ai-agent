-- MySQL 第二十一课。用 ALTER TABLE 修改已经有数据的学生表。
-- 在 Navicat 选「数据库实验」和 db_lab，修改两处 TODO，再运行整份脚本。
-- 1. 新增 birth_day，类型为 DATE，允许 NULL。
-- 2. 将 sname 从 VARCHAR(100) 改为 VARCHAR(50)，保留 NOT NULL。
-- DESCRIBE 用来核对列定义，最后的 SELECT 用来核对原来的两条记录。
-- 观察：新增的 birth_day 允许 NULL，两条已有记录的出生日期都为 NULL。
-- 修改列时重新写 NOT NULL，DESCRIBE 显示 sname 为 varchar(50)，Null 为 NO。

DROP TEMPORARY TABLE IF EXISTS lab21_student;

CREATE TEMPORARY TABLE lab21_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(100) NOT NULL,
    age INT NOT NULL
) ENGINE=InnoDB;

INSERT INTO lab21_student (sno, sname, age) VALUES
    (101, '小林', 19),
    (102, '小陈', 20);

-- TODO 1：用 ALTER TABLE 新增出生日期列。
ALTER TABLE lab21_student
    ADD COLUMN birth_day DATE NULL;
-- TODO 2：用 ALTER TABLE 修改姓名列的长度。
ALTER TABLE lab21_student
    MODIFY COLUMN sname VARCHAR(50) NOT NULL;
DESCRIBE lab21_student;

SELECT *
FROM lab21_student
ORDER BY sno;
