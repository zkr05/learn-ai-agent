"""D10 和为 K 的子数组（前缀和 + 哈希）   LeetCode 560   Medium   <- 子串第 1 题

思路：这题本质上就是 **D01 两数之和**，只是把「数」换成了「前缀和」。

     关键等式：
       sum(i..j) = prefix[j] - prefix[i-1]
     => 「找 sum(i..j) == k」等价于「找 prefix[i-1] == prefix[j] - k」
     => 扫到 j 时问：**之前出现过几次 (prefix[j] - k)？** —— 这就是两数之和。

     为什么能到 O(n)，是**两步**（很多人只想到第二步）：
       ① 前缀和：消灭「重复累加」。暴力里固定 i 后，每个 j 都要把 i..j 重新加一遍；
          有前缀和后，任意区间和变成一次减法。
       ② 哈希：消灭「查找」。找 prefix[i-1] 从 O(n) 降到 O(1)。

     ⚠️ `cnt[0] = 1` 不能少：
        cnt 记录「已经出现过的前缀和」，而 cnt[0] 代表**空前缀**（下标 -1 处，和为 0）。
        当 s == k 时 s - k == 0，需要 cnt[0] 才能数到「**从下标 0 开始**」的那个子数组。
        实测去掉它：[1,1,1] k=2 少 1；[3] k=3 全丢。

     ⚠️ 先查再存，顺序不能反：
        先 `cnt[s] += 1` 再 `ans += cnt[s-k]`，k == 0 时会把**当前前缀自己**算进去
        （相当于把空子数组当成答案）。实测 [0,0,0] k=0 返回 9（正确 6）；[1] k=0 返回 1（正确 0）。
        这就是 D01 的「先查再存」——同一个坑。

     ⚠️ 不能用滑动窗口：数组可能有**负数**，窗口和不再单调，
        「和太大就缩左边」这个假设失效。实测 [1,-1,1] k=1：滑窗得 2，正确 3。

复杂度：时间 O(n)   —— 一次遍历，每步 O(1) 哈希查/存
        空间 O(n)   —— cnt 里最多 n+1 个不同的前缀和

状态：完成（卡点：卡在从 O(n^2) 暴力优化到 O(n)）｜ 复习D3 待做
"""

import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def subarray_sum(nums: list[int], k: int) -> int:
    """返回和恰好为 k 的连续子数组个数。"""
    cnt = defaultdict(int)
    cnt[0] = 1                 # 空前缀（下标 -1，和 0）—— 少了它就漏掉"从 0 开始"的子数组
    ans = s = 0
    for x in nums:
        s += x
        ans += cnt[s - k]      # 先查
        cnt[s] += 1            # 再存（顺序反了，k=0 时会把空子数组算进去）
    return ans


def _brute(nums: list[int], k: int) -> int:
    """暴力：枚举左右端点。只用来对拍。"""
    n, total = len(nums), 0
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s == k:
                total += 1
    return total


if __name__ == "__main__":
    for nums, k, want in [
        ([1, 1, 1], 2, 2),
        ([1, 2, 3], 3, 2),
        ([1, -1, 0], 0, 3),
        ([1], 0, 0),
        ([0, 0, 0], 0, 6),        # 全 0：每个子数组和都是 0
        ([-1, -1, 1], 0, 1),
        ([3, 4, 7, 2, -3, 1, 4, 2], 7, 4),
        ([], 0, 0),
        ([1], 1, 1),
        ([100, 1, 2, 3, 4], 6, 1),
    ]:
        got = subarray_sum(nums, k)
        assert got == want, f"{nums} k={k} -> {got}，期望 {want}"

    import random
    random.seed(31)
    for _ in range(3000):
        nums = [random.randint(-3, 3) for _ in range(random.randint(0, 12))]
        k = random.randint(-3, 3)
        assert subarray_sum(nums, k) == _brute(nums, k), f"对拍失败: {nums} {k}"
    print("✅ D10 通过")
