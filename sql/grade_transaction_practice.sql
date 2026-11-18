-- MySQL 第二十五课。对比一批成绩更新的回滚和提交。
-- 在 Navicat 选「数据库实验」和 db_lab，运行整份脚本。
-- 两个事务都要把 101 的 2 号课改为 93，把 102 的 2 号课改为 82。
-- 第一段保留 ROLLBACK，第二段把 ROLLBACK 改成 COMMIT。
-- 比较三个结果页中的两条成绩，按学号顺序查看。
-- 观察：第一次事务的两条更新可见，回滚后一起恢复为 NULL 和 76。
-- 第二次事务执行同样的更新，提交后保留 93 和 82。

DROP TEMPORARY TABLE IF EXISTS lab25_sc;

CREATE TEMPORARY TABLE lab25_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2),
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

INSERT INTO lab25_sc (sno, cno, grade) VALUES
    (101, 1, 88),
    (101, 2, NULL),
    (102, 2, 76);

-- 第一段事务。写入两条成绩，然后回滚。
START TRANSACTION;

-- TODO 1：写两条 UPDATE，分别更新两位学生的 2 号课成绩。
UPDATE lab25_sc
SET grade = 93
WHERE sno = 101 AND cno = 2;

UPDATE lab25_sc
SET grade = 82
WHERE sno = 102 AND cno = 2;
-- 结果 1：回滚前，在当前连接查看事务内的成绩，应为 93 和 82。
SELECT sno, cno, grade
FROM lab25_sc
WHERE cno = 2
ORDER BY sno;

ROLLBACK;

-- 结果 2：回滚后，应恢复为 NULL 和 76。
SELECT sno, cno, grade
FROM lab25_sc
WHERE cno = 2
ORDER BY sno;

-- 第二段事务。再次执行同一批更新，然后提交。
START TRANSACTION;

-- TODO 2：写入上面相同的两条 UPDATE。
UPDATE lab25_sc
SET grade = 93
WHERE sno = 101 AND cno = 2;

UPDATE lab25_sc
SET grade = 82
WHERE sno = 102 AND cno = 2;
-- TODO 3：把这一句改为 COMMIT，提交第二段的更新。
COMMIT;

-- 结果 3：提交后，应保留 93 和 82。
SELECT sno, cno, grade
FROM lab25_sc
WHERE cno = 2
ORDER BY sno;
