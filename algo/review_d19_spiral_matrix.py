"""复习32（D19 的第 3 天复习） ｜ 螺旋矩阵 ｜ LeetCode 54 ｜ 中等

规则：不许打开 d19_spiral_matrix.py，也不许翻 notes.md。凭记忆独立写。

目标：12 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么 `(di + 1) % 4` 就等于「顺时针转 90 度」？把四个方向写出来对照。
     自述 1：di=0 (0, 1)   右：列 +1        di=1 (1, 0)   下：行 +1
           di=2 (0,-1)   左：列 -1        di=3 (-1,0)   上：行 -1
     
         加一就是转 90 度 -> `di = (di + 1) % 4`（3+1 回到 0，不用写 if）。
     ⚠️ 半对：答的是"是什么"，不是"为什么"。而且这段和 d19_spiral_matrix.py 的 docstring
        一字不差（连反引号都一样）—— 如果是照着抄的，这题自述等于没做。
     三层答案：
       ① 方向表本身按**顺时针顺序**排：右 -> 下 -> 左 -> 上。
          所以 di+1 = 顺时针的下一个方向 = 转 90 度。这是**约定**，不是巧合。
       ② %4：3+1=4 回到 0，省掉 if di == 4: di = 0。（这层你说对了）
       ③ 为什么"右->下"是顺时针而不是逆时针：矩阵里**行号向下增长**（第 0 行在最上面）。
          所以"列+1"再"行+1"，在屏幕上就是往右下拐 = 顺时针。
          若行号向上增长（数学坐标系），同一张表就是逆时针。

  2) 为什么必须「先探路、撞墙就转、再走」，而不是「走一步再看撞没撞」？
     （后者会在什么时候出错？举出具体位置。）
     自述 2：如果先探路，此时发生越界错误，就会直接IndexError退出了，不会回退。
     ⚠️ 主语反了：**探路恰恰是不会报错的那个**。它只用坐标做算术，压根不碰 matrix[x][y]，
        越界只是"x 或 y 超范围"这个布尔条件为真。
     会炸的是"先走一步再判断"：走出去以后要判断就得读 matrix[i][j]。
        实测第 2 格走完 -> 坐标 (0,3) -> IndexError: list index out of range。
     而且"先走"还多一个麻烦：已经离开正确位置，撞墙后要**回退**，得额外记上一次坐标。
     一句话：**探路是"算"，先走是"动"。算错了不疼，动错了要回滚。**

  3) 为什么用 None 标记已访问、而不是 0？这样做的副作用是什么？
     自述 3：因为矩阵元素可能是0或者是负数，所以要用None来标记。副作用是会修改matrix的值。
     ✅ 对，但副作用要说"后果"：调用方拿到的矩阵已经被破坏成一片 None，
        它后面若还要用这个矩阵就算错了；想保留必须 deepcopy。
        LeetCode 只判返回值所以能过，真实代码里这是 bug 源头。
        替代方案：visited = set()（O(mn) 额外空间，不改输入）或四边界法（O(1) 且不改输入）。

状态：完成（2026-11-02 独立重写成功，3000 组对拍）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DIRS = (0, 1), (1, 0), (0, -1), (-1, 0)
def spiral_order(matrix: list[list[int]]) -> list[int]:
    """按顺时针螺旋顺序返回所有元素。"""
    m, n = len(matrix), len(matrix[0])
    ans = []
    i = j = di = 0
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
    ]:
        got = spiral_order([row[:] for row in src])
        want = _ref(src)
        assert got == want, f"{src} -> {got}，期望 {want}"

    import random
    random.seed(402)
    for _ in range(3000):
        m = random.randint(1, 6)
        n = random.randint(1, 6)
        src = [[random.randint(0, 99) for _ in range(n)] for _ in range(m)]
        assert spiral_order([row[:] for row in src]) == _ref(src), f"对拍失败: {src}"
    print("✅ 复习D19（第3天）通过 —— 独立重写成功")
