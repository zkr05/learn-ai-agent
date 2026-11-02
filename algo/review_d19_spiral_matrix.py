"""复习32（D19 的第 3 天复习） ｜ 螺旋矩阵 ｜ LeetCode 54 ｜ 中等

规则：不许打开 d19_spiral_matrix.py，也不许翻 notes.md。凭记忆独立写。

目标：12 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么 `(di + 1) % 4` 就等于「顺时针转 90 度」？把四个方向写出来对照。
     自述 1：

  2) 为什么必须「先探路、撞墙就转、再走」，而不是「走一步再看撞没撞」？
     （后者会在什么时候出错？举出具体位置。）
     自述 2：

  3) 为什么用 None 标记已访问、而不是 0？这样做的副作用是什么？
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def spiral_order(matrix: list[list[int]]) -> list[int]:
    """按顺时针螺旋顺序返回所有元素。"""
    # TODO: 你来写（不许看旧文件）
    raise NotImplementedError


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