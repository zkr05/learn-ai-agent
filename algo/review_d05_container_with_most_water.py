"""复习7（D05 的第 3 天复习，**合并**第 7 天） ｜ 盛最多水的容器 ｜ LeetCode 11 ｜ 中等

为什么合并：生病欠了 3 天账，D05 的 D3（原定 10-15）和 D7（原定 10-19）只差 4 天，
         一次重写就能同时达到两个目的（两个复习测的都是"还会不会写"）。

规则：不许打开 d05_container_with_most_water.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

证明三段式（**这次的重点** —— 上次你答的是"怎么让和变大"（操作），不是"丢掉它会不会漏"（正确性））：
  1) 瓶颈：
  2) 排除：为什么丢掉它不会漏答案？（关键那一句 —— 要写出不等式）
  3) 结论：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_area(height: list[int]) -> int:
    """两条竖线与 x 轴围成的容器，能装的最大水量。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


if __name__ == "__main__":
    for h, want in [
        ([1, 8, 6, 2, 5, 4, 8, 3, 7], 49),
        ([1, 1], 1),
        ([4, 3, 2, 1, 4], 16),
        ([1, 2, 1], 2),
        ([2, 3, 4, 5, 18, 17, 6], 17),
        ([1, 1, 1, 1], 3),
        ([1, 2], 1),
    ]:
        got = max_area(h[:])
        assert got == want, f"{h} -> {got}，期望 {want}"
    print("✅ 复习D05 通过 —— 重写成功（同时清掉 D3 + D7 两笔账）")
