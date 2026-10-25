"""复习17（D07 的第 7 天复习，第 2 次重写） ｜ 接雨水 ｜ LeetCode 42 ｜ 困难

规则：不许打开 d07_trapping_rain_water.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天（10-21）你自述 1 写出了 min(...) = pre_max 那一步（真进步），
     但自述 2（空间为什么 O(1)）又退回成「一边推进一边丢弃」。

目标：12 分钟内写完。

两个自述（第 2 次）：

  1) `pre_max < suf_max` 时为什么能立刻结算 left 并丢掉？
     要写出 `min(左边最高, 右边最高) = pre_max` 这一步。
     自述 1：对pre_max < suf_max ,此时则说明右边一定有柱子大于此时的left的对应柱子，则说明这根柱子不会导致
     后面的数没有被记录，则可以结算推进，右边也是同理。
     补全（**前提对了，缺那个等式** —— 10-21 你写出过，这次忘了）：
       设 pre_max < suf_max。因为 suf_max = max(h[right..n-1]) > pre_max，
       所以右边至少有一根柱子比 pre_max 高 -> 右边最高 >= 那根柱子 > pre_max
       -> **min(左边最高, 右边最高) = pre_max** -> 水位 = pre_max - h[left]，完全确定。

  2) 空间为什么能不用那两个 O(n) 数组？（一句话，要说到"不需要精确值"）
     自述 2：此时不需要精确的数，因为每次对比之后，都直接把这个地方的最优结果算进去了。
     补全（「不需要精确值」说对了，但「为什么」没说）：
       因为 min 被 pre_max **封顶** -> 「右边最高具体是多少」根本不进入计算。
       那两个 O(n) 数组存在的理由就是「逐位置取 min 时要两边的精确值」；
       一旦证明矮的那边就够，精确值就不需要了。

状态：完成（2026-10-25 第 2 次独立重写成功）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def trap(height: list[int]) -> int:
    """每个位置能接的水 = min(左边最高, 右边最高) - height[i]（负数记 0）；返回总和。"""
    n = len(height)
    ans = pre_max = suf_max = 0
    left = 0
    right = n - 1
    while left < right:
        pre_max = max(pre_max, height[left])
        suf_max = max(suf_max, height[right])
        if pre_max < suf_max:
            ans += pre_max - height[left]
            left += 1
        else:
            ans += suf_max - height[right]
            right -= 1
    return ans


def _ref(height: list[int]) -> int:
    total = 0
    for i in range(len(height)):
        lmax = max(height[:i], default=0)
        rmax = max(height[i + 1:], default=0)
        total += max(0, min(lmax, rmax) - height[i])
    return total


if __name__ == "__main__":
    for height, want in [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([], 0), ([1], 0), ([5, 5, 5], 0),
        ([3, 1, 2], 1), ([0, 0, 0], 0),
        ([5, 4, 3, 2, 1], 0), ([1, 2, 3, 4, 5], 0),
        ([2, 0, 2], 2), ([0, 2, 0], 0), ([4, 2, 3], 1),
    ]:
        got = trap(height[:])
        assert got == want, f"{height} -> {got}，期望 {want}"

    import random
    random.seed(5)
    for _ in range(2000):
        height = [random.randint(0, 9) for _ in range(random.randint(0, 14))]
        assert trap(height[:]) == _ref(height), f"对拍失败: {height}"
    print("✅ 复习D07（第7天）通过 —— 第 2 次独立重写成功")
