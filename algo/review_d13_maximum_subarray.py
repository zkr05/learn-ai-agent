"""复习20（D13 的第 3 天复习） ｜ 最大子数组和 ｜ LeetCode 53 ｜ 中等

规则：不许打开 d13_maximum_subarray.py，也不许翻 notes.md。凭记忆独立写。

目标：6 分钟内写完。

三个自述（跑绿之后填）：

  1) 你这版（前缀和 + 最小前缀）和经典 DP 是怎么对应的？
     `pre_sum - min_pre_sum` 相当于 DP 里的哪个量？
     自述 1：

  2) `ans` 为什么初始化成 `-inf` 而不是 0？
     自述 2：因为第一次比较的时候，需要有一个数一定可以更新ans的值，如果初始化为具体的值总会有反例。
     确认：✅ 对 —— `-inf` 保证第一个真实值一定能更新 ans；任何具体值（包括 0）都会在全负数时出错。

  3) `min_pre_sum` 为什么必须在算完 `ans` 之后更新？先更新会变成什么？
     自述 3：如果先更新min_pre_sum的值，则不符合题目的子数字最少包含一个元素，则如果最大和小于0，
     则答案只会输出0.
     确认：✅ 完全正确 —— 「子数组至少一个元素」正是这个坑的本质：
      先更新就等于允许 `pre[i] - pre[i] = 0`，也就是空区间。

状态：完成（2026-10-26 独立重写成功）
"""

import sys
from math import inf

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_sub_array(nums: list[int]) -> int:
    """返回和最大的连续子数组的和（至少包含一个元素）。"""
    min_pre_sum = 0
    pre_sum = 0
    ans = -inf
    for x in nums:
        pre_sum += x
        ans = max(ans,pre_sum - min_pre_sum)
        min_pre_sum = min(pre_sum,min_pre_sum)
    return ans

def _brute(nums: list[int]) -> int:
    best = -inf
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            best = max(best, s)
    return best


if __name__ == "__main__":
    for nums, want in [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([5, 4, -1, 7, 8], 23),
        ([-3, -1, -2], -1),        # 全负数
        ([-1], -1),
        ([0], 0),
        ([-2, -1], -1),
        ([1, 2, 3, 4], 10),
        ([-1, -2, -3, -4], -1),
    ]:
        got = max_sub_array(nums[:])
        assert got == want, f"{nums} -> {got}，期望 {want}"

    import random
    random.seed(61)
    for _ in range(2000):
        nums = [random.randint(-10, 10) for _ in range(random.randint(1, 14))]
        assert max_sub_array(nums[:]) == _brute(nums), f"对拍失败: {nums}"
    print("✅ 复习D13 通过 —— 独立重写成功")
