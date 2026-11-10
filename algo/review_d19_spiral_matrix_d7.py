"""复习39（D19 的第 7 天复习，第 2 次重写） ｜ 螺旋矩阵 ｜ LeetCode 54 ｜ 中等

规则：不许打开 d19_spiral_matrix.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

⚠️ 第 3 天（11-02）的情况：
   - 自述 1 把原文件的 docstring 抄了一遍（我当场指出过），这次必须自己组织语言
   - 自述 2 主语说反了（把"先探路"和"先走一步"搞混）

三个自述（跑绿之后填）：

  1) `(di + 1) % 4` 为什么等于「顺时针转 90 度」？
     要说三层：方向表按什么顺序排 / %4 的作用 / 为什么"右→下"是顺时针而不是逆时针
     自述 1：方向表按右，下，左，上，就是顺时针的顺序，当走完一个循环之后 di的值到了5，此时%4得到1，又回到原来的右。
     ⚠️ 半对。方向表顺序对 ✓，但 %4 那里举例错了，第三层完全没答。
     ❌ "di 到 5" 不会发生 —— 每次都是 (di+1)%4，结果永远落在 0..3：
          0 -> 1 -> 2 -> 3 -> 0 -> 1 ...      （3+1=4，4%4=0，回到 0=右，不是 1）
     缺的第三层（这题最值钱的一句）：
        矩阵里**行号向下增长**（第 0 行在最上面），所以"列+1"再"行+1"在屏幕上是往右下拐 = 顺时针。
        若行号向上增长（数学坐标系），同一张方向表就是逆时针。


  2) 为什么必须「先探路、撞墙就转、再走」，而不是「先走一步再看撞没撞」？
     后者在哪一步就会炸？炸的时候坐标是多少？
     自述 2：如果直接走，遇到越界行为，就直接报错了，比如2是边界，直接走会到3，就报了。
     ✅ 方向对：先走会越界，越界后再去索引就报 IndexError。例子"列 0..2，走到 3"也对。
        缺具体坐标：3x3 矩阵走完第 2 格（第一行最右）后走到 (0,3) -> IndexError。

  3) 用 None 标记已访问，副作用是什么？如果调用方不希望输入被改，有哪两种替代做法？
     自述 3：副作用是会修改原来的数组，将数组改变。
     传matrix的值出来，不要直接修改， 引入额外空间。
     ⚠️ 副作用对，但"两种替代做法"没说准。
        "传值出来/拷贝一份"是调用方自己防，算法内部还是在改输入，而且仍是 O(mn)。
     标准两种做法：
        ① visited = set() 记坐标    -> O(mn) 额外空间，不改输入
        ② 四边界法（上下左右四条边各自收缩）-> **O(1) 且不改输入**（最优解，面试想听这个）

状态：完成（2026-11-10 第 7 天复习第 2 次重写；自述 2 对，1、3 半对）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)
def spiral_order(matrix: list[list[int]]) -> list[int]:
    """按顺时针螺旋顺序返回所有元素。"""
    ans = []
    i = j = di = 0
    n, m = len(matrix), len(matrix[0])
    for _ in range(n * m):
        ans.append(matrix[i][j])
        matrix[i][j] = None
        x, y = i + DIRS[di][0], j + DIRS[di][1]
        if x < 0 or x >= n or y < 0 or y >= m or matrix[x][y] is None:
            di = (di + 1) % 4
        i += DIRS[di][0]
        j += DIRS[di][1]
    return ans


def _ref(matrix: list[list[int]]) -> list[int]:
    """独立实现：每次剥掉第一行，再把剩下的逆时针转 90 度。"""
    res = []
    m = [row[:] for row in matrix]
    while m and m[0]:
        res += m.pop(0)
        m = [list(row) for row in zip(*m)][::-1] if m else []
    return res


if __name__ == "__main__":
    for src in [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
        [[1, 2, 3]],
        [[1], [2], [3]],
        [[1]],
        [[1, 2], [3, 4]],
        [[1, 2, 3], [4, 5, 6]],
        [[1, 2], [3, 4], [5, 6]],
        [[1, 2, 3, 4, 5]],
    ]:
        got = spiral_order([row[:] for row in src])
        want = _ref(src)
        assert got == want, f"{src} -> {got}，期望 {want}"

    import random
    random.seed(5470)
    for _ in range(3000):
        m = random.randint(1, 6)
        n = random.randint(1, 6)
        src = [[random.randint(0, 99) for _ in range(n)] for _ in range(m)]
        assert spiral_order([row[:] for row in src]) == _ref(src), f"对拍失败: {src}"
    print("✅ 复习D19（第7天）通过 —— 第 2 次独立重写成功")
