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
     自述 1：首先右上角的值有一个特性，它是该行最大值，也是改列最小值，所以一定可以排除一行或一列，
     左上角没有这种特性，谁都比他大，右下角谁都比他大
     ⚠️ 前 2/3 对，最后一句**说反了**。
     ✅ 对的部分：右上角 = 该行最大值 + 该列最小值 -> 比较一次就能二选一。
     ❌ 错的部分：右下角是**全局最大值**，应该是"谁都比他小"，不是"比他大"。你和左上角写重复了。
     四角对照（关键是同向/反向）：
        左上角  右更大、下更大  -> 同向 -> 砍不掉    ✗
        右下角  左更小、上更小  -> 同向 -> 砍不掉    ✗
        右上角  左更小、下更大  -> 反向 -> 能二选一  ✓
        左下角  上更小、右更大  -> 反向 -> 能二选一  ✓

  2) `matrix[i][j] < target` 时移动的是 i 还是 j？这一下扔掉的是第 i 行还是第 j 列？
     凭什么保证被扔掉的那些格子里一定没有 target？
     自述 2：移动的是i，这一下是丢掉了第i行，因为此时该行最大值小于target，所以可以放心扔掉。
     ✅ 对，而且这次把"为什么安全"补上了（上次只说"扔掉第 i 行"就停了）。
        matrix[i][j] 是当前剩余区域里第 i 行的最右端，行内升序 -> 它就是这一段的 max
        -> max < target 则整行没戏。对称的一半：> target 时扔第 j 列。

  3) 为什么总步数 <= m + n？`while i < n and j >= 0` 为什么不用再检查 i >= 0 和 j < m？
     自述 3：总步数是行数加列数，因为每一步都会砍掉一行或者一列，所以最差的情况就是全部砍掉，
     i最大到行数-1，j最多到0，加起来就是i + j.
     因为i和j的初始值分别是0和m-1，后续i只会变大，j只会变小，所以没必要加这一步。
     ⚠️ 第二问**完全正确**（单调单向 -> 各检查一侧就够），这是关键洞察。
     第一问结论对，但推导两处松：
       ① "i 最大到行数-1" -> 实际 i 最大到 n（i == n 时循环才退出）。你数的是"最后一个下标"，
          要数的是"移动了几次"。
       ② "加起来就是 i + j" -> 步数 = i 的增加次数 + j 的减少次数 = i_final + (m-1-j_final)，
          不是 i + j。
     正确说法：i 从 0 只增，最多增 n 次；j 从 m-1 只减，最多减 m 次；两者互不干扰 -> 总步数 <= n + m。

状态：完成（2026-11-10 第 3 天复习；自述 2、3 第二问对，1 有一处说反）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """行内升序、列内升序的矩阵里查 target；不许用 O(m*n) 全扫。"""
    n = len(matrix)
    m = len(matrix[0])
    i = 0
    j = m-1
    while i < n and j >= 0:
        if target == matrix[i][j]:
            return True
        if target < matrix[i][j]:
            j -= 1
        else:
            i += 1
    return False



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
