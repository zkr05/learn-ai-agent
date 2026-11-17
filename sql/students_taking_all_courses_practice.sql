-- MySQL 第十六课。查找选修了全部课程的学生。
-- sc_sample 中有该学生和课程的记录就算已选，成绩可以为 NULL。
-- 第一步：从 student_sample 出发，找没有选 3 号课的学生。预期 102、104。
-- 第二步：改成查选修全部课程的学生。预期 101、105。
-- 两步都返回 sno、sname，按学号升序。保留 WITH 样例，修改末尾查询。
-- 观察：内层按学号和课程号查选课，找不到记录的课进入该学生的漏选清单。
-- 外层保留漏选清单为空的学生，101 和 105 入选。成绩为 NULL 的记录仍算已选。

WITH student_sample AS (
    SELECT 101 AS sno, '小林' AS sname
    UNION ALL SELECT 102, '小陈'
    UNION ALL SELECT 103, '小周'
    UNION ALL SELECT 104, '小吴'
    UNION ALL SELECT 105, '小徐'
),
course_sample AS (
    SELECT 1 AS cno, '数据库原理' AS cname
    UNION ALL SELECT 2, '计算机网络'
    UNION ALL SELECT 3, '操作系统'
),
sc_sample AS (
    SELECT 101 AS sno, 1 AS cno, 88 AS grade
    UNION ALL SELECT 101, 2, 79
    UNION ALL SELECT 101, 3, NULL
    UNION ALL SELECT 102, 1, 78
    UNION ALL SELECT 102, 2, 87
    UNION ALL SELECT 103, 2, 85
    UNION ALL SELECT 103, 3, 90
    UNION ALL SELECT 105, 1, 86
    UNION ALL SELECT 105, 2, 92
    UNION ALL SELECT 105, 3, 89
)
SELECT s.sno, s.sname
FROM student_sample AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM course_sample AS c
    WHERE NOT EXISTS(
        SELECT 1
        FROM sc_sample AS sc
        WHERE sc.sno = s.sno
          AND sc.cno = c.cno
    )
)
ORDER BY s.sno;
