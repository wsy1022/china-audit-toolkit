#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""术语查询小工具（离线，只用标准库）。

用法：
    python term_lookup.py revenue                # 英→中，模糊匹配
    python term_lookup.py --zh 坏账准备            # 中→英
    python term_lookup.py --exact "net profit"   # 精确匹配
    python term_lookup.py --part 审计             # 按部分筛选
    python term_lookup.py --list-parts           # 看有哪些分类
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CANDS = [
    os.path.join(os.path.dirname(HERE), "references", "glossary.csv"),
    os.path.join(HERE, "glossary.csv"),
]


def load():
    for p in CANDS:
        if os.path.exists(p):
            with open(p, encoding="utf-8-sig") as f:
                return list(csv.DictReader(f)), p
    sys.exit("找不到 glossary.csv，请在 skills/accounting-audit-en-zh 目录内运行")


def show(rows):
    if not rows:
        print("没有匹配。试试更短的关键词，或用 --zh 反查。")
        return
    w1 = max(len(r["en"]) for r in rows)
    w1 = min(max(w1, 12), 46)
    for r in rows:
        print(f"{r['en']:<{w1}}  {r['zh']}    [{r.get('part','')} · {r.get('chapter','')}]")
    print(f"\n共 {len(rows)} 条")


def main():
    ap = argparse.ArgumentParser(description="会计审计术语查询（750 条）")
    ap.add_argument("query", nargs="?", default="", help="要查的英文或中文词")
    ap.add_argument("--zh", action="store_true", help="按中文反查英文")
    ap.add_argument("--exact", action="store_true", help="精确匹配")
    ap.add_argument("--part", default="", help="按分类筛选：会计原理/财务会计/成本与管理会计/国际会计/审计/报表行项目")
    ap.add_argument("--list-parts", action="store_true", help="列出所有分类")
    a = ap.parse_args()

    rows, path = load()
    print(f"# 术语库：{path}（{len(rows)} 条）\n")

    if a.list_parts:
        parts = {}
        for r in rows:
            parts[r.get("part", "")] = parts.get(r.get("part", ""), 0) + 1
        for k, v in sorted(parts.items(), key=lambda x: -x[1]):
            print(f"  {k or '(未分类)'}  {v} 条")
        return

    q = a.query.strip().lower()
    sel = [r for r in rows if not a.part or a.part in r.get("part", "")]
    if not q:
        show(sel[:60])
        return

    key = "zh" if a.zh else "en"
    if a.exact:
        hits = [r for r in sel if r[key].lower() == q]
    else:
        hits = [r for r in sel if q in r[key].lower()]
    # 前缀命中优先，短的在前
    hits.sort(key=lambda r: (0 if r[key].lower().startswith(q) else 1, len(r[key])))
    show(hits[:80])


if __name__ == "__main__":
    main()
