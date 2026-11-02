"""复习31（D18 的第 3 天复习） ｜ 矩阵置零 ｜ LeetCode 73 ｜ 中等

规则：不许打开 d18_set_matrix_zeroes.py，也不许翻 notes.md。凭记忆独立写。

目标：12 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么不能「边遍历边清零」？会出什么后果？
     自述 1：如果一边遍历边清零，会出现后面遇到被置零的数，导致再次置零。

  2) 为什么可以用第一行/第一列当标记数组？（省掉了什么？）
     自述 2：省掉了一个额外的空间去保存0的情况。

  3) 第 0 行和第 0 列自己的信息，为什么必须先单独存起来？
     自述 3：因为如果不单独存起来，第一行第一列要存的内容可能跟原先的内容冲突。

状态：完成（2026-11-02 独立重写成功，10 条用例 + 3000 组对拍）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def set_zeroes(matrix: list[list[int]]) -> None:
    """若某个元素是 0，则把它所在行和列全置 0（原地修改）。"""
    m,n = len(matrix),len(matrix[0])
    first_row_has_zero = 0 in matrix[0]
    for i in range(1,m):
        for j in range(n):
            if matrix[i][j] == 0:
                matrix[i][0] = matrix[0][j] = 0
    for i in range(1,m):
        for j in range(n-1,-1,-1):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if first_row_has_zero:
        for i in range(n):
            matrix[0][i] = 0


def _ref(matrix: list[list[int]]) -> list[list[int]]:
    m, n = len(matrix), len(matrix[0])
    rows = {i for i in range(m) for j in range(n) if matrix[i][j] == 0}
    cols = {j for i in range(m) for j in range(n) if matrix[i][j] == 0}
    for i in rows:
        for j in range(n):
            matrix[i][j] = 0
    for j in cols:
        for i in range(m):
            matrix[i][j] = 0
    return matrix


if __name__ == "__main__":
    for src in [
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],
        [[1, 2, 3], [4, 0, 6]],
        [[1]], [[0]], [[1, 0]], [[0, 1]],
        [[1, 1], [0, 1]],
        [[0, 0, 1]],
        [[5, 0]],
    ]:
        got = [row[:] for row in src]
        assert set_zeroes(got) is None, "题目要求原地修改、不返回"
        assert got == _ref([row[:] for row in src]), f"{src} -> {got}"

    import random
    random.seed(307)
    for _ in range(3000):
        m = random.randint(1, 5)
        n = random.randint(1, 5)
        src = [[random.choice([0, 1, 2, 3, 9]) for _ in range(n)] for _ in range(m)]
        got = [row[:] for row in src]
        set_zeroes(got)
        assert got == _ref([row[:] for row in src]), f"对拍失败: {src}"
    print("✅ 复习D18 通过 —— 独立重写成功")
