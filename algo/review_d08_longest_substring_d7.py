"""复习19（D08 的第 7 天复习，第 2 次重写） ｜ 无重复字符的最长子串 ｜ LeetCode 3 ｜ 中等

规则：不许打开 d08_longest_substring_without_repeating.py，也不许翻 notes.md。
     第 3 天（10-21）你两处都没到位：自述 1 写成了"循环在干什么"，自述 2 没说判据。

目标：8 分钟内写完。

两个自述（第 2 次，这次都要写成"对任意/判据"）：

  1) 窗口里出现重复时，为什么 left 可以**一次推好几格**？
     必须写成「对任意 left' <= pos，窗口都 ___」的形式。
     自述 1：
     （这次没填。参考版：设 x 上次出现在 pos。对**任意** left' <= pos，
      窗口 [left', right] 都**同时包含两个 x** -> 不合法 -> 全部作废 -> left 可以跳到 pos+1。）

  2) `while` 能不能换 `if`？判据一句话 + 一个会出错的字符串。
     自述 2：
     （这次没填。参考版：判据 = 一轮里可能需要**多次**收缩吗？需要就 while。
      反例 "abba"：加第三个字符后窗口是 "abb"，上一个 b 在下标 1、left 在下标 0，
      中间隔着 a -> 要移两次。）

状态：完成（2026-10-26 第 2 次独立重写成功；自述未填）
"""

from collections import defaultdict
import sys

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
        ("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("", 0), (" ", 1),
        ("dvdf", 3), ("abba", 2), ("tmmzuxt", 5), ("au", 2), ("aab", 2),
    ]:
        got = length_of_longest_substring(s)
        assert got == want, f"{s!r} -> {got}，期望 {want}"

    import random
    random.seed(13)
    for _ in range(2000):
        s = "".join(random.choice("abcd") for _ in range(random.randint(0, 12)))
        assert length_of_longest_substring(s) == _brute(s), f"对拍失败: {s!r}"
    print("✅ 复习D08（第7天）通过 —— 第 2 次独立重写成功")
