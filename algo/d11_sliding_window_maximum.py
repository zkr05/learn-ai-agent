"""D11 滑动窗口最大值（单调队列）   LeetCode 239   Hard   <- 子串第 2 题

思路：维护一个**下标双端队列**，队列里的元素满足两条：
       值：单调递减（队首最大）
       下标：单调递增（队尾最新）
     于是队首就是当前窗口最大值。

     两端各管一件事（这题最容易混的地方）：
       队首（左）出队 = 扔掉【已经过期】的（下标滑出窗口）—— 管「时间」
       队尾（右）入队前，把【值 <= 新元素】的都弹掉 = 扔掉【永远没机会】的 —— 管「能力」

     为什么弹队尾是安全的（排除论证）：
       新来 x 在下标 i，队尾 y 在下标 j（j < i）且 y <= x。
       对**任意**包含 y 的窗口：只要 y 还在窗口里，x 就一定也在（i > j，x 更晚过期），
       而 x >= y，所以那个窗口的最大值不可能是 y。
       => y 被 x 完全支配，永远不可能成为答案 => 可以安全丢弃。

     两种顺序都对：
       代码可以先「队首过期」再「队尾淘汰」（标准解），也可以反过来（这版就是反的）。
       因为**过期元素只可能出现在队首**（下标递增），而队尾淘汰只按「值」删，互不干扰。
       实测 5000 组随机输入，两种顺序结果一致。

     ⚠️ 队首用 `if` 就够，不需要 `while` —— 这和 D08 正好相反：
        每轮 left 只前进 1 格，而下标唯一 -> 每轮**最多 1 个**元素过期
        （实测 5000 组，同一时刻过期元素最多 1 个）。
        判据还是那句：**一轮里可能需要多次收缩吗？**

     为什么存下标而不是值：只有下标能判断「是否过期」。

复杂度：时间 O(n)   —— 每个下标最多入队一次、出队一次 -> 总操作 <= 2n
        空间 O(k)   —— 队列里最多 k 个下标

状态：完成（卡点：看不懂队首/队尾的进出；看了题解；约 40 分钟）｜ 复习D3 待做
"""

import sys
from collections import deque

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """返回每个长度为 k 的窗口里的最大值。"""
    q = deque()                                # 存下标
    ans = [0] * (len(nums) - k + 1)

    for i, x in enumerate(nums):
        while q and nums[q[-1]] <= x:          # 队尾：被 x 支配的都扔掉
            q.pop()
        q.append(i)

        left = i - k + 1
        if q[0] < left:                        # 队首：过期（每轮最多 1 个）
            q.popleft()

        if left >= 0:
            ans[left] = nums[q[0]]             # 队首就是窗口最大值
    return ans


def _brute(nums: list[int], k: int) -> list[int]:
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


if __name__ == "__main__":
    for nums, k, want in [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),
        ([1], 1, [1]),
        ([1, -1], 1, [1, -1]),
        ([7, 2, 4], 2, [7, 4]),
        ([9, 8, 7, 6], 2, [9, 8, 7]),
        ([1, 2, 3, 4, 5], 2, [2, 3, 4, 5]),    # 单调递增
        ([5, 4, 3, 2, 1], 2, [5, 4, 3, 2]),    # 单调递减
        ([2, 2, 2, 2], 2, [2, 2, 2]),          # 全相等
    ]:
        got = max_sliding_window(nums[:], k)
        assert got == want, f"{nums} k={k} -> {got}，期望 {want}"

    import random
    random.seed(41)
    for _ in range(5000):
        n = random.randint(1, 14)
        k = random.randint(1, n)
        nums = [random.randint(-5, 9) for _ in range(n)]
        assert max_sliding_window(nums[:], k) == _brute(nums, k), f"对拍失败: {nums} {k}"
    print("✅ D11 通过")
