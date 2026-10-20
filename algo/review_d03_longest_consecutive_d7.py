"""复习9（D03 的第 7 天复习，第 2 次重写） ｜ 最长连续序列 ｜ LeetCode 128 ｜ 中等

规则：不许打开 d03_longest_consecutive.py，也不许翻 notes.md。凭记忆独立写。
     第 3 天那次你写出来了，自述说了机制但没给计数论证。

目标：5 分钟内写完。

两个自述（跑绿之后填 —— 都用上「所以呢？」这一行）：

  1) 三段式：为什么「跳过非起点」是安全的？
     也就是：对任意一个**非起点** x（即 x-1 在集合里），为什么永远不需要从它开始数？
     自述 1：

  2) 复杂度：写出「`while` 的总迭代次数 ≤ n」这一步是怎么来的。
     （第 3 天你答了「while 只在起点执行，所以不是嵌套」——机制对，但没给∑那一步。）
     自述 2：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def longest_consecutive(nums: list[int]) -> int:
    """最长连续整数序列的长度（不要求在原数组里相邻）。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


if __name__ == "__main__":
    for nums, want in [
        ([100, 4, 200, 1, 3, 2], 4),
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),
        ([], 0),
        ([1], 1),
        ([1, 2, 0, 1], 3),
        ([0, -1, 1], 3),
        ([5, 5, 5, 5], 1),          # 全重复
        ([1, 2, 3, 4, 5], 5),       # 一个长段
    ]:
        got = longest_consecutive(nums[:])
        assert got == want, f"{nums} -> {got}，期望 {want}"
    print("✅ 复习D03（第7天）通过 —— 第 2 次独立重写成功")
