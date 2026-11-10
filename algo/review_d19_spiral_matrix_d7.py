"""复习39（D19 的第 7 天复习，第 2 次重写） ｜ 螺旋矩阵 ｜ LeetCode 54 ｜ 中等

规则：不许打开 d19_spiral_matrix.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

⚠️ 第 3 天（11-02）的情况：
   - 自述 1 把原文件的 docstring 抄了一遍（我当场指出过），这次必须自己组织语言
   - 自述 2 主语说反了（把"先探路"和"先走一步"搞混）

三个自述（跑绿之后填）：

  1) `(di + 1) % 4` 为什么等于「顺时针转 90 度」？
     要说三层：方向表按什么顺序排 / %4 的作用 / 为什么"右→下"是顺时针而不是逆时针
     自述 1：

  2) 为什么必须「先探路、撞墙就转、再走」，而不是「先走一步再看撞没撞」？
     后者在哪一步就会炸？炸的时候坐标是多少？
     自述 2：

  3) 用 None 标记已访问，副作用是什么？如果调用方不希望输入被改，有哪两种替代做法？
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