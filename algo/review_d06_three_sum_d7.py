"""复习13（D06 的第 7 天复习，第 2 次重写） ｜ 三数之和 ｜ LeetCode 15 ｜ 中等

规则：不许打开 d06_three_sum.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天那次（10-19）你写出来了，但三段式只走到「前提」，去重的理由写成了「做法」。

目标：10 分钟内写完。

三个自述（第 2 次，要比 10-19 那轮更硬）：

  1) 三段式：`s < 0` 时为什么移 `j`（不移 `k`）？
     10-19 你写的是「nums 已排序，对任意 i 有 nums[i] <= nums[k]」—— 只到前提。
     这次要推到结论：写出「对任意 ___，都有 ___ < 0」-> 「所以 j 作废」。
     自述 1：

  2) 去重 **3 处**，逐处说明**为什么需要**。
     10-19 你写的是「对比移动前后是否相同，相同去重」—— 那是**做法**，不是**理由**。
     自述 2：

  3) 空间复杂度：算上 `nums.sort()` 是多少？为什么？
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def three_sum(nums: list[int]) -> list[list[int]]:
    """返回所有和为 0 且不重复的三元组。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


def _norm(triples) -> list[tuple]:
    return sorted(tuple(sorted(t)) for t in triples)


if __name__ == "__main__":
    for nums, want in [
        ([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]]),
        ([0, 1, 1], []),
        ([0, 0, 0], [[0, 0, 0]]),
        ([0, 0, 0, 0], [[0, 0, 0]]),
        ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),
        ([], []),
        ([1, 2, 3], []),
        ([1, -1, -1, 0], [[-1, 0, 1]]),
    ]:
        got = three_sum(nums[:])
        assert _norm(got) == _norm(want), f"{nums} -> {got}，期望 {want}"
        assert len(got) == len({tuple(t) for t in got}), f"{nums} 返回了重复三元组: {got}"
    print("✅ 复习D06（第7天）通过 —— 第 2 次独立重写成功")
