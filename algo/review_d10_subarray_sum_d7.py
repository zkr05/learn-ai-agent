"""复习23（D10 的第 7 天复习，第 2 次重写） ｜ 和为 K 的子数组 ｜ LeetCode 560 ｜ 中等

规则：不许打开 d10_subarray_sum_equals_k.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天（10-23）你答了「内层循环用哈希」，但没说出「前缀和消灭了什么」；
     `cnt[0]=1` 也只举了例子，没说清「漏的是哪一类」。

目标：8 分钟内写完。

两个自述（第 2 次，都要答到机制）：

  1) 这题为什么能到 O(n)？**优化其实是两步** —— 每一步分别消灭了什么？
     （提示：一步消灭"重复累加"，一步消灭"重复查找"。）
     自述 1：

  2) `cnt[0] = 1` 去掉会漏掉**哪一类**子数组？（要说准，不能只举例子）
     自述 2：

状态：待做
"""

import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def subarray_sum(nums: list[int], k: int) -> int:
    """返回和恰好为 k 的连续子数组个数。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


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
    print("✅ 复习D10（第7天）通过 —— 第 2 次独立重写成功")
