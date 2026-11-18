-- MySQL 第二十四课。只给 101 号学生的 2 号课补录 93 分。
-- 在 Navicat 选「数据库实验」和 db_lab。完成两个 TODO，运行整份脚本。
-- 第一个结果应只有 (101, 2, NULL)。最后确认只改了这一条记录。
-- 观察：先用 SELECT 验证学号和课程号只匹配一条记录，再用相同条件更新。
-- 只有 101 的 2 号课从未录分变为 93，其余两条成绩仍为 88 和 76。

DROP TEMPORARY TABLE IF EXISTS lab24_sc;

CREATE TEMPORARY TABLE lab24_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2),
    PRIMARY KEY (sno, cno)
) ENGINE=InnoDB;

INSERT INTO lab24_sc (sno, cno, grade) VALUES
    (101, 1, 88),
    (101, 2, NULL),
    (102, 2, 76);

-- TODO 1：用 SELECT 确认要修改的是哪一条选课记录。
SELECT sno, cno, grade
FROM lab24_sc
WHERE sno = 101 AND cno = 2;
-- TODO 2：使用同一个 WHERE 条件，把这条记录的成绩改为 93。
UPDATE lab24_sc
SET grade = 93
WHERE sno = 101 AND cno = 2;
-- 检查更新后的三条记录。
SELECT sno, cno, grade
FROM lab24_sc
ORDER BY sno, cno;
