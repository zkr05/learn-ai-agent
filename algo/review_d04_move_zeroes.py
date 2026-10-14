"""复习1（D04 的第 3 天复习） ｜ 移动零 ｜ LeetCode 283 ｜ 简单

规则：不许打开 d04_move_zeroes.py，也不许翻 notes.md。凭记忆独立写。

目标：5 分钟内写完。

证明三段式（跑绿之后填 —— 这是新加的固定动作）：
  1) 瓶颈：当前状态下，是哪一边/哪个位置限制了结果？
  2) 排除：为什么丢掉它不会漏掉答案？（关键那一句）
  3) 结论

自述 1（瓶颈）：nums[start0]
自述 2（排除）：每次nums[start0]都是指向0元素，遇到非0的时候，会将0与nums[i]交换，并推进start0
自述 3（结论）：所以每轮可以放心交换推进start0

状态：完成（2026-10-14 独立重写成功，6 条断言一次通过）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def move_zeroes(nums: list[int]) -> None:
    """把 0 全部移到末尾，非零元素保持原相对顺序 —— 原地修改，不返回。"""
    start0 = 0
    for i in range(len(nums)):
        if nums[i]:
            nums[start0], nums[i] = nums[i], nums[start0]
            start0 += 1



if __name__ == "__main__":
    cases = [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([0, 1], [1, 0]),                 # ← 只赋值不交换的话，这里会变成 [1, 1]
        ([1, 0], [1, 0]),
        ([], []),
        ([-1, 0, 2], [-1, 2, 0]),
        ([0, 0, 1], [1, 0, 0]),
    ]
    for src, want in cases:
        got = src[:]
        assert move_zeroes(got) is None, "题目要求原地修改、不返回"
        assert got == want, f"{src} -> {got}，期望 {want}"
    print("✅ 复习D04 通过 —— 独立重写成功")
