"""复习18（D12 的第 3 天复习） ｜ 最小覆盖子串 ｜ LeetCode 76 ｜ 困难

规则：不许打开 d12_minimum_window_substring.py，也不许翻 notes.md。凭记忆独立写。

目标：15 分钟内写完（Hard）。

两个自述（跑绿之后填）：

  1) 两个优化分别消灭了什么？
     ① diff 单字典相对计数 ／ ② ge_cnt + kinds 计数器。
     自述 1：每次字符都做一次diff += 1，
     ge_cnt的优化是每当一个字母的出现次数与t相同了再 + 1，就是diff[x] == 0,出的时候只有恰好是0变为-1，再减
     这种结果答案不会漏掉。
    确认：机制描述对 ✅（尤其临界点 -1->0 / 0->-1）。但问题问的是「**消灭了什么**」：
      ① `diff` 相对计数：消灭「比较两个 Counter」的 O(|Σ|)，变成一次加法和一次 `== 0`
      ② `ge_cnt` + `kinds`：消灭「遍历整个 dict 判断覆盖」的 O(|Σ|)，变成比较两个整数

  2) 为什么左边界可以一直缩？要写成「对任意 ___，都 ___」（排除论证）。
     自述 2：首先先拿出来左边界的字母，查看是否这个字母在diff里是0，如果是0，则说明当他缩的时候，ge_cnt就不等kinds了，
     记录下之后缩，所以每次缩的时候都有比对的。
    纠正（**这是代码流程，不是排除论证**）：
      你写的是「拿 s[left]、看 diff 是否为 0、缩、ge_cnt 变化」—— 这是循环怎么走。
      问题是「为什么可以缩、缩了不会漏」。正确写法：
      对**任意**以 right 结尾、左边界 left' <= left 的窗口：它都**不短于**当前窗口
      -> 就算合法也不会更优 -> 可以全部丢弃。（排除类型：不可能更优，不是不合法。）

状态：完成（2026-10-25 独立重写成功）
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
    ge_cnt = 0
    ans_left, ans_right = -1 ,len(s)
    left = 0
    for right, x in enumerate(s):
        diff[x] += 1
        if diff[x] == 0:
            ge_cnt += 1
        while ge_cnt == kinds:
            if right - left < ans_right - ans_left:
                ans_left, ans_right = left, right
            c = s[left]
            if diff[c] == 0:
                ge_cnt -= 1
            diff[c] -= 1
            left += 1
    return ""if ans_left < 0 else  s[ans_left: ans_right + 1]

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
    print("✅ 复习D12 通过 —— 独立重写成功")
