"""复习33（D15 的第 7 天复习，第 2 次重写） ｜ 轮转数组 ｜ LeetCode 189 ｜ 中等

规则：不许打开 d15_rotate_array.py，也不许翻 notes.md。

目标：8 分钟内写完。

三个自述：

  1) `k` 为什么要先对 n 取模？
     自述 1：如果这里的k是大于n的一个数，如果不取模，则会出现超出nums的数，reverse里面的函数就会出错。
     从而后面报错，同时取模的意思也不会改变原先的意思。
     ✅ 但浅：「不取模会越界」是事实（实测 k=5 -> IndexError），但解释不了全部 ——
        k=4（正好等于 n）不取模也不报错、结果还是原样（实测 [1,2,3,4] -> [1,2,3,4]）。
     真正理由：**右移 k 位和右移 k+n 位是同一个操作**（连续转 n 次回到原样，周期是 n）。
        所以 k 的取值本来就是"模 n 的等价类"，取模是把同一类的代表元挑出来。
        你最后那句"取模不改变原先的意思"其实就是等价性，但没说出来。
     附带坑：k=0 或 k=n 时 reverse(0, k-1) 变成 reverse(0, -1)，
        而 -1 在 Python 里是合法下标，while i < j 直接不进去 -> 没炸。这是**运气**不是设计。

  2) 为什么「整体反转 + 前 k 个反转 + 后 n-k 个反转」就等于右移 k 位？
     （用 A + B 的切分讲，写清每一步之后数组长什么样。）
     自述 2：A + B 整体反转 -> B转+A转 前k个反转 -> B + A转 后n-k个反转 -> B + A
     ✅ 对，链条一步没错。"前 k 个正好是 B转"是这题的命门（因为 B 的长度就是 k），抓住了。
        唯一缺口：没落成具体数组。面试口头讲符号推导容易自己绕晕，边讲边写数字最稳：
          A+B          [1,2,3,4,5,6,7]
          整体反转      [7,6,5,4,3,2,1]   = B转 + A转
          前 k=3 反转   [5,6,7,4,3,2,1]   = B + A转
          后 n-k=4 反转 [5,6,7,1,2,3,4]   = B + A

  3) 这里说的「额外空间 O(1)」具体指什么？reverse 函数内部用了几个变量？
     自述 3：具体是指不借用额外的数组空间来做，只对原来的数组进行修改。reverse内部用了两个变量，分别是
     起点和终点。
     ✅ 对。补一个细节：i、j 两个循环变量 + `nums[i], nums[j] = nums[j], nums[i]`
        那个**元组临时变量**（2 个元素，常数）。所以是"2 个循环变量 + 常数个临时"，与 n 无关。
        关键：**O(1) 说的是"和 n 无关"，不是"一个变量都不用"。**

状态：完成（2026-11-02 第 2 次独立重写成功，3000 组对拍；逾期 1 天补做）
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(nums: list[int], k: int) -> None:
    """向右轮转 k 步，原地修改，不返回值。"""
    def reverse(i: int , j: int):
            while i < j:
                nums[i],nums[j] = nums[j],nums[i]
                i += 1
                j -= 1
    n = len(nums)
    k = k % n
    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)

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
