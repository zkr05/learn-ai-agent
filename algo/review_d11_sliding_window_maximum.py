"""复习16（D11 的第 3 天复习） ｜ 滑动窗口最大值 ｜ LeetCode 239 ｜ 困难

规则：不许打开 d11_sliding_window_maximum.py，也不许翻 notes.md。凭记忆独立写。

目标：12 分钟内写完（单调队列是新工具，给足时间）。

两个自述（跑绿之后填）：

  1) 两端各管什么？
     队首出队 = 扔掉 ___；队尾出队 = 扔掉 ___。
     自述 1：队首出队=扔掉已经超过的元素，是窗口离开了；队尾出列=此时队里的元素没有新进来的元素大，而在窗口离开该数之前，
     该数会一直跟新进来最大的元素一起，所以可以队尾可以直接出队，新的元素到队尾。
     ✅ 对。关键那句是「在窗口离开该数之前，该数会一直跟新进来最大的元素一起」——
     正是「**更大 + 更晚过期**」这两个性质。

  2) 为什么队尾可以扔？要写成「对任意 ___，都有 ___」的形式（排除论证）。
     自述 2：对任意的 x >= nums[q[-1]],此时x比队尾元素更新更大，所以把队尾直接丢弃，不会对最大值有影响。
     ✅ 基本对（更大 + 更新都说了）。再严谨一点：量词应该落在「包含 y 的**任意窗口**」上 ——
     对任意包含队尾 y 的窗口，只要 y 还在，x 也一定在（x 更晚过期），而 x >= y
     -> 那个窗口的最大值不可能是 y。

状态：完成（2026-10-24 独立重写成功）
"""

import sys
from collections import deque

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """返回每个长度为 k 的窗口里的最大值。"""
    ans = [0] * (len(nums) - k + 1)
    q = deque()

    for i ,x in enumerate(nums):
        while q and nums[q[-1]] <= x:
            q.pop()
        q.append(i)

        left = i - k + 1
        if q[0] < left:
            q.popleft()


        if left >= 0:
            ans[left] = nums[q[0]]

    return ans




def _brute(nums: list[int], k: int) -> list[int]:
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]


if __name__ == "__main__":
    for nums, k, want in [
        ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
        ([1, 3, 1, 2, 0, 5], 3, [3, 3, 2, 5]),
        ([1], 1, [1]),
        ([7, 2, 4], 2, [7, 4]),
        ([1, 2, 3, 4, 5], 2, [2, 3, 4, 5]),
        ([5, 4, 3, 2, 1], 2, [5, 4, 3, 2]),
        ([2, 2, 2, 2], 2, [2, 2, 2]),
    ]:
        got = max_sliding_window(nums[:], k)
        assert got == want, f"{nums} k={k} -> {got}，期望 {want}"

    import random
    random.seed(41)
    for _ in range(2000):
        n = random.randint(1, 14)
        k = random.randint(1, n)
        nums = [random.randint(-5, 9) for _ in range(n)]
        assert max_sliding_window(nums[:], k) == _brute(nums, k), f"对拍失败: {nums} {k}"
    print("✅ 复习D11 通过 —— 独立重写成功")
