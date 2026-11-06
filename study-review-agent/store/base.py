# -*- coding: utf-8 -*-
"""存储层的公共约定 —— 只有数据定义和契约说明，没有实现。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReportMeta:
    """一篇报告的元信息（纯数据，不含存储细节）。

    为什么不用 Path：Path 会让上层可以 read_text() / copy2() /
    拼路径，等于把"存储是文件"焊死在调用方。用纯数据就不会泄漏。
    """

    week: str          # 例如 "2026-W45"
    size_bytes: int    # 正文的 UTF-8 字节数
    modified: str      # ISO 8601 时间字符串，例如 "2026-11-03T09:00:00"


# 每个后端模块必须提供下面 4 个函数（签名与语义完全一致）：
#
#   list_reports() -> list[ReportMeta]
#       全部报告，按 week 升序（旧 -> 新）。
#
#   read_report_text(week: str) -> str | None
#       读正文；没有这一周返回 None（"没有"是事实，不是异常）。
#
#   write_report(week: str, text: str, created_at: str | None = None) -> None
#       写入/覆盖。**必须幂等**：同一个 week 写两次结果一样，不抛错、不产生重复。
#       created_at 是可选的回填时间（ISO 字符串）；不传就用"现在"。
#       它的存在是为了迁移/回填时能保留历史时间，而不是全变成"入库那一刻"。
#
#   available_weeks() -> list[str]
#       list_reports() 的轻量版，只要周次，升序。
