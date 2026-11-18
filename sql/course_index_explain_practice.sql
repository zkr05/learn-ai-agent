-- MySQL 第二十二课。对比加课程号索引前后的执行计划。
-- 在 Navicat 选「数据库实验」和 db_lab。保留数据准备部分，运行整份脚本。
-- 在两条 EXPLAIN 中间的 TODO 处添加单列索引，名字用 idx_lab22_cno。
-- 对照两份执行计划的 type、key、rows。42 号课实际有 100 条选课记录。
-- 观察：添加 cno 索引后，MySQL 从全表扫描改成按索引查找，实际匹配仍是 100 条。
-- 在 Navicat 的结果 1 和结果 2 对比执行计划，结果 3 显示实际匹配行数。

DROP TEMPORARY TABLE IF EXISTS lab22_sc;

CREATE TEMPORARY TABLE lab22_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2) NOT NULL,
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

-- 准备 10000 条样例选课，平均分布在 100 门课，仅用于对比执行计划。
INSERT INTO lab22_sc (sno, cno, grade)
WITH digits AS (
    SELECT 0 AS digit
    UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3
    UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6
    UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9
), numbers AS (
    SELECT ones.digit + 10 * tens.digit + 100 * hundreds.digit + 1000 * thousands.digit AS n
    FROM digits AS ones
    CROSS JOIN digits AS tens
    CROSS JOIN digits AS hundreds
    CROSS JOIN digits AS thousands
)
SELECT n + 1, MOD(n, 100) + 1, MOD(n, 101)
FROM numbers;

-- 加索引前。
EXPLAIN FORMAT=TRADITIONAL
SELECT sno, grade
FROM lab22_sc
WHERE cno = 42;

-- TODO：在这里给 cno 建一个单列索引。
CREATE INDEX idx_lab22_cno ON lab22_sc (cno);

-- 加索引后，再看完全相同的查询。
EXPLAIN FORMAT=TRADITIONAL
SELECT sno, grade
FROM lab22_sc
WHERE cno = 42;

SELECT COUNT(*) AS actual_rows
FROM lab22_sc
WHERE cno = 42;
