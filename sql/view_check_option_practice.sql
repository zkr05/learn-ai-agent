-- MySQL 第二十七课：用 WITH CHECK OPTION 约束通过视图的修改。
-- 在 Navicat 连接「数据库实验」。先运行准备区，再按题号选中语句逐段运行。
-- 准备区只重建 lab27_is_students 视图和 lab27_student 练习表。

-- 准备区
USE db_lab;

DROP VIEW IF EXISTS lab27_is_students;
DROP TABLE IF EXISTS lab27_student;

CREATE TABLE lab27_student (
    sno INT PRIMARY KEY,
    sname VARCHAR(50) NOT NULL,
    dept VARCHAR(20) NOT NULL
) ENGINE=InnoDB;

INSERT INTO lab27_student (sno, sname, dept) VALUES
    (101, '小林', 'is'),
    (102, '小陈', 'cs'),
    (103, '小周', 'is'),
    (104, '小吴', 'cs');

-- 1. TODO：创建 lab27_is_students，显示 sno、sname、dept，只保留信息系 'is'。
--    在视图定义末尾加上本课学到的检查，再查视图，预期看到 101、103。
CREATE VIEW lab27_is_students AS
SELECT sno, sname, dept
FROM lab27_student
WHERE dept = 'is'
WITH CHECK OPTION;
-- 2. TODO：通过视图把 101 的姓名改成 '小林同学'。查基础表看看姓名是否改变。
UPDATE lab27_is_students
SET sname = '小林同学'
WHERE sno = 101;

SELECT * FROM lab27_student WHERE sno = 101;
-- 3. TODO：通过视图尝试把 101 的 dept 改成 'cs'。单独运行这句，预期报错 1369。
UPDATE lab27_is_students
SET dept = 'cs'
WHERE sno = 101;
-- 4. TODO：报错后另选中并运行核对语句，查基础表的 101，再查视图。
--    记下基础表的 dept，以及视图里是否还能看到 101。
SELECT * FROM lab27_is_students WHERE sno = 101;

-- 选做：直接改基础表，让 101 转到 'cs'，再查视图。重跑准备区可以恢复初始数据。
-- 观察：为什么两种 UPDATE 的结果不同？
-- 改名后 dept 仍是 'is'，所以更新成功，姓名写入基础表。
-- 通过视图把 dept 改成 'cs' 会让该行不再满足筛选条件，因此报错 1369。
-- 报错后可重跑第 2 步的基础表 SELECT，第 4 步的视图查询也仍会读到 101。
-- 直接写基础表不触发这个检查，我用独立练习表验证时，改系成功且 101 不再出现在视图里。