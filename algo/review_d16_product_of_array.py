"""复习27（D16 的第 3 天复习） ｜ 除自身以外数组的乘积 ｜ LeetCode 238 ｜ 中等

规则：不许打开 d16_product_of_array_except_self.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么能做到**额外** O(1) 空间？（提示：答案数组本身可以怎么用？）
     自述 1：题目说输出数组不算n，所以这里可以算O(1).
     ⚠️ 半对：你答的是「**为什么允许**算 O(1)」（题目规定输出不算），但没答「**怎么做到**」。
     关键是：**把答案数组本身当草稿纸** —— 先倒着把后缀积写进 suf[]，
     再顺着用一个 pre 滚前缀积、边滚边乘进去，于是省掉一整个 left[] 数组。
     （允许 ≠ 做到：题目允许用输出数组，但真正省下空间的是「复用它」这个动作。）

  2) 为什么 `pre *= x` 必须在 `suf[i] *= pre` 之后？
     自述 2：如果先更新pre *= x ，会把自身也加到乘积里面，不符合题意
     ✅ 对。

  3) 为什么不能用除法？
     自述 3：首先是题目要求不能用除，其次是当自身为0，除以0会崩。
     ✅ 对。补一句：就算特判 0，还要按「数组里有几个 0」分情况，反而更复杂。

状态：完成（2026-10-29 独立重写成功）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def product_except_self(nums: list[int]) -> list[int]:
    """返回每个位置「除自身以外所有元素」的乘积（不用除法，额外空间 O(1)）。"""
    n = len(nums)
    suf = [1] * n
    for i in range(n-2,-1,-1):
        suf[i] = suf[i + 1] * nums[i + 1]
    pre = 1
    for i , x in enumerate(nums):
        suf[i] *= pre
        pre *= x

    return suf


def _brute(nums: list[int]) -> list[int]:
    out = []
    for i in range(len(nums)):
        p = 1
        for j, v in enumerate(nums):
            if i != j:
                p *= v
        out.append(p)
    return out


if __name__ == "__main__":
    for nums, want in [
        ([1, 2, 3, 4], [24, 12, 8, 6]),
        ([-1, 1, 0, -3, 3], [0, 0, 9, 0, 0]),
        ([2, 3], [3, 2]),
        ([1], [1]),
        ([0, 0], [0, 0]),
        ([0, 1, 2], [2, 0, 0]),
        ([-1, -2, -3], [6, 3, 2]),
    ]:
        got = product_except_self(nums[:])
        assert got == want, f"{nums} -> {got}，期望 {want}"

    import random
    random.seed(101)
    for _ in range(2000):
        nums = [random.randint(-3, 3) for _ in range(random.randint(1, 10))]
        assert product_except_self(nums[:]) == _brute(nums), f"对拍失败: {nums}"
    print("✅ 复习D16 通过 —— 独立重写成功")
