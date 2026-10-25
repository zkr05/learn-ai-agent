"""D14 合并区间（排序 + 扫描）   LeetCode 56   Medium   <- 普通数组第 2 题

思路：**先按起点排序**，然后一次扫描，只跟「答案里最后一个区间」比。

     为什么必须排序（反例 [[1,2],[3,4],[2,3]]）：
       不排序时 [2,3] 最后才出现，它把已经分开的 [1,2] 和 [3,4] **桥接**起来 ——
       但 ans 里已经定死，没法回头改 -> 返回 [[1,2],[3,4]]（正确是 [[1,4]]）。
       排序保证「当前区间的起点 >= 所有已处理区间的起点」，
       所以它若不和最后一个重叠，也不可能和更早的重叠 -> 一次向前扫描就够。

     两个容易错的点：
       1) end 要取 max(prev_end, cur_end)，不能直接 = cur_end
          （[[1,10],[2,3]]：p[0]=2 <= 10 重叠，但 p[1]=3 < 10，直接写 3 会丢掉 [3,10]）
       2) 端点相接算重叠，所以判断用 <= 不是 <（[[1,4],[4,5]] -> [[1,5]]）

     ⚠️ 一个生产环境的坑：`ans.append(p)` 传的是**引用**，
        后面 `ans[-1][1] = ...` 会把**输入 intervals 里的那个子列表**也改掉。
        实测：输入 [[1,3],[2,6],[8,10]] 调用后变成 [[1,6],[2,6],[8,10]]。
        LeetCode 只看返回值所以没事，但真实项目里这是「悄悄改了调用方的数据」。
        修法：`ans.append([p[0], p[1]])`。

复杂度：时间 O(n log n)（排序占主导，扫描 O(n)）；空间 O(n)（结果列表）。
        注：原数组是**原地排序**的，不想改输入要先 copy。

状态：完成 ｜ 复习D3 待做
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
            ans[-1][1] = max(ans[-1][1], p[1])
        else:
            ans.append([p[0], p[1]])      # 拷贝一份，避免改掉输入
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
        ([[1, 4], [4, 5]], [[1, 5]]),          # 端点相接
        ([[1, 4], [0, 4]], [[0, 4]]),          # 同终点、起点更小
        ([[1, 4], [2, 3]], [[1, 4]]),          # 被包含
        ([], []),
        ([[1, 4]], [[1, 4]]),
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
        ([[1, 10], [2, 3], [4, 5]], [[1, 10]]),
        ([[2, 3], [4, 5], [6, 7], [8, 9], [1, 10]], [[1, 10]]),
    ]:
        got = merge([p[:] for p in src])
        assert got == want, f"{src} -> {got}，期望 {want}"

    import random
    random.seed(83)
    for _ in range(3000):
        src = []
        for _ in range(random.randint(0, 8)):
            a = random.randint(0, 12)
            src.append([a, random.randint(a, 14)])
        assert merge([p[:] for p in src]) == _ref(src), f"对拍失败: {src}"

    # 不许改掉输入（生产环境的坑）
    src = [[1, 3], [2, 6], [8, 10]]
    before = [p[:] for p in src]
    merge(src)
    assert src == before, f"输入被修改了: {src}"
    print("✅ D14 通过")
