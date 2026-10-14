"""复习2（D01 的第 7 天复习，第 2 次重写） ｜ 两数之和 ｜ LeetCode 1 ｜ 简单

规则：不许打开 d01_two_sum.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天那次你 10 分钟写出来了，这次目标 **5 分钟**。

目标：5 分钟内写完。

两个自述（跑绿之后填，第 2 次要比第 1 次答得更透）：
  1) 一遍扫描为什么就够？（提示：扫到 j 的那一刻，i 在哪？）
  2) 如果题目改成「返回**所有**和为 target 的下标对」，现在写法里的哪一句会失效？为什么？

自述 1：
自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def two_sum(nums: list[int], target: int) -> list[int]:
    """返回两个下标，使对应的元素之和等于 target。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


if __name__ == "__main__":
    cases = [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),          # ← 先查再存的陷阱用例
        ([0, 4, 3, 0], 0, [0, 3]),    # ← 两个 0：考验「查的时候自己还没进字典」
    ]
    for nums, target, want in cases:
        got = two_sum(nums, target)
        assert got == want, f"two_sum({nums}, {target}) -> {got}，期望 {want}"
    print("✅ 复习D01（第7天）通过 —— 第 2 次独立重写成功")
