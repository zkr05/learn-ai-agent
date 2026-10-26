"""D15 轮转数组（三次反转）   LeetCode 189   Medium   <- 普通数组第 3 题

思路：向右轮转 k 步 = 把数组切成 A + B（B 是最后 k 个），变成 B + A。
     不能直接搬（要原地、两段长度还不等），所以用**三次反转**：

       ① 反转整个数组   -> B^R + A^R     （两段换了位置，但每段内部反了序）
       ② 反转前 k 个    -> B   + A^R     （把 B^R 修正回来）
       ③ 反转后 n-k 个  -> B   + A       （把 A^R 修正回来）

     为什么能想到这招：
       反转是**原地操作里最便宜的"换位置"**（两个指针交换，O(1) 空间）。
       但它有副作用：**内部顺序也反了**。所以再反两次把副作用抵消。
       一句话：**一次反转 = 换位置 + 反序；我们只要换位置，于是多反两次抵消反序。**

     两个边界：
       1) `k %= n` —— 轮 n 次等于没轮（k=10, n=7 实际只转 3 步）
       2) k = 0 时 `reverse(0, -1)` 是**安全空操作**（`while i < j` 一开始就 False）
       注：n = 0 时 `k % n` 会 ZeroDivisionError；本题保证 n >= 1。

复杂度：时间 O(n)（三次反转加起来，每个元素被访问常数次）；空间 O(1)（满足进阶要求）。

状态：完成（卡点：怎么想到「负负得正」的翻转；约 20 分钟）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(nums: list[int], k: int) -> None:
    """把数组向右轮转 k 步（原地修改，不返回）。"""
    def reverse(i: int, j: int) -> None:
        while i < j:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
            j -= 1

    n = len(nums)
    k = k % n
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)


def _ref(nums: list[int], k: int) -> list[int]:
    n = len(nums)
    k %= n
    return nums[-k:] + nums[:-k] if k else nums[:]


if __name__ == "__main__":
    for src, k, want in [
        ([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4]),
        ([-1, -100, 3, 99], 2, [3, 99, -1, -100]),
        ([1], 0, [1]),
        ([1], 5, [1]),
        ([1, 2], 3, [2, 1]),          # k > n
        ([1, 2, 3], 0, [1, 2, 3]),    # k = 0 -> 空操作
        ([1, 2, 3], 3, [1, 2, 3]),    # k = n
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], 1, [5, 1, 2, 3, 4]),
    ]:
        got = src[:]
        assert rotate(got, k) is None, "题目要求原地修改、不返回"
        assert got == want, f"{src} k={k} -> {got}，期望 {want}"

    import random
    random.seed(97)
    for _ in range(5000):
        n = random.randint(1, 12)
        k = random.randint(0, 25)
        arr = [random.randint(-9, 9) for _ in range(n)]
        got = arr[:]
        rotate(got, k)
        assert got == _ref(arr[:], k), f"对拍失败: {arr} k={k}"
    print("✅ D15 通过")
