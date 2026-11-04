# -*- coding: utf-8 -*-
"""存储层契约测试：同一组断言对**两个后端**各跑一遍。

为什么必须这样测：
    两个后端的价值在于"上层换存储不用改代码"。如果它们的行为有一丝不同，
    换后端就会出 bug —— 而这种 bug 类型检查和代码审查都看不出来。
    所以把"行为"写成断言，跑两遍。

用法：python test_store_contract.py
通过标准：最后打印 ✅ 并且退出码 0。
"""

import os
import sys
import tempfile
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ⚠️ 必须在 import store.* 之前设好环境变量 —— 两个后端都在模块级读路径
_TMP = tempfile.mkdtemp(prefix="store_contract_")
os.environ["STUDY_REPORTS_DIR"] = os.path.join(_TMP, "reports")
os.environ["STUDY_DB_PATH"] = os.path.join(_TMP, "contract.db")

from store import file_backend, sqlite_backend       # noqa: E402


def check(cond, msg):
    if not cond:
        raise AssertionError(msg)


def run_contract(mod, name):
    """对一个后端跑全套契约断言。"""
    print(f"\n=== 契约测试：{name} ===")

    # 0) 干净起点
    if hasattr(mod, "init_db"):
        mod.init_db()

    # 1) 空仓库
    check(mod.list_reports() == [], f"{name}: 空仓库 list_reports 应为 []")
    check(mod.available_weeks() == [], f"{name}: 空仓库 available_weeks 应为 []")
    check(mod.read_report_text("2026-W01") is None, f"{name}: 不存在的周次应返回 None")
    print("  ✅ 空仓库行为一致")

    # 2) 写入两篇（故意乱序写，验证排序由后端负责）
    text_b = "## B 周\n\n- 内容含中文和 emoji 🎯\n"
    text_a = "## A 周\n\n短一点。\n"
    mod.write_report("2026-W02", text_b)
    mod.write_report("2026-W01", text_a)

    weeks = mod.available_weeks()
    check(weeks == ["2026-W01", "2026-W02"], f"{name}: available_weeks 应升序，实得 {weeks}")
    metas = mod.list_reports()
    check(len(metas) == 2, f"{name}: list_reports 应有 2 条，实得 {len(metas)}")
    check([m.week for m in metas] == ["2026-W01", "2026-W02"], f"{name}: list_reports 应升序")
    print("  ✅ 写入 + 升序")

    # 3) 读回原文（含中文/emoji，验证编码往返）
    check(mod.read_report_text("2026-W02") == text_b, f"{name}: 读回内容应与写入一致")
    print("  ✅ 正文往返（UTF-8 / 中文 / emoji）")

    # 4) 幂等：同一周写两次，内容以最后一次为准，且不抛错、不产生重复
    text_b2 = "## B 周（第二版）\n\n改过了。\n"
    mod.write_report("2026-W02", text_b2)
    mod.write_report("2026-W02", text_b2)          # 再写一次，必须依然不炸
    check(mod.read_report_text("2026-W02") == text_b2, f"{name}: 覆盖写后应是新内容")
    check(len(mod.available_weeks()) == 2, f"{name}: 重复写不应产生新行，实得 {mod.available_weeks()}")
    print("  ✅ 幂等写入（覆盖而非追加）")

    # 5) 元信息：size_bytes = UTF-8 字节数
    meta = {m.week: m for m in mod.list_reports()}["2026-W02"]
    check(meta.size_bytes == len(text_b2.encode("utf-8")),
          f"{name}: size_bytes 应为 {len(text_b2.encode('utf-8'))}，实得 {meta.size_bytes}")
    print("  ✅ size_bytes = UTF-8 字节数")

    # 6) modified 必须是能被 fromisoformat 解析的 ISO 字符串
    try:
        datetime.fromisoformat(meta.modified)
    except ValueError:
        raise AssertionError(f"{name}: modified 不是合法 ISO 时间：{meta.modified!r}")
    print(f"  ✅ modified 是合法 ISO：{meta.modified}")

    return {"2026-W01": len(text_a.encode("utf-8")),
            "2026-W02": len(text_b2.encode("utf-8"))}


def main() -> int:
    try:
        sizes_file = run_contract(file_backend, "file_backend")
        sizes_sql = run_contract(sqlite_backend, "sqlite_backend")

        # 7) 跨后端一致性：同样的内容，两个后端报出的 week 和 size 必须相同
        print("\n=== 跨后端一致性 ===")
        check(sizes_file == sizes_sql, f"两个后端的 size 不一致：{sizes_file} vs {sizes_sql}")
        print("  ✅ 同一批内容，两后端 week / size 一致")

        # 8) 门面分派
        print("\n=== 门面分派（reports_store）===")
        import reports_store

        os.environ["STUDY_STORE"] = "file"
        check(isinstance(reports_store._backend(), type(file_backend)),
              "STUDY_STORE=file 应选到 file_backend")
        os.environ["STUDY_STORE"] = "sqlite"
        check(isinstance(reports_store._backend(), type(sqlite_backend)),
              "STUDY_STORE=sqlite 应选到 sqlite_backend")
        os.environ["STUDY_STORE"] = "bogus"
        try:
            reports_store._backend()
        except ValueError as e:
            print(f"  ✅ 非法后端名立即报错：{e}")
        else:
            raise AssertionError("非法 STUDY_STORE 应该抛 ValueError")
        os.environ.pop("STUDY_STORE", None)
        check(isinstance(reports_store._backend(), type(file_backend)),
              "未设置时应默认 file_backend")
        print("  ✅ 默认后端 = file")

    except AssertionError as e:
        print(f"\n❌ 契约测试失败：{e}")
        return 1

    print("\n✅ 全部契约通过 —— 两个后端行为一致，上层可以放心切换")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())