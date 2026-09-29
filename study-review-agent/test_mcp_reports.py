# -*- coding: utf-8 -*-
"""study-reports MCP server 的验收测试（stdio 端到端）。

设计要点：**测试自己造数据**。仓库里 reports/ 下的周报是 LLM 生成的、每周内容都变，
拿它们当断言依据会周期性误报。这里改成在临时目录里造两份内容固定的报告，
通过 STUDY_REPORTS_DIR 环境变量指给 server。
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import asyncio
import os
import re
import tempfile
from pathlib import Path

from fastmcp import Client
from fastmcp.client.transports import StdioTransport

HERE = Path(__file__).resolve().parent
SERVER = str(HERE / "mcp_reports_server.py")

# fixture：内容由测试控制，永远不变
FIXTURE = {
    # 注意第 5 行故意放了 3 次「标记词」：用来证明 total 计的是"命中的行数"而不是出现次数
    "2026-W01-review.md": (
        "# 第一周\n\n"
        "本周研究了 Agent_Kit 的封装方式。\n"      # 故意混合大小写：只小写关键词的 bug 会在这里暴露
        "标记词 标记词 标记词\n"
        "标记词 再来一次\n"
    ),
    "2026-W02-review.md": (
        "# 第二周\n\n"
        "继续 agent_kit，另外试了 embedding 的相似度。\n"
        "标记词 又一次\n"
    ),
    # 本地草稿：必须被排除在列表和搜索之外
    "2026-W01-review.local.md": (
        "# 本地草稿\n\n这行不该出现在任何搜索结果里：ZZZ_LOCAL_ONLY\n"
    ),
}


async def run_checks() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        for name, text in FIXTURE.items():
            (work / name).write_text(text, encoding="utf-8")

        env = {**os.environ, "STUDY_REPORTS_DIR": str(work)}
        transport = StdioTransport(command=sys.executable, args=[SERVER], env=env)

        async with Client(transport) as c:
            # ① 工具名齐全
            names = {t.name for t in await c.list_tools()}
            assert names == {"list_reports", "read_report", "search_reports"}, names

            # ② 每个参数都要有说明（docstring 少个空行会让它静默变成 null）
            for tool in await c.list_tools():
                for pname, prop in tool.inputSchema.get("properties", {}).items():
                    assert prop.get("description"), f"{tool.name}.{pname} 缺参数说明"

            # ③ list_reports：只认正式报告、按周排序
            d = (await c.call_tool("list_reports", {})).data
            weeks = [r["week"] for r in d["reports"]]
            assert weeks == ["2026-W01", "2026-W02"], weeks
            assert all(".local" not in r["file"] for r in d["reports"]), d

            # ④ read_report：四种写法归一化到同一周
            for raw in ("2026-W01", "2026-w01", "W01", "2026-W01-review.md"):
                d = (await c.call_tool("read_report", {"week": raw})).data
                assert d.get("week") == "2026-W01", (raw, d)
                assert d.get("content"), (raw, d)

            # ⑤ 两种失败要分开：认不出格式 vs 没有这份
            d = (await c.call_tool("read_report", {"week": "abc"})).data
            assert "error" in d, d
            assert re.search(r"\d{4}-W\d{2}", d["retry_hint"]), d      # 给出具体格式例子

            d = (await c.call_tool("read_report", {"week": "1999-W01"})).data
            assert "error" in d, d
            assert "2026-W01" in d["retry_hint"] and "2026-W02" in d["retry_hint"], d

            # ⑥ search_reports：跨文件命中，行号 1-based
            d = (await c.call_tool("search_reports", {"keyword": "agent_kit"})).data
            assert d["total"] == 2, d
            assert {m["week"] for m in d["matches"]} == {"2026-W01", "2026-W02"}, d
            assert all(m["line"] >= 1 for m in d["matches"]), d

            # ⑦ 大小写不敏感
            d = (await c.call_tool("search_reports", {"keyword": "AGENT_KIT"})).data
            assert d["total"] == 2, d

            # ⑧ 本地草稿不参与搜索
            d = (await c.call_tool("search_reports", {"keyword": "ZZZ_LOCAL_ONLY"})).data
            assert d["total"] == 0 and d["matches"] == [], d

            # ⑨ 搜不到就老实说搜不到
            d = (await c.call_tool("search_reports", {"keyword": "根本不存在的词xyz"})).data
            assert d["total"] == 0 and d["matches"] == [], d

            # ⑩ 封顶但不说谎：matches 截断，total 仍是真实命中数
            #    这里 total 应为 3（3 个命中行），而不是 5（标记词出现 5 次）—— total 计行数
            d = (await c.call_tool("search_reports", {"keyword": "标记词", "limit": 2})).data
            assert len(d["matches"]) == 2 and d["truncated"] is True, d
            assert d["total"] == 3, d

            # ⑪ 空关键词要拦住（否则等于搜"每一行"）
            d = (await c.call_tool("search_reports", {"keyword": "   "})).data
            assert "error" in d, d

    print("✅ MCP server 验收通过 — 3 个工具 / 11 组断言（数据来自临时 fixture，不依赖真实周报）")


if __name__ == "__main__":
    asyncio.run(run_checks())
