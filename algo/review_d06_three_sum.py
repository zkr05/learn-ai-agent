"""复习8（D06 的第 3 天复习） ｜ 三数之和 ｜ LeetCode 15 ｜ 中等

规则：不许打开 d06_three_sum.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完（这题细节多，比前几题给的时间长）。

三个自述（跑绿之后填 —— 前两个是 D06 当天没答好的）：

  1) 三段式：`s < 0` 时为什么移 `j`、不移 `k`？
     必须写成「对任意 ___，都有 ___」的形式 —— 不要只写「因为 k 已经最大了，要让它变大」。
     自述 1：

  2) 去重一共**几处**？把数量数出来，并逐处说明为什么需要。
     （D06 当天问你「几处」时没数出来。）
     自述 2：

  3) 空间复杂度是 O(1) 还是 O(n)？为什么？（提示：`nums.sort()` 的开销算不算？）
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
        ([0, 0, 0, 0], [[0, 0, 0]]),        # <- 去重必须彻底，否则这里会返回多组
        ([-2, 0, 0, 2, 2], [[-2, 0, 2]]),
        ([], []),
        ([1, 2, 3], []),
        ([1, -1, -1, 0], [[-1, 0, 1]]),
    ]:
        got = three_sum(nums[:])
        assert _norm(got) == _norm(want), f"{nums} -> {got}，期望 {want}"
        assert len(got) == len({tuple(t) for t in got}), f"{nums} 返回了重复三元组: {got}"
    print("✅ 复习D06 通过 —— 独立重写成功")
