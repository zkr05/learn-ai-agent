"""复习41（D21 的第 7 天复习）｜搜索二维矩阵 II｜LeetCode 240｜中等

规则：不打开 d21_search_matrix.py，也不翻 notes.md。凭记忆独立重写。
目标：先独立写代码，再运行本文件；通过后回答下面三个自述。

上次（11-10）第 3 天复习：右上角的行列性质、`< target` 时扔掉第 i 行，
以及单调指针的出界检查都答对了。四角比较时把右下角的大小关系说反了，
复杂度推导也把下标值和移动次数混在了一起。这次重点讲清方向和计数。

自述：
1) 为什么右上角能每步排除一整行或一整列？左上角、右下角为什么不行？
   请比较两个邻居的方向是“同向”还是“反向”，并准确说出四角的大小关系。
   自述 1：因为右上角的值是该行最大，该列最小，需要有这个特性，所以左上右下不行。
   邻居方向是方向，左上角是最小，右下角是最大，左下右上无法比较。

2) 当前值小于 target 时，移动哪个指针、排除哪一整行？为什么能确定这一行不含 target？
   当前值大于 target 时，对称地排除什么？
   自述 2：小于target时，移动i指针，排除掉第i行，因为改行最大值小于target，
   大于则排除第j列。

3) 为什么最多移动 m + n 次？请分别数清 i、j 各自最多移动几次。
   为什么循环条件 `i < rows and j >= 0` 已足够？
   自述 3：因为m，n分别是行数和列数，i从0到n-1， j从m-1到0，最多加起来是m+n，
   同理最多是移动到这范围。

批改：代码及固定用例、2000 组随机对拍通过。自述2正确。自述1说对四角方向，但尚未解释同向时比较不能像右上角那样排除一整行或一整列。自述3的移动次数正确：i 最多 rows 次，j 最多 cols 次；循环边界也正确：i 单调增加，不会小于 0；j 单调减小，不会超过 cols-1。
状态：完成（2026-11-11 第7天复习；代码通过，概念薄弱点已批改）
"""

import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    n, m = len(matrix), len(matrix[0])
    i = 0
    j = m-1
    while i < n and j >= 0:
        if matrix[i][j] == target:
            return True
        if matrix[i][j] < target:
            i += 1
        else:
            j -= 1
    return False


def _ref(matrix: list[list[int]], target: int) -> bool:
    """暴力查找，仅供本文件对拍。"""
    return any(value == target for row in matrix for value in row)


if __name__ == "__main__":
    big = [
        [1, 4, 7, 11, 15],
        [2, 5, 8, 12, 19],
        [3, 6, 9, 16, 22],
        [10, 13, 14, 17, 24],
        [18, 21, 23, 26, 30],
    ]
    for target in [1, 5, 15, 30, 18, 20, 16, 0, 31, -5, 24, 22]:
        assert search_matrix([row[:] for row in big], target) == _ref(big, target), target

    for matrix, target in [
        ([[1]], 1), ([[1]], 2), ([[-5]], -5),
        ([[1, 1]], 1), ([[1], [1]], 1),
        ([[1, 2, 3]], 2), ([[1], [2], [3]], 2),
        ([[1, 2], [3, 4]], 3),
    ]:
        assert search_matrix([row[:] for row in matrix], target) == _ref(matrix, target)

    random.seed(2421)
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
        target = random.randint(-2, 60)
        assert search_matrix([row[:] for row in grid], target) == _ref(grid, target), (
            f"对拍失败：{grid} target={target}"
        )

    print("✅ D21 第 7 天复习通过")