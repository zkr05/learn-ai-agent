"""D07 接雨水（双指针）   LeetCode 42   Hard   <- 双指针小节的最后一题

思路：每个位置的水量 = min(左边最高的柱子, 右边最高的柱子) - height[i]（负数记 0）。
     这就是 D05「容器水位」的**同一个直觉**：水位由**矮的那一侧封顶**。

     常见做法（O(n) 空间）：先从左扫一遍记下「每个位置左边的最高」，再从右扫一遍记「右边最高」，
     最后逐位置取 min、减掉自己。

     双指针把它压到 O(1) —— 关键在于：**不需要知道另一边的精确最高值，只要知道「哪边更矮」**。
       当 pre_max < suf_max 时：
         pre_max = max(h[0..left])；而右边**一定存在**一根比 pre_max 更高的柱子
         （因为 suf_max = max(h[right..n-1]) > pre_max）
         => min(左边最高, 右边最高) = pre_max
         => left 位置的水位**完全确定**，可以立刻结算并丢掉 left。
       反过来同理结算 right。所以两个变量就够，不需要那两个数组。

复杂度：时间 O(n)   —— left/right 单调向内，每个位置最多被访问一次
        空间 O(1)   —— 只有 left / right / pre_max / suf_max 四个变量

注（这版的一个细节）：用 `while left <= right`，比标准写法 `left < right` 多跑一轮。
    多跑那轮 left == right：此时 pre_max 和 suf_max 都被更新过、**都包含 h[left] 自己**，
    实测加进去的值是 0；20000 组随机输入与标准写法结果一致 —— 是**合法变体**，不是 bug。
    （标准 < 版本停下时落点位置的真实水量恒为 0，所以它不需要处理那一格。）

状态：完成（看题解才会，自己想不出来）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def trap(height: list[int]) -> int:
    """每个位置能接的水 = min(左边最高, 右边最高) - height[i]（负数记 0）；返回总和。"""
    n = len(height)
    left, right = 0, n - 1
    pre_max = 0
    suf_max = 0
    ans = 0
    while left <= right:
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
    """参考解（直译定义）：每个位置左右各求一次最高。只用来对拍，O(n^2)。"""
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
        ([], 0),
        ([1], 0),
        ([5, 5, 5], 0),
        ([3, 1, 2], 1),
        ([0, 0, 0], 0),
        ([5, 4, 3, 2, 1], 0),      # 单调递减，接不到水
        ([1, 2, 3, 4, 5], 0),      # 单调递增，接不到水
        ([2, 0, 2], 2),
        ([0, 2, 0], 0),
        ([4, 2, 3], 1),
    ]:
        got = trap(height[:])
        assert got == want, f"{height} -> {got}，期望 {want}"

    import random
    random.seed(5)
    for _ in range(3000):
        height = [random.randint(0, 9) for _ in range(random.randint(0, 14))]
        assert trap(height[:]) == _ref(height), f"对拍失败: {height}"
    print("✅ D07 通过")
