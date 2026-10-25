#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Financial Statement Translator  —  财务报表中英翻译器
=====================================================
把英文财务报表 / 财务数据（.txt .md .docx .xlsx .csv .pdf）翻译成中文，
并用内置 629 条会计审计术语库强制术语一致、自动核对数字是否丢失。

两种运行方式：
  1) 图形界面（双击 exe 即用）
  2) 命令行：  translator.exe --cli 报表.docx -o 报表_中文.docx --bilingual

翻译引擎使用任意 OpenAI 兼容接口（默认 DeepSeek；也可填 OpenAI / 通义 / 智谱 / 本地 Ollama）。
API Key 只保存在本机 %APPDATA%\\AccountingTranslator\\config.json，不上传任何地方。
"""
import argparse
import json
import os
import re
import sys
import threading
import urllib.request
import urllib.error

APP_NAME = "AccountingTranslator"
APP_VER = "1.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
CFG_DIR = os.path.join(os.environ.get("APPDATA", HERE), APP_NAME)
CFG_PATH = os.path.join(CFG_DIR, "config.json")
DEFAULT_CFG = {
    "api_key": "",
    "base_url": "https://api.deepseek.com/v1",
    "model": "deepseek-chat",
    "strict_terms": True,
    "bilingual": True,
    "chunk_chars": 1600,
}

# ---------------------------------------------------------------- 术语库

def glossary_paths():
    """术语库可能被打包进 exe，也可能放在同目录。"""
    cands = []
    if getattr(sys, "_MEIPASS", None):
        cands.append(os.path.join(sys._MEIPASS, "glossary.json"))
    cands += [
        os.path.join(HERE, "glossary.json"),
        os.path.join(os.path.dirname(HERE), "app", "glossary.json"),
        os.path.join(os.path.dirname(os.path.dirname(HERE)), "skills",
                     "accounting-audit-en-zh", "references", "glossary.csv"),
    ]
    return [p for p in cands if os.path.exists(p)]


def load_glossary():
    """返回 {en_lower: {en, zh}}，支持 json 与 csv 两种来源。"""
    for p in glossary_paths():
        try:
            if p.endswith(".json"):
                with open(p, encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    return data
            else:
                import csv
                out = {}
                with open(p, encoding="utf-8-sig") as f:
                    for row in csv.DictReader(f):
                        out[row["en"].lower()] = {"en": row["en"], "zh": row["zh"]}
                return out
        except Exception:
            continue
    return {}


GLOSSARY = load_glossary()
# 长词优先，避免 "current assets" 被 "assets" 抢先匹配
GLOSS_KEYS = sorted(GLOSSARY.keys(), key=len, reverse=True)


def find_terms(text):
    """在文本中查找出现的术语（英文原词），返回 [(en, zh), ...]，长词优先、去重。"""
    if not text:
        return []
    low = text.lower()
    hits, seen = [], set()
    for key in GLOSS_KEYS:
        if len(key) < 3 or key in seen:
            continue
        if key in low:
            seen.add(key)
            hits.append((GLOSSARY[key]["en"], GLOSSARY[key]["zh"]))
    return hits[:80]


# ---------------------------------------------------------------- 配置

def load_cfg():
    cfg = dict(DEFAULT_CFG)
    try:
        with open(CFG_PATH, encoding="utf-8") as f:
            cfg.update(json.load(f))
    except Exception:
        pass
    if not cfg.get("api_key"):
        cfg["api_key"] = os.environ.get("TRANSLATOR_API_KEY", "")
    return cfg


def save_cfg(cfg):
    os.makedirs(CFG_DIR, exist_ok=True)
    with open(CFG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- 翻译引擎

SYS_PROMPT = (
    "你是资深财务翻译，专精中英财务报表与审计报告。规则：\n"
    "1) 只输出译文，不要解释、不要加引号、不要 Markdown 代码块。\n"
    "2) 术语必须使用下方【术语表】给出的中文，不得自创同义词；术语表没有的词按中国会计准则惯例译。\n"
    "3) 数字、单位（thousand/million/billion）、百分号、括号负数、日期原样保留，不得四舍五入或改写。\n"
    "4) 保持原文的换行与条目结构，表格行与行之间不要合并。\n"
    "5) 专有名词（公司名、人名、准则编号 IFRS 15 / ASC 606 / ISA 700）保留英文原文。\n"
    "6) 若原文每行带「L编号|」前缀，输出必须逐行对应、保留同样的编号前缀，不得合并、不得增删行。\n"
)


def build_messages(text, hits, strict):
    if hits:
        lines = "；".join(f"{en} = {zh}" for en, zh in hits[:120])
        term_part = f"【术语表】{lines}\n\n"
    else:
        term_part = ""
    user = f"{term_part}【原文】\n{text}\n\n【中文译文】"
    return [{"role": "system", "content": SYS_PROMPT}, {"role": "user", "content": user}]


def build_repair_messages(text, zh_draft, missing):
    """术语未被采用的补救重译请求。"""
    want = "；".join(f"{en} 必须译为「{zh}」" for en, zh in missing[:40])
    user = (
        f"【必须遵守的译法】{want}\n\n"
        f"【英文原文】\n{text}\n\n"
        f"【上一版译文（存在问题）】\n{zh_draft}\n\n"
        "请重译，务必使用上面规定的译法，其余保持忠实、结构与数字不变。只输出最终中文译文。"
    )
    return [{"role": "system", "content": SYS_PROMPT}, {"role": "user", "content": user}]


def term_missing(hits, zh_text):
    """返回译文中未采用规定译法的术语列表。"""
    out = []
    for en, zh in hits:
        if not zh:
            continue
        if zh in zh_text:
            continue
        if len(zh) >= 2 and zh[:2] in zh_text:   # 宽松：核心词已出现即视为达标
            continue
        out.append((en, zh))
    return out


def call_api(messages, cfg, timeout=180):
    url = cfg["base_url"].rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": cfg["model"],
        "messages": messages,
        "temperature": 0.1,
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": "Bearer " + cfg["api_key"],
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


NUM_RE = re.compile(r"\d[\d,\.]*")


def numbers_of(s):
    out = set()
    for m in NUM_RE.finditer(s or ""):
        v = m.group(0).rstrip(".,")
        if re.search(r"\d", v):
            out.add(v)
    return out


def split_blocks(text, limit):
    """按空行/换行切块，超长块再按句子切。"""
    blocks, buf = [], ""
    for line in text.splitlines(True):
        if len(buf) + len(line) > limit and buf.strip():
            blocks.append(buf)
            buf = ""
        buf += line
    if buf.strip():
        blocks.append(buf)
    return blocks or [text]


def translate_one(text, cfg, log=None):
    """译一块：首译 → 术语达标检查 → 必要时补救重译一次。返回 (译文, 命中术语)。"""
    hits = find_terms(text)
    zh = call_api(build_messages(text, hits, cfg.get("strict_terms", True)), cfg)
    if cfg.get("strict_terms", True) and hits:
        miss = term_missing(hits, zh)
        # 只有当未达标术语较多（≥2 条且占命中数一半以上）才值得多花一次调用
        if len(miss) >= max(2, len(hits) // 2):
            if log:
                log(f"    术语未达标 {len(miss)} 条，补救重译…")
            zh2 = call_api(build_repair_messages(text, zh, miss), cfg)
            if len(term_missing(hits, zh2)) < len(miss):
                zh = zh2
    return zh, hits


def is_table_like(text):
    """报表型输入：行多、行短。这类按行翻译，保证中英逐行对齐。"""
    lines = [l for l in text.splitlines() if l.strip()]
    if len(lines) < 5:
        return False
    lens = sorted(len(l) for l in lines)
    return lens[len(lens) // 2] <= 110


NUM_PREFIX = re.compile(r"^\s*L?(\d+)\s*[|｜]\s*(.*)$")


def translate_lines(lines, cfg, log=None, batch=12):
    """按行翻译：用 L编号| 协议保证一一对应；解析失败时退回整块翻译再切分。"""
    out = []
    for i in range(0, len(lines), batch):
        chunk = lines[i:i + batch]
        payload = "\n".join(f"L{j+1}| {l}" for j, l in enumerate(chunk))
        hits = find_terms(payload)
        zh = call_api(build_messages(payload, hits, cfg.get("strict_terms", True)), cfg)
        got = {}
        for raw in zh.splitlines():
            m = NUM_PREFIX.match(raw)
            if m:
                got[int(m.group(1))] = m.group(2).strip()
        if len(got) < len(chunk):
            # 协议失败：整块译一次，按行数能否对齐决定是否拆分
            block = call_api(build_messages("\n".join(chunk), find_terms("\n".join(chunk)),
                                            cfg.get("strict_terms", True)), cfg)
            bl = [x for x in block.splitlines() if x.strip()]
            if len(bl) == len(chunk):
                out.extend(bl)
            else:
                out.extend((bl + [""] * len(chunk))[:len(chunk)])
                if log:
                    log(f"    第 {i//batch+1} 批未能逐行对齐，已按整块输出")
            continue
        for j in range(len(chunk)):
            out.append(got.get(j + 1, ""))
    return out


def translate_text(text, cfg, log=print, progress=None):
    """返回 (译文全文, 明细列表[(原文块, 译文块)], 数字校验缺失列表)"""
    # 报表型输入：逐行翻译，中英严格对齐
    if is_table_like(text):
        raw_lines = text.splitlines()
        idx = [i for i, l in enumerate(raw_lines) if l.strip()]
        content = [raw_lines[i] for i in idx]
        zh_lines = translate_lines(content, cfg, log=log)
        details, missing = [], []
        for src, zh in zip(content, zh_lines):
            details.append((src, zh))
            lost = numbers_of(src) - numbers_of(zh)
            if lost:
                missing.extend(sorted(lost))
        if progress:
            progress(1, 1)
        return "\n".join(zh_lines), details, missing

    blocks = split_blocks(text, int(cfg.get("chunk_chars", 1600)))
    out, details, missing = [], [], []
    for i, b in enumerate(blocks, 1):
        if not b.strip():
            out.append(b)
            details.append((b, b))
            continue
        zh, hits = translate_one(b, cfg, log=log)
        out.append(zh if zh.endswith("\n") else zh + "\n")
        details.append((b, zh))
        lost = numbers_of(b) - numbers_of(zh) - numbers_of(" ".join(h[0] for h in hits))
        if lost:
            missing.extend(sorted(lost))
        if progress:
            progress(i, len(blocks))
    return "".join(out), details, missing


# ---------------------------------------------------------------- 读写各格式

def read_any(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in (".txt", ".md", ".csv"):
        for enc in ("utf-8-sig", "utf-8", "gbk", "latin-1"):
            try:
                with open(path, encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise RuntimeError("无法识别文本编码")
    if ext == ".docx":
        from docx import Document
        d = Document(path)
        parts = [p.text for p in d.paragraphs]
        for t in d.tables:
            for row in t.rows:
                parts.append("\t".join(c.text.strip() for c in row.cells))
        return "\n".join(parts)
    if ext == ".xlsx":
        from openpyxl import load_workbook
        wb = load_workbook(path, data_only=True)
        lines = []
        for ws in wb.worksheets:
            lines.append(f"### {ws.title}")
            for row in ws.iter_rows(values_only=True):
                if any(c not in (None, "") for c in row):
                    lines.append("\t".join("" if c is None else str(c) for c in row))
        return "\n".join(lines)
    if ext == ".pdf":
        import pymupdf
        doc = pymupdf.open(path)
        return "\n".join(p.get_text() for p in doc)
    raise RuntimeError("不支持的格式：" + ext)


def write_out(details, out_path, bilingual=True):
    ext = os.path.splitext(out_path)[1].lower()
    if ext == ".docx":
        from docx import Document
        from docx.shared import Pt
        d = Document()
        st = d.styles["Normal"]
        st.font.name = "微软雅黑"
        st.font.size = Pt(10.5)
        if bilingual:
            t = d.add_table(rows=1, cols=2)
            t.style = "Table Grid"
            h = t.rows[0].cells
            h[0].text, h[1].text = "English (source)", "中文译文"
            for src, zh in details:
                if not src.strip():
                    continue
                sl = [x for x in src.rstrip("\n").split("\n")]
                zl = [x for x in zh.rstrip("\n").split("\n")]
                if len(sl) == len(zl) and len(sl) > 1:
                    for a, b in zip(sl, zl):
                        c = t.add_row().cells
                        c[0].text = a.strip()
                        c[1].text = b.strip()
                else:
                    c = t.add_row().cells
                    c[0].text = src.strip()
                    c[1].text = zh.strip()
        else:
            for _, zh in details:
                d.add_paragraph(zh.strip())
        d.save(out_path)
        return out_path
    if ext == ".xlsx":
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "translation"
        ws.append(["English (source)", "中文译文"] if bilingual else ["中文译文"])
        for src, zh in details:
            ws.append([src.strip(), zh.strip()] if bilingual else [zh.strip()])
        ws.column_dimensions["A"].width = 70
        ws.column_dimensions["B"].width = 60
        wb.save(out_path)
        return out_path
    # 默认纯文本
    if bilingual:
        body = "\n\n".join(f"【原文】\n{s.strip()}\n【译文】\n{z.strip()}" for s, z in details if s.strip())
    else:
        body = "\n".join(z.strip() for s, z in details if s.strip())
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(body)
    return out_path


# ---------------------------------------------------------------- 命令行

def run_cli(argv):
    ap = argparse.ArgumentParser(description="英文财务报表翻译器（中英对照）")
    ap.add_argument("input", help="输入文件：txt/md/docx/xlsx/csv/pdf")
    ap.add_argument("-o", "--output", help="输出文件（默认与输入同名加 _中文 后缀）")
    ap.add_argument("--bilingual", action="store_true", default=True, help="输出中英对照（默认）")
    ap.add_argument("--zh-only", dest="bilingual", action="store_false", help="只输出中文")
    ap.add_argument("--api-key", help="覆盖配置中的 API Key")
    ap.add_argument("--base-url", help="OpenAI 兼容接口地址")
    ap.add_argument("--model", help="模型名")
    args = ap.parse_args(argv)

    cfg = load_cfg()
    if args.api_key:
        cfg["api_key"] = args.api_key
    if args.base_url:
        cfg["base_url"] = args.base_url
    if args.model:
        cfg["model"] = args.model
    if not cfg["api_key"]:
        print("缺少 API Key：请在图形界面填写，或设置环境变量 TRANSLATOR_API_KEY")
        return 2

    src = read_any(args.input)
    print(f"读取 {args.input}：{len(src)} 字符，术语库 {len(GLOSSARY)} 条")
    zh, details, missing = translate_text(src, cfg, progress=lambda i, n: print(f"  进度 {i}/{n}"))
    out = args.output or os.path.splitext(args.input)[0] + "_中文" + os.path.splitext(args.input)[1]
    write_out(details, out, args.bilingual)
    print(f"已保存：{out}")
    if missing:
        print("⚠ 以下数字在译文中未找到（请人工复核）：" + ", ".join(missing[:20]))
    return 0


# ---------------------------------------------------------------- 图形界面

def run_gui():
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    cfg = load_cfg()
    root = tk.Tk()
    root.title(f"财务报表中英翻译器 v{APP_VER}　术语库 {len(GLOSSARY)} 条")
    root.geometry("880x660")

    top = ttk.LabelFrame(root, text="1. 选择文件与输出")
    top.pack(fill="x", padx=10, pady=6)
    f_var = tk.StringVar()
    o_var = tk.StringVar()
    ttk.Entry(top, textvariable=f_var, width=70).grid(row=0, column=0, columnspan=3, padx=6, pady=4, sticky="we")
    ttk.Button(top, text="选择文件…", command=lambda: pick_in()).grid(row=0, column=3, padx=6)

    def pick_in():
        p = filedialog.askopenfilename(
            title="选择英文财务报表",
            filetypes=[("全部支持", "*.txt *.md *.docx *.xlsx *.csv *.pdf"), ("Word", "*.docx"),
                       ("Excel", "*.xlsx"), ("PDF", "*.pdf"), ("文本", "*.txt *.md *.csv")])
        if p:
            f_var.set(p)
            base, ext = os.path.splitext(p)
            o_var.set(base + "_中文" + (ext if ext in (".docx", ".xlsx", ".txt") else ".docx"))

    ttk.Entry(top, textvariable=o_var, width=70).grid(row=1, column=0, columnspan=3, padx=6, pady=4, sticky="we")
    ttk.Button(top, text="另存为…", command=lambda: save_as()).grid(row=1, column=3, padx=6)

    def save_as():
        p = filedialog.asksaveasfilename(defaultextension=".docx",
                                         filetypes=[("Word", "*.docx"), ("Excel", "*.xlsx"), ("文本", "*.txt")])
        if p:
            o_var.set(p)

    mid = ttk.LabelFrame(root, text="2. 翻译设置")
    mid.pack(fill="x", padx=10, pady=6)
    k_var = tk.StringVar(value=cfg.get("api_key", ""))
    b_var = tk.StringVar(value=cfg.get("base_url", ""))
    m_var = tk.StringVar(value=cfg.get("model", ""))
    bil = tk.BooleanVar(value=bool(cfg.get("bilingual", True)))
    strict = tk.BooleanVar(value=bool(cfg.get("strict_terms", True)))
    for i, (lab, var) in enumerate([("API Key", k_var), ("接口地址", b_var), ("模型", m_var)]):
        ttk.Label(mid, text=lab).grid(row=i, column=0, sticky="e", padx=6, pady=3)
        ttk.Entry(mid, textvariable=var, width=58, show="*" if lab == "API Key" else "").grid(
            row=i, column=1, columnspan=3, sticky="we", padx=6)
    ttk.Checkbutton(mid, text="输出中英对照", variable=bil).grid(row=3, column=1, sticky="w", padx=6)
    ttk.Checkbutton(mid, text="术语强制一致", variable=strict).grid(row=3, column=2, sticky="w")
    ttk.Label(mid, text="（默认 DeepSeek；也可填 OpenAI / 通义 / 本地 Ollama 的兼容地址）",
              foreground="#666").grid(row=4, column=1, columnspan=3, sticky="w", padx=6, pady=(0, 4))

    btns = ttk.Frame(root)
    btns.pack(fill="x", padx=10, pady=4)
    run_btn = ttk.Button(btns, text="开始翻译")
    run_btn.pack(side="left")
    ttk.Button(btns, text="保存设置", command=lambda: (save_cfg(cfg), messagebox.showinfo("提示", "设置已保存"))).pack(side="left", padx=8)
    ttk.Button(btns, text="清空日志", command=lambda: txt.delete("1.0", "end")).pack(side="left")
    pb = ttk.Progressbar(btns, mode="determinate", length=260)
    pb.pack(side="right")

    txt = tk.Text(root, wrap="word", font=("Consolas", 10))
    txt.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def log(*a):
        txt.insert("end", " ".join(str(x) for x in a) + "\n")
        txt.see("end")
        root.update_idletasks()

    log(f"就绪：内置术语库 {len(GLOSSARY)} 条（教材术语 + 报表行项目）。")
    log("用法：选择文件 → 填 API Key → 开始翻译；输出为中英对照 Word，表格逐行对应。")
    log("运行时会核对每一条数字，译文中缺失的数字会在结束时列出。")

    def work():
        cfg.update({"api_key": k_var.get().strip(), "base_url": b_var.get().strip(),
                    "model": m_var.get().strip(), "bilingual": bil.get(),
                    "strict_terms": strict.get()})
        save_cfg(cfg)
        if not cfg["api_key"]:
            messagebox.showwarning("缺少 API Key", "请先填写 API Key")
            return
        try:
            src = read_any(f_var.get())
        except Exception as e:
            messagebox.showerror("读取失败", str(e))
            return
        log(f"读取完成：{len(src)} 字符，术语库 {len(GLOSSARY)} 条")
        pb["maximum"] = max(1, len(split_blocks(src, int(cfg["chunk_chars"]))))
        try:
            zh, details, missing = translate_text(
                src, cfg, log=log, progress=lambda i, n: (pb.configure(value=i), root.update_idletasks()))
        except urllib.error.HTTPError as e:
            log("接口报错", e.code, e.read()[:300])
            messagebox.showerror("接口报错", f"HTTP {e.code}，请检查 Key / 地址 / 模型")
            return
        except Exception as e:
            log("失败：", e)
            messagebox.showerror("翻译失败", str(e))
            return
        out = write_out(details, o_var.get(), cfg["bilingual"])
        log("已保存：", out)
        if missing:
            log("⚠ 译文中未见这些数字，请复核：", ", ".join(missing[:20]))
        log("完成。")

    run_btn.configure(command=lambda: threading.Thread(target=work, daemon=True).start())

    # 命令行带文件：预填并在 --auto 时自动开始（拖拽 / 脚本调用都能用）
    _pre = [a for a in sys.argv[1:] if not a.startswith("-")]
    if _pre and os.path.exists(_pre[0]):
        f_var.set(_pre[0])
        _base, _ext = os.path.splitext(_pre[0])
        o_var.set(_base + "_中文" + (_ext if _ext in (".docx", ".xlsx", ".txt") else ".docx"))
        log("已载入命令行指定的文件。")
        if "--auto" in sys.argv:
            root.after(1200, lambda: run_btn.invoke())

    root.mainloop()


if __name__ == "__main__":
    # 打包成 windowed exe 后 sys.stdout 为 None，CLI 模式需要兜底输出流
    if sys.stdout is None or sys.stderr is None:
        import tempfile
        _log = open(os.path.join(tempfile.gettempdir(), "FinancialStatementTranslator_cli.log"), "a", encoding="utf-8")
        sys.stdout = sys.stdout or _log
        sys.stderr = sys.stderr or _log
    if "--cli" in sys.argv:
        i = sys.argv.index("--cli")
        sys.exit(run_cli(sys.argv[i + 1:]))
    run_gui()
