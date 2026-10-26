"""复习21（D09 的第 7 天复习，第 2 次重写） ｜ 找到字符串中所有字母异位词 ｜ LeetCode 438 ｜ 中等

规则：不许打开 d09_find_all_anagrams.py，也不许翻 notes.md。
     第 3 天（10-21）自述 1 只答了「移 0」，漏了「移 2」；这次两个都要。

目标：8 分钟内写完。

两个自述（第 2 次）：

  1) 固定长度窗口：右边界进一格后，左边为什么**只能移出一个**？
     移 0 个会怎样？移 2 个又会怎样？（两个都要答）
     自述 1：

  2) `cnt_p == cnt_s` 依赖 `Counter` 的什么语义？换成普通 dict 会出什么问题？
     自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_anagrams(s: str, p: str) -> list[int]:
    """返回 s 中所有「是 p 的异位词」的子串起始下标。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


def _brute(s: str, p: str) -> list[int]:
    k, target = len(p), sorted(p)
    return [i for i in range(len(s) - k + 1) if sorted(s[i:i + k]) == target]


if __name__ == "__main__":
    for s, p, want in [
        ("cbaebabacd", "abc", [0, 6]),
        ("abab", "ab", [0, 1, 2]),
        ("a", "a", [0]),
        ("a", "ab", []),
        ("", "a", []),
        ("aa", "aa", [0]),
        ("baa", "aa", [1]),
        ("abc", "cba", [0]),
        ("abaab", "ab", [0, 1, 3]),
    ]:
        got = find_anagrams(s, p)
        assert got == want, f"s={s!r} p={p!r} -> {got}，期望 {want}"

    import random
    random.seed(23)
    for _ in range(2000):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 14)))
        p = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
        assert find_anagrams(s, p) == _brute(s, p), f"对拍失败: {s!r} {p!r}"
    print("✅ 复习D09（第7天）通过 —— 第 2 次独立重写成功")
