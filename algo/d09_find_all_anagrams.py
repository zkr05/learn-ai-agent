"""D09 找到字符串中所有字母异位词（固定长度滑动窗口）   LeetCode 438   Medium   <- 滑动窗口最后一题

思路：这题是 D02（字母异位词）的滑窗版。
     和 D08 的区别：D08 是**变长**窗口（左边按需收缩）；
                   这题是**固定长度**窗口（= len(p)）—— 右进一个、左出一个、长度恒定。
                   这是滑窗的第二种形态，值得和 D08 对照着记。

     两件事让它做到 O(n)：
       1) **增量更新**：窗口右滑一格只改变两个字符的计数（进一个、出一个），O(1)。
          如果每次都重新 `Counter(s[left:right+1])` 就是 O(k) x n 个窗口 = O(nk)，
          那一步正是「重复扫描」—— 也就是这题要消灭的东西。
       2) **增量比较**：`cnt_p == cnt_s`。Counter 有自己的 `__eq__`，
          **计数为 0 的键视为不存在**（实测 `Counter(a=1) == Counter(a=1, b=0)` 为 True）。
          所以滑动后留下的 0 计数键不会让判断失败。
          ⚠️ 这个语义是 Python 3.10+ 才有的；换成普通 dict 比较，那些 0 键会让判断失败。

复杂度：时间 O(n)   —— 每步 O(1) 更新 + 比较 O(|字符集|)，|字符集| 是常数（小写字母 26）
        空间 O(|字符集|) —— 两个 Counter 的键数不超过字符集大小

状态：完成（卡在「左边的窗口要怎么缩短」；约 40 分钟）｜ 复习D3 待做
"""

import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def find_anagrams(s: str, p: str) -> list[int]:
    """返回 s 中所有「是 p 的异位词」的子串起始下标。"""
    cnt_p = Counter(p)
    cnt_s = Counter()
    ans = []

    for right, x in enumerate(s):
        cnt_s[x] += 1

        left = right - len(p) + 1
        if left < 0:
            continue

        if cnt_p == cnt_s:
            ans.append(left)
        cnt_s[s[left]] -= 1
    return ans


def _brute(s: str, p: str) -> list[int]:
    """暴力：逐个等长子串排序后比较。只用来对拍。"""
    k, target = len(p), sorted(p)
    return [i for i in range(len(s) - k + 1) if sorted(s[i:i + k]) == target]


if __name__ == "__main__":
    for s, p, want in [
        ("cbaebabacd", "abc", [0, 6]),
        ("abab", "ab", [0, 1, 2]),
        ("a", "a", [0]),
        ("a", "ab", []),           # p 比 s 还长
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
    for _ in range(3000):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 14)))
        p = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
        assert find_anagrams(s, p) == _brute(s, p), f"对拍失败: {s!r} {p!r}"
    print("✅ D09 通过")
