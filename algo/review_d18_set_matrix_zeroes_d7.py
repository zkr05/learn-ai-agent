"""复习38（D18 的第 7 天复习，第 2 次重写） ｜ 矩阵置零 ｜ LeetCode 73 ｜ 中等

规则：不许打开 d18_set_matrix_zeroes.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

⚠️ 第 3 天（11-02）的情况：自述 2、3 对，自述 1 只答了"会发生什么操作"，
   没答"后果是什么"。另外「第 0 列不需要单独存」那个加分点当时是我补的，
   你没自己说出来 —— 这次要自己答。

三个自述（跑绿之后填）：

  1) 如果「边遍历边清零」，举一个具体矩阵，说出最后得到什么、正确应该是什么。
     （要给出两个具体的矩阵，不是"会出错"这种话）
     自述 1：[111][101][111],第一步先检查第一行有没有0，之后从第二行开始遍历元素，遇到101中的0，
     此时将第一行的第二个元素置为0，第二行第一列为0，继续遍历，发现没有0了，到下一步，从后面出发，
     检查第一行第一列是否有0 有零则将这个数化为0。
     ❌ 答非所问。你描述的是**正确算法**的流程，题目问的是"如果边遍历边清零会得到什么"。
        而且 [[1,1,1],[1,0,1],[1,1,1]] 这个例子看不出问题 —— 零在正中间，那样做恰好也对。
     要选"零不在正中间"的例子：
        输入        [[1,0,1],[1,1,1],[1,1,1]]
        边遍历清零  [[0,0,0],[0,0,0],[0,0,0]]    <- 全灭
        正确        [[0,0,0],[1,0,1],[1,0,1]]    <- 只有第 0 行、第 1 列
     机制（追问后答对了）：清第 1 列时把 (1,1)、(2,1) 这两个原本是 1 的格子写成了 0；
        后面扫到 (1,1)，它已经是 0 了 —— **这个 0 是自己刚写进去的，不是原本的**，
        于是误判"第 1 行本来有 0"，整行清掉。后果叫**过度清零**。

  2) 第 0 行必须提前存 `first_row_has_zero`，但第 0 列**不需要**单独存。
     为什么？两种标记的"含义"有什么不同？
     自述 2：因为此时存储了第一行的0，第0列就不需要存了，因为第0列的值，不管是标记的0还是原先的0，
     都要将该行置0，所以不需要存起来。
     ✅ 对，而且这次是自己说出来的（第 3 天是我补的）。
        matrix[i][0] == 0 有两种来源（第 i 行本来有 0 / 第 0 列被标记要清），
        但两种情况后果都是"第 i 行清零"，所以不用区分。

  3) 用第一行/第一列当标记数组，凭什么"够用"？（说清位数和需求量的对应关系）
     自述 3：第一行和第一列当标记数组，加起来就是m + n 个位置，正好将这个数组覆盖了。
     ✅ 数量对上了，但"覆盖"这个词太含糊，要说清对应关系：
        第 i 行有没有 0 -> 存在 matrix[i][0]（i = 0..m-1，共 m 格）
        第 j 列有没有 0 -> 存在 matrix[0][j]（j = 0..n-1，共 n 格）
        **一一对应，一个不多一个不少**，所以不会漏。

状态：完成（2026-11-10 第 7 天复习第 2 次重写；自述 1 需重答，2 对，3 浅）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def set_zeroes(matrix: list[list[int]]) -> None:
    """若某个元素是 0，则把它所在行和列全置 0（原地修改）。"""
    first_row_has_zero = 0 in matrix[0]
    n, m = len(matrix), len(matrix[0])
    for i in range(1,n):
        for j in range(m):
            if matrix[i][j] == 0:
                matrix[i][0] = matrix[0][j] = 0

    for i in range(1,n):
        for j in range(m-1,-1,-1):
            if matrix[i][0] == 0 or matrix[0][j] ==0:
                matrix[i][j] = 0
    if first_row_has_zero:
        for j in range(m):
            matrix[0][j] = 0

         

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
