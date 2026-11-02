"""D21 搜索二维矩阵 II（阶梯贪心）   LeetCode 240   Medium   <- 矩阵第 4 题（收尾）

题目：m x n 矩阵，**每行从左到右升序**，**每列从上到下升序**。
      判断 target 是否在矩阵里。

    [[ 1,  4,  7, 11, 15],
     [ 2,  5,  8, 12, 19],
     [ 3,  6,  9, 16, 22],
     [10, 13, 14, 17, 24],
     [18, 21, 23, 26, 30]]

    找 5  -> True      找 20 -> False

要求：比 O(m*n) 暴力快，最好做到 **O(m + n)**。

---------------------------------------------------------------
核心想法：**站在一个「一条路一定变大、另一条路一定变小」的角上。**

  左上角 (0,0)：往右变大、往下也变大   -> 两条路都变大，没法排除 ✗
  右下角 (m-1,n-1)：往左变小、往上也变小 -> 两条路都变小，没法排除 ✗
  右上角 (0,n-1)：往左一定变小、往下一定变大 -> 能二选一 ✓
  左下角 (m-1,0)：往上一定变小、往右一定变大 -> 也能二选一 ✓

站在右上角，每一步比较 `matrix[i][j]` 和 target：

    相等          -> 找到
    当前 < target -> 这一整**行**都不可能有了（行内往右更大、但这列往下才更大），往下走
    当前 > target -> 这一整**列**都不可能有了，往左走

每一步扔掉一整行或一整列 -> 最多走 m + n 步就出界。

---------------------------------------------------------------
写之前先自问（写完回答，我会判对错）：

  1) 为什么左上角/右下角不行？用「两条路都变大」解释清楚，别只说"不能那么走"。

  2) 「当前 < target 就往下走」这一步，扔掉的到底是**一整行**还是一整列？
     为什么扔掉它是安全的？（被扔掉的那些格子里，凭什么保证都不等于 target？）

  3) 为什么总步数是 O(m + n)？出界条件怎么写最省事？

复杂度：时间 O(m + n)；空间 O(1)。

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """行内升序、列内升序的矩阵里查 target；不许用 O(m*n) 全扫。"""
    # TODO: 你来写
    raise NotImplementedError


def _ref(matrix: list[list[int]], target: int) -> bool:
    """暴力扫（O(m*n)），只用来对拍。"""
    return any(x == target for row in matrix for x in row)


if __name__ == "__main__":
    big = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]
    for t in [1, 5, 15, 30, 18, 20, 16, 0, 31, -5]:
        assert search_matrix([r[:] for r in big], t) == _ref(big, t), f"target={t}"

    for m, t in [
        ([[1]], 1), ([[1]], 2), ([[-5]], -5),
        ([[1, 1]], 1), ([[1], [1]], 1),
        ([[1, 2, 3]], 2), ([[1], [2], [3]], 2),
    ]:
        assert search_matrix([r[:] for r in m], t) == _ref(m, t), f"{m} target={t}"

    import random
    random.seed(240)
    for _ in range(2000):
        rows = random.randint(1, 6)
        cols = random.randint(1, 6)
        # 造一个行、列都升序的矩阵：先造 sorted 的基矩阵再累加
        grid = [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            grid[i].sort()
        for i in range(1, rows):
            for j in range(cols):
                grid[i][j] += grid[i - 1][j] + 1
        for j in range(1, cols):
            for i in range(rows):
                grid[i][j] = max(grid[i][j], grid[i][j - 1] + 1)
        t = random.randint(-2, 60)
        assert search_matrix([r[:] for r in grid], t) == _ref(grid, t), f"对拍失败 {grid} t={t}"
    print("✅ D21 通过 —— 搜索二维矩阵 II，O(m+n)")