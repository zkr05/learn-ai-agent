"""复习1（D03 的第 3 天复习） ｜ 最长连续序列 ｜ LeetCode 128 ｜ 中等

规则：不许打开 d03_longest_consecutive.py，也不许翻 notes.md。凭记忆独立写。
     这次的重点不只是「写不写得出来」，还有「复杂度还能不能讲清」——
     跑绿之后，用一句话回答：这版为什么是 O(n)？（写在下面「复杂度自述」处）

目标：5 分钟内写完。

复杂度自述：
是先找到起点，再单独在这里 while —— 看着像嵌套循环，但实际不是。
为什么不是（补上上次答漏的那半句）：`while` **只在起点**执行，而每个数只属于一个连续段，
所以所有段长之和 ≤ n，`while` 的**总**迭代次数 ≤ n（**不是**每次 n 次）。
于是 n + n = O(n)，**不是** n × n。

状态：完成（2026-10-12 独立重写成功）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def longest_consecutive(nums: list[int]) -> int:
    """最长连续整数序列的长度（不要求在原数组里相邻）。"""
    d = set(nums)
    ans = 0
    for x in d:
        if x - 1 in d:
            continue
        y = x + 1
        while y in d:
            y += 1
        ans = max(ans, y - x)
    return ans


if __name__ == "__main__":
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0
    assert longest_consecutive([1, 2, 0, 1]) == 3
    assert longest_consecutive([0, -1, 1]) == 3
    print("✅ 复习D03 通过 —— 独立重写成功")
