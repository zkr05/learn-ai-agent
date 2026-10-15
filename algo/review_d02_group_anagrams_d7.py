"""复习6（D02 的第 7 天复习，第 2 次重写） ｜ 字母异位词分组 ｜ LeetCode 49 ｜ 中等

规则：不许打开 d02_group_anagrams.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天那次（10-12 补做）你独立写出来了，这次目标 **5 分钟**。

目标：5 分钟内写完。

两个自述（跑绿之后填，第 2 次要比第 3 天答得更硬）：

  1) 复杂度：给出**完整式子**，并指出哪个符号是变量、为什么不能省略它。
     （第 3 天你只答了「用了排序，复杂度就不是 n 了」—— 方向对，但没有式子、没有原因。）
     自述 1：

  2) 为什么「排序后的字符串」当 key 是**安全**的？也就是：它凭什么既不会漏、也不会混？
     提示：一个好的 key 必须同时满足两个方向 —— 你能说清是哪两个吗？
     自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def group_anagrams(strs: list[str]) -> list[list[str]]:
    """把字母构成相同的词分到一组。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


def _norm(groups: list[list[str]]) -> list[list[str]]:
    """归一化后比较 —— 组内顺序和组间顺序都不保证，必须先排序再比。"""
    return sorted(sorted(g) for g in groups)


if __name__ == "__main__":
    cases = [
        (["eat", "tea", "tan", "ate", "nat", "bat"],
         [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
        (["ba", "ab"], [["ba", "ab"]]),        # ← 不排序直接拿原词当 key 的话，这里会分成两组
        ([""], [[""]]),
        (["a"], [["a"]]),
        (["", ""], [["", ""]]),
        (["ab", "ba", "abc"], [["ab", "ba"], ["abc"]]),
    ]
    for strs, want in cases:
        got = group_anagrams(strs)
        assert _norm(got) == _norm(want), f"{strs} -> {got}，期望 {want}"
    print("✅ 复习D02（第7天）通过 —— 第 2 次独立重写成功")
