"""复习11（D08 的第 3 天复习） ｜ 无重复字符的最长子串 ｜ LeetCode 3 ｜ 中等

规则：不许打开 d08_longest_substring_without_repeating.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

两个自述（跑绿之后填）：

  1) 三段式：窗口里出现重复时，为什么 `left` 可以**一次推好几格**？
     要写成「对任意 ___，窗口都 ___」的形式。
     自述 1：

  2) `while` 能不能换成 `if`？判据是什么？（用一句话说清，并举一个会出错的字符串）
     自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def length_of_longest_substring(s: str) -> int:
    """不含重复字符的最长子串长度（子串 = 连续）。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


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
    print("✅ 复习D08 通过 —— 独立重写成功")
