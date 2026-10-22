"""复习12（D09 的第 3 天复习） ｜ 找到字符串中所有字母异位词 ｜ LeetCode 438 ｜ 中等

规则：不许打开 d09_find_all_anagrams.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

两个自述（跑绿之后填 —— D09 当天这几个问题没答，这次补上）：

  1) 三段式：窗口右边界进一格后，为什么左边**只能移出一个**字符？
     移 0 个会怎样？移 2 个又会怎样？
     （提示：这题和 D08 的区别是"长度固定"，把长度算清楚就出来了。）
     自述 1：题目要求对比异位词，则要求固定长度，所以是定长滑窗，右边界进一，左边也只能移一，
     如果移0，则if 判断异位词永远无法成立，
     补全（主体对，但**只答了"移 0"，漏了"移 2"**；而且"移 0"的结论要精确一点）：
       移 0 个：窗口长度一路增长（3 -> 4 -> 5 ...）-> 计数总和 > len(p) -> 之后永远不相等。
                严格说**第一个窗口仍会命中**（那时还没移过），之后才永远不等。
       移 2 个：窗口长度变成 len(p)-1（3 -> 2）-> 计数总和 < len(p) -> 同样永远不相等。
                结果一样：只有第一个窗口能命中，之后全漏。
       实测（s="cbaebabacd", p="abc"）：
         移 1 个 -> [0, 6] ✅    移 0 个 -> [0]    移 2 个 -> [0]
       所以「只能移一个」的理由是：**长度必须恰好 = len(p)**，多一个少一个都不是候选。

  2) `cnt_p == cnt_s` 这一行依赖 `Counter` 的什么语义？
     如果换成普通 dict 比较，会出什么问题？
     自述 2：依赖的是Counter对比时候会忽略0的情况，如果用普通的dict，左边缩进后value变为0，
     普通dict比较，会出错。
     确认：**完全正确** ✅ —— Counter 的 `__eq__` 把 0 计数的键视为不存在；
           普通 dict 会把那些 0 键也拿去比较，于是窗口其实匹配了也判成不等。

状态：完成（2026-10-21 独立重写成功）
"""

from collections import Counter
import sys

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
        if cnt_s == cnt_p:
            ans.append(left)
        
        cnt_s[s[left]] -= 1
    return ans

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
    print("✅ 复习D09 通过 —— 独立重写成功")
