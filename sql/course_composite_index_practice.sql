-- MySQL 第二十三课。对比单列索引和组合索引的执行计划。
-- 在 Navicat 选「数据库实验」和 db_lab，只在 TODO 处添加一条建索引语句。
-- 索引名为 idx_lab23_cno_grade，按课程号、成绩的顺序写两列。
-- 整份运行，比较结果 1、2 的 key、type、rows。结果 3 是实际匹配行数。
-- 观察：组合索引先按课程号定位，再按成绩取范围，MySQL 改用 idx_lab23_cno_grade。
-- type 从 ref 变成 range，查询实际匹配 6 条选课。

DROP TEMPORARY TABLE IF EXISTS lab23_sc;

CREATE TEMPORARY TABLE lab23_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2) NOT NULL,
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

-- 准备 10000 条样例选课，平均分布在 100 门课。
INSERT INTO lab23_sc (sno, cno, grade)
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

CREATE INDEX idx_lab23_cno ON lab23_sc (cno);

-- 有课程号单列索引时的计划。
EXPLAIN FORMAT=TRADITIONAL
SELECT sno, grade
FROM lab23_sc
WHERE cno = 42 AND grade BETWEEN 85 AND 90;

-- TODO：在这里添加组合索引。
CREATE INDEX idx_lab23_cno_grade ON lab23_sc (cno, grade);

-- 添加组合索引后，再看同一条查询。
EXPLAIN FORMAT=TRADITIONAL
SELECT sno, grade
FROM lab23_sc
WHERE cno = 42 AND grade BETWEEN 85 AND 90;

SELECT COUNT(*) AS actual_rows
FROM lab23_sc
WHERE cno = 42 AND grade BETWEEN 85 AND 90;
