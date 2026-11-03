"""复习35（D17 的第 7 天复习） ｜ 缺失的第一个正数 ｜ LeetCode 41 ｜ 困难

规则：不许打开 d17_first_missing_positive.py，也不许翻 notes.md。

⚠️ 第 3 天（10-30）自述 1 答错过一次：你把"去掉守卫条件的后果"说成了
   "没法从后面再遍历查看谁是缺少的数"，实际是 **[1,1] 这种重复值会死循环**。
   这次重答，先说"去掉之后最坏会怎样"。

目标：12 分钟内写完。

三个自述：

  1) `while` 里的 `nums[nums[i]-1] != nums[i]` 是干什么的？**去掉之后最坏会怎样？**
     自述 1：是查看有没有有重复的数出现，避免出现死循环。去掉之后会一直把重复的数来回换。
     ✅ 这次答对了（10-30 那次是错的："没法从后面再遍历"）。
        更精确：nums[nums[i]-1] != nums[i] 判断的是「**它的家已经放着同一个值**」，
        对重复值来说就是"已经归位了"，所以不用再换。守卫的作用是**防止原地打转**。

  2) 看着是循环套循环，为什么总时间是 O(n)？说清每一步让什么"永久变好"。
     自述 2：因为实际上每一次都会找出一个正确的值，所以是n。每一步让数组更符合我们的要求。
     ⚠️ 半对：前半句方向对；后半句"每一步让数组更符合我们的要求"是空话
        （套到任何题上都能用 -> 说明太泛）。
     精确版：**每次交换都把某个值放到它的家，且这个值之后不会再被移走**
        （家被占了就直接跳过）-> 每个值最多归位一次 -> 总交换 <= n。

  3) 为什么可以完全不管 `<= 0` 和 `> n` 的数？
     自述 3：题目要求的是正数，<= 0的数可以忽略，如果大于n的数出现，则此时数组里没有他的位置了。
     ✅ 基本对：长度 n 的数组若 1..n 全在，答案就是 n+1，所以 > n 的数不可能成为答案。
     代码边界有个坑（结果恰好对，但写法错）：
        你写 `0 <= nums[i] < n`，标准是 `1 <= nums[i] <= n`（即 0 < nums[i] <= n）。
        多放行了 0（0-1 = -1 -> 访问 nums[-1]，最后一个元素），漏掉了 n（n 该去 n-1 位置）。
        穷举 n <= 5 共 35414 组结果**全对**（0 被换到末尾、换出来的值随后会被处理；
        n 不处理也无害）—— 但这是"能跑但理由说不清"，面试官会立刻问"为什么是 < n 不是 <= n"。

状态：完成（2026-11-03 第 2 次独立重写成功，3000 组对拍 + 穷举 35414 组；自述 1 修正成功）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def first_missing_positive(nums: list[int]) -> int:
    """返回不在 nums 里的最小正整数。要求 O(n) 时间、O(1) 额外空间。"""
    n = len(nums)
    for i in range(n):
        while 0 <= nums[i] < n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i],nums[j] = nums[j],nums[i]
    for i in range(n):
        if nums[i] - 1 != i:
            return i + 1
    return n + 1


def _ref(nums: list[int]) -> int:
    """暴力：从 1 开始一个个试。"""
    s = set(nums)
    x = 1
    while x in s:
        x += 1
    return x


if __name__ == "__main__":
    for src in [
        [1, 2, 0],
        [3, 4, -1, 1],
        [7, 8, 9, 11, 12],
        [1],
        [2],
        [0],
        [-1],
        [1, 1],
        [1, 1, 1],
        [2, 2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [0, 1, 2],
        [-5, -3, -1],
        [100, 101],
        [1, 1000],
    ]:
        got = first_missing_positive(src[:])
        want = _ref(src)
        assert got == want, f"{src} -> {got}，期望 {want}"

    import random
    random.seed(41)
    for _ in range(3000):
        n = random.randint(1, 8)
        src = [random.randint(-3, 10) for _ in range(n)]
        assert first_missing_positive(src[:]) == _ref(src), f"对拍失败: {src}"
    print("✅ 复习D17（第7天）通过 —— 第 2 次独立重写成功")
