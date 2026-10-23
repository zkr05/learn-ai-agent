"""复习14（D10 的第 3 天复习） ｜ 和为 K 的子数组 ｜ LeetCode 560 ｜ 中等

规则：不许打开 d10_subarray_sum_equals_k.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

三个自述（跑绿之后填）：

  1) 核心等式：怎么把「子数组和 = k」变成「两数之和」？把等式写出来。
     自述 1：

  2) `cnt[0] = 1` 为什么必须有？去掉会漏掉**哪一类**子数组？
     （10-21 你举了 [1],k=1 的例子，但没说清"哪一类"。）
     自述 2：

  3) 为什么这题不能用滑动窗口？
     自述 3：

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
    print("✅ 复习D10 通过 —— 独立重写成功")
