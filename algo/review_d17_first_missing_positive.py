"""复习29（D17 的第 3 天复习） ｜ 缺失的第一个正数 ｜ LeetCode 41 ｜ 困难

规则：不许打开 d17_first_missing_positive.py，也不许翻 notes.md。凭记忆独立写。

目标：12 分钟内写完。

两个自述（跑绿之后填）：

  1) `while` 条件里的 `nums[nums[i]-1] != nums[i]` 是干什么的？
     （去掉会怎样？）
     自述 1：

  2) 每次都像嵌套循环，为什么总时间是 O(n)？
     自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def first_missing_positive(nums: list[int]) -> int:
    """返回缺失的最小正整数（O(n) 时间 + O(1) 额外空间）。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


def _brute(nums: list[int]) -> int:
    s = set(nums)
    x = 1
    while x in s:
        x += 1
    return x


if __name__ == "__main__":
    for nums, want in [
        ([1, 2, 0], 3),
        ([3, 4, -1, 1], 2),
        ([7, 8, 9, 11, 12], 1),
        ([1], 2),
        ([-1], 1),
        ([0], 1),
        ([1, 1], 2),
        ([2, 2], 1),
        ([1, 2, 3], 4),
        ([-5], 1),
        ([1, 1000], 2),
    ]:
        got = first_missing_positive(nums[:])
        assert got == want, f"{nums} -> {got}，期望 {want}"

    import random
    random.seed(211)
    for _ in range(2000):
        nums = [random.randint(-5, 12) for _ in range(random.randint(1, 12))]
        assert first_missing_positive(nums[:]) == _brute(nums), f"对拍失败: {nums}"
    print("✅ 复习D17 通过 —— 独立重写成功")
