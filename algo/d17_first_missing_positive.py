"""D17 缺失的第一个正数（原地哈希）   LeetCode 41   Hard   <- 普通数组第 5 题（小节收尾）

思路：答案一定在 1 ~ n+1 之间（n 个格子最多装 n 个数，鸽巢）。
     所以**负数 / 0 / 大于 n 的数全部无视**。

     核心：**把数组本身当哈希表** —— 数字 x（1 <= x <= n）应该待在下标 x-1。
     扫一遍，把每个能归位的数交换到它该在的位置：
       while nums[i] 在 [1,n] 且 目标位置还没放同样的值:
           交换
     再扫一遍：第一个 nums[i] != i+1 的位置 -> 答案 i+1；全对则 n+1。

     ⚠️ 守卫条件 `nums[nums[i]-1] != nums[i]` 不是可选的：
        没有它，[1,1] / [2,2] 这种重复值会**死循环**（实测超过 10 万步）。
        作用：目标位置已经放了同样的值 -> 再换也没意义 -> 跳过。

     ⚠️ 交换的老问题（和 D04 同一个主题）：被覆盖的值去哪了？
        这里是**交换**不是赋值，两个值都不会丢 —— 这也是为什么必须用交换。

复杂度：时间 O(n) —— 每次交换至少让一个数**永久归位**，总交换次数 <= n
        空间 O(1) —— 只在原数组上交换

状态：完成（卡点：遇到重复的数怎么处理；约 20 分钟）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def first_missing_positive(nums: list[int]) -> int:
    """返回缺失的最小正整数（O(n) 时间 + O(1) 额外空间）。"""
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]

    for i in range(n):
        if nums[i] - 1 != i:
            return i + 1
    return n + 1


def _brute(nums: list[int]) -> int:
    s = set(nums)
    x = 1
    while x in s:
        x += 1
    return x


if __name__ == "__main__":
    for nums, want in [
        ([1, 2, 0], 3),
        ([3, 4, -1, 1], 2),
        ([7, 8, 9, 11, 12], 1),
        ([1], 2),
        ([-1], 1),
        ([0], 1),
        ([1, 1], 2),          # 重复值：守卫条件在这里起作用
        ([2, 2], 1),
        ([1, 2, 3], 4),
        ([-5], 1),
        ([1, 1000], 2),       # 大于 n 的数要无视
    ]:
        got = first_missing_positive(nums[:])
        assert got == want, f"{nums} -> {got}，期望 {want}"

    import random
    random.seed(211)
    for _ in range(5000):
        nums = [random.randint(-5, 12) for _ in range(random.randint(1, 12))]
        assert first_missing_positive(nums[:]) == _brute(nums), f"对拍失败: {nums}"
    print("✅ D17 通过")
