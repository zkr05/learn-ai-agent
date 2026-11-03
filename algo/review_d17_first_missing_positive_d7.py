"""复习35（D17 的第 7 天复习） ｜ 缺失的第一个正数 ｜ LeetCode 41 ｜ 困难

规则：不许打开 d17_first_missing_positive.py，也不许翻 notes.md。

⚠️ 第 3 天（10-30）自述 1 答错过一次：你把"去掉守卫条件的后果"说成了
   "没法从后面再遍历查看谁是缺少的数"，实际是 **[1,1] 这种重复值会死循环**。
   这次重答，先说"去掉之后最坏会怎样"。

目标：12 分钟内写完。

三个自述：

  1) `while` 里的 `nums[nums[i]-1] != nums[i]` 是干什么的？**去掉之后最坏会怎样？**
     自述 1：

  2) 看着是循环套循环，为什么总时间是 O(n)？说清每一步让什么"永久变好"。
     自述 2：

  3) 为什么可以完全不管 `<= 0` 和 `> n` 的数？
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def first_missing_positive(nums: list[int]) -> int:
    """返回不在 nums 里的最小正整数。要求 O(n) 时间、O(1) 额外空间。"""
    # TODO: 你来写（不许看旧文件）
    raise NotImplementedError


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