-- MySQL 第三十六课：用 AFTER UPDATE 触发器自动重算学绩分。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 准备区只重建本课的 lab36 对象。先整段运行准备区。

-- 【准备区】
USE db_lab;
DROP TRIGGER IF EXISTS lab36_sc_after_update;
DROP TRIGGER IF EXISTS lab36_sc_before_update;
DROP PROCEDURE IF EXISTS lab36_refresh_credit_grade;
DROP TABLE IF EXISTS lab36_sc;
DROP TABLE IF EXISTS lab36_course;
DROP TABLE IF EXISTS lab36_student;

CREATE TABLE lab36_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL,
    credit_grade DECIMAL(5,2) DEFAULT NULL
) ENGINE=InnoDB;

CREATE TABLE lab36_course (
    cno INT PRIMARY KEY,
    credit INT NOT NULL,
    CHECK (credit > 0)
) ENGINE=InnoDB;

CREATE TABLE lab36_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL,
    PRIMARY KEY (sno, cno),
    FOREIGN KEY (sno) REFERENCES lab36_student(sno),
    FOREIGN KEY (cno) REFERENCES lab36_course(cno)
) ENGINE=InnoDB;

INSERT INTO lab36_student (sno, sname) VALUES (101, '小林'), (102, '小陈');
INSERT INTO lab36_course (cno, credit) VALUES (1, 2), (2, 4);
INSERT INTO lab36_sc (sno, cno, grade) VALUES (101, 1, 88), (101, 2, 76), (102, 1, 75);

-- 提供：复用第 29 课的做法，把指定学生的计算结果写回学生表。
-- 本课只计算已录分的课程：NULL 不进入分子或分母，0 分会参与计算。
CREATE PROCEDURE lab36_refresh_credit_grade(IN p_sno INT)
UPDATE lab36_student
SET credit_grade = (
    SELECT ROUND(SUM(sc.grade * c.credit) / SUM(c.credit), 2)
    FROM lab36_sc AS sc
    JOIN lab36_course AS c ON sc.cno = c.cno
    WHERE sc.sno = p_sno AND sc.grade IS NOT NULL
)
WHERE sno = p_sno;

-- 设置初始学绩分；后面的自测直接改成绩，不再手动调用过程。
CALL lab36_refresh_credit_grade(101);
CALL lab36_refresh_credit_grade(102);

-- 提供：上一课的 BEFORE UPDATE 检查，只负责拒绝越界的非空新成绩。
DELIMITER $$
CREATE TRIGGER lab36_sc_before_update
BEFORE UPDATE ON lab36_sc
FOR EACH ROW
BEGIN
    IF NOT (OLD.grade <=> NEW.grade) THEN
        IF NEW.grade IS NOT NULL AND (NEW.grade < 0 OR NEW.grade > 100) THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'grade must be between 0 and 100';
        END IF;
    END IF;
END$$
DELIMITER ;

-- 【练习】定义 lab36_sc_after_update。
-- 成绩确实变化时，自动调用 lab36_refresh_credit_grade，传入这行的学号。
-- 解除注释、完成 TODO 后，选中整个创建区运行。
DELIMITER $$
CREATE TRIGGER lab36_sc_after_update
AFTER UPDATE ON lab36_sc
FOR EACH ROW
BEGIN
    IF NOT(OLD.grade <=> NEW.grade) THEN
        CALL lab36_refresh_credit_grade(new.sno);
    END IF;
END$$
DELIMITER ;


-- 【自测】先确认初始学绩分：101 是 80.00，102 是 75.00。
SELECT sno, sname, credit_grade FROM lab36_student ORDER BY sno;

-- 把 101 的第 2 门课从 76 改到 94：只有 101 的学绩分应变成 92.00。
UPDATE lab36_sc SET grade = 94 WHERE sno = 101 AND cno = 2;
SELECT sno, sname, credit_grade FROM lab36_student ORDER BY sno;

-- 再写一次相同的成绩：没有变化，学绩分仍为 92.00。
UPDATE lab36_sc SET grade = 94 WHERE sno = 101 AND cno = 2;
SELECT sno, sname, credit_grade FROM lab36_student ORDER BY sno;

-- 清为待录：只剩第 1 门课参与计算，101 的学绩分变为 88.00。
UPDATE lab36_sc SET grade = NULL WHERE sno = 101 AND cno = 2;
SELECT sno, sname, credit_grade FROM lab36_student ORDER BY sno;

-- 选做：单独运行下一条，预期报 1644。之后再查询明细和学绩分核对。
UPDATE lab36_sc SET grade = 101 WHERE sno = 101 AND cno = 2;

-- 观察：若在 BEFORE UPDATE 中调用过程，第一次改 76→94 时，过程里的
--       SELECT 从成绩表读到的是 76 还是 94？会算出哪个学绩分？
-- BEFORE 时 NEW.grade 已经是 94，但成绩表还存着 76。过程查的是表，所以算出 80.00。AFTER 时查到 94，才会算出 92.00。