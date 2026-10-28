"""复习27（D16 的第 3 天复习） ｜ 除自身以外数组的乘积 ｜ LeetCode 238 ｜ 中等

规则：不许打开 d16_product_of_array_except_self.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么能做到**额外** O(1) 空间？（提示：答案数组本身可以怎么用？）
     自述 1：

  2) 为什么 `pre *= x` 必须在 `suf[i] *= pre` 之后？
     自述 2：

  3) 为什么不能用除法？
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def product_except_self(nums: list[int]) -> list[int]:
    """返回每个位置「除自身以外所有元素」的乘积（不用除法，额外空间 O(1)）。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


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
