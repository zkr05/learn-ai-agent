-- MySQL 第三十九课：串联录分、改分、逻辑删除、学绩分重算和日志。
-- Navicat 沿用「数据库实验－函数」（127.0.0.1:3308），选中 db_lab。
-- 准备区只重建本课的 lab39 对象。先整段运行准备区。

-- 【准备区】
USE db_lab;
DROP TRIGGER IF EXISTS lab39_sc_after_update;
DROP TRIGGER IF EXISTS lab39_sc_after_insert;
DROP TRIGGER IF EXISTS lab39_sc_before_update;
DROP TRIGGER IF EXISTS lab39_sc_before_insert;
DROP TRIGGER IF EXISTS lab39_sc_before_delete;
DROP PROCEDURE IF EXISTS lab39_sc_delete;
DROP PROCEDURE IF EXISTS lab39_sc_update;
DROP PROCEDURE IF EXISTS lab39_sc_insert;
DROP PROCEDURE IF EXISTS lab39_refresh_credit_grade;
DROP TABLE IF EXISTS lab39_sc_grade_log;
DROP TABLE IF EXISTS lab39_sc;
DROP TABLE IF EXISTS lab39_course;
DROP TABLE IF EXISTS lab39_student;

CREATE TABLE lab39_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL,
    credit_grade DECIMAL(5,2) DEFAULT NULL
) ENGINE=InnoDB;

CREATE TABLE lab39_course (
    cno INT PRIMARY KEY,
    credit INT NOT NULL CHECK (credit > 0)
) ENGINE=InnoDB;

CREATE TABLE lab39_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(5,2) DEFAULT NULL,
    op_user VARCHAR(20) NOT NULL,
    is_del TINYINT NOT NULL DEFAULT 0,
    PRIMARY KEY (sno, cno),
    FOREIGN KEY (sno) REFERENCES lab39_student(sno),
    FOREIGN KEY (cno) REFERENCES lab39_course(cno),
    CHECK (is_del IN (0, 1))
) ENGINE=InnoDB;

CREATE TABLE lab39_sc_grade_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sno INT NOT NULL,
    cno INT NOT NULL,
    old_grade DECIMAL(5,2) DEFAULT NULL,
    new_grade DECIMAL(5,2) DEFAULT NULL,
    op_desc VARCHAR(30) NOT NULL,
    op_user VARCHAR(20) NOT NULL,
    op_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

INSERT INTO lab39_student (sno, sname) VALUES (101, '小林'), (102, '小陈');
INSERT INTO lab39_course (cno, credit) VALUES (1, 2), (2, 4), (3, 2);
INSERT INTO lab39_sc (sno, cno, grade, op_user) VALUES
    (101, 1, 88, '初始化'), (101, 2, 76, '初始化'), (102, 1, 75, '初始化');

-- 提供：只使用在用且有成绩的选课，重算一位学生的学绩分。
CREATE PROCEDURE lab39_refresh_credit_grade(IN p_sno INT)
UPDATE lab39_student
SET credit_grade = (
    SELECT ROUND(SUM(sc.grade * c.credit) / SUM(c.credit), 2)
    FROM lab39_sc AS sc
    JOIN lab39_course AS c ON c.cno = sc.cno
    WHERE sc.sno = p_sno AND sc.grade IS NOT NULL AND sc.is_del = 0
)
WHERE sno = p_sno;

CALL lab39_refresh_credit_grade(101);
CALL lab39_refresh_credit_grade(102);

-- 提供：应用调用的三个入口，一次操作只处理一条选课记录。
CREATE PROCEDURE lab39_sc_insert(
    IN p_sno INT, IN p_cno INT, IN p_grade DECIMAL(5,2), IN p_op_user VARCHAR(20)
)
INSERT INTO lab39_sc (sno, cno, grade, op_user)
VALUES (p_sno, p_cno, p_grade, p_op_user);

CREATE PROCEDURE lab39_sc_update(
    IN p_sno INT, IN p_cno INT, IN p_grade DECIMAL(5,2), IN p_op_user VARCHAR(20)
)
UPDATE lab39_sc SET grade = p_grade, op_user = p_op_user
WHERE sno = p_sno AND cno = p_cno AND is_del = 0;

CREATE PROCEDURE lab39_sc_delete(IN p_sno INT, IN p_cno INT, IN p_op_user VARCHAR(20))
UPDATE lab39_sc SET is_del = 1, op_user = p_op_user
WHERE sno = p_sno AND cno = p_cno AND is_del = 0;

-- 提供：先检查，写入成功后才更新学绩分并写日志。
DELIMITER $$
CREATE TRIGGER lab39_sc_before_insert
BEFORE INSERT ON lab39_sc
FOR EACH ROW
BEGIN
    IF NEW.grade IS NOT NULL AND (NEW.grade < 0 OR NEW.grade > 100) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'grade must be between 0 and 100';
    END IF;
END$$

CREATE TRIGGER lab39_sc_before_update
BEFORE UPDATE ON lab39_sc
FOR EACH ROW
BEGIN
    IF OLD.is_del = 1 AND NEW.is_del = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'deleted enrollment cannot be restored';
    END IF;
    IF NEW.grade IS NOT NULL AND (NEW.grade < 0 OR NEW.grade > 100) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'grade must be between 0 and 100';
    END IF;
END$$

CREATE TRIGGER lab39_sc_before_delete
BEFORE DELETE ON lab39_sc
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'direct delete is not allowed';
END$$

CREATE TRIGGER lab39_sc_after_insert
AFTER INSERT ON lab39_sc
FOR EACH ROW
BEGIN
    INSERT INTO lab39_sc_grade_log (sno, cno, old_grade, new_grade, op_desc, op_user)
    VALUES (NEW.sno, NEW.cno, NULL, NEW.grade, '新增成绩', NEW.op_user);
    CALL lab39_refresh_credit_grade(NEW.sno);
END$$
DELIMITER ;

-- 【练习】解除注释并补齐 AFTER UPDATE，再运行整个创建区。
-- 1. 从在用变成已删除：写「逻辑删除」日志，旧成绩保留在日志里；
--    日志 new_grade 记 NULL，表示这门课不再有在用成绩，再重算学绩分。
-- 2. 更新前后都在用、且成绩确实变化：写「修改成绩」，记录旧分和新分，再重算。
-- 3. 其他 UPDATE 不写日志、不重算。两个分支可用 IF ... ELSEIF ... END IF。
DELIMITER $$
CREATE TRIGGER lab39_sc_after_update
AFTER UPDATE ON lab39_sc
FOR EACH ROW
BEGIN
    IF OLD.is_del = 0 AND NEW.is_del = 1 THEN
        INSERT INTO lab39_sc_grade_log (sno, cno, old_grade, new_grade, op_desc, op_user)
        VALUES (NEW.sno, NEW.cno, OLD.grade, NULL, '逻辑删除', NEW.op_user);
        CALL lab39_refresh_credit_grade(NEW.sno);
    ELSEIF OLD.is_del = 0 AND NEW.is_del = 0
        AND NOT (OLD.grade <=> NEW.grade) THEN
        INSERT INTO lab39_sc_grade_log (sno, cno, old_grade, new_grade, op_desc, op_user)
        VALUES (NEW.sno, NEW.cno, OLD.grade, NEW.grade, '修改成绩', NEW.op_user);
        CALL lab39_refresh_credit_grade(NEW.sno);
    END IF;
END$$
DELIMITER ;


-- 【自测】每完成一个 CALL，就运行下面的「核对查询」，比较三张表。
-- 初始 101 学绩分为 80.00，102 为 75.00，日志为空。
CALL lab39_sc_insert(101, 3, 92, '教务A'); -- 101：83.00；日志 1 条
CALL lab39_sc_update(101, 2, 94, '教务B'); -- 101：92.00；日志 2 条
CALL lab39_sc_delete(101, 2, '教务C');     -- 101：90.00；日志 3 条
CALL lab39_sc_delete(101, 2, '教务D');     -- 重复删除；日志仍 3 条
CALL lab39_sc_update(101, 3, 92, '教务D'); -- 分数没变；日志仍 3 条

-- 【核对查询】最终 101/2 原行仍在：grade=94.00、is_del=1、op_user=教务C。
SELECT sno, cno, grade, is_del, op_user FROM lab39_sc ORDER BY sno, cno;
SELECT sno, credit_grade FROM lab39_student ORDER BY sno;
SELECT sno, cno, old_grade, new_grade, op_desc, op_user FROM lab39_sc_grade_log ORDER BY id;

-- 选做：解除注释、单独运行，应该报 1644；再核对，成绩、学绩分和日志都不变。
CALL lab39_sc_update(101, 1, 101, '教务D');

-- 观察：第 2 门课被逻辑删除后，原表明明还保留着 94 分，为什么学绩分会变成 90？
--       越界改分被拒绝时，为什么没有附带产生一条改分日志？

-- 第二课被删除之后，is_del 变成 1，不满足重算成绩里面的筛选is_del 为 0
-- 改分日志的前提是，这条改分不会被拒绝，并且两个成绩不同才会有改分日志。