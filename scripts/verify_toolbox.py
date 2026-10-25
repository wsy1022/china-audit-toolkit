# -*- coding: utf-8 -*-
"""核对本机工具箱是否与清单一致。

用法：
    python verify_toolbox.py --root "E:\\审计数据处理工具箱"
    python verify_toolbox.py --root . --fast        # 只查存在与大小，不算哈希
    python verify_toolbox.py --root . --json        # 机器可读输出

退出码：0 全部一致；1 有缺失或哈希不符；2 清单读不到。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)


def load_json(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def load_sha(path):
    """tools.sha256 是 tab 分隔的五列：id / label / path / size / sha256。"""
    rows = {}
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 5:
                continue
            tid, label, rel, size, digest = parts[:5]
            rows[(tid, label)] = {"path": rel, "size": int(size), "sha256": digest}
    return rows


def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n} GB"


def main(argv=None):
    ap = argparse.ArgumentParser(description="核对工具箱与清单是否一致")
    ap.add_argument("--root", default=REPO, help="工具箱根目录（含 组件/ 的那一层）")
    ap.add_argument("--fast", action="store_true", help="只核对存在与文件大小，不计算 SHA-256")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args(argv)

    root = os.path.abspath(args.root)
    manifest_path = os.path.join(REPO, "tools.json")
    sha_path = os.path.join(REPO, "tools.sha256")
    if not os.path.exists(manifest_path):
        print(f"找不到清单：{manifest_path}", file=sys.stderr)
        return 2

    data = load_json(manifest_path)
    known = load_sha(sha_path)

    results = []
    for t in data.get("tools", []):
        entries = [(t.get("name", ""), t.get("exe", ""))]
        for v in t.get("variants", []):
            entries.append((v.get("label", ""), v.get("exe", "")))
        for label, rel in entries:
            path = os.path.normpath(os.path.join(root, rel.replace("/", os.sep)))
            item = {"id": t.get("id"), "label": label, "path": rel, "status": "ok", "detail": ""}
            if not os.path.exists(path):
                item["status"] = "missing"
                item["detail"] = "文件不存在"
                results.append(item)
                continue

            size = os.path.getsize(path)
            item["size"] = size
            ref = known.get((t.get("id", ""), label))
            if ref and ref["size"] and size != ref["size"]:
                item["status"] = "size"
                item["detail"] = f"大小 {human(size)}，清单 {human(ref['size'])}"
            elif not args.fast and ref and ref["sha256"] not in ("", "MISSING"):
                got = sha256_of(path)
                if got != ref["sha256"]:
                    item["status"] = "sha"
                    item["detail"] = f"哈希不符 ({got[:12]}… ≠ {ref['sha256'][:12]}…)"
            results.append(item)

    bad = [r for r in results if r["status"] != "ok"]
    if args.json:
        print(json.dumps({"root": root, "checked": len(results), "problems": bad}, ensure_ascii=False, indent=2))
    else:
        print(f"工具箱：{root}")
        print(f"清单条目：{len(results)} 个文件（含变体）\n")
        width = max((len(r["id"] or "") for r in results), default=3)
        for r in results:
            mark = {"ok": "OK  ", "missing": "缺失", "size": "大小", "sha": "哈希"}[r["status"]]
            print(f"  [{mark}] {str(r['id']).ljust(width)}  {r['label']}　{r['detail']}")
        print()
        if bad:
            print(f"发现 {len(bad)} 处问题；其余 {len(results) - len(bad)} 个文件与清单一致。")
        else:
            print(f"全部 {len(results)} 个文件与清单一致。")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
