-- MySQL 第二课。查出学生学号、姓名、选修课程名称和成绩。
-- 已完成（2026-11-12）。每行表示一次选课，先按学号升序，同学号按课程号升序。
-- 自述：两个连接分别匹配学号和课程号，成绩为 NULL 的选课记录也会显示。

WITH student_sample AS (
    SELECT 101 AS sno, '小林' AS sname
    UNION ALL SELECT 102, '小陈'
    UNION ALL SELECT 103, '小周'
),
course_sample AS (
    SELECT 1 AS cno, '数据库原理' AS cname
    UNION ALL SELECT 2, '计算机网络'
    UNION ALL SELECT 3, '操作系统'
),
sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 102, 1, NULL
    UNION ALL SELECT 101, 2, 76
)
SELECT s.sno, s.sname, c.cname, e.grade
FROM sc_sample AS e
LEFT JOIN student_sample AS s ON e.sno = s.sno
LEFT JOIN course_sample AS c ON e.cno = c.cno
ORDER BY e.sno ASC, e.cno ASC;
