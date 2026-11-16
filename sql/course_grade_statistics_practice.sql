-- MySQL 第十三课。学校实验二：查每门课程的最高分、最低分、平均分。
-- 在 Navicat 选「数据库实验」连接和 db_lab，运行整个脚本。
-- 前半段准备本连接临时表。请修改最后的 SELECT，再运行整个脚本。
-- 返回 cno、cname、max_grade、min_grade、avg_grade，按课程号升序。
-- 每门课一行。保留无人选课或全未录分的课，成绩统计显示 NULL。
-- 观察：按课分组后有四行。有选课但没录分和无人选课的课，三项成绩统计都为 NULL。
-- 0 分是已录成绩，参与最低分和平均分的计算。

DROP TEMPORARY TABLE IF EXISTS lab13_sc, lab13_course;

CREATE TEMPORARY TABLE lab13_course (
    cno INT PRIMARY KEY,
    cname VARCHAR(30) NOT NULL
);

CREATE TEMPORARY TABLE lab13_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2),
    PRIMARY KEY (sno, cno)
);

INSERT INTO lab13_course (cno, cname) VALUES
    (1, '数据库原理'),
    (2, '计算机网络'),
    (3, '操作系统'),
    (4, '离散数学');

INSERT INTO lab13_sc (sno, cno, grade) VALUES
    (101, 1, 90),
    (102, 1, 70),
    (103, 1, NULL),
    (101, 2, NULL),
    (102, 4, 0),
    (104, 4, 60);

-- 练习从这里开始。先连接查看每行，再按课程分组统计。
SELECT c.cno, c.cname, MAX(sc.grade) AS max_grade, MIN(sc.grade) AS min_grade, AVG(sc.grade) AS avg_grade
FROM lab13_course AS c
LEFT JOIN lab13_sc AS sc ON sc.cno = c.cno
GROUP BY cno
ORDER BY c.cno;
