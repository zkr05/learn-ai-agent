"""复习13（D06 的第 7 天复习，第 2 次重写） ｜ 三数之和 ｜ LeetCode 15 ｜ 中等

规则：不许打开 d06_three_sum.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天那次（10-19）你写出来了，但三段式只走到「前提」，去重的理由写成了「做法」。

目标：10 分钟内写完。

三个自述（第 2 次，要比 10-19 那轮更硬）：

  1) 三段式：`s < 0` 时为什么移 `j`（不移 `k`）？
     10-19 你写的是「nums 已排序，对任意 i 有 nums[i] <= nums[k]」—— 只到前提。
     这次要推到结论：写出「对任意 ___，都有 ___ < 0」-> 「所以 j 作废」。
     自述 1：此时如果移动k，对任意的v小于k，x + nums[j] + nums[v] < 0, 因为nums[v] <= nums[k]
     确认：**这次推到结论了** ✅ —— 「任意 v < k 都 < 0」这一句出来了，理由（nums[v] <= nums[k]）也对。
     只差最后一句收尾：「所以 j 这个位置作废 -> j += 1 是安全的」。
     （你这版是从「移 k 也没用」切入的，和标准写法「j 的搭档都不行」是同一件事的两面。）

  2) 去重 **3 处**，逐处说明**为什么需要**。
     10-19 你写的是「对比移动前后是否相同，相同去重」—— 那是**做法**，不是**理由**。
     自述 2：第一处，因为题目要求不重复的三元组，且该数已经全都比对过，所以推进时不受影响。
            第二处，如果不跳过，会出现j，j+1 与 k的重复三元组
            第三处，与二处类似，会出现k-1，k 与 j的重复三元组
     确认：三处都给了理由 ✅。第二/三处准确；第一处方向对但不够精确 ——
     准确的机制是：nums[i] == nums[i-1] 时，这一轮的范围 [i+1, n-1] 是上一轮 [i, n-1] 的**子集**
     -> 能找出的三元组上一轮已经全找过。「已经全都比对过」要补上「为什么」。

  3) 空间复杂度：算上 `nums.sort()` 是多少？为什么？
     自述 3：算是sort是nlogn，n是nums的长度，python中的sort会占用空间
     纠正（**答成了时间**）：O(n log n) 是排序的**时间**。问的是**空间**：
     Timsort 需要 O(n) 的临时数组 -> **总空间 O(n)**。
     （「会占用空间」这个直觉对，但要说出量级。）

状态：完成（2026-10-23 第 2 次独立重写成功）
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
                ans.append([x, nums[j], nums[k]])
                j +=1
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
