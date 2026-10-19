"""复习8（D06 的第 3 天复习） ｜ 三数之和 ｜ LeetCode 15 ｜ 中等

规则：不许打开 d06_three_sum.py，也不许翻 notes.md。凭记忆独立写。

目标：10 分钟内写完（这题细节多，比前几题给的时间长）。

三个自述（跑绿之后填 —— 前两个是 D06 当天没答好的）：

  1) 三段式：`s < 0` 时为什么移 `j`、不移 `k`？
     必须写成「对任意 ___，都有 ___」的形式 —— 不要只写「因为 k 已经最大了，要让它变大」。
     自述 1：因为此时的nums已经排完序，对任何的i，都有nums[i] <= nums[k]
     补全（**前提对了，但只走到一半**。缺的是推理链，而且量词放错了对象）：
       固定 x 和 k。若 x + nums[j] + nums[k] < 0，则对**任意 k'（j < k' < k）**：
         nums[k'] <= nums[k]                          （数组有序）
         => x + nums[j] + nums[k'] <= x + nums[j] + nums[k] < 0
       即：保持 j 不动、任何更小的右指针都凑不出 0
       -> **j 这个位置彻底作废** -> 可以丢（j += 1）。
       注意：量词要放在「任意 k'」上，不是「任意 i」—— 要排除的是**每一个右指针**。

  2) 去重一共**几处**？把数量数出来，并逐处说明为什么需要。
     （D06 当天问你「几处」时没数出来。）
     自述 2：if > 0 and x == nums[i-1] 第一处，此时nums[i] 也可以和后面的数组成和为0。
     j 和 k 移动之后对比移动前后是否相同，相同去重
     补全（**数量对了：3 处**；但两处理由都不准 —— 写的是"做法"，不是"为什么需要"）：
       处1  i 去重：nums[i] == nums[i-1] 时，这一轮的可选范围 [i+1, n-1] 是上一轮 [i, n-1] 的
                    **子集** -> 能找出的三元组上一轮**已经全找过了** -> 跳过不会漏。
       处2  j 去重：找到答案后若 nums[j+1] == nums[j]，(j+1, k) 会产生**同一个值的三元组**
                    -> 必须跳过。
       处3  k 去重：同理，(j, k-1) 与 (j, k) 值相同 -> 必须跳过。

  3) 空间复杂度是 O(1) 还是 O(n)？为什么？（提示：`nums.sort()` 的开销算不算？）
     自述 3：空间复杂度是O(1)，数组是临时O(n).
     确认：概念到位 —— 这次你**看到了 sort 的临时数组**（10-14 那天漏掉了）。结论要写明确：
           **算上 sort，总空间是 O(n)**；只有说「不计排序」时才是 O(1)。

状态：完成（2026-10-19 独立重写成功，比原定的 10-20 提前一天）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def three_sum(nums: list[int]) -> list[list[int]]:
    """返回所有和为 0 且不重复的三元组。"""
    nums.sort()
    ans = []
    n = len(nums)
    for i in range(n-2):
        x = nums[i]
        if i > 0 and x == nums[i-1]:
            continue
        if x + nums[i+1] + nums[i+2] > 0:
            break
        if x + nums[-2] + nums[-1] < 0:
            continue
        j = i + 1
        k = n - 1
        while j < k:
            s = x + nums[j] + nums[k]
            if s < 0:
                j += 1
            elif s > 0:
                k -= 1
            else:
                ans.append([x,nums[j],nums[k]])
                j += 1
                while j < k and nums[j] == nums[j-1]:
                    j += 1
                k -= 1
                while k > j and nums[k] == nums[k+1]:
                    k -= 1
    return ans

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
