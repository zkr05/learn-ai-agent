"""复习10（D07 的第 3 天复习） ｜ 接雨水 ｜ LeetCode 42 ｜ 困难

规则：不许打开 d07_trapping_rain_water.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完。

两个自述（跑绿之后填。两个都对着 D07 当天没答好的地方）：

  1) 三段式：`pre_max < suf_max` 时，为什么可以**立刻**给 `left` 结算水量并丢掉它？
     必须写出 `min(左边最高, 右边最高) = pre_max` 这一步 —— 不能只写「右边一定更高」。
     自述 1：

  2) 空间：为什么双指针能不用「左边最高数组 / 右边最高数组」那两个 O(n) 数组？
     一句话说清（提示：它跟第 1 题的最后一步是同一个原因）。
     自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def trap(height: list[int]) -> int:
    """每个位置能接的水 = min(左边最高, 右边最高) - height[i]（负数记 0）；返回总和。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


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
