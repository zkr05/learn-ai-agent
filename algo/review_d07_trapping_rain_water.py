"""复习10（D07 的第 3 天复习） ｜ 接雨水 ｜ LeetCode 42 ｜ 困难

规则：不许打开 d07_trapping_rain_water.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

两个自述（跑绿之后填。两个都对着 D07 当天没答好的地方）：

  1) 三段式：`pre_max < suf_max` 时，为什么可以**立刻**给 `left` 结算水量并丢掉它？
     必须写出 `min(左边最高, 右边最高) = pre_max` 这一步 —— 不能只写「右边一定更高」。
     自述 1：如果pre_max[left] <= suf_max[right],由于suf_max[right] <= suf_max[left],
     则pre_max[left]<=suf_max[right]<=suf_max[left],所以min(pre_max[left],suf_max[left]) = pre_max[left]
     所以可以求出水量
     确认：**这一条对了** —— 第一次自己写出「min(...) = pre_max」这一步（不是只写"右边更高"）。
     只差一个小理由：为什么 suf_max[right] <= suf_max[left]？
     因为区间 [right..n-1] 是 [left..n-1] 的**子集**，而子集的最大值不会超过全集的最大值。

  2) 空间：为什么双指针能不用「左边最高数组 / 右边最高数组」那两个 O(n) 数组？
     一句话说清（提示：它跟第 1 题的最后一步是同一个原因）。
     自述 2：因为这里是一边推进，一边丢弃。
     补全（**又是"操作"** —— 这句话在任何双指针题里都成立，没有信息量）：
       真正的原因：**不需要知道另一边的精确最高值**。
       当 pre_max < suf_max 时，右边至少有一根柱子比 pre_max 高（自述 1 的等式），
       所以水位完全由 pre_max 决定 —— 「右边最高具体是多少」根本不进入计算。
       那两个 O(n) 数组存在的理由就是「逐位置取 min 时需要两边的精确值」；
       一旦证明「矮的那边就够」，精确值就不需要了 -> 两个数组可以省掉。

状态：完成（2026-10-21 独立重写成功；逾期 4 天补做）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def trap(height: list[int]) -> int:
    """每个位置能接的水 = min(左边最高, 右边最高) - height[i]（负数记 0）；返回总和。"""
    ans = pre_max = suf_max = 0
    left, right = 0, len(height)-1
    while left < right:
        pre_max = max(pre_max, height[left])
        suf_max = max(suf_max, height[right])
        if pre_max < suf_max:
            ans += (pre_max - height[left])
            left += 1
        else:
            ans += (suf_max - height[right])
            right -= 1
    return ans

def _ref(height: list[int]) -> int:
    """参考解（直译定义），只用来对拍。"""
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
        ([5, 4, 3, 2, 1], 0),      # 单调递减
        ([1, 2, 3, 4, 5], 0),      # 单调递增
        ([2, 0, 2], 2), ([0, 2, 0], 0), ([4, 2, 3], 1),
    ]:
        got = trap(height[:])
        assert got == want, f"{height} -> {got}，期望 {want}"

    import random
    random.seed(5)
    for _ in range(2000):
        height = [random.randint(0, 9) for _ in range(random.randint(0, 14))]
        assert trap(height[:]) == _ref(height), f"对拍失败: {height}"
    print("✅ 复习D07 通过 —— 独立重写成功")
