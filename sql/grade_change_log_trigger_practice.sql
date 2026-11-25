-- MySQL 第三十七课：用触发器记录成绩变更。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 准备区只重建本课的 lab37 表和触发器。先整段运行准备区。

-- 【准备区】
USE db_lab;
DROP TRIGGER IF EXISTS lab37_sc_after_update_log;
DROP TRIGGER IF EXISTS lab37_sc_before_update;
DROP TABLE IF EXISTS lab37_sc_grade_log;
DROP TABLE IF EXISTS lab37_sc;

CREATE TABLE lab37_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL,
    op_user VARCHAR(20) DEFAULT NULL,
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

CREATE TABLE lab37_sc_grade_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sno INT NOT NULL,
    cno INT NOT NULL,
    old_grade DECIMAL(5,2) DEFAULT NULL,
    new_grade DECIMAL(5,2) DEFAULT NULL,
    op_desc VARCHAR(30) NOT NULL,
    op_user VARCHAR(20) DEFAULT NULL,
    op_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO lab37_sc (sno, cno, grade) VALUES (101, 1, 88), (102, 1, NULL);

-- 提供：更新前检查，新成绩越界时拒绝本次更新。
DELIMITER $$
CREATE TRIGGER lab37_sc_before_update
BEFORE UPDATE ON lab37_sc
FOR EACH ROW
BEGIN
    IF NEW.grade IS NOT NULL AND (NEW.grade < 0 OR NEW.grade > 100) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'grade must be between 0 and 100';
    END IF;
END$$
DELIMITER ;

-- 【练习】解除注释、补全触发器，再选中整个创建区运行。
-- 只有 grade 确实变化时，才向 lab37_sc_grade_log 插入一条日志。
-- 记录学号、课程号、旧分、新分、操作描述「修改成绩」和本次操作人。
-- 由日志表自动填 id、op_time，这两个字段不用写在 INSERT 里。
DELIMITER $$
CREATE TRIGGER lab37_sc_after_update_log
AFTER UPDATE ON lab37_sc
FOR EACH ROW
BEGIN
    IF NOT (NEW.grade <=> OLD.grade) THEN
        INSERT INTO lab37_sc_grade_log
            (sno, cno, old_grade, new_grade, op_desc, op_user)
        VALUES
            (NEW.sno, NEW.cno, OLD.grade, NEW.grade, '修改成绩', NEW.op_user);
    END IF;
END$$
DELIMITER ;


-- 【自测 1】88 → 92，预计新增 1 条日志。
UPDATE lab37_sc SET grade = 92, op_user = '教务A' WHERE sno = 101 AND cno = 1;
SELECT * FROM lab37_sc_grade_log ORDER BY id;

-- 【自测 2】只改 op_user，保留 92 分，日志应仍有 1 条。
UPDATE lab37_sc SET op_user = '教务B' WHERE sno = 101 AND cno = 1;
SELECT * FROM lab37_sc_grade_log ORDER BY id;

-- 【自测 3】补录 76 分、清空 92 分，各新增 1 条日志。
UPDATE lab37_sc SET grade = 76, op_user = '教务B' WHERE sno = 102 AND cno = 1;
UPDATE lab37_sc SET grade = NULL, op_user = '教务A' WHERE sno = 101 AND cno = 1;
SELECT * FROM lab37_sc_grade_log ORDER BY id; -- 共 3 条，顺序为 88→92、NULL→76、92→NULL

-- 选做：单独运行下一条，预期报 1644；再查日志仍是 3 条，102 仍是 76 分。
UPDATE lab37_sc SET grade = 101, op_user = '教务A' WHERE sno = 102 AND cno = 1;

-- 观察：为什么只修改 op_user 不会新增日志？日志里的旧分、新分和本次操作人分别从哪取？
-- UPDATE 成功后会触发这段代码；只有成绩确实变化时，IF 里面的 INSERT 才写日志。
-- 旧分取 OLD.grade，新分取 NEW.grade，本次操作人取 NEW.op_user。