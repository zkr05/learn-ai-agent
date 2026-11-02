"""复习33（D15 的第 7 天复习，第 2 次重写） ｜ 轮转数组 ｜ LeetCode 189 ｜ 中等

规则：不许打开 d15_rotate_array.py，也不许翻 notes.md。

目标：8 分钟内写完。

三个自述：

  1) `k` 为什么要先对 n 取模？
     自述 1：

  2) 为什么「整体反转 + 前 k 个反转 + 后 n-k 个反转」就等于右移 k 位？
     （用 A + B 的切分讲，写清每一步之后数组长什么样。）
     自述 2：

  3) 这里说的「额外空间 O(1)」具体指什么？reverse 函数内部用了几个变量？
     自述 3：

状态：待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(nums: list[int], k: int) -> None:
    """向右轮转 k 步，原地修改，不返回值。"""
    # TODO: 你来写（不许看旧文件）
    raise NotImplementedError


def _ref(nums: list[int], k: int) -> list[int]:
    n = len(nums)
    if n == 0:
        return []
    k %= n
    return nums[n - k:] + nums[:n - k] if k else nums[:]


if __name__ == "__main__":
    for src, k in [
        ([1, 2, 3, 4, 5, 6, 7], 3),
        ([-1, -100, 3, 99], 2),
        ([1, 2], 1),
        ([1, 2], 2),
        ([1, 2], 3),
        ([1], 0),
        ([1], 5),
        ([1, 2, 3, 4, 5], 0),
        ([1, 2, 3], 7),
    ]:
        got = src[:]
        assert rotate(got, k) is None, "题目要求原地修改、不返回值"
        want = _ref(src, k)
        assert got == want, f"{src} k={k} -> {got}，期望 {want}"

    box = [1, 2, 3]
    ref_id = id(box)
    rotate(box, 1)
    assert id(box) == ref_id, "不许用 nums = ... 重新绑定（外面看不到）"
    assert box == [3, 1, 2], f"原地修改失败: {box}"

    import random
    random.seed(189)
    for _ in range(3000):
        n = random.randint(1, 8)
        src = [random.randint(0, 99) for _ in range(n)]
        k = random.randint(0, 20)
        got = src[:]
        rotate(got, k)
        assert got == _ref(src, k), f"对拍失败: {src} k={k} -> {got}"
    print("✅ 复习D15（第7天）通过 —— 第 2 次独立重写成功")