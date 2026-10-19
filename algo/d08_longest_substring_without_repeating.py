"""D08 无重复字符的最长子串（滑动窗口）   LeetCode 3   Medium   <- 滑动窗口第 1 题

思路：滑动窗口 = 一个会伸缩的**区间** + 一个记录「区间里有什么」的**哈希**。
     这题就是把两块旧零件拼起来：D02（哈希记见过什么）+ D04/D05/D07（双指针维护区间）。
       right 逐个吃字符 -> 计数 +1
       窗口里出现重复（cnt[x] > 1）就把 left 往右推，直到 x 只剩一个
       每步用 [left, right] 的长度更新答案

     为什么 left 可以一次推好几格（排除论证）：
       设 x 上一次出现在 pos（left <= pos < right）。那么对**任意** left' <= pos，
       窗口 [left', right] 都同时包含 pos 和 right 两个 x —— **不合法**。
       而我们要的是「以 right 结尾的最长**合法**子串」：
       那些更小的 left' 虽然更长，但**全都不合法**，所以丢掉它们不会漏掉任何合法解。
       => left 直接跳到 pos + 1（代码里就是 while 一直推到 cnt[x] == 1）。
       注意这题的排除理由是「**根本不合法**」，不是 D05 那种「**不可能更优**」。

     ⚠️ 必须 while，不能用 if 只缩一次：
       一轮只加一个字符，但**要把重复的 x 降到一个，可能得移掉多个字符**
       （上一个 x 不在 left 处时，中间还隔着别的字符）。
       实测 if 版本在 "abba" 上返回 3（正确 2）；5000 组随机输入错 2374 组。
       判据：**一轮里可能需要多次收缩吗？** 需要就必须 while。

复杂度：时间 O(n)   —— right 前进 n 次；left 只增不减、总共最多前进 n 次 -> 2n = O(n)
        空间 O(min(n, |字符集|)) —— 计数器最多存 min(串长, 字符集大小) 个键

状态：完成（卡点在「怎么移动窗口左边」；约 30 分钟）｜ 复习D3 待做
"""

import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def length_of_longest_substring(s: str) -> int:
    """不含重复字符的最长子串长度（子串 = 连续）。"""
    ans = left = 0
    cnt = defaultdict(int)
    for right, x in enumerate(s):
        cnt[x] += 1
        while cnt[x] > 1:
            cnt[s[left]] -= 1
            left += 1
        ans = max(ans, right - left + 1)
    return ans


def _brute(s: str) -> int:
    """暴力：枚举所有子串、逐个检查有没有重复。只用来对拍。"""
    best = 0
    for i in range(len(s)):
        seen = set()
        for j in range(i, len(s)):
            if s[j] in seen:
                break
            seen.add(s[j])
            best = max(best, j - i + 1)
    return best


if __name__ == "__main__":
    for s, want in [
        ("abcabcbb", 3),
        ("bbbbb", 1),
        ("pwwkew", 3),
        ("", 0),
        (" ", 1),
        ("dvdf", 3),
        ("abba", 2),        # <- 这题最容易错的一个：while 必须是 while
        ("tmmzuxt", 5),
        ("au", 2),
        ("aab", 2),
    ]:
        got = length_of_longest_substring(s)
        assert got == want, f"{s!r} -> {got}，期望 {want}"

    import random
    random.seed(13)
    for _ in range(3000):
        s = "".join(random.choice("abcd") for _ in range(random.randint(0, 12)))
        assert length_of_longest_substring(s) == _brute(s), f"对拍失败: {s!r}"
    print("✅ D08 通过")
