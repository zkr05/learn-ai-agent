"""D20 旋转图像（转置 + 翻转）   LeetCode 48   Medium   <- 矩阵第 3 题

题目：给一个 n x n 矩阵，**原地**顺时针旋转 90 度。

    [[1,2,3],        [[7,4,1],
     [4,5,6],   ->    [8,5,2],
     [7,8,9]]         [9,6,3]]

约束：不许新建一个 n x n 矩阵（要原地改），额外空间 O(1)。

---------------------------------------------------------------
先想清楚这一件事，代码就只剩几行：

    位置 (i, j) 上的元素，旋转 90 度**顺时针**之后应该去哪？
    （用 3x3 例子点名：1 在 (0,0)，转完跑到哪？7 在 (2,0)，转完跑到哪？）

想通之后，你会发现「一次旋转」太绕（每个元素要跟着换位置，容易绕成环）。
换个角度：**能不能拆成两次我们已经会做的对称变换，让它们复合起来正好是 90 度？**
提示：你在 D15「轮转数组」用过「三次反转合成一次轮转」——同一个套路。
矩阵里最常用的两个对称是：**沿主对角线翻转（转置）** 和 **左右/上下翻转**。

---------------------------------------------------------------
写之前先自问：

  1) 转置 `(i,j) <-> (j,i)` 只要遍历 `j > i` 的那一半，为什么不能遍历整个矩阵？
     （如果遍历整个矩阵，会发生什么？）

  2) 转置 + 某种翻转 = 顺时针 90 度。那「逆时针 90 度」该换成哪种翻转？

  3) 这题的循环为什么能保证 O(1) 额外空间？（对比一下「新开一个矩阵再填」的做法）

复杂度：时间 O(n^2)（每个元素都要动）；空间 O(1)。

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(matrix: list[list[int]]) -> None:
    """顺时针旋转 90 度，原地修改，不返回值。"""
    # TODO: 你来写
    raise NotImplementedError


def _ref(matrix: list[list[int]]) -> list[list[int]]:
    """独立实现：直接按 (i,j) -> (j, n-1-i) 算新矩阵（不原地）。"""
    n = len(matrix)
    return [[matrix[n - 1 - c][r] for c in range(n)] for r in range(n)]


if __name__ == "__main__":
    for src in [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
        [[1, 2], [3, 4]],
        [[1]],
        [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],
    ]:
        got = [row[:] for row in src]
        assert rotate(got) is None, "题目要求原地修改、不返回值"
        want = _ref(src)
        assert got == want, f"{src}\n -> {got}\n 期望 {want}"

    # 必须真的原地改：传进去的那个 list 对象本身被改了
    box = [[1, 2], [3, 4]]
    ref_id = id(box)
    rotate(box)
    assert id(box) == ref_id, "不许用 matrix = ... 重新绑定（那样外部看不到）"
    assert box == [[3, 1], [4, 2]], f"原地修改失败: {box}"

    import random
    random.seed(489)
    for _ in range(2000):
        n = random.randint(1, 9)
        src = [[random.randint(0, 99) for _ in range(n)] for _ in range(n)]
        got = [row[:] for row in src]
        rotate(got)
        assert got == _ref(src), f"对拍失败: {src}"
    print("✅ D20 通过 —— 旋转图像，原地 O(1) 空间")