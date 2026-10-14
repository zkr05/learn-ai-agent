"""D06 三数之和（排序 + 双指针）   LeetCode 15   Medium

思路：这题不是新知识，是两块旧东西的**组合** ——
       降维（把「找三个」变成「固定一个 + 找两个」）+ 有序数组的双指针（D05 刚练过）。
     步骤：排序 -> 固定 nums[i] -> 在 [i+1, n-1] 里用左右指针找另外两个。

     三个容易漏的细节（本题一半的工作量在这里）：

     【去重 3 处】
       1) i 去重：`if i > 0 and x == nums[i-1]: continue` —— 同一个 x 会找出同一批三元组
       2) 3) 找到答案后，j 和 k 各自跳过重复值（那两个 while）
          实测：去掉这两个 while，3000 组随机输入里 841 组返回**重复**三元组
          （例 [-2,0,0,2,2] 会返回两个 [-2,0,2]）
          注：`j += 1` 在 while 之前，作用是**保证指针至少前进一格**（防御性，不是正确性必需 ——
              实测去掉它 3000 组 0 差异；但依赖「此刻 nums[j] != nums[j-1] 必然成立」这种
              微妙不变量比多写一行危险）

     【剪枝 2 处，一个能 break 一个只能 continue —— 判据是单调性方向】
       1) `x + nums[i+1] + nums[i+2] > 0` -> break
          最小的三个都 > 0 了；i 往右 x 只会更大 -> 后面全都不可能 -> 整个循环可以退出
       2) `x + nums[-1] + nums[-2] < 0` -> continue
          只是**这个** x 凑不到 0；i 往右 x 变大，还可能凑到 -> 所以不能 break

复杂度：时间 O(n^2)   —— 排序 O(n log n) + n 次双指针（每次 O(n)）-> 取 O(n^2)
        空间 O(1)~O(n) —— 算法本身只用几个下标；但 Python 的 sort（Timsort）需要 O(n) 临时数组。
                          说 O(1) 时要么说明「不算排序」，要么说清这个不确定性从哪来。

状态：完成（看题解才会，自己只想到 O(n^3)；约 30 分钟）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def three_sum(nums: list[int]) -> list[list[int]]:
    """返回所有和为 0 且不重复的三元组。"""
    nums.sort()
    ans = []
    n = len(nums)
    for i in range(n - 2):
        x = nums[i]
        if i > 0 and x == nums[i - 1]:          # 去重 1：跳过重复的固定数
            continue
        if x + nums[i + 1] + nums[i + 2] > 0:   # 剪枝 1：最小的三个都 > 0 -> 后面都不可能
            break
        if x + nums[-1] + nums[-2] < 0:         # 剪枝 2：只是这个 x 凑不到 -> 后面还有可能
            continue
        j, k = i + 1, n - 1
        while j < k:
            s = x + nums[j] + nums[k]
            if s < 0:
                j += 1
            elif s > 0:
                k -= 1
            else:
                ans.append([x, nums[j], nums[k]])
                j += 1
                while j < k and nums[j] == nums[j - 1]:   # 去重 2
                    j += 1
                k -= 1
                while k > j and nums[k] == nums[k + 1]:   # 去重 3
                    k -= 1
    return ans


def _brute(nums: list[int]) -> list[tuple]:
    """暴力解（组合 + 去重）—— 只用来对拍。"""
    import itertools
    return sorted({c for c in itertools.combinations(sorted(nums), 3) if sum(c) == 0})


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
        ([-1, 0, 1], [[-1, 0, 1]]),
        ([1, -1, -1, 0], [[-1, 0, 1]]),
        ([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],
         [[-4, -2, 6], [-4, 0, 4], [-4, 1, 3], [-4, 2, 2], [-2, -2, 4], [-2, 0, 2]]),
    ]:
        got = three_sum(nums[:])
        assert _norm(got) == _norm(want), f"{nums} -> {got}，期望 {want}"
        # 结果里不许有重复的三元组
        assert len(got) == len({tuple(t) for t in got}), f"{nums} 返回了重复三元组: {got}"

    # 对拍：400 组随机输入必须和暴力解完全一致
    import random
    random.seed(11)
    for _ in range(400):
        nums = [random.randint(-6, 6) for _ in range(random.randint(0, 12))]
        assert _norm(three_sum(nums[:])) == _brute(nums), f"对拍失败: {nums}"
    print("✅ D06 通过")
