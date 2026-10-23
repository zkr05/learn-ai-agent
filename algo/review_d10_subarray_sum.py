"""复习14（D10 的第 3 天复习） ｜ 和为 K 的子数组 ｜ LeetCode 560 ｜ 中等

规则：不许打开 d10_subarray_sum_equals_k.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

三个自述（跑绿之后填）：

  1) 核心等式：怎么把「子数组和 = k」变成「两数之和」？把等式写出来。
     自述 1：设i<j，如果nums[i] 到 nums[j-1]的元素和等于k,用前缀和表示
                    s[j] - s[i] = k -> s[j] + (-s[i]) = k则为两数之和
     确认：等式对 ✅（按你的定义 s[j] = nums[0..j-1] 之和）。
     但「变成两数之和」的落点不在这个变形，而在：**扫到 j 时，问「s[j] - k 之前出现过几次」**——
     也就是把 s[i] 当成「要找的那个数」，再套 D01 的哈希。

  2) `cnt[0] = 1` 为什么必须有？去掉会漏掉**哪一类**子数组？
     （10-21 你举了 [1],k=1 的例子，但没说清"哪一类"。）
     自述 2：表示空前缀的元素和等于0，如果不加会忽略哪些本身的和为k的数组
     半对：要说准是**从下标 0 开始的那一类**（此时 s[j] == k，需要 s[j]-k == 0 有匹配）。
     不是「和为 k 的数组」（那样别的左边界也能处理），而是**左边界恰好是数组开头**的那些。

  3) 为什么这题不能用滑动窗口？
     自述 3：因为这题的数组大小不固定，而且存在负数，窗口的移动也是一个问题。
     纠正：**「数组大小不固定」这句是错的**——数组长度由输入给定，是固定的。
     不固定的是**窗口**。真正的原因只有一条：**有负数 -> 窗口和不单调**
     -> 右移不一定变大、左缩不一定变小 -> 「和太大就缩左边」的假设失效。

状态：完成（2026-10-23 独立重写成功）
"""

import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def subarray_sum(nums: list[int], k: int) -> int:
    """返回和恰好为 k 的连续子数组个数。"""
    cnt = defaultdict(int)
    cnt[0] = 1
    ans = s = 0
    for x in nums:
        s += x
        ans += cnt[s-k]
        cnt[s] += 1
    return ans


def _brute(nums: list[int], k: int) -> int:
    n, total = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == k:
                total += 1
    return total


if __name__ == "__main__":
    for nums, k, want in [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1, -1, 0], 0, 3),
        ([1], 0, 0),
        ([0, 0, 0], 0, 6),
        ([-1, -1, 1], 0, 1),
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
        ([], 0, 0),
        ([1], 1, 1),
        ([100, 1, 2, 3, 4], 6, 1),
    ]:
        got = subarray_sum(nums, k)
        assert got == want, f"{nums} k={k} -> {got}，期望 {want}"

    import random
    random.seed(31)
    for _ in range(2000):
        nums = [random.randint(-3, 3) for _ in range(random.randint(0, 12))]
        k = random.randint(-3, 3)
        assert subarray_sum(nums, k) == _brute(nums, k), f"对拍失败: {nums} {k}"
    print("✅ 复习D10 通过 —— 独立重写成功")
