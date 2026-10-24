"""复习15（D04 的第 7 天复习，第 2 次重写） ｜ 移动零 ｜ LeetCode 283 ｜ 简单

规则：不许打开 d04_move_zeroes.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天（10-14）你写出来了，但三段式的「排除」第一次只写到观察（"是 0"），
     没写到机制（"那个 0 的去处"）。

目标：5 分钟内写完。

证明三段式（第 2 次，要写到机制）：
  1) 瓶颈：
  2) 排除：为什么丢掉它不会漏答案？（要写清"那个被覆盖的 0 去哪了"）
  3) 结论：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def move_zeroes(nums: list[int]) -> None:
    """把 0 全部移到末尾，非零元素保持原相对顺序 —— 原地修改，不返回。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


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
