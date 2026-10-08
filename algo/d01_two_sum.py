"""D01 两数之和（数组 / 哈希）   LeetCode 1

读题注意：题目保证「每种输入只会对应一个答案」「同一元素不能重复使用」，
        所以只要返回一对下标，不用处理多解。

思路（暴力解）：双重循环枚举所有下标对 (i, j)，i < j，检查 nums[i] + nums[j] == target。

复杂度：
  暴力解：时间 O(n^2) —— 两层循环，最坏比较 n(n-1)/2 次 ／ 空间 O(1)
  优化版：时间 O(n)   —— 外层 n 次，字典查找与插入都是 O(1) ／ 空间 O(n)（用空间换时间）

状态：完成（暴力解 + 优化版都通过）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def two_sum(nums: list[int], target: int) -> list[int]:
    """返回和为 target 的两个数的下标。"""
    for i in range(len(nums)):
        for j in range(i+1,len(nums)):
            if nums[i] + nums[j] == target:
                return [i,j]



# --- 优化尝试（失败，保留作记录）-----------------------------------------
# 想法：先算出"需要和谁配对"（target - nums[i]），再看它在不在后面。方向是对的，
#       但查找用了 in 和 .index() —— 它们作用在 list 上就是线性扫描，还额外复制了切片。
#       结果：复杂度仍是 O(n^2)，实际比暴力解还慢。
# 结论：要用"查找 O(1)"的容器替换 list，具体看题解。
def two_sum_attempt(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        res = target - nums[i]
        if res in nums[i+1:]:
            return [i, nums[i+1:].index(res) + i + 1]
    return []


# --- 优化版（哈希表）------------------------------------------------------
# 思路：一边遍历一边查 —— 用字典记住「见过的值 -> 它的下标」。
#       查 target - x 在不在字典里是 O(1)，插入 idx[x] = j 也是 O(1)，
#       外层只走 n 次 => 整体 O(n)。
# 关键：必须先查、再存（idx[x] = j 放在 if 后面）。
#       反过来的话 [3, 3] 会返回 [0, 0] —— 同一个元素被用了两次，违反题目约束。
def two_sum_v2(nums: list[int], target: int) -> list[int]:
    idx = {}
    for j, x in enumerate(nums):
        if target - x in idx:
            return [idx[target - x], j]
        idx[x] = j
    return []


if __name__ == "__main__":
    # 本地自测（LeetCode 用自己的判题，这里是为了你自己跑）
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    assert two_sum_attempt([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum_attempt([3, 3], 6) == [0, 1]
    assert two_sum_v2([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum_v2([3, 2, 4], 6) == [1, 2]
    assert two_sum_v2([3, 3], 6) == [0, 1]      # 陷阱用例
    print("✅ D01 全部通过：暴力解 / 失败尝试 / 优化版")
    

# --- 附：笔试是 ACM 模式时要自己读输入 -----------------------------------
# import sys
# def main():
#     data = sys.stdin.read().split()      # 一次读完
#     ...
#     print(ans)
# if __name__ == "__main__":
#     main()
