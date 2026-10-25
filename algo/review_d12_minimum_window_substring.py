"""复习18（D12 的第 3 天复习） ｜ 最小覆盖子串 ｜ LeetCode 76 ｜ 困难

规则：不许打开 d12_minimum_window_substring.py，也不许翻 notes.md。凭记忆独立写。

目标：15 分钟内写完（Hard）。

两个自述（跑绿之后填）：

  1) 两个优化分别消灭了什么？
     ① diff 单字典相对计数 ／ ② ge_cnt + kinds 计数器。
     自述 1：

  2) 为什么左边界可以一直缩？要写成「对任意 ___，都 ___」（排除论证）。
     自述 2：

状态：待做
"""

import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def min_window(s: str, t: str) -> str:
    """返回 s 里最短的、包含 t 所有字符（含重复次数）的子串；没有则返回 ""。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


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
