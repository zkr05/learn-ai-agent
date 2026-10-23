"""D12 最小覆盖子串（变长滑窗 + 两个计数器）   LeetCode 76   Hard   <- 子串小节最后一题

思路：变长滑窗的顶配版。右边界扩张直到「覆盖 t」，再收缩左边界直到「不再覆盖」，
     过程中记录最短。骨架和 D08 一样，区别只是「满足条件」变复杂了。

     两个优化 —— 都是「把重新计算换成增量维护」（和 D09 同一个思想）：

     ① 一个 diff 字典做「相对计数」，不用两个 Counter 比：
          diff[c] <  0  -> 窗口里还差 |diff[c]| 个 c
          diff[c] == 0  -> 刚好够
          diff[c] >  0  -> 多了
        每来一个字符只做 diff[c] += 1；判断「这个字符够不够」变成一次 == 0 -> O(1)。

     ② ge_cnt（已满足的字符种类数）+ kinds（t 里不同字符数）：
        把「整体是否覆盖」从「遍历整个 dict」（O(|Σ|)）变成「比较两个整数」（O(1)）。
        注意临界点：只有 diff[c] 从 -1 变 0 的那一瞬间才 ge_cnt += 1（刚够）；
                     收缩时只有 diff[x] 从 0 变 -1 的那一瞬间才 ge_cnt -= 1（不再够）。
        如果写成 diff[c] > 0 就 +1，那同一个字符每多来一个就会重复累加 —— 错。

     为什么左边界可以一直缩（排除论证）：
       当前窗口 [left, right] 已经覆盖 t。考虑**任何**以 right 结尾、左边界 left' <= left 的窗口：
       它都**不短于**当前窗口 -> 就算合法也不会更优。
       而我们要的是「最短」-> 这些更长的候选全部可以丢弃 -> left 可以往右走。
       排除类型：**不可能更优**（和 D05/D07 同类），不是「不合法」。

     收缩的停止条件：ge_cnt < kinds（某个字符不再够）—— 再缩连合法都不是了。

复杂度：时间 O(|s| + |t|) —— right 走 n 次、left 至多走 n 次，每次判断 O(1)
        空间 O(|Σ|) —— diff 的键数不超过 t 的字符种类

状态：完成（卡点：卡在「怎么优化掉每次都判断是否覆盖」；约 40 分钟）｜ 复习D3 待做
"""

import sys
from collections import defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def min_window(s: str, t: str) -> str:
    """返回 s 里最短的、包含 t 所有字符（含重复次数）的子串；没有则返回 ""。"""
    diff = defaultdict(int)
    for c in t:
        diff[c] -= 1                 # 还差几个
    kinds = len(diff)                # t 里有多少种字符

    ans_left, ans_right = -1, len(s)  # 哨兵：初始长度 = len(s)+1
    ge_cnt = 0                        # 已经"够了"的字符种类数
    left = 0

    for right, c in enumerate(s):
        diff[c] += 1
        if diff[c] == 0:              # 刚好从"不够"跨到"够"
            ge_cnt += 1

        while ge_cnt == kinds:        # 覆盖了 -> 尝试缩短
            if right - left < ans_right - ans_left:
                ans_left, ans_right = left, right

            x = s[left]
            if diff[x] == 0:          # 刚好从"够"要跨回"不够"
                ge_cnt -= 1
            diff[x] -= 1
            left += 1

    return "" if ans_left < 0 else s[ans_left:ans_right + 1]


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
                break                  # 固定 i 时更长的不会更好
    return best


if __name__ == "__main__":
    for s, t, want in [
        ("ADOBECODEBANC", "ABC", "BANC"),
        ("a", "a", "a"),
        ("a", "aa", ""),           # t 里有重复，s 不够
        ("", "a", ""),
        ("ab", "b", "b"),
        ("aa", "aa", "aa"),
        ("abc", "abc", "abc"),
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
    print("✅ D12 通过")
