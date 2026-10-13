"""D05 盛最多水的容器（双指针）   LeetCode 11   Medium

思路：双指针从两端向中间夹逼。每轮算一次面积，然后**只移动矮的那一边**。

     为什么移动矮边是安全的（本题灵魂，排除法证明）：
       设 h[left] < h[right]。考虑 left 和任何更靠内的 k（left < k < right）组成的容器：
         面积(left,k) = min(h[left], h[k]) * (k - left)
                      <= h[left] * (k - left)        因为 min <= h[left]
                      <  h[left] * (right - left)    因为 k < right
                      =  当前面积
       所以 left 这条线和任何更窄的右边界组合都不可能更优 -> left 已被榨干，可以安全丢弃。
     机制一句话：**矮边封死了高度上限，想更优只能靠变宽，而宽度只会变小**。

     为什么不能乱移（实测，2000 组随机输入）：
       无脑移左边     错 770/2000  (38.5%)
       移动高的一边   错 1272/2000 (63.6%)
       最小反例 [3,3,1]：正确 3（下标 0,1）；无脑移左边得 2（它只走过 (0,2) 和 (1,2)）

复杂度：时间 O(n)   —— 每轮窗口长度严格减 1，从 n 收到 1，最多 n-1 轮（实测 n=50 -> 49 轮）
        空间 O(1)   —— 只有 left / right / ans 三个变量
        注意与 D03 的 O(n) 机制不同：D03 是「每个元素最多被数一次」的计数论证，
                                    这题是「每轮消灭一个候选」的窗口收缩论证。

状态：完成（看题解才会，卡在「为什么移动短边」；约 25 分钟）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_area(height: list[int]) -> int:
    """两条竖线与 x 轴围成的容器，能装的最大水量。"""
    ans = 0
    left = 0
    right = len(height) - 1
    while left < right:
        area = (right - left) * min(height[left], height[right])
        ans = max(ans, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return ans


def _brute(height: list[int]) -> int:
    """O(n^2) 暴力解 —— 只用来对拍，验证双指针没漏掉最优解。"""
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, (j - i) * min(height[i], height[j]))
    return best


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
        assert max_area(h) == want, f"{h} -> {max_area(h)}，期望 {want}"

    # 对拍：双指针必须和暴力解完全一致，否则说明「丢掉的组合」里其实有最优解
    import random
    random.seed(7)
    for _ in range(300):
        h = [random.randint(1, 40) for _ in range(random.randint(2, 25))]
        assert max_area(h) == _brute(h), f"对拍失败: {h}"
    print("✅ D05 通过")
