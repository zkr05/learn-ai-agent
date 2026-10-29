"""复习26（D12 的第 7 天复习，第 2 次重写） ｜ 最小覆盖子串 ｜ LeetCode 76 ｜ 困难

规则：不许打开 d12_minimum_window_substring.py，也不许翻 notes.md。
     第 3 天（10-25）两处都没到位：自述 1 讲的是机制不是「消灭了什么」，
     自述 2 写成了代码流程，不是排除论证。

目标：15 分钟内写完。

两个自述（第 2 次）：

  1) 两个优化**分别消灭了什么代价**？（不是"怎么做的"，是"省掉了什么"）
     自述 1：一个diff字典做相对计数，不用两个Counter比较，每次一个字符只做diff[c] += 1
     判断够不够变成一次 == 0 -> O(1)

     ge_cnt  + kins:把是否覆盖从整个dict遍历变成比较两个整数 O(1).
     ✅ **这次答对了「消灭了什么」**（10-25 只讲了机制）：
       ① 不用比较两个 Counter（省掉 O(|Σ|)）② 不用遍历整个 dict（省掉 O(|Σ|)）。
  2) 左边界为什么可以一直缩？写成「对任意 left' <= left，都 ___」。
     自述 2：当前窗口[left,right] 已经覆盖t，考虑任何right结尾，left' <= left的窗口，都不短于当前
     窗口，就算合法也不会更优。停止的时候是当收缩连合法都不是了。
     ✅ **这次写成排除论证了**（10-25 写成了代码流程），量词「任何 right 结尾、left' <= left」也有了。
     （排除类型：**不可能更优**，不是不合法。）

状态：完成（2026-10-29 第 2 次独立重写成功）
"""

import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def min_window(s: str, t: str) -> str:
    """返回 s 里最短的、包含 t 所有字符（含重复次数）的子串；没有则返回 ""。"""
    diff = defaultdict(int)
    for c in t:
        diff[c] -= 1
    kinds = len(diff)

    ans_left,ans_right = -1,len(s)
    ge_cnt = 0
    left = 0

    for right,c in enumerate(s):
        diff[c] += 1
        if diff[c] == 0:
            ge_cnt += 1

        while ge_cnt == kinds:
            if right - left < ans_right - ans_left:
                ans_left,ans_right = left,right

            x = s[left]
            if diff[x] == 0:
                ge_cnt -= 1
            diff[x] -= 1
            left += 1
    return ""if ans_left < 0 else s[ans_left:ans_right+1]

def _brute(s: str, t: str) -> str:
    from collections import Counter
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            w = s[i:j + 1]
            cw = Counter(w)
            if all(cw[ch] >= need[ch] for ch in need):
                if not best or len(w) < len(best):
                    best = w
                break
    return best


if __name__ == "__main__":
    for s, t, want in [
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("a", "a", "a"),
        ("a", "aa", ""),
        ("", "a", ""),
        ("ab", "b", "b"),
        ("aa", "aa", "aa"),
        ("bba", "ab", "ba"),
        ("cabwefgewcwaefgcf", "cae", "cwae"),
        ("aaflslflsldkalskaaa", "aaa", "aaa"),
    ]:
        got = min_window(s, t)
        assert got == want, f"s={s!r} t={t!r} -> {got!r}，期望 {want!r}"

    import random
    random.seed(53)
    for _ in range(2000):
        s = "".join(random.choice("abc") for _ in range(random.randint(0, 13)))
        t = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
        assert min_window(s, t) == _brute(s, t), f"对拍失败: {s!r} {t!r}"
    print("✅ 复习D12（第7天）通过 —— 第 2 次独立重写成功")
