"""复习1（D01 的第 3 天复习） ｜ 两数之和 ｜ LeetCode 1 ｜ 简单

规则：不许打开 d01_two_sum.py，也不许翻 notes.md。凭记忆独立写。
     写不出来才是这次复习的价值 —— 说明当时是「看懂了」不是「会写了」。

目标：5 分钟内写完，一次通过。

复习结果（2026-10-10）：10 分钟独立写出最优解（一遍哈希 + 先查再存），3 条断言一次通过。
      对比第一次（10-08）：看题解才会 —— 思路记住了，手也还能写。

状态：完成 ｜ 下次复习（D7）：2026-10-14
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def two_sum(nums: list[int], target: int) -> list[int]:
    """返回两个下标，使对应的元素之和等于 target。"""

    idx = {}
    for j, x in enumerate(nums):
        if target - x in idx:
            return [idx[target - x], j]
        idx[x] = j
    return []      # 无解时返回空列表；不写的话函数会隐式返回 None，调用方容易踩坑


if __name__ == "__main__":
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]      # 同一个元素不能用两次
    print("✅ 复习1 通过 —— D01 独立重写成功")
