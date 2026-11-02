"""复习31（D18 的第 3 天复习） ｜ 矩阵置零 ｜ LeetCode 73 ｜ 中等

规则：不许打开 d18_set_matrix_zeroes.py，也不许翻 notes.md。凭记忆独立写。

目标：12 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么不能「边遍历边清零」？会出什么后果？
     自述 1：如果一边遍历边清零，会出现后面遇到被置零的数，导致再次置零。
     ⚠️ 只答了"发生什么操作"，没答"后果"。实测 [[1,0,1],[1,1,1],[1,1,1]]：
       正确          -> [[0,0,0],[1,0,1],[1,0,1]]
       边遍历边清零  -> [[0,0,0],[0,0,0],[0,0,0]]   <- 第 1、2 行被误清
     机制：(0,1) 是真 0，清列 1 时把 (1,1)、(2,1) 写成 0；后面扫到 (1,1) 这个**假 0**，
       误以为第 1 行有 0 -> 整行清掉。
     后果叫**过度清零**：假 0 落在还没访问的行里，那一行就被连坐。"再次置零"听起来无害，不是答案。

  2) 为什么可以用第一行/第一列当标记数组？（省掉了什么？）
     自述 2：省掉了一个额外的空间去保存0的情况。
     ✅ 对，但只答了"省什么"，没答"凭什么能"。
        省的是 m+n 个布尔标记；能用的原因是**数量刚好对上**：
        需要的正是"第 i 行有没有 0"+"第 j 列有没有 0"共 m+n 位，
        而第一列正好 m 格、第一行正好 n 格 —— 不用额外分配，位数正好等于需求数。

  3) 第 0 行和第 0 列自己的信息，为什么必须先单独存起来？
     自述 3：因为如果不单独存起来，第一行第一列要存的内容可能跟原先的内容冲突。
     ✅ 对，"冲突"要展开：第 0 行被征用当"列标记"，原值被覆盖 ->
        "第 0 行原本有没有 0"丢了这个信息 -> 必须提前 0 in matrix[0] 存起来。
        加分点（第 0 列**不用**单独存）：matrix[i][0]==0 既可能是真 0 也可能是标记，
        但两种情况后果都是"第 i 行要清零"，所以不用区分 —— 这才是只存一个
        first_row_has_zero 的原因。

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
