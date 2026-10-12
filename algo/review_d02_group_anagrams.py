"""复习1（D02 的第 3 天复习，补做 —— 到期日 10-11 休息了） ｜ 字母异位词分组 ｜ LeetCode 49 ｜ 中等

规则：不许打开 d02_group_anagrams.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

两个自述（跑绿之后填）：
  1) 你用的 key 是什么？它抹掉了哪个「无关差异」？
  2) 复杂度为什么不能只写 O(n)？

自述 1：用的 key 是「把每个词排序后的字母」—— 抹掉了**字母的排列顺序**这个无关差异
       （eat / tea / ate 排序后都是 aet，所以归成一类）
自述 2：因为用了排序，复杂度就不是 O(n) 了 —— 准确说是 **O(n·k log k)**。
       n 是单词个数、k 是单词最大长度；每个词排序是 O(k log k)，n 个词相乘。
       **k 是变量，不能当常数丢掉** —— 这才是不能只写 O(n) 的原因。

状态：完成（2026-10-12 补做，独立重写成功）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """把字母构成相同的词分到一组。"""
    idx = {}
    for x in strs:
        sorted_x = ''.join(sorted(x))
        if sorted_x not in idx:
            idx[sorted_x] = []
        idx[sorted_x].append(x)
    return list(idx.values())



def _norm(groups: list[list[str]]) -> list[list[str]]:
    """把分组结果归一化后比较 —— 组内顺序和组间顺序都不保证，必须先排序再比。"""
    return sorted(sorted(g) for g in groups)


if __name__ == "__main__":
    expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    assert _norm(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == _norm(expected)
    assert _norm(group_anagrams([""])) == _norm([[""]])
    assert _norm(group_anagrams(["a"])) == _norm([["a"]])
    assert _norm(group_anagrams(["", ""])) == _norm([["", ""]])
    assert _norm(group_anagrams(["ab", "ba", "abc"])) == _norm([["ab", "ba"], ["abc"]])
    print("✅ 复习D02 通过 —— 独立重写成功")
