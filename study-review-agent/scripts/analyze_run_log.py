# -*- coding: utf-8 -*-
"""把 run_log.jsonl 清洗成一张统计表。

为什么要单独一个脚本：
    这是"分析"，不是"服务"。跑一次看结果，不进 API、不进 CI。
    需要 pandas，而 pandas 不是服务的依赖（requirements.txt 里没有它）。

用法：
    python scripts/analyze_run_log.py           # 统计 + 写 CSV
    python scripts/analyze_run_log.py --check   # 只跑验收断言

数据里有三个坑，写代码前先知道（这是"读题"）：
    1) 文件是 JSONL：每行一个 JSON，不是 JSON 数组 -> 读的时候 lines=True
    2) 两种记录结构不一样：
         eval   有 pass_rate / results
         report 有 backend / tokens / cost / stats
    3) tokens 是嵌套字典，不是两列 -> 要拍平
"""

from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
LOG_PATH = BASE / "reports" / "run_log.jsonl"
OUT_CSV = BASE / "reports" / "run_log_stats.csv"


# ---------------------------------------------------------------- 1. 读入
def load(path: Path = LOG_PATH) -> pd.DataFrame:
    """读 JSONL -> DataFrame。"""
    df = pd.read_json(path, lines=True)
    return df

# ---------------------------------------------------------------- 2. 拍平
def flatten(df: pd.DataFrame) -> pd.DataFrame:
    """把嵌套的 tokens 列拍平成 in_tok / out_tok 两列。"""
    tok = pd.json_normalize(df["tokens"])
    tok.columns = ["in_tok", "out_tok"]
    df = pd.concat([df, tok], axis=1)
    df = df.drop(columns=["tokens"])
    return df


# ---------------------------------------------------------------- 3. 清洗
def clean(df: pd.DataFrame) -> pd.DataFrame:
    """按业务含义处理缺失值。

    ⚠️ 这题的核心：三处缺失含义完全不同，不能一律 fillna(0)。

        缺失位置                 含义                        处理
        backend 空 + eval        字段不适用（eval 没有后端）  填 "(eval)" 作为分类
        cost 空 + local          真没花钱                    填 0.0
        cost 空 + cloud          数据缺失（异常！）           保持 NaN，不许填 0
    """

    df = df.copy()

    df["backend"] = df["backend"].fillna("(eval)")
    mask = (df["backend"] == "local") & df["cost"].isna()
    df.loc[mask, "cost"] = 0.0

    df["in_tok"] = df["in_tok"].fillna(0).astype(int)
    df["out_tok"] = df["out_tok"].fillna(0).astype(int)

    return df
    

# ---------------------------------------------------------------- 4. 聚合
def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """按 backend 汇总：次数 / 输入 token / 平均输出 / 总成本。"""

    stat = df.groupby("backend").agg(
        次数=("event", "size"),
        输入token=("in_tok", "sum"),
        平均输出=("out_tok", "mean"),
        总成本=("cost", "sum"),
    ).round(4)
    return stat



# ---------------------------------------------------------------- 5. 输出
def report(df: pd.DataFrame) -> dict:
    """关键数字整理成一个 dict，打印和验收都用它。"""
    paid = df[df["cost"] > 0]                        # NaN > 0 是 False，天然被排除
    cost_missing = df[(df["backend"] == "cloud") & df["cost"].isna()]
    return {
        "总记录": len(df),
        "eval次数": int((df["event"] == "eval").sum()),
        "report次数": int((df["event"] == "report").sum()),
        "计费次数": int(len(paid)),
        "总成本": round(float(paid["cost"].sum()), 4),
        "单次最低": round(float(paid["cost"].min()), 5) if len(paid) else 0.0,
        "单次最高": round(float(paid["cost"].max()), 5) if len(paid) else 0.0,
        "云端缺成本条数": int(len(cost_missing)),
        "各后端次数": {str(k): int(v) for k, v in df["backend"].value_counts().items()},
    }


# ---------------------------------------------------------------- 验收（别改这段）
def verify(raw: pd.DataFrame, flat: pd.DataFrame, cleaned: pd.DataFrame, summary: pd.DataFrame) -> None:
    """契约式验收：把你写的东西按"应该是什么样"检查一遍。"""

    # 1) 读入：行数必须和文件里的有效行数一致
    n_lines = sum(1 for line in LOG_PATH.read_text(encoding="utf-8").splitlines() if line.strip())
    assert len(raw) == n_lines, f"读入 {len(raw)} 行，文件里实际 {n_lines} 行"

    # 2) 拍平：多了两列、少了原来那列
    assert "in_tok" in flat.columns and "out_tok" in flat.columns, "拍平后应有 in_tok / out_tok 两列"
    assert len(flat) == len(raw), "拍平不许丢行"
    assert flat["in_tok"].isna().sum() < len(flat), "in_tok 全是空？拍平没成功"

    # 3) backend 不许有空值
    assert cleaned["backend"].isna().sum() == 0, "backend 还有空值"

    # 4) local 的 cost 必须是 0（本地跑不花钱）
    local_cost = cleaned.loc[cleaned["backend"] == "local", "cost"]
    assert (local_cost.fillna(-1) == 0).all(), "local 的 cost 应该全是 0"

    # 5) ★核心★ 云端缺成本的记录必须保持 NaN，不能被填成 0
    expect_missing = int(((raw["backend"] == "cloud") & raw["cost"].isna()).sum())
    got_missing = int(((cleaned["backend"] == "cloud") & cleaned["cost"].isna()).sum())
    assert expect_missing > 0, "测试数据里应该至少有一条云端缺成本，检查一下 run_log"
    assert got_missing == expect_missing, (
        f"云端缺成本的记录有 {expect_missing} 条，但清洗后只剩 {got_missing} 条 —— "
        "说明你把 NaN 填成 0 了。这是数据缺失，不是'没花钱'，不许填 0。"
    )

    # 6) token 列必须是整数
    assert cleaned["in_tok"].dtype.kind in "iu", f"in_tok 应该是整数，实际 {cleaned['in_tok'].dtype}"
    assert cleaned["out_tok"].dtype.kind in "iu", f"out_tok 应该是整数，实际 {cleaned['out_tok'].dtype}"

    # 7) 汇总表：三个 backend 分类都在（(eval) / local / cloud）
    assert set(summary.index) == {"(eval)", "local", "cloud"}, f"汇总分类不对：{list(summary.index)}"
    assert summary.loc["cloud", "次数"] == int((cleaned["backend"] == "cloud").sum()), "cloud 次数对不上"

    print("\n✅ 验收通过：")


def main(argv: list[str]) -> int:
    raw = load()
    flat = flatten(raw)
    cleaned = clean(flat)
    summary = summarize(cleaned)
    info = report(cleaned)

    if "--check" not in argv:
        print("=== 按后端汇总 ===")
        print(summary.to_string())
        print("\n=== 关键数字 ===")
        for k, v in info.items():
            print(f"  {k}: {v}")
        summary.to_csv(OUT_CSV, encoding="utf-8-sig")
        print(f"\n已写出 {OUT_CSV}")

    try:
        verify(raw, flat, cleaned, summary)
        print(f"   读入 {len(raw)} 行 / 拍平后 {len(flat)} 行 / 汇总 {len(summary)} 组")
    except AssertionError as e:
        print(f"\n❌ 验收失败：{e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))