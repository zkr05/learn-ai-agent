-- MySQL 第二十课。让数据库检查录入的成绩是否在 0 至 100 分之间，含两端。
-- 成绩为 NULL 表示尚未录入，应允许。给建表语句加一条 CHECK。
-- 在 Navicat 选「数据库实验」和 db_lab，运行整份脚本。前面会重建本课的临时表。
-- 正常结果应有 4 行。再逐条取消末尾测试的注释，整份运行，预期测试插入报 3819。
-- 测试完成后恢复注释，保存正常能运行的版本。
-- 观察：BETWEEN 包含 0 和 100 两端。成绩为 NULL 时比较结果未知，允许未录入。
-- 正常的四行均可插入，-1 和 100.01 都被 CHECK 拒绝，报错 3819。

DROP TEMPORARY TABLE IF EXISTS lab20_sc;

CREATE TEMPORARY TABLE lab20_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2),
    PRIMARY KEY (sno, cno),
    CHECK (grade BETWEEN 0 AND 100)
    -- 在这里加成绩范围约束，记得用逗号和上一项分隔。
) ENGINE=InnoDB;

INSERT INTO lab20_sc (sno, cno, grade) VALUES
    (101, 1, 0),
    (101, 2, 100),
    (102, 1, 88.50),
    (102, 2, NULL);

SELECT sno, cno, grade
FROM lab20_sc
ORDER BY sno, cno;

-- 测试 1：低于 0 分，应报 3819。
-- INSERT INTO lab20_sc (sno, cno, grade) VALUES (103, 1, -1);

-- 测试 2：高于 100 分，应报 3819。
-- INSERT INTO lab20_sc (sno, cno, grade) VALUES (103, 2, 100.01);
