"""复习30（D14 的第 7 天复习，第 2 次重写） ｜ 合并区间 ｜ LeetCode 56 ｜ 中等

规则：不许打开 d14_merge_intervals.py，也不许翻 notes.md。
     第 3 天（10-27）自述 1 过程说混了（[3,4] 没被跳过，是它吸收了 [2,3]），
     自述 2 误解了问题，自述 3 对。

目标：8 分钟内写完。

三个自述（第 2 次）：

  1) 为什么必须先按起点排序？用 `[[1,2],[3,4],[2,3]]` 说清（重点说"谁被谁吸收"）。
     自述 1：必须先按起点排序，如果不排序，则[1,2]不会吸收[3,4],而[2,3]被[1,2]吸收之后就到[3,4]了
     ⚠️ 半对：提到了"吸收"，但事件顺序说反了。实测不排序 [[1,2],[3,4],[2,3]]：
       [1,2] 新开区间 -> ans=[[1,2]]
       [3,4] 新开区间 -> ans=[[1,2],[3,4]]
       [2,3] 并入 ans[-1]，ans 一点没变（max(4,3)=4、起点仍是 3）-> [2,3] 连痕迹都没留下；
       而它真正该合并的 [1,2] 早已写进 ans、再也改不到。
     准确说法：每个新区间只能跟"当前最后一个"比较，早结账的区间回不去；[2,3] 出现太晚，
       被错误塞给 [3,4] 后静默丢弃。[1,2] 本来就不该吸收 [3,4]（不重叠），原句不成立。
     判断法：理由里必须出现一个结论里没有的新对象 —— 这题的新对象是"已结账的区间改不动了"。

  2) `end` 为什么必须取 `max(prev_end, cur_end)`？举一个具体反例。
     自述 2：如果是[1,5][2,3]如果直接取融合p[1]，则此时出错。
     ✅ 对：反例精准（[1,5]+[2,3] 若取 p[1] 得 [1,3]，[3,5] 被凭空丢掉）。
        不足：只写"出错"，没写错成什么样 —— 面试要能说出 [1,3] 这个具体结果。

  3) `ans.append(p)` 有什么副作用？怎么修？
     自述 3：会修改intervals的内容，可以传入的值，而不要传引用。
     ✅ 对，且代码里已修（写的是 ans.append([p[0], p[1]])，新建 list）。
        实测不拷贝的后果：返回 [[1,5]]，输入被改成 [[1,5],[2,5]]。
        补充：intervals.sort() 原地改了**输入顺序**（[[3,4],[1,2]] -> [[1,2],[3,4]]），
        不改输入要写 sorted(intervals)。被问"有没有副作用"时，内层引用 + 外层顺序两处都算。

状态：完成（2026-11-02 第 2 次独立重写成功，8 分钟内）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def merge(intervals: list[list[int]]) -> list[list[int]]:
    """合并所有重叠区间；端点相接也算重叠。"""
    intervals.sort(key=lambda p:p[0])
    ans = []
    for p in intervals:
        if ans and p[0] <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1],p[1])
        else:
            ans.append([p[0],p[1]])
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
    print("✅ 复习D14（第7天）通过 —— 第 2 次独立重写成功")
