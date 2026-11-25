-- MySQL 第三十五课：用 BEFORE UPDATE 触发器检查修改后的成绩。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 准备区只重建本课的 lab35_sc 表、删除本课的旧触发器。

-- 【准备区】
USE db_lab;
DROP TRIGGER IF EXISTS lab35_sc_before_update;
DROP TABLE IF EXISTS lab35_sc;

CREATE TABLE lab35_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL,
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

INSERT INTO lab35_sc (sno, cno, grade) VALUES
    (101, 1, 88.00), (102, 1, NULL), (103, 1, 76.00);

-- 【练习】解除注释，补全触发器；选中整个创建区运行。
-- 先用 OLD.grade 和 NEW.grade 判断成绩是否改变，注意 NULL。
-- 成绩改变时，只有非空的新成绩超出 0～100 才报 1644。
DELIMITER $$
CREATE TRIGGER lab35_sc_before_update
BEFORE UPDATE ON lab35_sc
FOR EACH ROW
BEGIN
-- TODO：成绩改变后，检查 NEW.grade，用 SIGNAL 拒绝越界值。
    IF NOT (OLD.grade <=> NEW.grade) THEN
        IF NEW.grade IS NOT NULL AND (NEW.grade < 0 OR NEW.grade > 100) THEN
            SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'grade must be between 0 and 100';
        END IF;
    END IF;
END$$
DELIMITER ;


-- 【自测 1】下面五次更新都应运行成功。
UPDATE lab35_sc SET grade = 88.00 WHERE sno = 101 AND cno = 1; -- 没变
UPDATE lab35_sc SET grade = 92.00 WHERE sno = 101 AND cno = 1; -- 合法改分
UPDATE lab35_sc SET grade = 65.00 WHERE sno = 102 AND cno = 1; -- 补录
UPDATE lab35_sc SET grade = NULL WHERE sno = 103 AND cno = 1; -- 清为待录
UPDATE lab35_sc SET grade = NULL WHERE sno = 103 AND cno = 1; -- 仍是待录

-- 【自测 2】分别单独运行，每条都应报 1644。
UPDATE lab35_sc SET grade = 101.00 WHERE sno = 101 AND cno = 1;
UPDATE lab35_sc SET grade = -1.00 WHERE sno = 103 AND cno = 1;

-- 【自测 3】最终应保留 101→92.00、102→65.00、103→NULL。
SELECT sno, cno, grade FROM lab35_sc ORDER BY sno, cno;

-- 观察：103 的原成绩是 NULL。为什么用 OLD.grade <> NEW.grade
--       判断是否改变时，可能放过把 103 改成 -1 的那条语句？
-- 如果是NULL，用<>的时候会输出NULL，无法过外层的检查，就可能会被写入不合法的值。