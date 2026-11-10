"""复习38（D18 的第 7 天复习，第 2 次重写） ｜ 矩阵置零 ｜ LeetCode 73 ｜ 中等

规则：不许打开 d18_set_matrix_zeroes.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

⚠️ 第 3 天（11-02）的情况：自述 2、3 对，自述 1 只答了"会发生什么操作"，
   没答"后果是什么"。另外「第 0 列不需要单独存」那个加分点当时是我补的，
   你没自己说出来 —— 这次要自己答。

三个自述（跑绿之后填）：

  1) 如果「边遍历边清零」，举一个具体矩阵，说出最后得到什么、正确应该是什么。
     （要给出两个具体的矩阵，不是"会出错"这种话）
     自述 1：

  2) 第 0 行必须提前存 `first_row_has_zero`，但第 0 列**不需要**单独存。
     为什么？两种标记的"含义"有什么不同？
     自述 2：

  3) 用第一行/第一列当标记数组，凭什么"够用"？（说清位数和需求量的对应关系）
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def set_zeroes(matrix: list[list[int]]) -> None:
    """若某个元素是 0，则把它所在行和列全置 0（原地修改）。"""
    # TODO: 你来写（不许看旧文件）
    raise NotImplementedError


def _ref(matrix: list[list[int]]) -> list[list[int]]:
    """独立实现：先用集合记下要清零的行列，再统一清。"""
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
    cases = [
        [[1, 1, 1], [1, 0, 1], [1, 1, 1]],
        [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],
        [[1, 2, 3], [4, 0, 6]],
        [[1]], [[0]], [[1, 0]], [[0, 1]],
        [[1, 1], [0, 1]],
        [[0, 0, 1]],
        [[5, 0]],
        [[1, 0, 1], [1, 1, 1], [1, 1, 1]],
        [[0], [1], [1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 0]],
    ]
    for src in cases:
        got = [row[:] for row in src]
        assert set_zeroes(got) is None, "题目要求原地修改、不返回"
        assert got == _ref([row[:] for row in src]), f"{src} -> {got}"

    import random
    random.seed(7307)
    for _ in range(3000):
        m = random.randint(1, 5)
        n = random.randint(1, 5)
        src = [[random.choice([0, 1, 2, 3, 9]) for _ in range(n)] for _ in range(m)]
        got = [row[:] for row in src]
        set_zeroes(got)
        assert got == _ref([row[:] for row in src]), f"对拍失败: {src}"
    print("✅ 复习D18（第7天）通过 —— 第 2 次独立重写成功")