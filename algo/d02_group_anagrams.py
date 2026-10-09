"""D02 字母异位词分组（哈希）   LeetCode 49   Medium

思路：异位词（字母构成相同的词）排序后完全相同 —— 所以「排序后的字符串」可以当分组依据。
     用字典：key = 排序后的字符串，value = 该组的所有原词。

复杂度：时间 O(n * k log k) —— n 是个数，k 是单词最大长度
           每个词排序 O(k log k)，n 个词相乘
        空间 O(n * k)       —— 要存下所有词

状态：完成 ｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """把字母构成相同的词分到一组。"""
    d = {}
    for s in strs:
        sorted_s = ''.join(sorted(s))
        if sorted_s not in d:
            d[sorted_s] = []
        d[sorted_s].append(s)
    return list(d.values())


def _norm(groups: list[list[str]]) -> list[list[str]]:
    """把分组结果归一化，用于比较（组内顺序、组间顺序都不保证）。"""
    return sorted(sorted(g) for g in groups)


if __name__ == "__main__":
    # 注意：这题不能直接断言 == [["bat"],["nat","tan"],["ate","eat","tea"]]
    #       因为组内和组间的顺序都不保证 —— 要先归一化再比
    expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    got = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert _norm(got) == _norm(expected), got

    assert _norm(group_anagrams([""])) == _norm([[""]])
    assert _norm(group_anagrams(["a"])) == _norm([["a"]])
    assert _norm(group_anagrams(["", ""])) == _norm([["", ""]])
    print("✅ D02 通过")


# --- 进阶：不用排序的写法（复杂度降到 O(n * k)）----------------------------
# 用「每个字母出现次数」当 key —— 异位词的计数必然相同。
# 坑：list 不能当 dict 的 key（不可哈希），要转成 tuple。
#
# from collections import defaultdict
#
# def group_anagrams_fast(strs):
#     d = defaultdict(list)
#     for s in strs:
#         count = [0] * 26
#         for ch in s:
#             count[ord(ch) - ord("a")] += 1
#         d[tuple(count)].append(s)          # ← tuple 才能当 key
#     return list(d.values())
