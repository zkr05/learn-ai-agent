"""D18 矩阵置零（用第一行/第一列当标记数组）   LeetCode 73   Medium   <- 矩阵第 1 题

思路：不能「边遍历边清零」—— 那样会把原本不是 0 的格子也变 0，后面越清越多。
     标准做法分三段：

     ① 先记住「第 0 行原本有没有 0」（first_row_has_zero）。
        因为标记只从第 1 行开始，第 0 行的信息会被覆盖，所以必须先存。
     ② 用第一行、第一列当**标记数组**（只扫 i >= 1 的部分）：
          matrix[i][0] = 0  ->  第 i 行要清零
          matrix[0][j] = 0  ->  第 j 列要清零
     ③ 按标记清零（i >= 1）；最后如果 first_row_has_zero，整行清零。

     ⚠️ 一个隐晦但成立的技巧：`matrix[0][0]` 同时承担两个标记 ——
        「第 0 列有 0」由它记录（(i,0) 的零会把 matrix[0][0] 置 0），
        「第 0 行有 0」则由 first_row_has_zero 单独记（标记循环不碰第 0 行）。
        两者不冲突：第 0 行要清零时 first_row_has_zero 一定为真。

     🐛 第一版最后一行写成了 `for i in matrix[0]: matrix[0][i] = 0` ——
        **拿元素的值当下标用**。两个后果：
          - [[0,0,1]]：值是 0,0,1 -> 只覆盖下标 0,1，下标 2 没清 -> 答案错
          - [[5,0]]：值 5 -> matrix[0][5] -> IndexError
        改成 `for j in range(n): matrix[0][j] = 0` 后，5000 组随机对拍全绿。
        **遍历值和遍历下标是两件事**：`for x in lst` 给值，`for i in range(len(lst))` 给下标。

复杂度：时间 O(m*n)（常数遍扫描）；空间 O(1)（只用第一行/第一列当标记，原地）。

状态：完成（卡点：理清循环顺序 + 优化到 O(1)；约 30 分钟）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def set_zeroes(matrix: list[list[int]]) -> None:
    """若某个元素是 0，则把它所在行和列全置 0（原地修改）。"""
    m, n = len(matrix), len(matrix[0])

    first_row_has_zero = 0 in matrix[0]

    for i in range(1, m):
        for j in range(n):
            if matrix[i][j] == 0:
                matrix[i][0] = 0
                matrix[0][j] = 0

    for i in range(1, m):
        for j in range(n - 1, -1, -1):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0

    if first_row_has_zero:
        for j in range(n):
            matrix[0][j] = 0


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
        [[1]],
        [[0]],
        [[1, 0]],
        [[0, 1]],
        [[1, 1], [0, 1]],
        [[0, 0, 1]],          # 第一版在这里错（最后一行没清全）
        [[5, 0]],             # 第一版在这里 IndexError（拿值当下标）
    ]:
        got = [row[:] for row in src]
        assert set_zeroes(got) is None, "题目要求原地修改、不返回"
        assert got == _ref([row[:] for row in src]), f"{src} -> {got}"

    import random
    random.seed(307)
    for _ in range(5000):
        m = random.randint(1, 5)
        n = random.randint(1, 5)
        src = [[random.choice([0, 1, 2, 3, 9]) for _ in range(n)] for _ in range(m)]
        got = [row[:] for row in src]
        set_zeroes(got)
        assert got == _ref([row[:] for row in src]), f"对拍失败: {src}"
    print("✅ D18 通过")
