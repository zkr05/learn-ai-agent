"""复习36（D20 的第 3 天复习） ｜ 旋转图像 ｜ LeetCode 48 ｜ 中等

规则：不许打开 d20_rotate_image.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

⚠️ 上次（11-02）两处答得不实，这次重点答这两处：
   - 问「整行遍历会怎样」，你只说"变成把单独一行的逆转了"，
     没说出**具体结果**，也没说**为什么**（转置被抵消）。
   - 问「凭什么 O(1)」，你答的是复述结论，没说判断标准。

三个自述（跑绿之后填）：

  1) 转置那一层，`for j in range(i)` 和 `for j in range(i+1, n)` 都能过测试。
     为什么两种都行？如果写成 `for j in range(n)`，3x3 矩阵会得到什么？（写出具体结果）
     自述 1：如果写成for j in range(n) ， 第一步转置后的矩阵按正常来说应该是和原来的一样。
     ⚠️ 半对，但抓到了核心。「转置后的矩阵和原来一样」是对的，而且是上次没答出的关键：
        整行遍历时每对 (i,j)/(j,i) 被交换两次，净效果 0 —— 转置等于没做。
     漏了两点：
       ① 为什么 range(i) 和 range(i+1,n) 都行 —— 两种都是把每个**无序对 {i,j}**
          恰好枚举一次（一个取下三角、一个取上三角）。
       ② 题目要"写出具体结果"，你只答了第一步。整个 rotate 之后是**左右镜像**：
          [[1,2,3],[4,5,6],[7,8,9]] -> [[3,2,1],[6,5,4],[9,8,7]]

  2) 位置 (i, j) 的元素，经过「转置 → 每行反转」之后落在哪？
     把两步的中间位置也写出来。
     自述 2：位置(i.j)，转置后到了(j,i),每一行反转之后到了(j,n-i-1)。
     ✅ 对。(i,j) --转置--> (j,i) --每行反转，列 c 变 n-1-c--> (j, n-1-i)。

  3) 如果题目改成「逆时针 90 度」，只改一行就够。改哪一行、为什么？
     顺便说清这题的额外空间为什么是 O(1)。
     自述 3：改成列反转就可以了。因为这道题的数组没有借用额外的数组，都是在原有的数组里进行修改。
     ⚠️ 半对。「列反转」方向对（每列上下翻转 = 整个矩阵上下翻转 = matrix.reverse()），
        但题目问"只改一行"，要具体到代码：`for row in matrix: row.reverse()` 换成 `matrix.reverse()`。
     ⚠️ O(1) 的理由**第二次**还是复述结论（"没借用额外数组"）。
        标准说法：**额外空间 = 除输入之外申请的东西**。这里循环体只有一次元组解包交换
        （常数个临时变量），row.reverse() 也是原地，没有任何和 n 同阶的容器。
        判断法：先问"我分配了和 n 同阶的东西吗"，再问"它在不在题目豁免名单里"。

状态：完成（2026-11-10 第 3 天复习；自述 2 对，1、3 半对）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(matrix: list[list[int]]) -> None:
    """顺时针旋转 90 度，原地修改，不返回值。"""
    n = len(matrix)
    for i in range(n):
        for j in range(i):
            matrix[i][j], matrix[j][i] = matrix[j][i],matrix[i][j]
    for row in matrix:
        row.reverse()


def _ref(matrix: list[list[int]]) -> list[list[int]]:
    """独立实现：直接按映射 (i,j) -> (j, n-1-i) 生成新矩阵（不原地）。"""
    n = len(matrix)
    return [[matrix[n - 1 - c][r] for c in range(n)] for r in range(n)]


if __name__ == "__main__":
    for src in [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
        [[1, 2], [3, 4]],
        [[1]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
        [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]],
    ]:
        got = [row[:] for row in src]
        assert rotate(got) is None, "题目要求原地修改、不返回值"
        want = _ref(src)
        assert got == want, f"{src}\n -> {got}\n 期望 {want}"

    import random
    random.seed(4890)
    for _ in range(2000):
        n = random.randint(1, 9)
        src = [[random.randint(0, 99) for _ in range(n)] for _ in range(n)]
        got = [row[:] for row in src]
        rotate(got)
        assert got == _ref(src), f"对拍失败: {src}"
    print("✅ 复习D20（第3天）通过 —— 独立重写成功")
