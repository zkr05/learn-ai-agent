"""复习28（D13 的第 7 天复习，第 2 次重写） ｜ 最大子数组和 ｜ LeetCode 53 ｜ 中等

规则：不许打开 d13_maximum_subarray.py，也不许翻 notes.md。
     第 3 天（10-26）自述 2、3 都对，只有自述 1（与 DP 版的对应关系）没填。

目标：6 分钟内写完。

三个自述（第 2 次）：

  1) 你这版（前缀和 + 最小前缀）和经典 DP 怎么对应？
     `pre_sum - min_pre_sum` 相当于 DP 里的哪个量？
     自述 1：等于cur
     ✅ 对（`cur` = 以 i 结尾的最大子数组和），但太短了。补全一句：
        一个用「前缀和 - 最小前缀」直接算，一个用 `max(x, cur + x)` 递推，**算的是同一个量**
        （逐行对比 + 5000 组随机输入一致）。

  2) `ans` 为什么初始化成 `-inf` 而不是 0？
     自述 2：因为当前面的数前缀和小于0的时候，如果初始化为一个具体的值，总会比它小，
     所以弄能无穷小。
     半对：结论对（用 `-inf`），但表述绕了。准确的说法：
       全负数时答案是**负数**，任何具体初值（比如 0）都可能**大于**答案，
       于是 `max` 永远保留那个初值 -> 用 `-inf` 保证第一个真实值一定能更新它。

  3) `min_pre_sum` 为什么必须在算完 `ans` 之后更新？
     自述 3：因为如果先更新的话，会得到一个空的数组，不符合题目的子数组最少包含一个元素。
     ✅ 对（和 10-26 一致）—— 「子数组至少一个元素」正是这个坑的本质。

状态：完成（2026-10-30 第 2 次独立重写成功）
"""

import sys
from math import inf

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_sub_array(nums: list[int]) -> int:
    """返回和最大的连续子数组的和（至少包含一个元素）。"""
    ans = -inf
    min_pre_sum = pre_sum = 0
    for x in nums:
        pre_sum += x
        ans = max(ans, pre_sum - min_pre_sum)
        min_pre_sum = min(pre_sum, min_pre_sum)
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
        ([-3, -1, -2], -1),
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
    print("✅ 复习D13（第7天）通过 —— 第 2 次独立重写成功")
