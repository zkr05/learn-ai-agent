-- MySQL 第十八课。给学生、课程和选课三张表各加一个主键。
-- 在 Navicat 选「数据库实验」和 db_lab，修改下面三个临时表的定义，再运行整份脚本。
-- 正常数据应全部插入，最后的查询显示 3 条选课记录。
-- 通过后，每次取消注释一个末尾的重复插入，再运行整份脚本，预期该插入报 1062。
-- 测完把三条重复插入恢复成注释，保存能正常运行的版本。
-- 观察：学生按学号唯一，课程按课程号唯一，选课按学号和课程号的组合唯一。
-- 三条正常选课都能插入；三种重复主键各自触发 1062，即使姓名、课程名或成绩不同。

DROP TEMPORARY TABLE IF EXISTS lab18_sc, lab18_course, lab18_student;

CREATE TEMPORARY TABLE lab18_student (
    sno INT NOT NULL,
    sname VARCHAR(50) NOT NULL,
    PRIMARY KEY (sno)
    -- 在这里补学生表的主键。记得在上一列末尾加逗号。
);

CREATE TEMPORARY TABLE lab18_course (
    cno INT NOT NULL,
    cname VARCHAR(30) NOT NULL,
    PRIMARY KEY(cno)
    -- 在这里补课程表的主键。
);

CREATE TEMPORARY TABLE lab18_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2),
    PRIMARY KEY(sno, cno)
    -- 在这里补选课表的主键。
);

INSERT INTO lab18_student (sno, sname) VALUES (101, '小林'), (102, '小陈');
INSERT INTO lab18_course (cno, cname) VALUES (1, '数据库原理'), (2, '计算机网络');
INSERT INTO lab18_sc (sno, cno, grade) VALUES (101, 1, 88), (101, 2, NULL), (102, 1, 76);

SELECT sno, cno, grade
FROM lab18_sc
ORDER BY sno, cno;

-- 重复学号，姓名换了也应该被拦住：
-- INSERT INTO lab18_student (sno, sname) VALUES (101, '另一个学生');

-- 重复课程号，课名换了也应该被拦住：
-- INSERT INTO lab18_course (cno, cname) VALUES (1, '另一门课');

-- 重复选同一门课，分数换了也应该被拦住：
-- INSERT INTO lab18_sc (sno, cno, grade) VALUES (101, 1, 99);
