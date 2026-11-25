-- MySQL 第三十八课：用标记逻辑删除选课记录，并保留日志。
-- 沿用 Navicat「数据库实验－函数」连接（127.0.0.1:3308），选中 db_lab。
-- 准备区只重建本课的 lab38 对象。先整段运行准备区。

-- 【准备区】
USE db_lab;
DROP PROCEDURE IF EXISTS lab38_delete_enrollment;
DROP TRIGGER IF EXISTS lab38_sc_before_delete;
DROP TRIGGER IF EXISTS lab38_sc_before_update;
DROP TRIGGER IF EXISTS lab38_sc_after_update;
DROP TABLE IF EXISTS lab38_sc_grade_log;
DROP TABLE IF EXISTS lab38_sc;

CREATE TABLE lab38_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL,
    op_user VARCHAR(20) DEFAULT NULL,
    is_del TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (sno, cno),
    CHECK (is_del IN (0, 1))
) ENGINE=InnoDB;

CREATE TABLE lab38_sc_grade_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL,
    op_desc VARCHAR(30) NOT NULL,
    op_user VARCHAR(20) DEFAULT NULL,
    op_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO lab38_sc (sno, cno, grade) VALUES
    (101, 1, 88), (101, 2, 76), (102, 1, 65);

-- 提供：禁止物理删除；禁止把已删除记录改回在用；标记从 0 → 1 时记日志。
DELIMITER $$
CREATE TRIGGER lab38_sc_before_delete
BEFORE DELETE ON lab38_sc
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'direct delete is not allowed';
END$$

CREATE TRIGGER lab38_sc_before_update
BEFORE UPDATE ON lab38_sc
FOR EACH ROW
BEGIN
    IF OLD.is_del = 1 AND NEW.is_del = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'deleted enrollment cannot be restored';
    END IF;
END$$

CREATE TRIGGER lab38_sc_after_update
AFTER UPDATE ON lab38_sc
FOR EACH ROW
BEGIN
    IF OLD.is_del = 0 AND NEW.is_del = 1 THEN
        INSERT INTO lab38_sc_grade_log (sno, cno, grade, op_desc, op_user)
        VALUES (NEW.sno, NEW.cno, OLD.grade, '逻辑删除', NEW.op_user);
    END IF;
END$$
DELIMITER ;

-- 【练习 1】用一条 UPDATE 作为过程主体。传入学号、课号和本次操作人。
-- 只处理还在用的目标行，把 is_del 改为 1，并把操作者写入 op_user。
CREATE PROCEDURE lab38_delete_enrollment(
    IN p_sno INT, IN p_cno INT, IN p_op_user VARCHAR(20)
)
UPDATE lab38_sc
SET is_del = 1, op_user = p_op_user
WHERE sno = p_sno
  AND cno = p_cno
  AND is_del = 0;


-- 【练习 2】写日常名单查询，只显示仍在用的选课记录，按学号、课号排序。
-- 删除前应有 3 行；完成第一次 CALL 后再执行，应该只剩 2 行。
SELECT sno, cno, grade, is_del
FROM lab38_sc
WHERE is_del = 0
ORDER BY sno, cno;

-- 【自测 1】把 101 的第 2 门课标记为已删除。
CALL lab38_delete_enrollment(101, 2, '教务A');
SELECT sno, cno, grade, is_del, op_user FROM lab38_sc ORDER BY sno, cno;
SELECT sno, cno, grade, op_desc, op_user FROM lab38_sc_grade_log ORDER BY id;

-- 【自测 2】用另一个操作人重复调用。101/2 仍是教务A，日志仍是一条。
CALL lab38_delete_enrollment(101, 2, '教务B');
SELECT sno, cno, grade, is_del, op_user FROM lab38_sc ORDER BY sno, cno;
SELECT sno, cno, grade, op_desc, op_user FROM lab38_sc_grade_log ORDER BY id;

-- 选做：下列两句分别解除注释、单独运行，预期各报 1644。
DELETE FROM lab38_sc WHERE sno = 102 AND cno = 1;
UPDATE lab38_sc SET is_del = 0 WHERE sno = 101 AND cno = 2;

-- 观察：为什么重复调用时不能把教务A改成教务B？查询在用记录时为什么要筛 is_del？
-- 因为调用一次之后is_del = 1了，无法满足where筛选的要求，就没有触发触发器。
-- 因为逻辑删除是把is_del set 为 1，如果不筛选，删除后的依然会出现。