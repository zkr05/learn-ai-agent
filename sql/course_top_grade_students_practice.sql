-- MySQL 第十四课。找出每门课达到最高分的所有学生，包括并列。
-- 在 Navicat 选「数据库实验」和 db_lab。保留数据准备段，每次运行整份脚本。
-- 返回 cno、cname、sno、sname、grade，按课程号、学号升序。
-- 只有已录成绩才能入选，0 分参与比较。
-- 观察：按课程号和分数连接最高分表，1 号课的两条 90 分都能匹配。
-- 使用内连接筛掉未达到本课最高分的选课记录，5 号课的已录 0 分保留。

DROP TEMPORARY TABLE IF EXISTS lab14_course_max, lab14_sc, lab14_student, lab14_course;

CREATE TEMPORARY TABLE lab14_course (
    cno INT PRIMARY KEY,
    cname VARCHAR(30) NOT NULL
);

CREATE TEMPORARY TABLE lab14_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL
);

CREATE TEMPORARY TABLE lab14_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2),
    PRIMARY KEY (sno, cno)
);

INSERT INTO lab14_course (cno, cname) VALUES
    (1, '数据库原理'),
    (2, '计算机网络'),
    (3, '操作系统'),
    (4, '软件工程'),
    (5, '离散数学');

INSERT INTO lab14_student (sno, sname) VALUES
    (101, '小林'),
    (102, '小陈'),
    (103, '小周'),
    (104, '小吴');

INSERT INTO lab14_sc (sno, cno, grade) VALUES
    (101, 1, 90),
    (102, 1, 90),
    (103, 1, 70),
    (104, 1, NULL),
    (101, 2, 95),
    (103, 2, 90),
    (102, 4, NULL),
    (104, 5, 0);

-- 第一步：把下面的查询改成每门课一行，返回 cno 和 max_grade。
-- 核对结果后，在 SELECT 前加 CREATE TEMPORARY TABLE lab14_course_max AS。
CREATE TEMPORARY TABLE lab14_course_max AS
SELECT cno, MAX(grade) AS max_grade
FROM lab14_sc
GROUP BY cno
ORDER BY cno;

-- 第二步：在这里写另一条 SELECT，把最高分接回选课明细，再查课程名和学生姓名。
SELECT sc.cno, c.cname, sc.sno, st.sname, sc.grade
FROM lab14_sc AS sc
JOIN lab14_course_max AS cm ON cm.cno = sc.cno AND cm.max_grade = sc.grade
LEFT JOIN lab14_student AS st ON st.sno = sc.sno
LEFT JOIN lab14_course AS c ON c.cno = sc.cno
ORDER BY sc.cno, sc.sno;
