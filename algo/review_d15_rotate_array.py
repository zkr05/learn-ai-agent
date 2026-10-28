"""复习24（D15 的第 3 天复习） ｜ 轮转数组 ｜ LeetCode 189 ｜ 中等

规则：不许打开 d15_rotate_array.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

两个自述（跑绿之后填）：

  1) 三次反转为什么等于「向右轮转 k 步」？
     用 A + B 的记号把三步写出来（注意用词：这三步都是**反转**，不是轮转）。
     自述 1：

  2) 空间复杂度是多少？为什么能满足题目的进阶要求？
     自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(nums: list[int], k: int) -> None:
    """把数组向右轮转 k 步（原地修改，不返回）。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


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
        ([1, 2], 3, [2, 1]),
        ([1, 2, 3], 0, [1, 2, 3]),
        ([1, 2, 3], 3, [1, 2, 3]),
        ([1, 2, 3, 4], 4, [1, 2, 3, 4]),
        ([1, 2, 3, 4, 5], 1, [5, 1, 2, 3, 4]),
    ]:
        got = src[:]
        assert rotate(got, k) is None, "题目要求原地修改、不返回"
        assert got == want, f"{src} k={k} -> {got}，期望 {want}"

    import random
    random.seed(97)
    for _ in range(2000):
        n = random.randint(1, 12)
        k = random.randint(0, 25)
        arr = [random.randint(-9, 9) for _ in range(n)]
        got = arr[:]
        rotate(got, k)
        assert got == _ref(arr[:], k), f"对拍失败: {arr} k={k}"
    print("✅ 复习D15 通过 —— 独立重写成功")
