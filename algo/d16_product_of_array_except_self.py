"""D16 除自身以外数组的乘积（前缀积 + 后缀积）   LeetCode 238   Medium   <- 普通数组第 4 题

思路：答案 = 「左边所有元素的积」x「右边所有元素的积」。
     ① 倒着扫一遍：把「后缀积」直接写进答案数组（suf[i] = nums[i+1] * ... * nums[n-1]）
     ② 顺着扫一遍：用一个 pre 滚「前缀积」，边滚边乘进答案（suf[i] *= pre; pre *= nums[i]）

     为什么能做到额外 O(1)：
       答案数组本身是**返回值**，题目明确说不算额外空间 -> **可以拿它当草稿纸**。
       先存右半边，再从右往左把左半边乘上去，于是省掉了一整个 left[] 数组。

     ⚠️ 顺序细节：`pre *= x` 必须在 `suf[i] *= pre` **之后**。
        先乘的话，suf[i] 里乘进去的是**包含 nums[i] 自己**的前缀积 -> 每个元素都多乘了自己。

     为什么不能用除法：数组里可能有 0。
       - 对值为 0 的元素，`总积 / 0` 直接崩（0/0 也无意义）
       - 就算特判，还要按「数组里有几个 0」分情况，反而更复杂

复杂度：时间 O(n)（两遍扫描）；空间 O(1) 额外（答案数组不算）。

状态：完成（卡点：把空间优化成 O(1)；约 20 分钟）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def product_except_self(nums: list[int]) -> list[int]:
    """返回每个位置「除自身以外所有元素」的乘积（不用除法，额外空间 O(1)）。"""
    n = len(nums)
    suf = [1] * n                       # 先用答案数组存后缀积
    for i in range(n - 2, -1, -1):
        suf[i] = suf[i + 1] * nums[i + 1]

    pre = 1
    for i, x in enumerate(nums):
        suf[i] *= pre                   # 先乘左半边（不含自己）
        pre *= x                        # 再把 x 纳进前缀积

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
    for _ in range(5000):
        nums = [random.randint(-3, 3) for _ in range(random.randint(1, 10))]
        assert product_except_self(nums[:]) == _brute(nums), f"对拍失败: {nums}"
    print("✅ D16 通过")
