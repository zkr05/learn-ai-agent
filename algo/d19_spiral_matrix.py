"""D19 螺旋矩阵（方向表 DIRS）   LeetCode 54   Medium   <- 矩阵第 2 题

思路：**把「方向」编码成「坐标增量」**，撞墙就转 90 度。

    DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)

      di=0 (0, 1)   右：列 +1        di=1 (1, 0)   下：行 +1
      di=2 (0,-1)   左：列 -1        di=3 (-1,0)   上：行 -1

    加一就是转 90 度 -> `di = (di + 1) % 4`（3+1 回到 0，不用写 if）。

    每步的顺序很重要：
      ① 访问当前格  ② 标记已访问（None）  ③ **先探路**：按当前方向试走一步
      ④ 出界或已访问就转 90 度            ⑤ 按（可能转过的）方向真正走一步
    是「探路 -> 撞墙就转 -> 再走」，不是「走一步再看撞没撞」。

    三个细节：
      - 用 `None` 标记已访问（矩阵元素可能是 0 或负数，0 不能当标记）
      - `for _ in range(m*n)` 保证正好访问 m*n 格，不用写结束条件
      - 边界检查用 `or` 短路：前面任一为真就不再索引 -> 最后一格越界也不会 IndexError

    ⚠️ 副作用：`matrix[i][j] = None` **修改了输入**（和 D14 的 `ans.append(p)` 同类）。
        LeetCode 只判返回值所以没事；真实项目里若不希望改输入，可以：
          a) 用 `visited = set()` 记坐标（O(mn) 空间，不改输入）
          b) 换成「四条边界」法（O(1) 空间，也不改输入）

    和四边界法对比：DIRS 代码短、通用性强（任何方向规则都能写），但需要标记已访问；
    四边界法不需要标记、不改输入，但要小心单行/单列重复添加（两个 if 守卫）。

复杂度：时间 O(m*n)；空间 O(1) 额外（不改输入的话要 O(mn) 的 visited）。

状态：完成（卡点：DIRS / 方向表；约 35 分钟）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)


def spiral_order(matrix: list[list[int]]) -> list[int]:
    """按顺时针螺旋顺序返回矩阵所有元素（注意：会修改输入矩阵）。"""
    m, n = len(matrix), len(matrix[0])
    i = j = di = 0
    ans = []
    for _ in range(m * n):
        ans.append(matrix[i][j])
        matrix[i][j] = None
        x, y = i + DIRS[di][0], j + DIRS[di][1]
        if x < 0 or x >= m or y < 0 or y >= n or matrix[x][y] is None:
            di = (di + 1) % 4
        i += DIRS[di][0]
        j += DIRS[di][1]
    return ans


def _ref(matrix: list[list[int]]) -> list[int]:
    """独立实现（剥第一行 + 逆时针转 90 度），不依赖方向表。"""
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
        [[1, 2, 3]],          # 单行
        [[1], [2], [3]],      # 单列
        [[1]],                # 1x1
        [[1, 2], [3, 4]],
    ]:
        got = spiral_order([row[:] for row in src])
        want = _ref(src)
        assert got == want, f"{src} -> {got}，期望 {want}"

    import random
    random.seed(401)
    for _ in range(3000):
        m = random.randint(1, 6)
        n = random.randint(1, 6)
        src = [[random.randint(0, 99) for _ in range(n)] for _ in range(m)]
        assert spiral_order([row[:] for row in src]) == _ref(src), f"对拍失败: {src}"
    print("✅ D19 通过")
