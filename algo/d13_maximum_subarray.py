"""D13 最大子数组和（前缀和 / 动态规划）   LeetCode 53   Medium   <- 普通数组第 1 题（DP 第一道）

这题的两种写法是「同一个东西」：

  写法 A（本文件，前缀和 + 最小前缀）：
    以 i 结尾的最大子数组和 = pre[i] - min(pre[0..i-1])
    扫一遍，维护「当前前缀和」和「之前见过的最小前缀和」即可。
    这也是 D10（前缀和 + 哈希）的同一个母题 —— 配件从「哈希」换成了「最小前缀」。

  写法 B（经典 DP）：
    cur  = 以 i 结尾的最大子数组和
    cur  = max(nums[i], cur + nums[i])   # 要么重新开始，要么接上前一个
    best = max(best, cur)                # 答案不一定以最后一个元素结尾
    判据：cur > 0 就接上（cur + x > x），否则重新开始。

  两者等价：逐行对比，cur 恒等于 pre - min_pre（实测 5000 组随机输入 0 差异）。

⚠️ 两个边界（都会静默算错，不报错）：
  1) ans 初始化为 -inf，不是 0 —— 全负数时答案是最大的那个负数
     （[-3,-1,-2] -> -1，用 0 初始化会返回 0）
  2) min_pre 必须在算完 ans **之后**更新 —— 先更新就等于允许「空子数组」，
     全负数时返回 0（实测 [-1] -> 0，正确 -1）

复杂度：时间 O(n)   —— 一次遍历，每步 O(1)
        空间 O(1)   —— 只用了 pre / min_pre / ans 三个变量

状态：完成（卡点：无，想通前缀和就顺；约 25 分钟）｜ 复习D3 待做
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
        ans = max(ans, pre_sum - min_pre_sum)   # 先算：以当前结尾的最大和
        min_pre_sum = min(min_pre_sum, pre_sum)  # 再更新：之前的最小前缀和
    return ans


def _dp_version(nums: list[int]) -> int:
    """经典 DP 写法，用来对照（两者结果应完全一致）。"""
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


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
        ([-3, -1, -2], -1),        # 全负数：答案是最大的那个负数
        ([-1], -1),
        ([0], 0),
        ([-2, -1], -1),
        ([1, 2, 3, 4], 10),
        ([-1, -2, -3, -4], -1),
    ]:
        got = max_sub_array(nums[:])
        assert got == want, f"{nums} -> {got}，期望 {want}"
        assert got == _dp_version(nums[:]) == _brute(nums[:])

    import random
    random.seed(61)
    for _ in range(5000):
        nums = [random.randint(-10, 10) for _ in range(random.randint(1, 14))]
        assert max_sub_array(nums[:]) == _brute(nums), f"对拍失败: {nums}"
    print("✅ D13 通过")
