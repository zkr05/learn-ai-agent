"""复习34（D16 的第 7 天复习） ｜ 除自身以外数组的乘积 ｜ LeetCode 238 ｜ 中等

规则：不许打开 d16_product_of_array_except_self.py，也不许翻 notes.md。

目标：10 分钟内写完。

三个自述：

  1) 为什么 `suf` 必须先在**倒序**那一轮算完，再从左往右乘 `pre`？
     如果顺序反了（先从左往右乘 pre、再算 suf），会怎样？
     自述 1：

  2) 题目说「输出数组不算额外空间」，那这题的额外空间到底是 O(1) 还是 O(n)？
     说清判断依据。
     自述 2：

  3) 为什么这题不能用除法？（举出会崩的具体输入）
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def product_except_self(nums: list[int]) -> list[int]:
    """返回数组 ans，其中 ans[i] = 除 nums[i] 之外所有元素的乘积。"""
    # TODO: 你来写（不许看旧文件）
    raise NotImplementedError


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