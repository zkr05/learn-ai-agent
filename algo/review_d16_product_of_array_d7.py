"""复习34（D16 的第 7 天复习） ｜ 除自身以外数组的乘积 ｜ LeetCode 238 ｜ 中等

规则：不许打开 d16_product_of_array_except_self.py，也不许翻 notes.md。

目标：10 分钟内写完。

三个自述：

  1) 为什么 `suf` 必须先在**倒序**那一轮算完，再从左往右乘 `pre`？
     如果顺序反了（先从左往右乘 pre、再算 suf），会怎样？
     自述 1：在这道题，如果先从左往右乘pre，此时pre没法存储各个点对应的除了他之外的前面的乘积
     值就丢了再算suf没有用。
     ⚠️ **这题的前提是我出错了**："suf 必须先算"是假的。两轮互相独立，顺序随便 ——
        实测 7 组用例，先 suf 再 pre、先 pre 再 suf 结果完全一致。
     真正的约束只有一条：**每一轮里，先把「自己的那份」乘进 ans[i]，再更新累积变量**。
        写成 pre *= x 然后再 ans[i] *= pre，就会把 nums[i] 自己乘进去 —— 这才是错的地方。
     你原话是在追我那个错误前提，不算你的错。
  2) 题目说「输出数组不算额外空间」，那这题的额外空间到底是 O(1) 还是 O(n)？
     说清判断依据。
     自述 2：这道题的额外空间是O(1),因为没有引入额外的数组空间，全程都在修改suf的值。
     ⚠️ 结论（按题目口径）对，但**理由和你自己的代码打架**：
        你第一行就是 suf = [1] * n，这是长度 n 的新数组，不是"没有引入额外数组"。
     正确说法：**除了输出数组之外只用了 pre 一个变量 -> O(1)**；
        题目明确把输出数组排除在额外空间之外，所以总账记 O(1)。
     判断依据：先问"分配了和 n 同阶的容器吗"，再问"它在不在题目的豁免名单里"。

  3) 为什么这题不能用除法？（举出会崩的具体输入）
     自述 3：不能用除法，除零会让结果直接崩。就算可以也要判断有多少个零，更麻烦。
     ✅ 对。

状态：完成（2026-11-03 第 2 次独立重写成功，3000 组对拍；逾期 1 天补做）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def product_except_self(nums: list[int]) -> list[int]:
    """返回数组 ans，其中 ans[i] = 除 nums[i] 之外所有元素的乘积。"""
    n = len(nums)
    suf = [1] * n
    for i in range(n-2,-1,-1):
        suf[i] = suf[i + 1] * nums[i + 1]
    pre = 1
    for i ,x in enumerate(nums):
        suf[i] *= pre
        pre *= x
    return suf


def _ref(nums: list[int]) -> list[int]:
    """暴力：每个位置重算一遍乘积。"""
    out = []
    for i in range(len(nums)):
        p = 1
        for j, x in enumerate(nums):
            if j != i:
                p *= x
        out.append(p)
    return out


if __name__ == "__main__":
    for src in [
        [1, 2, 3, 4],
        [-1, 1, 0, -3, 3],
        [2, 3],
        [1],
        [0, 0],
        [0, 5],
        [5, 0],
        [-2, -3, -4],
        [1, 1, 1, 1],
        [2, -1, 3, -4, 5],
    ]:
        got = product_except_self(src[:])
        want = _ref(src)
        assert got == want, f"{src} -> {got}，期望 {want}"
        assert len(got) == len(src), "长度不对"

    import random
    random.seed(238)
    for _ in range(3000):
        n = random.randint(1, 8)
        src = [random.randint(-4, 4) for _ in range(n)]
        assert product_except_self(src[:]) == _ref(src), f"对拍失败: {src}"
    print("✅ 复习D16（第7天）通过 —— 第 2 次独立重写成功")
