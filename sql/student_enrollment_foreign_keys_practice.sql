-- MySQL 第十九课。给选课表添加两条外键。
-- 在 Navicat 选「数据库实验」连接，使用 db_lab。
-- 每次运行整份脚本会重建本课的三张 lab19_ 练习表，先重建选课所依赖的两张表。
-- 修改 lab19_sc 的建表语句。正常数据应能插入，最后的查询显示 3 条选课记录。
-- 再单独取消注释末尾的一条测试，运行整份脚本，检查相应错误码。测完恢复注释。
-- 观察：学号和课程号都必须在各自的父表中存在。缺任一父行的选课记录会被拒绝。
-- 默认删除规则会阻止删除仍被选课记录引用的学生 101，避免选课失去对应学生。

USE db_lab;

DROP TABLE IF EXISTS lab19_sc;
DROP TABLE IF EXISTS lab19_course, lab19_student;

CREATE TABLE lab19_student (
    sno INT NOT NULL,
    sname VARCHAR(50) NOT NULL,
    PRIMARY KEY (sno)
) ENGINE=InnoDB;

CREATE TABLE lab19_course (
    cno INT NOT NULL,
    cname VARCHAR(30) NOT NULL,
    PRIMARY KEY (cno)
) ENGINE=InnoDB;

CREATE TABLE lab19_sc (
    sno INT NOT NULL,
    cno INT NOT NULL,
    grade DECIMAL(6, 2),
    PRIMARY KEY (sno, cno),
    -- 在这里加两条外键。一条检查学生是否存在，另一条检查课程是否存在。
    FOREIGN KEY(sno) REFERENCES lab19_student(sno),
    FOREIGN KEY(cno) REFERENCES lab19_course(cno)
) ENGINE=InnoDB;

INSERT INTO lab19_student (sno, sname) VALUES (101, '小林'), (102, '小陈');
INSERT INTO lab19_course (cno, cname) VALUES (1, '数据库原理'), (2, '计算机网络');
INSERT INTO lab19_sc (sno, cno, grade) VALUES (101, 1, 88), (101, 2, NULL), (102, 1, 76);

SELECT sno, cno, grade
FROM lab19_sc
ORDER BY sno, cno;

-- 测试 1：学号 999 不存在，应报 1452。
-- INSERT INTO lab19_sc (sno, cno, grade) VALUES (999, 1, 88);

-- 测试 2：课程号 999 不存在，应报 1452。
-- INSERT INTO lab19_sc (sno, cno, grade) VALUES (101, 999, 88);

-- 选做：学生 101 还有选课记录，尝试删除该练习学生，应报 1451。
-- DELETE FROM lab19_student WHERE sno = 101;
