
"""agent_kit —— 可复用的LLM agent 通用零件

从 study-review-agent 抽出：后端解析 / LLM调用记账 / 计时 / 成本核算 / 
遥测日志 / 工具注册 / 结构校验。
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import json
import os
import time
from contextlib import contextmanager
from openai import OpenAI
from pathlib import Path


def env(name: str, default: str = "") -> str:
    """读环境变量。注意：空字符串要视为未设置（Actions 未配 var 会传空值）。"""
    # TODO 1: 实现
    value = os.environ.get(name,"")
    if not value:
        return default

    return value


def resolve_backend(choice: str) -> dict:
    """返回 {"name", "base_url", "model", "api_key"} 字典。

    - local:  Ollama，默认 http://localhost:11434/v1 + qwen2.5:7b
    - cloud:  OpenAI 兼容 API，必须配置 CLOUD_API_KEY，否则报错退出
    - auto:   用 client.models.list() 带 3s 超时探测本地；不通则 fallback 云端
    """
    if choice == "local":
        return {
            "name": "local",
            "base_url": env("LOCAL_BASE_URL", "http://localhost:11434/v1"),
            "model": env("LOCAL_MODEL", "qwen2.5:7b"),
            "api_key": "ollama",
        }
    if choice == "cloud":
        key = env("CLOUD_API_KEY")
        if not key:
            print("key为空")
            raise SystemExit(1)
        return {
            "name": "cloud",
            "base_url": env("CLOUD_BASE_URL", "https://api.openai.com/v1"),
            "model": env("CLOUD_MODEL", "gpt-4o-mini"),
            "api_key": key,
        }
    if choice == "auto":
        client = OpenAI(base_url=env("LOCAL_BASE_URL","http://localhost:11434/v1"),api_key ="ollama", timeout=3.0)
        try:
           client.models.list()
           return resolve_backend("local")
        except Exception:
           return resolve_backend("cloud")

    print(f"错误：未知后端 '{choice}'，可选 local / cloud / auto")
    raise SystemExit(1)


@contextmanager
def timed(label: str, stats: list):
    """Stage 7 练习 3 的老朋友：计时 contextmanager，结束把 latency 写进 stats。"""
    t0 = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - t0) * 1000
        stats.append({"tool": label, "latency_ms": elapsed})


def call_llm(client: OpenAI, cfg: dict, system: str, user: str, stats: list) -> tuple[str, dict]:
    """调用 chat.completions，返回 (回复文本, {"input": n, "output": n})。
    token 数从 resp.usage 里拿；把 tokens 也写进 stats。"""
    with timed("call_llm", stats):
        resp = client.chat.completions.create(
            model = cfg["model"],
            messages = [{"role": "system", "content":system},
                        {"role": "user", "content":user}]
        )
        in_tokens = resp.usage.prompt_tokens
        out_tokens = resp.usage.completion_tokens
        stats.append({"tokens": {"input": in_tokens, "output": out_tokens}})
        text = resp.choices[0].message.content
        return text , {"input": in_tokens, "output": out_tokens}


def estimate_cost(cfg: dict, tokens: dict) -> float | None:
    """仅 cloud 后端且配置了 CLOUD_PRICE_IN/OUT（每百万 token 单价）才算，否则 None。"""
    if cfg["name"] != "cloud":
        return None
    price_in = env("CLOUD_PRICE_IN")
    price_out = env("CLOUD_PRICE_OUT")
    if not price_in or not price_out:
        return None

    price_in = float(price_in)
    price_out = float(price_out)
    cost = (tokens["input"] * price_in + tokens["output"] * price_out) / 1_000_000
    return cost


def check_structure(report: str, headers: list) -> list:
    """返回缺失的标题列表（空列表 = 结构完整）。"""
    return [h for h in headers if h not in report]


def append_run_log(entry: dict, log_path) -> None:
    """把运行遥测追加写入 log_path（一行一个 JSON）。"""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


class ToolRegistry:
    """工具注册表。用实例持有工具，避免多个项目共用一个全局dict。"""

    def __init__(self):
        self.tools = {}

    def register(self, name: str, description: str):
        def deco(fn):
            self.tools[name] = {"impl": fn, "description": description}
            return fn
        return deco
    
    def get(self, name: str):
        return self.tools.get(name) 


if __name__ == "__main__":
    stats = []
    with timed("sleep_test", stats):
        time.sleep(0.05)
    print("env fallback:", env("NO_SUCH_VAR", "默认值"))
    print("stats:", stats)
    print("backend local:", resolve_backend("local"))
    print("estimate_cost(local):", estimate_cost({"name": "local"}, {"input": 100, "output": 50}))
    test_log = Path("_selftest_log.jsonl")
    append_run_log({"event": "selftest"}, test_log)
    print("append_run_log ok:", test_log.read_text(encoding="utf-8").strip())
    test_log.unlink()
    reg = ToolRegistry()

    @reg.register("echo", "回显输入")
    def echo(x):
        return x

    print("registry:", reg.get("echo")["description"], "->", reg.get("echo")["impl"]("hi"))
    print("未知工具:", reg.get("没有这个"))