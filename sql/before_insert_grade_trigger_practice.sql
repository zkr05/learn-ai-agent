-- MySQL 第三十四课：用 BEFORE INSERT 触发器检查新录入的成绩。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 准备区只重建本课的 lab34_sc 表、删除本课的旧触发器。

-- 【准备区】
USE db_lab;
DROP TRIGGER IF EXISTS lab34_sc_before_insert;
DROP TABLE IF EXISTS lab34_sc;

CREATE TABLE lab34_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL,
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

-- 【练习】解除注释并填写 TODO。创建触发器时选中这整段，包括两个 DELIMITER。
-- 非空的成绩只允许 0 到 100（含边界）。NULL 表示尚未录分，应允许写入。
DELIMITER $$
CREATE TRIGGER lab34_sc_before_insert
BEFORE INSERT ON lab34_sc
FOR EACH ROW
BEGIN
-- TODO：检查 NEW.grade，在不合法时用 SIGNAL 抛出自定义错误。
    IF NEW.grade IS NOT NULL AND (NEW.grade < 0 OR NEW.grade > 100) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'grade must be between 0 and 100';
    END IF;
END$$

DELIMITER ;


-- 【自测 1】创建成功后，选中这一条 INSERT，应写入全部四行。
INSERT INTO lab34_sc (sno, cno, grade) VALUES
    (101, 1, 88.00), (102, 1, NULL), (103, 1, 0.00), (104, 1, 100.00);

-- 【自测 2】下面两条分别选中运行。预期都被拒绝，错误码为 1644。
INSERT INTO lab34_sc (sno, cno, grade) VALUES (105, 1, 101.00);
INSERT INTO lab34_sc (sno, cno, grade) VALUES (106, 1, -1.00);

-- 【自测 3】确认表里只有 101～104 的四行，102 的成绩仍为 NULL。
SELECT sno, cno, grade FROM lab34_sc ORDER BY sno, cno;

-- 观察：没有 CALL，触发器为什么也会运行？NEW.grade 指的是哪一个值？
-- 触发器的运行规则是每次插入前检查，默认运行，是指插入值的成绩。