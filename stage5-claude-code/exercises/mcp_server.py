# 练习：写你的第一个 MCP server（用 FastMCP）
# 需要：pip install fastmcp（已装）
#
# 任务：自己设计一个工具（温度换算/汇率/计算器都行），用 FastMCP 包成 server。
# 写完运行 `python mcp_server.py` 确认能启动，然后叫我验证工具。
#
# 作业：跑通后在顶部注释回答：
# 观察1（server 启动后是什么状态）：server 独立进程启动，INFO 日志显示 transport='stdio'，等 host 连接（不是被框架调用）
# 观察2（@mcp.tool 和你 Stage 4 的 @tool 区别）：@mcp.tool 和 @tool 语法像但运行不同——@tool在框架进程内被直接调用；@mcp.tool在独立进程通过stdio协议被任意host远程调用

from fastmcp import FastMCP

# ① 创建 server
mcp = FastMCP("my-tools")

# ② 注册工具（✍️ 你自己设计：函数名、参数、docstring）

RATES = {
    "USD":1.0,
    "CNY":6.7,
    "EUR":0.89,
    "JPY":159.0,
}

@mcp.tool
def exchange_rate(from_currency: str,to_currency: str) -> dict:
    """查询两种货币之间的汇率。

    Args:
        from_currency: 源货币代码，如 USD、CNY。
        to_currency: 目标货币代码，如 USD、CNY。
    """

    f = from_currency.upper()
    t = to_currency.upper()
    if f not in RATES or t not in RATES:
        return {"error": f"不支持的币种: {from_currency} -> {to_currency}",
                "retry_hint": f"支持的币种: {list(RATES.keys())}"}
    rate = RATES[t] / RATES[f]
    return {"from": from_currency, "to": to_currency, "rate": rate}
# ③ 启动（stdio 协议，等 host 连接）
if __name__ == "__main__":
    mcp.run()
