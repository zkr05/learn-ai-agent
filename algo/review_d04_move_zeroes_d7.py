"""复习15（D04 的第 7 天复习，第 2 次重写） ｜ 移动零 ｜ LeetCode 283 ｜ 简单

规则：不许打开 d04_move_zeroes.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天（10-14）你写出来了，但三段式的「排除」第一次只写到观察（"是 0"），
     没写到机制（"那个 0 的去处"）。

目标：5 分钟内写完。

证明三段式（第 2 次，要写到机制）：
  1) 瓶颈：nums[start0] —— 每轮"覆盖写"的那个位置（被覆盖的值会被销毁）
  2) 排除：为什么丢掉它不会漏答案？（要写清"那个被覆盖的 0 去哪了"），那个被覆盖的0不是消失了，而是每次nums[i]和nums[start0]
  交换了位置，并且start0推进
     ✅ 这次写到机制了 —— 关键是「那个 0 不是消失了，而是交换到了 nums[i]」。
     这就是 10-14 那次缺的那半句（当时只写到观察"是 0"）。
  3) 结论：所以 **0 的个数守恒** -> 每轮交换并推进 start0 都是安全的。

状态：完成（2026-10-24 第 2 次独立重写成功；逾期 6 天补做）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def move_zeroes(nums: list[int]) -> None:
    """把 0 全部移到末尾，非零元素保持原相对顺序 —— 原地修改，不返回。"""
    start0 = 0
    n = len(nums)
    for i in range(n):
        if nums[i]:
            nums[start0],nums[i] = nums[i],nums[start0]
            start0 += 1
        


if __name__ == "__main__":
    for src, want in [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0, 1], [1, 0]),                 # <- 只赋值不交换的话，这里会变成 [1, 1]
        ([1, 0], [1, 0]),
        ([], []),
        ([-1, 0, 2], [-1, 2, 0]),
        ([0, 0, 1], [1, 0, 0]),
    ]:
        got = src[:]
        assert move_zeroes(got) is None, "题目要求原地修改、不返回"
        assert got == want, f"{src} -> {got}，期望 {want}"
    print("✅ 复习D04（第7天）通过 —— 第 2 次独立重写成功")
