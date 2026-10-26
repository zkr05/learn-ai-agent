"""复习22（D14 的第 3 天复习） ｜ 合并区间 ｜ LeetCode 56 ｜ 中等

规则：不许打开 d14_merge_intervals.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么必须先按起点排序？用 `[[1,2],[3,4],[2,3]]` 说清（不要只说"不排序会错"）。
     自述 1：

  2) `end` 为什么必须取 `max(prev_end, cur_end)`？举个反例。
     自述 2：

  3) `ans.append(p)` 有什么副作用？（生产环境为什么会出问题，怎么修）
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def merge(intervals: list[list[int]]) -> list[list[int]]:
    """合并所有重叠区间；端点相接也算重叠。"""
    # TODO: 你来写（不看旧文件）
    raise NotImplementedError


def _ref(intervals: list[list[int]]) -> list[list[int]]:
    pts = sorted(intervals)
    ans = []
    for s, e in pts:
        if ans and s <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1], e)
        else:
            ans.append([s, e])
    return ans


if __name__ == "__main__":
    for src, want in [
        ([[1, 3], [2, 6], [8, 10], [15, 18]], [[1, 6], [8, 10], [15, 18]]),
        ([[1, 4], [4, 5]], [[1, 5]]),
        ([[1, 4], [0, 4]], [[0, 4]]),
        ([[1, 4], [2, 3]], [[1, 4]]),
        ([], []),
        ([[1, 4]], [[1, 4]]),
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
        ([[1, 10], [2, 3], [4, 5]], [[1, 10]]),
    ]:
        got = merge([p[:] for p in src])
        assert got == want, f"{src} -> {got}，期望 {want}"

    import random
    random.seed(83)
    for _ in range(2000):
        src = []
        for _ in range(random.randint(0, 8)):
            a = random.randint(0, 12)
            src.append([a, random.randint(a, 14)])
        assert merge([p[:] for p in src]) == _ref(src), f"对拍失败: {src}"
    print("✅ 复习D14 通过 —— 独立重写成功")
