-- MySQL 第四十课：让选课记录跟随学生学号的修改和删除。
-- 沿用 Navicat「数据库实验－函数」（127.0.0.1:3308），选中 db_lab。
-- 这是独立的 lab40 练习。准备区只重建本课对象，不使用第 39 课的表。

-- 【准备区】
USE db_lab;
DROP TRIGGER IF EXISTS lab40_student_bu;
DROP TRIGGER IF EXISTS lab40_student_bd;
DROP TABLE IF EXISTS lab40_fk_sc;
DROP TABLE IF EXISTS lab40_fk_student;
DROP TABLE IF EXISTS lab40_sc;
DROP TABLE IF EXISTS lab40_student;

-- 第一组：实验六要求的手写触发器。此组不定义外键。
CREATE TABLE lab40_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL
) ENGINE=InnoDB;

CREATE TABLE lab40_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2),
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

INSERT INTO lab40_student (sno, sname) VALUES (101, '小林'), (102, '小陈');
INSERT INTO lab40_sc (sno, cno, grade) VALUES (101, 1, 88), (101, 2, 76), (102, 1, 75);

-- 第二组：已给出外键级联，使用同一批初始数据做对照。
CREATE TABLE lab40_fk_student LIKE lab40_student;
CREATE TABLE lab40_fk_sc LIKE lab40_sc;
ALTER TABLE lab40_fk_sc
    ADD FOREIGN KEY (sno) REFERENCES lab40_fk_student(sno)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

INSERT INTO lab40_fk_student SELECT sno, sname FROM lab40_student;
INSERT INTO lab40_fk_sc SELECT sno, cno, grade FROM lab40_sc;

-- 【练习 1】在 lab40_student 上写 BEFORE UPDATE 触发器。
-- 学号真的改了才处理：只移动旧学号的选课记录，课号和成绩不变。
DELIMITER $$
CREATE TRIGGER lab40_student_bu
BEFORE UPDATE ON lab40_student
FOR EACH ROW
BEGIN
    IF NOT (OLD.sno <=> NEW.sno) THEN
        UPDATE lab40_sc
        SET sno = NEW.sno
        WHERE sno = OLD.sno;
    END IF;
END$$
DELIMITER ;


-- 【练习 2】在 lab40_student 上写 BEFORE DELETE 触发器。
-- 删除一名学生时，删除他在 lab40_sc 的全部选课记录，不影响其他学生。
DELIMITER $$
CREATE TRIGGER lab40_student_bd
BEFORE DELETE ON lab40_student
FOR EACH ROW
BEGIN
    DELETE FROM lab40_sc
    WHERE sno = OLD.sno;
END$$
DELIMITER ;


-- 【自测 1】选中运行：改学号后，旧 101 的两门课应移到 201，102 不变。
UPDATE lab40_student SET sno = 201 WHERE sno = 101;
SELECT sno, sname FROM lab40_student ORDER BY sno;
SELECT sno, cno, grade FROM lab40_sc ORDER BY sno, cno;

-- 【自测 2】单独运行：删除 201 后，学生表和选课表都应该只剩 102。
DELETE FROM lab40_student WHERE sno = 201;
SELECT sno, sname FROM lab40_student ORDER BY sno;
SELECT sno, cno, grade FROM lab40_sc ORDER BY sno, cno;

-- 【对照 1】换成外键级联的表，不创建触发器，观察同样的改学号操作。
UPDATE lab40_fk_student SET sno = 201 WHERE sno = 101;
SELECT sno, sname FROM lab40_fk_student ORDER BY sno;
SELECT sno, cno, grade FROM lab40_fk_sc ORDER BY sno, cno;

-- 【对照 2】外键级联删除也应只剩 102。
DELETE FROM lab40_fk_student WHERE sno = 201;
SELECT sno, sname FROM lab40_fk_student ORDER BY sno;
SELECT sno, cno, grade FROM lab40_fk_sc ORDER BY sno, cno;

-- 选做：给学号 999 插入一条选课，试试哪一组会拒绝它。只在本课表测试。
INSERT INTO lab40_sc (sno, cno, grade)
VALUES (999, 1, 88);
INSERT INTO lab40_fk_sc (sno, cno, grade)
VALUES (999, 1, 88);
-- 观察：为什么 BEFORE UPDATE 里找选课要用旧学号，写入却用新学号？
--    两组自测的结果一样，哪一组还可以拦住不存在学生的选课记录？
-- 找选课是需要定位到之前的选课记录，所以要用OLD.sno来找，新学号则是需要把旧的改成新的
-- 第二组可以拦住，因为第二组需要先把信息存在学生表里面。