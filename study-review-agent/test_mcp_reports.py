import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


import asyncio
from fastmcp import Client


async def main():
    async with Client("mcp_reports_server.py") as c:
        assert {t.name for t in await c.list_tools()} == {"list_reports", "read_report", "search_reports"}
        for t in await c.list_tools():
            for pname, p in t.inputSchema.get("properties", {}).items():
                assert p.get("description"), f"{t.name}.{pname} 缺参数说明"
        d = (await c.call_tool("list_reports", {})).data
        weeks = [r["week"] for r in d["reports"]]
        assert len(weeks) >= 2, f"至少该有两份报告，实际 {weeks}"
        assert weeks == sorted(weeks), f"没有按周排序: {weeks}"       
        assert all(".local" not in r["file"] for r in d["reports"]) 

        for raw in ("2026-W39", "2026-w39", "W39", "2026-W39-review.md"):    # 四种归一化写法
            d   = (await c.call_tool("read_report", {"week": raw})).data
            assert d.get("week") == "2026-W39", (raw, d)
            assert d.get("content")

        d = (await c.call_tool("read_report", {"week": "1999-W01"})).data
        assert "error" in d and "2026-W39" in d["retry_hint"]      # retry_hint 必须含动态周次列表

        d  = (await c.call_tool("read_report", {"week": "abc"})).data
        assert "error" in d and "2026-W39" in d["retry_hint"]      # 格式提示里要有正确例子

        d = (await c.call_tool("search_reports", {"keyword": "embedding"})).data
        assert d["total"] >= 2, d
        hit_weeks = {m["week"] for m in d["matches"]}
        assert {"2026-W38", "2026-W39"} <= hit_weeks, f"没跨到两份报告: {hit_weeks}"
        assert all(m["line"] >= 1 for m in d["matches"])         # 行号 1-based

        d = (await c.call_tool("search_reports", {"keyword": "AGENT_KIT"})).data
        assert d["total"] >= 2, d                                      # 大小写不敏感

        d = (await c.call_tool("search_reports", {"keyword": "不存在的东西xyz"})).data
        assert d["total"] == 0 and d["matches"] == []

        d = (await c.call_tool("search_reports", {"keyword": "e", "limit": 3})).data
        assert len(d["matches"]) == 3 and d["truncated"] is True    # 封顶但不说谎
        print("✅ MCP 工具全部验收通过")


if __name__ == "__main__":
    asyncio.run(main())