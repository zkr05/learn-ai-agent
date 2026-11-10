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
     自述 1：

  2) 位置 (i, j) 的元素，经过「转置 → 每行反转」之后落在哪？
     把两步的中间位置也写出来。
     自述 2：

  3) 如果题目改成「逆时针 90 度」，只改一行就够。改哪一行、为什么？
     顺便说清这题的额外空间为什么是 O(1)。
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(matrix: list[list[int]]) -> None:
    """顺时针旋转 90 度，原地修改，不返回值。"""
    # TODO: 你来写（不许看旧文件）
    raise NotImplementedError


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