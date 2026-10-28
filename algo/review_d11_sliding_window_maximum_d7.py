"""复习25（D11 的第 7 天复习，第 2 次重写） ｜ 滑动窗口最大值 ｜ LeetCode 239 ｜ 困难

规则：不许打开 d11_sliding_window_maximum.py，也不许翻 notes.md。
     第 3 天（10-24）两端分工答对了，但「队尾为什么能扔」的量词还不够硬。

目标：12 分钟内写完。

两个自述（第 2 次）：

  1) 队尾出队的排除论证，写成「对任意 ___，都 ___」。
     自述 1：

  2) 队首为什么用 `if` 就够、不需要 `while`？判据是什么？
     （提示：这和 D08 必须用 `while` 是同一条判据的两个结论。）
     自述 2：

状态：待做
"""

import sys
from collections import deque

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """返回每个长度为 k 的窗口里的最大值。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


def _brute(nums: list[int], k: int) -> list[int]:
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


if __name__ == "__main__":
    for nums, k, want in [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),
        ([1], 1, [1]),
        ([7, 2, 4], 2, [7, 4]),
        ([1, 2, 3, 4, 5], 2, [2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], 2, [5, 4, 3, 2]),
        ([2, 2, 2, 2], 2, [2, 2, 2]),
    ]:
        got = max_sliding_window(nums[:], k)
        assert got == want, f"{nums} k={k} -> {got}，期望 {want}"

    import random
    random.seed(41)
    for _ in range(2000):
        n = random.randint(1, 14)
        k = random.randint(1, n)
        nums = [random.randint(-5, 9) for _ in range(n)]
        assert max_sliding_window(nums[:], k) == _brute(nums, k), f"对拍失败: {nums} {k}"
    print("✅ 复习D11（第7天）通过 —— 第 2 次独立重写成功")
