# AI Agent 学习路线全图（Track B — Agent Builder）

> 这份文档是你 Stage 0-7 的完整复习地图。每周翻一遍，哪里模糊回看对应 stage 的 notes/。

## 0. 总览：三层工程（贯穿全部 stage）

| 层 | 核心问题 | 对应 stage | 你的代表作 |
|---|---|---|---|
| Prompt | 这次怎么问？ | Stage 2 | system/few-shot/CoT/refine |
| Context | 这次给哪些信息？ | Stage 6 | RAG + Memory |
| Harness | 整个流程怎么跑起来？ | Stage 7 | loop/retry/eval/observability/cost |

**一句话**：LLM 是大脑，Context 是喂给大脑的信息，Harness 是把大脑接上手脚跑起来的系统。

---

## 1. 各阶段速查

### Stage 0 — Python 基础（14 天）
- **技能**：变量/字符串/list/dict、函数、类、async/await、模块/pip、错误处理、文件+JSON、requests API、YAML
- **产出**：GitHub API 调用、带 token 的 API 认证、YAML 配置读写

### Stage 1 — LLM 基础
- **3 个核心词**：token（中文 1 字≈1.5-2 token）、context window（模型一次能看多少）、temperature（0=稳定/1=创意）
- **关键体验**：推理模型 max_tokens 要留够（思考吃 token）；本机 vs 云端 trade-off（$0 但慢 vs 贵但快）
- **成本公式**：(输入token×单价 + 输出token×单价) / 1M × 次数

### Stage 2 — Prompt 工程
- **system**：设定人设/规则/格式（放 messages 第一位）
- **few-shot**：0-shot 不给例子 / few-shot 给 2-5 个例子（钉格式+示范判准；不保证每次更准，要多跑）
- **CoT**：让模型先想再答；⚠️ 对推理模型别硬塞手写 CoT
- **refine**：模糊→加读者→加格式→加示例→加禁忌（约束越具体越收敛）
- **核心**：prompt 颗粒度要匹配模型能力；写"只回 JSON"要明确禁止+给 schema

### Stage 3 — Tool Use & 第一个 Agent
- **Agent 3 部件**：🧠LLM + 🔧Tools + 🔁Loop（缺一不可）
- **Function calling**：tools=[schema] → 模型返回 tool_calls（不是 content！）
- **ReAct 循环**（你从零写过）：
  ```python
  for step in range(max_iter):
      resp = llm.chat.completions.create(model=MODEL, tools=TOOLS, messages=messages)
      tool_calls = resp.choices[0].message.tool_calls or []
      messages.append({"role":"assistant","content":thought,"tool_calls":...})  # 坑1:必须接回
      if not tool_calls: return final_answer  # 收尾
      for tc in tool_calls:
          obs = TOOL_IMPL[tc.function.name](json.loads(tc.function.arguments))
          messages.append({"role":"tool","tool_call_id":tc.id,"content":obs})  # 坑2:带id
  ```
- **3 个坑**：assistant 必须接回（否则失忆死循环）/ tool 消息带 tool_call_id（配对）/ max_iter 安全网
- **错误是数据**：工具错误 `return {"error":..., "retry_hint":...}` 而不是 raise（模型自己恢复）
- **schema 设计**：name 具体、description 写"何时用"、type 用对、required+enum

### Stage 4 — Agent 框架
- **workflow vs agent**：代码决定下一步 vs LLM 决定
- **multi-agent 4 信号**：任务天然分解 / token explosion / 角色冲突 / 并行加速（都不在→别硬上，3-10x token）
- **5 个 pattern**：Routing → Sequential → Parallel → Supervisor-Worker → Debate
- **框架对比**：LangGraph（图式/状态/checkpoint，适合复杂流程）、CrewAI（角色式/上手快/黑盒）、Smolagents（CodeAct 写代码）、Pydantic AI（类型安全输出）
- **CodeAct vs JSON tool**：写代码更灵活但对模型要求高
- **工具输入归一化**（踩 3 次的坑）：工具只认英文→模型传中文→查不到；加别名 .lower() 解决

### Stage 5 — CLI agent 生态
- **CLI agent**：有完整电脑权限（file/shell/git），比 web 强但危险→权限+沙箱
- **AGENTS.md**：给 agent 的项目说明书（5 原则：可读/短/单一源/可验证/透明）
- **MCP**：工具标准化协议（写一次 server 任何 host 用）：
  ```python
  from fastmcp import FastMCP
  mcp = FastMCP("my-tools")
  @mcp.tool
  def my_tool(x: str) -> str:
      """说明。Args: x: ..."""
      ...
  if __name__ == "__main__": mcp.run()
  ```
- **Skill**：SKILL.md（frontmatter description + 步骤 + 通过标准），description 匹配自动加载
- **区分**：MCP=能力、Skill=行为、Plugin=打包、Subagent=独立 worker

### Stage 6 — 记忆 / RAG
- **名词切开**：Retrieval（找资料动作）/ RAG（retrieve+generate 流程）/ Embedding（文本→向量）/ Vector store（存向量）/ Chunking（切块）/ Memory（记住事）
- **RAG 流水线**：chunk → embed → store → retrieve（余弦相似度）→ generate
- **⚠️ embedding 对大小写/拼写敏感**（ReAct≠React）→ 查询规范化/混合搜索
- **Memory**：Working（当前窗口）vs Long-term（跨 session）；Episodic/Semantic/Procedural 三种内容
- **3 个 Pattern**：1 全塞（短对话）/ 2 摘要+近N轮（中长）/ 3 向量检索（跨session）；生产混用 2+3

### Stage 7 — 生产化
- **Harness 8 元件**：loop / tool registry / context manager / safety / retry / telemetry / eval / cost
- **反馈循环**：agent 变强靠反馈不靠完美 prompt；**独立验收最重要**（自己检查会自我称赞）
- **Eval**（LLM 的 pytest）：EVAL_CASES（问题+期望词）→ agent 回答 → evaluator 判断 → 通过率；测正确性+诚实性（说"不知道"）
- **Observability 4 原语**：latency / token / trace / errors（@contextmanager 自动计时）
- **Streaming**：stream=True，chunk.choices[0].delta.content；first_token 时间决定体验
- **Cost**：公式 + prompt caching（重复前缀省 90% 输入成本）

---

## 2. 常用代码模板（可复制）

### ReAct 循环（最核心，背下来）
```python
for step in range(max_iter):
    resp = client.chat.completions.create(model=MODEL, tools=TOOLS_SPEC, messages=messages)
    msg = resp.choices[0].message
    thought = msg.content or ""
    tool_calls = msg.tool_calls or []
    messages.append({"role": "assistant", "content": thought,
                     **({"tool_calls": [{"id": tc.id, "type": "function",
                       "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                       for tc in tool_calls]} if tool_calls else {})})
    if not tool_calls:
        return thought
    for tc in tool_calls:
        fn = TOOL_IMPL.get(tc.function.name)
        args = json.loads(tc.function.arguments)
        try:
            obs = fn(args) if fn else f"error: unknown tool {tc.function.name}"
        except Exception as e:
            obs = f"error: {e}"
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": obs})
return None  # max_iter 用完
```

### RAG 核心（embed→retrieve→generate）
```python
def embed(text):
    return client.embeddings.create(model="bge-m3", input=text).data[0].embedding

def cosine(a, b):
    dot = sum(x*y for x,y in zip(a,b)); na = sum(x*x for x in a)**0.5; nb = sum(x*x for x in b)**0.5
    return dot/(na*nb) if na and nb else 0.0

def retrieve(question, top_k=2):
    q = embed(question)
    return [chunk for chunk, v in sorted(store, key=lambda i: cosine(q, i[1]), reverse=True)[:top_k]]
```

### Eval 骨架
```python
EVAL_CASES = [{"id": "x", "input": "...", "expected": "..."}]
def run_eval(cases):
    results = []
    for c in cases:
        answer = agent(c["input"])
        results.append({"id": c["id"], "passed": c["expected"] in answer, "answer": answer[:50]})
    rate = sum(1 for r in results if r["passed"]) / len(results)
    return results, rate
```

---

## 3. 概念速查词典

| 词 | 一句话 |
|---|---|
| token | LLM 计数的单位（中文 1 字≈1.5-2 token）|
| context window | 模型一次能看的 token 上限 |
| temperature | 采样随机度（0 稳定 / 1 创意）|
| system prompt | 人设/规则（messages 第一位）|
| few-shot | 给几个例子再问 |
| CoT | 让模型先想再答 |
| ReAct | 思考→行动→观察 循环 |
| tool_calls | 模型"想调工具"的请求（不在 content 里）|
| MCP | 工具标准化协议（跨 host 复用）|
| Skill | 特定情境的行为包（description 触发）|
| RAG | 检索增强生成（查资料再答）|
| embedding | 文本→向量（语义搜索）|
| Memory | 跨对话记住东西 |
| Harness | 模型外围的执行控制层 |
| Eval | LLM 的 pytest（量化成功率）|
| Observability | 让 agent 可观测（latency/token/trace/error）|

---

## 4. 踩坑记录（都是真金白银）

1. **推理模型吃 token**：max_tokens 要给 500+，否则 content 为空
2. **中文引号写进代码**：字符串里别用 ASCII 引号当内容
3. **模型抢跑**：多步任务别列工具清单，用"必须完成"短问题
4. **模型漏步**：3b 多步不稳，7b 更稳；生产换大模型或多跑
5. **工具输入不匹配**（踩 3 次）：工具和模型要对齐（中英文别名/归一化）
6. **embedding 大小写敏感**：ReAct≠React，查询要规范化
7. **模型改数字**：工具返回 6.7 模型可能用 6.7899——数据要校验
8. **自己检查会自我称赞**：验收要拆独立 agent（Debate/Critic）
9. **.codex 有敏感文件**：auth.json 不能提交

---

## 5. 毕业自测

- [ ] 能默写 ReAct 循环 + 说出 3 个坑
- [ ] 能搭一个 RAG（embed→retrieve→generate）
- [ ] 能给 agent 写 eval 并解释通过率
- [ ] 能说出 MCP/Skill/AGENTS.md 的区别
- [ ] 能判断：什么时候用框架/手写/RAG/multi-agent
- [ ] 能讲出 Harness 8 元件和你做过哪些
