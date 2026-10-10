"""D03 最长连续序列（哈希）   LeetCode 128   Medium

思路：题目要求 O(n)，这一步直接排除了排序（排序是 O(n log n)）。
     先把数组丢进 set 拿到 O(1) 查找，再找「连续段的起点」—— 起点 = x-1 不在 set 里的数。
     从起点往后数到数不动为止。

复杂度：时间 O(n)   —— 外层 n 次 O(1) 判断 + while 的总迭代次数 ≤ n（均摊，不是每次 n 次）
        空间 O(n)   —— set 要存下所有数

状态：完成（卡点：没想到「while 只针对起点」）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def longest_consecutive(nums: list[int]) -> int:
    """最长连续整数序列的长度（不要求在原数组里相邻）。"""
    st = set(nums)
    ans = 0
    for x in st:
        if x - 1 in st:
            continue                   # 不是起点就跳过 —— 这一行是 O(n) 的保证
        y = x + 1
        while y in st:
            y += 1
        ans = max(ans, y - x)          # 半开区间 [x, y) 的长度，不用 +1
    return ans


if __name__ == "__main__":
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0              # 空数组：ans 初始值 0 恰好就是答案
    assert longest_consecutive([1]) == 1
    assert longest_consecutive([1, 2, 0, 1]) == 3    # 有重复值
    assert longest_consecutive([0, -1, 1]) == 3      # 有负数
    assert longest_consecutive([5, 5, 5, 5]) == 1
    print("✅ D03 通过")
