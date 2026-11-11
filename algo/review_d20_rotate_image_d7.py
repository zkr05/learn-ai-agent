"""复习40（D20 的第 7 天复习）｜旋转图像｜LeetCode 48｜中等

规则：不打开 d20_rotate_image.py，也不翻 notes.md。凭记忆独立重写。
目标：先独立写代码，再运行本文件；通过后回答下面三个自述。

上次（11-10）第 3 天复习：位置映射答对；整行转置的具体结果、两种循环范围的理由，
以及 O(1) 的判断标准都不够完整。这次请把机制说出来，不只写结论。

自述：
1) 转置时，为什么 `range(i)` 和 `range(i + 1, n)` 都可以？
   如果错误地写 `range(n)`，3x3 示例做完转置和每行反转后会变成什么？为什么？
   自述 1：因为range(i)和range(i+1,n),都可以避免再走一遍。
   如果写range(n)，第一步转置后相当于没有发生变化，123，456，789，但是反转之后会变成
   321，654，987.因为range(n)则是相当于交换了两遍。

2) 原来在 `(i, j)` 的元素，经过转置、再经过每行反转，分别到哪里？
   自述 2：转置后到了(j,i)，反转后到了(j,n-1-i)

3) 改成逆时针 90 度，具体改哪一行？为什么？本题凭什么是 O(1) 额外空间？
   自述 3：改成逆时针，只需要修改行反转，改成列翻转。
   没有额外的空间，只在原先的数组里进行修改。

批改：代码及固定用例、2000 组随机对拍通过。自述2正确；自述1结论和结果对，但需说清 `range(i)` / `range(i+1,n)` 都让每个无序对恰好交换一次。整行遍历会让每对元素交换两次，转置抵消，最后只剩水平镜像。自述3方向对；逆时针应以 `matrix.reverse()` 替换逐行 `row.reverse()`。O(1) 判断看是否分配随 n 增长的额外容器；本题没有，只用常数个临时变量。
状态：完成（2026-11-11 第7天复习；代码通过，概念薄弱点已批改）
"""

import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def rotate(matrix: list[list[int]]) -> None:
    """顺时针旋转 90 度，原地修改。请独立实现。"""
    n = len(matrix)
    for i in range(n):
        for j in range(i):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()


def _ref(matrix: list[list[int]]) -> list[list[int]]:
    """额外空间参考实现，仅供本文件对拍。"""
    n = len(matrix)
    return [[matrix[n - 1 - c][r] for c in range(n)] for r in range(n)]


if __name__ == "__main__":
    cases = [
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],
        [[1, 2], [3, 4]],
        [[1]],
        [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20], [21, 22, 23, 24, 25]],
    ]
    for src in cases:
        got = [row[:] for row in src]
        assert rotate(got) is None, "应原地修改且不返回值"
        assert got == _ref(src), f"输入={src}\n得到={got}\n期望={_ref(src)}"

    random.seed(4820)
    for _ in range(2000):
        n = random.randint(1, 9)
        src = [[random.randint(0, 99) for _ in range(n)] for _ in range(n)]
        got = [row[:] for row in src]
        rotate(got)
        assert got == _ref(src), f"随机对拍失败：{src} -> {got}"

    print("✅ D20 第 7 天复习通过")