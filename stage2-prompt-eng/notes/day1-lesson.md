# 第 1 天：System Prompt（系统提示词）

> 对应 awesome-agentic-ai-zh Stage 2 练习 1。
> 这是 Stage 2 唯一的新概念入口：messages 数组里除了 user，还能放 system。

## 1. system 和 user 的区别

Stage 1 我们只用了 `messages=[{"role": "user", "content": "..."}]`。
Stage 2 开始在数组**最前面**加一条 `system`：

```python
messages=[
    {"role": "system", "content": "你是严谨的合约律师。回答要精准、引用法条编号。"},  # 人设/规则
    {"role": "user", "content": "请帮我解释什么是租赁合约。"},                        # 真正的问题
]
```

- `system` = 给模型的"工作说明书"：设定身份、规则、输出格式
- `user` = 用户实际问的话
- 同一个 user 问题，换不同的 system → 输出完全不同

## 2. 为什么 system 有用

模型没有"人格"，它只是根据上下文预测下一个词。
system prompt 就是在上下文里**预先铺好**你要的风格，让模型沿着那个方向生成。

## 3. 练习 1 的三个观察点

| system | 期待效果 |
|---|---|
| 严肃律师 | 精准、引用法条、不用形容词 |
| 幼儿园老师 | 口语、比喻、短（<80 字） |
| JSON 机器 | 只回 `{"answer": ..., "confidence": ...}` |

## 4. 今天的作业（含检验）

1. 运行 `practice_1.py`（3 个 system 各出 1 个回答）
2. 文件顶部注释里记录观察：
   - 观察1：三个回答的风格差异大吗？哪个 system 最"听话"？
   - 观察2：JSON 机器那个回答，真的是合法 JSON 吗？还是夹带了别的文字？
   - 观察3：如果 system 说"少于 80 字"，模型真的做到了吗？
3. 提交 git
4. 完成后口头回答（我会提问）：
   - system 和 user 的区别是什么？
   - 想让它"只回 JSON"，你会怎么写 system？
   - 为什么同一个问题，不同 system 会得到不同答案？

> 参考解答：`exercises/practice_1_reference.py`。先自己跑，卡住再看。
