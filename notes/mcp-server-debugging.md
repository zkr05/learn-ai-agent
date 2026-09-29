# MCP server 跨宿主排查记录

> 一次真实的黑盒排障：MCP server 在 Codex 里连不上，在别的客户端里正常。
> 这里记的是**过程**（怎么一步步缩小范围）和**方法**（下次遇到黑盒问题怎么下手），不是结论本身。

## 症状

`study-review-agent/mcp_reports_server.py` 写完后：

- 手工测试、CLI 调用、程序化客户端 **三种方式全部正常**
- 但挂到 Codex（桌面版 26.917）里，设置界面显示 server **已启用**，却**从来不加载工具**
- 问它"我最近两周的复盘都说了什么"，它回复"我先在你的工作区里查找" —— 然后去 `rg` 满盘搜文件了

## 第 0 步：先证明「我的东西没问题」

**关键原则：用多种*独立*方式验证，而不是反复重试同一种方式。**

| 方式 | 结果 |
|---|---|
| 手工构造 JSON-RPC（自己当 host，直接读写子进程管道） | ✅ stdout 第一行就是合法 `initialize` 响应 |
| `fastmcp call mcp_reports_server.py list_reports`（CLI，真 stdio 子进程） | ✅ 工具能列能调 |
| `Client(StdioTransport(command=<配置里的 python>, args=[<脚本>]))` | ✅ 连接成功、工具齐全 |

顺便把几个假设**实测排掉**（不是猜，是跑）：

- **帧格式**：Content-Length 帧 vs 换行分隔 JSON → 换行分隔正常
- **协议版本**：请求 `2024-11-05` / `2025-03-26` / `2025-06-18` / `2025-11-25` → server 都正常回应
- **中文路径 + 符号链接**：`C:\Users\庄堃锐` 是 `C:\Users\admin` 的**符号链接**，而配置里的 python 路径经过它 → 换成纯 ASCII 路径，**无效**
- **启动超时**：补上 `startup_timeout_sec = 120`，**无效**

## 第 1 步：把宿主当被测对象 —— 读它自己的日志

宿主的日志在 `~/.codex/logs_2.sqlite` 的 `logs` 表里（`feedback_log_body` 列）：

```sql
SELECT ts, level, target, feedback_log_body FROM logs
WHERE feedback_log_body LIKE '%study-reports%' ORDER BY id DESC
```

拿到第一条硬信息：

```
WARN codex_mcp::rmcp_client
  MCP server startup failed server_name="study-reports"
  error=handshaking with MCP server failed: connection closed:
         initialize response: connection closed: initialize response
```

以及每轮对话时的：

```
TRACE connection_manager::tool_catalog
  omitting MCP server without an exact ready client server_name=study-reports
  MCP server tools unavailable ... has_cached_tools=false startup_complete=true
```

**"omitting pending server"** 是第一句人话：宿主知道这个 server，但**拿不到一个 ready 的客户端**，于是跳过它。

## 第 2 步：它是「没启动」还是「启动了但握手失败」？

这一步有个**很便宜的关键实验**：把配置里的 `command` 改成一个**根本不存在的路径**，看错误变不变。

结果：**错误一模一样**。

推论链：

1. 如果宿主真去 spawn，路径不存在应该报 `系统找不到指定的路径 (os error 3)`（内置的另一个 server 就是这么报的）
2. 错误没变 → **宿主没读新配置**
3. 再查耗时：`handler_duration_ms=29` —— **29 毫秒**。真启动一个 Python 要 1~2 秒
4. → 宿主**缓存了失败状态，既不重试也不重读配置**

**实践结论：改 MCP 配置必须完全重启宿主进程，改完立刻测是测不到的。**

> 另外一个细节：只"关窗口"往往只是最小化到托盘，进程还在。要靠任务管理器确认进程真的退出了，或者用日志里的 `process_uuid` / pid 变化来验证。

## 第 3 步：在边界插桩

**核心思路：不要在外面猜，让边界自己说话。**

做法是写一个 wrapper 顶替 server 的位置（配置里 `args` 指向 wrapper），wrapper 记录完信息后**原样调用真正的 server**（`runpy.run_path(..., run_name="__main__")`，保证 stdio 不变形）。

迭代了 4 版，每版都是"上一版拿到的信息不够，再加一根探针"：

| 版本 | 记什么 | 为什么加 |
|---|---|---|
| v1 | cwd / argv / executable / env 数量 / isatty | 最基本的环境快照 |
| v2 | + stderr 重定向到文件、`atexit` 钩子、存活时长、异常 traceback | 想知道"进程为什么退出" |
| v3 | + `GetFileType` 探 fd 类型 | 判断 stdin/stdout 到底是管道还是文件 |
| v4 | + `PeekNamedPipe` 看管道里有没有待读数据 | 判断 host 有没有把 initialize 写进来 |

**v3 一开始探错了**：直接 `GetFileType(0/1/2)` 全返回 `UNKNOWN`。原因是 CRT 的 fd 号不等于 OS 句柄，得用 `msvcrt.get_osfhandle(fd)` 拿真句柄 —— **探针自己也会有 bug，先拿"已知正常的场景"校准它**。

结果（宿主确实启动了它）：

```
cwd=C:\Users\admin\Documents\Codex\...\yaml-stage-0-stage-1-c
executable=C:\Users\admin\...\python.exe
env_count=20   has_PATH=true
stdin_isatty=false   stdout_isatty=false
env_python_codex_mcp={}
```

→ **cwd / 环境变量 / argv 全部正常**，而且不是 tty 问题。于是"路径 / 环境 / 参数传递"这些假设全部排除。

**本地基线对照**（正常情况长什么样）：

```
fd0: type=PIPE(管道)  管道中待读字节=153   ← host 会立刻把 initialize 请求写进来
fd1: type=PIPE(管道)
fd2: type=PIPE(管道)
```

## 第 4 步：复现症状，验证机制

把 server 的 stdin 接到一个**空文件**（Windows 的 `nul` 设备）：

```
进程 3 秒内退出，退出码 0，stdout 一个字节都没有
```

**这和宿主报的 `connection closed: initialize response` 完全对得上**：stdin 立刻 EOF → Python 的 mcp SDK 读到流结束 → 优雅退出 → 客户端看到"握手时连接断开"。

诚实地说：这一步只证明了**症状的机制**，没有证明宿主就是这么做的 —— 宿主没把子进程的 stderr 记进自己的日志，最后一环拿不到。（`peek` 到的 fd 类型只在 v3 那版拿到过，但那次没成功握手，样本不完整。）

## 第 5 步：换宿主交叉验证 ← 决定性的一步

把**同一个** server 挂到另一个 MCP 客户端（WorkBuddy）→ **成功**。

为什么这一步无法替代：前面所有证据都是"我这边能行"，**只有换宿主才能排除"我们漏了某个环境因素"**。换完之后的结论是干净的：

> **server 本身无问题；故障域是 Codex 桌面版 26.917 在本机这个环境下的 MCP 加载/连接环节。**

## 方法论：黑盒问题的五步

| 步骤 | 要点 |
|---|---|
| 1. 先自证清白 | 用**多种独立方式**验证自己的东西，别反复重试同一种 |
| 2. 把对方当被测对象 | 读它的日志（哪怕是 sqlite）、看它的缓存行为和耗时 |
| 3. 在边界插桩 | 在外面猜不如让边界自己说话；探针要先用已知场景校准 |
| 4. 复现症状 | 造一个"已知会坏"的场景，确认它和线上症状**是同一个机制** |
| 5. 交叉验证 | 换一个同类宿主 —— 排除"我的环境"的终极手段 |

另外一条：**每个假设都要有"如果它成立，错误应该变成什么样"的预期**。比如第 2 步那个实验 —— "如果宿主读了新配置，错误应该变成路径不存在"。**没有预期的实验等于没做实验。**

## 附一：这段时间踩到的坑（按"错误的性质"分类）

前三类能在**代码里**看出来；第四类只能靠**文档 / 经验**，是另一种难度：

| 坑 | 性质 | 现象 | 对策 |
|---|---|---|---|
| `git push \n` | **shell 的解释规则** | 想在文件末尾补换行符，结果打成字面量 `\n`；bash 解析成 `git push n` → `fatal: 'n' does not appear to be a git repository`。**每次 CI 必红** | 写 commit message / 配置时用**单引号**，别让 shell 插手 |
| docstring 里 `Args:` 与摘要之间少一个空行 | **解析器的格式要求** | 工具的参数说明**静默变成 `null`**（不报错、不崩），模型只看到参数名和类型 | 把"参数说明不为空"写成断言（回归测试） |
| 断言里写死 `AGENT_KIT` | **依赖了会变的数据** | 报告是 LLM 生成的、每周措辞都变；词一消失 CI 就红 —— 这是**误报**，不是发现 bug | **测试自己造数据**（临时目录 + fixture），不要断言别人产出的内容 |
| bot 推送不触发 workflow | **平台的隐式规则** | 人类 `git push` 能触发，`github-actions[bot]` 推**不触发**；`paths` 配得再对也没用 | 用 `workflow_dispatch` / `repository_dispatch` 主动触发（官方例外），或别用 `GITHUB_TOKEN` 推送 |
| in-process 测试全绿 ≠ server 能用 | **测试盲区** | 漏了 `if __name__ == "__main__": mcp.run()`，但 `Client(mcp)` 照样 13 条断言全绿；真起子进程一连就 `Connection closed` | 端到端测试（真的起子进程、走真的 stdio 协议） |
| 宿主缓存失败状态 | **宿主的实现细节** | 改了 MCP 配置不生效 —— 连接失败被缓存，既不重试也不重读配置 | 完全重启宿主进程（"关窗口"常常只是最小化到托盘） |
| 批量改文件时行号漂移 | **编辑操作的副作用** | 先在第 30 行插 24 行，再用旧行号 85 插第二处 → 插到错误的位置 | 从后往前改，或**按内容定位**（find 锚点），不要按行号 |

## 附二：衡量"测试强度"的办法 —— 变异测试

"测试的测试"：**往代码里注入 bug，看测试抓不抓得住。**

```
注入的 bug                     测试能抓到吗
------------------------------------------
搜索改成大小写敏感                ✅
周次不做大写归一化                ✅
glob 把本地草稿也收进来           ✅
不拦空关键词                     ✅
list_reports 不排序              ❌
```

**两次"漏掉"都很有信息量：**

**① "不排序"漏掉，不是测试写错了，是文件系统差异。** NTFS 的目录项本身按名字排序（B 树索引），所以删掉 `sorted()` 在本机看不出来；Linux 的 ext4 是哈希顺序，**CI 上会被抓到**。

**② 而第一次跑变异测试时，"搜索改成大小写敏感"也没被抓到。** 原因是当时 fixture 里的 `agent_kit` 全是小写，而关键词也会被 `lower()` —— 两边碰巧一致，所以"只小写一边"的 bug 测不出来。**把 fixture 改成混合大小写 `Agent_Kit` 之后才抓得到。**

> **教训：测试"看起来在测某件事"和"真的在测那件事"，是两回事。**
> 唯一能确认的办法就是**把它弄坏一次**。
