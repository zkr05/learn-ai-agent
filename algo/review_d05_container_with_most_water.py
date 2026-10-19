"""复习7（D05 的第 3 天复习，**合并**第 7 天） ｜ 盛最多水的容器 ｜ LeetCode 11 ｜ 中等

为什么合并：生病欠了 3 天账，D05 的 D3（原定 10-15）和 D7（原定 10-19）只差 4 天，
         一次重写就能同时达到两个目的（两个复习测的都是"还会不会写"）。

规则：不许打开 d05_container_with_most_water.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

证明三段式（**这次重点** —— 上次答的是"怎么让和变大"（操作），不是"丢掉它会不会漏"（正确性））：
  1) 瓶颈：矮的那条边 —— 面积 = 高度 x 宽度，而高度被矮边**封顶**。
  2) 排除（**这次答对了**：分情况写法，比一长串不等式更好讲）：
     设 h[left] < h[right]，即 left 是矮边。对**任意** k（left < k < right）：
       - h[k] <= h[left] 时：面积 = h[k]x(k-left) <= h[left]x(k-left) < h[left]x(right-left) = 当前面积
       - h[k] >  h[left] 时：面积 = h[left]x(k-left) < h[left]x(right-left) = 当前面积
     两种情况都严格更小，而且情况是**穷尽**的 -> left 再也不可能更优。
     支点是那四个字：**矮边不变** —— 高度不能变大，想翻盘只能靠宽度，而宽度只会变小。
  3) 结论：所以可以安全丢弃 left -> left += 1。

状态：完成（2026-10-19 重写成功；同时清掉 D3 逾期 4 天 + D7 当天两笔账）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_area(height: list[int]) -> int:
    """两条竖线与 x 轴围成的容器，能装的最大水量。"""
    left = 0
    right = len(height) - 1
    ans = 0
    while left < right:
        area = min(height[left],height[right]) * (right - left)
        ans = max(area,ans)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return ans


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
