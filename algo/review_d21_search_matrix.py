"""复习37（D21 的第 3 天复习） ｜ 搜索二维矩阵 II ｜ LeetCode 240 ｜ 中等

规则：不许打开 d21_search_matrix.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

⚠️ 上次（11-03）答得浅，这次重点答这两处：
   - 问「为什么左上/右下不行」，你说"只能排除一个数"，
     说了现象没说机制（两条邻居**同向**，比较完砍不掉整行整列）。
   - 问「为什么 <= m+n、出界条件为什么这么写就够」，你只说了结论，没推。

三个自述（跑绿之后填）：

  1) 为什么从右上角出发，每步能砍掉一整行或一整列？左上角和右下角为什么不行？
     （要说出两条邻居方向的**同向/反向**）
     自述 1：

  2) `matrix[i][j] < target` 时移动的是 i 还是 j？这一下扔掉的是第 i 行还是第 j 列？
     凭什么保证被扔掉的那些格子里一定没有 target？
     自述 2：

  3) 为什么总步数 <= m + n？`while i < n and j >= 0` 为什么不用再检查 i >= 0 和 j < m？
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """行内升序、列内升序的矩阵里查 target；不许用 O(m*n) 全扫。"""
    # TODO: 你来写（不许看旧文件）
    raise NotImplementedError


def _ref(matrix: list[list[int]], target: int) -> bool:
    """暴力扫，只用来对拍。"""
    return any(x == target for row in matrix for x in row)


if __name__ == "__main__":
    big = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]
    for t in [1, 5, 15, 30, 18, 20, 16, 0, 31, -5, 24, 22]:
        assert search_matrix([r[:] for r in big], t) == _ref(big, t), f"target={t}"

    for m, t in [
        ([[1]], 1), ([[1]], 2), ([[-5]], -5),
        ([[1, 1]], 1), ([[1], [1]], 1),
        ([[1, 2, 3]], 2), ([[1], [2], [3]], 2),
        ([[1, 2], [3, 4]], 3),
    ]:
        assert search_matrix([r[:] for r in m], t) == _ref(m, t), f"{m} target={t}"

    import random
    random.seed(2400)
    for _ in range(2000):
        rows, cols = random.randint(1, 6), random.randint(1, 6)
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
    print("✅ 复习D21（第3天）通过 —— 独立重写成功")