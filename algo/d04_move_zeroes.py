"""D04 移动零（双指针）   LeetCode 283   Easy

思路：双指针 —— `start0` 指向「下一个非零元素该放的位置」，
     它同时等于「已处理区里非零元素的个数」。一遍遍历，遇到非零就和 nums[start0] 交换，
     然后 start0 前移。扫完后 [0, start0) 全是非零（相对顺序天然保持），[start0, n) 全是 0。

     为什么必须「交换」而不是「赋值」：**原地写入会覆盖掉原来的值，被覆盖的那个 0 必须有个去处**。
     交换就是把它安置到 i 位置 —— 0 的个数是守恒的。
     写成 nums[start0] = nums[i]（不换回来）会把 0 直接销毁：实测 [0,1] -> [1,1]。
     附带好处：start0 == i（还没遇到过 0）时交换是「自己和自己换」，天然空操作，
     不用额外加 if i != start0 判断。

复杂度：时间 O(n)   —— 每个元素只被访问一次
        空间 O(1)   —— 只用了 start0 / i 两个下标变量（**不算输入 nums 本身**）

状态：完成（卡点：没卡很久，想通了不难）｜ 复习D3 待做
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def move_zeroes(nums: list[int]) -> None:
    """把 0 全部移到末尾，非零元素保持原相对顺序 —— 原地修改，不返回。"""
    start0 = 0
    for i in range(len(nums)):
        if nums[i]:
            nums[i], nums[start0] = nums[start0], nums[i]
            start0 += 1


if __name__ == "__main__":
    for src, want in [
        ([0, 1, 0, 3, 12], [1, 3, 12, 0, 0]),
        ([], []),                              # 空数组
        ([0], [0]),                            # 只有 0
        ([1], [1]),                            # 只有非零
        ([1, 2, 3], [1, 2, 3]),                # 本来就没有 0
        ([0, 0, 0], [0, 0, 0]),                # 全是 0
        ([0, 0, 1], [1, 0, 0]),                # 0 在前
        ([1, 0], [1, 0]),                      # 0 在后
        ([-1, 0, 2], [-1, 2, 0]),              # 负数也要保持顺序
        ([0, 0, 0, 0, 7], [7, 0, 0, 0, 0]),
    ]:
        got = src[:]
        assert move_zeroes(got) is None, "题目要求原地修改、不返回"
        assert got == want, f"{src} -> {got}，期望 {want}"
    print("✅ D04 通过")
