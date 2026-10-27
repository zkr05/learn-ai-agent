"""复习22（D14 的第 3 天复习） ｜ 合并区间 ｜ LeetCode 56 ｜ 中等

规则：不许打开 d14_merge_intervals.py，也不许翻 notes.md。凭记忆独立写。

目标：8 分钟内写完。

三个自述（跑绿之后填）：

  1) 为什么必须先按起点排序？用 `[[1,2],[3,4],[2,3]]` 说清（不要只说"不排序会错"）。
     自述 1：如果没有排序，则示例的情况会出现，1，2遇到3，4过了之后，与2，3合并，但是3，4被永远跳过了，无法再合并。
     半对：结论对（不排序会漏），但过程说混了 —— **[3,4] 没有被跳过，它把 [2,3] 吸收了**：
       `[1,2]` 新开一组 -> `[3,4]` 新开一组 -> `[2,3]` 因为 2 <= 4 并入 `[3,4]`（end 保持 4）。
       结果 `[[1,2],[3,4]]`，而 `[1,2]` 的 end 本来该被 `[2,3]` 推到 3、再和 `[3,4]` 连成 `[1,4]`。
       核心：**后出现的区间把已经分开的两组桥接了，而 ans 已经定死，没法回头改**。

  2) `end` 为什么必须取 `max(prev_end, cur_end)`？举个反例。
     自述 2：哪来的这个问题
     说明：**你的代码是对的**（第 34 行确实用了 max）。这个问题是**反事实**的：
       「如果写成 `= p[1]` 会怎样？」—— 用来验证你是否知道 max 在保护什么。
       反例 `[[1,10],[2,3]]`：2 <= 10 重叠，但 `p[1] = 3 < 10`；
       直接写 3 -> `[[1,3]]`，把 `[3,10]` 这一段**丢掉**了。
       => max 保护的是「**当前区间被上一个区间包含**」这种情况。

  3) `ans.append(p)` 有什么副作用？（生产环境为什么会出问题，怎么修）
     自述 3：ans.append(p) 会改变输入的值，intervals的值也会被修改，可以改为传p的值进来。
     ✅ 对。修法：`ans.append([p[0], p[1]])`（或 `p[:]`）。
     （注意：本次复习代码第 36 行还是 `ans.append(p)` —— 坑还在，只是测试用例没检查输入是否被改。）

状态：完成（2026-10-27 独立重写成功）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def merge(intervals: list[list[int]]) -> list[list[int]]:
    """合并所有重叠区间；端点相接也算重叠。"""
    intervals.sort(key=lambda p: p[0])
    ans = []

    for p in intervals:
        if ans and p[0] <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1],p[1])
        else:
            ans.append(p)
    return ans

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
