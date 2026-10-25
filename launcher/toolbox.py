# -*- coding: utf-8 -*-
"""中国审计机关常用工具包 · 启动台

读取同目录 tools.json，把工具按分类铺成卡片，点击即启动；工具缺失时整卡降级提示。

设计要点
- 只依赖标准库 tkinter：单文件，PyInstaller 打包后 10 MB 级别；
- tools.json 优先读外部文件（用户可自行增删工具），读不到则用打包时内嵌的副本；
- 工具路径相对启动台所在目录解析，整包可放任意盘、任意目录；
- 声明 DPI 感知并整体按显示缩放绘图，高分屏不糊；
- 卡片区可滚动，工具再多也不会被窗口高度截断。
"""
import ctypes
import json
import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk

APP_TITLE = "中国审计机关常用工具包"
APP_VER = "1.1"

INK = "#17150F"
MUTED = "#6B6659"
PAPER = "#F7F3EB"
CARD = "#FFFFFF"
LINE = "#E4DCCC"
CHIP = "#EFE9DC"
ACCENT = "#A62B1F"
DISABLED = "#D9D2C2"


# ---------------------------------------------------------------- 环境

def enable_dpi_awareness():
    """声明 DPI 感知，避免 Windows 位图拉伸导致字体发糊。"""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)   # PER_MONITOR_AWARE_V2
    except Exception:  # noqa: BLE001
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:  # noqa: BLE001
            pass


def dpi_scale():
    try:
        dc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, 88)   # LOGPIXELSX
        ctypes.windll.user32.ReleaseDC(0, dc)
        return max(1.0, dpi / 96.0)
    except Exception:  # noqa: BLE001
        return 1.0


def base_dir():
    """启动台所在目录：打包后取 exe 所在目录，脚本运行取脚本所在目录。"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


def load_manifest():
    here = base_dir()
    p = os.path.join(here, "tools.json")
    if os.path.exists(p):
        with open(p, encoding="utf-8-sig") as f:
            return json.load(f), here
    if hasattr(sys, "_MEIPASS"):
        with open(os.path.join(sys._MEIPASS, "tools.json"), encoding="utf-8-sig") as f:
            return json.load(f), here
    raise SystemExit("找不到 tools.json")


def resolve(root, rel):
    return os.path.normpath(os.path.join(root, rel.replace("/", os.sep)))


def launch(path, parent):
    if not os.path.exists(path):
        messagebox.showwarning(
            "程序不存在",
            "未找到该工具的可执行文件：\n\n" + path +
            "\n\n请把官方工具解压到 组件/ 下对应目录，或修改 tools.json 里的路径。",
            parent=parent)
        return
    try:
        subprocess.Popen([path], cwd=os.path.dirname(path), shell=False)
    except Exception as e:  # noqa: BLE001
        messagebox.showerror("启动失败", f"{e}\n\n{path}", parent=parent)


def open_help(path, parent):
    if not os.path.exists(path):
        messagebox.showinfo("暂无说明", "这个工具没有附带说明文档。", parent=parent)
        return
    try:
        os.startfile(path)  # noqa: S606
    except AttributeError:
        subprocess.Popen(["xdg-open", path])
    except Exception as e:  # noqa: BLE001
        messagebox.showerror("打开失败", str(e), parent=parent)


class App:
    def __init__(self, root, data, here):
        self.root = root
        self.s = dpi_scale()
        self.data = data
        self.here = here
        self.tools = data.get("tools", [])
        self.cats = ["全部"] + data.get("categories", [])
        self.cur_cat = "全部"
        self.q = ""

        root.title(f"{APP_TITLE} v{APP_VER}")
        root.geometry(f"{int(1180 * self.s)}x{int(760 * self.s)}")
        root.minsize(int(880 * self.s), int(560 * self.s))
        root.configure(bg=PAPER)

        self._header()
        self._searchbar()
        self._tabs()
        self._grid_area()
        self._footer()
        self.render()

    # ------------------------------------------------------------ 字体
    def f(self, size, bold=False, mono=False):
        fam = "Consolas" if mono else "Microsoft YaHei"
        return (fam, -int(size * self.s), "bold") if bold else (fam, -int(size * self.s))

    # ------------------------------------------------------------ 结构
    def _header(self):
        h = tk.Frame(self.root, bg=PAPER)
        h.pack(fill="x", padx=int(18 * self.s), pady=(int(10 * self.s), int(4 * self.s)))
        tk.Label(h, text=APP_TITLE, bg=PAPER, fg=INK, font=self.f(19, bold=True)).pack(side="left")
        tk.Label(h, text=f"v{APP_VER}　全部离线运行　共 {len(self.tools)} 个工具",
                 bg=PAPER, fg=MUTED, font=self.f(11)).pack(side="left", padx=int(14 * self.s), pady=(int(6 * self.s), 0))
        tk.Label(h, text="开源启动台 · 工具著作权归原发布单位", bg=PAPER, fg=MUTED,
                 font=self.f(10)).pack(side="right", pady=(int(6 * self.s), 0))

    def _searchbar(self):
        s = tk.Frame(self.root, bg=PAPER)
        s.pack(fill="x", padx=int(18 * self.s), pady=(0, int(6 * self.s)))
        self.q_var = tk.StringVar()
        self.q_var.trace_add("write", lambda *_: self._on_query())
        e = tk.Entry(s, textvariable=self.q_var, font=self.f(11), relief="solid", bd=1, bg="white", fg=INK,
                     insertbackground=INK)
        e.pack(fill="x", ipady=int(5 * self.s))
        self.entry = e

    def _tabs(self):
        self.tabs = tk.Frame(self.root, bg=PAPER)
        self.tabs.pack(fill="x", padx=int(18 * self.s), pady=(0, int(4 * self.s)))
        self.tab_btns = {}
        for c in self.cats:
            b = tk.Button(self.tabs, text=c, relief="flat", bd=0, cursor="hand2", font=self.f(10),
                          padx=int(12 * self.s), pady=int(4 * self.s), command=lambda c=c: self.set_cat(c))
            b.pack(side="left", padx=(0, int(6 * self.s)))
            self.tab_btns[c] = b

    def _grid_area(self):
        wrap = tk.Frame(self.root, bg=PAPER)
        wrap.pack(fill="both", expand=True, padx=int(12 * self.s))
        self.canvas = tk.Canvas(wrap, bg=PAPER, highlightthickness=0)
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.inner = tk.Frame(self.canvas, bg=PAPER)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda e: self.canvas.itemconfigure(self._win, width=e.width))
        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(int(-e.delta / 120), "units"))

    def _footer(self):
        f = tk.Frame(self.root, bg=PAPER)
        f.pack(fill="x", padx=int(18 * self.s), pady=(int(4 * self.s), int(8 * self.s)))
        self.stat = tk.Label(f, text="", bg=PAPER, fg=MUTED, font=self.f(10))
        self.stat.pack(side="left")
        tk.Button(f, text="编辑清单", relief="flat", bd=0, cursor="hand2", bg=PAPER, fg=MUTED,
                  font=self.f(10),
                  command=lambda: os.startfile(os.path.join(self.here, "tools.json"))).pack(side="right")
        tk.Button(f, text="打开工具目录", relief="flat", bd=0, cursor="hand2", bg=PAPER, fg=MUTED,
                  font=self.f(10), command=lambda: os.startfile(self.here)).pack(side="right", padx=int(12 * self.s))

    # ------------------------------------------------------------ 交互
    def set_cat(self, c):
        self.cur_cat = c
        self.render()

    def _on_query(self):
        self.q = self.q_var.get().strip().lower()
        self.render()

    def visible(self):
        out = []
        for t in self.tools:
            if self.cur_cat != "全部" and t.get("cat") != self.cur_cat:
                continue
            if self.q:
                hay = " ".join(str(t.get(k, "")) for k in ("name", "desc", "keywords", "cat")).lower()
                if self.q not in hay:
                    continue
            out.append(t)
        return out

    def render(self):
        for c, b in self.tab_btns.items():
            b.configure(bg=INK if c == self.cur_cat else PAPER, fg="white" if c == self.cur_cat else MUTED)

        for w in self.inner.winfo_children():
            w.destroy()

        items = self.visible()
        cols = 3
        for i in range(cols):
            self.inner.grid_columnconfigure(i, weight=1, uniform="card")
        for i, t in enumerate(items):
            self.card(self.inner, t, i, cols)
        self.canvas.yview_moveto(0)
        self.stat.configure(text=f"显示 {len(items)} / 共 {len(self.tools)} 个工具")

    def card(self, parent, t, i, cols):
        s = self.s
        exe = resolve(self.here, t.get("exe", ""))
        ok = os.path.exists(exe)
        wrap = tk.Frame(parent, bg=CARD, highlightbackground=LINE, highlightthickness=1)
        wrap.grid(row=i // cols, column=i % cols, sticky="nsew",
                  padx=int(5 * s), pady=int(4 * s))

        top = tk.Frame(wrap, bg=CARD)
        top.pack(fill="x", padx=int(12 * s), pady=(int(8 * s), int(2 * s)))
        tk.Label(top, text=t.get("id", ""), bg=CHIP if ok else "#F1E7E5",
                 fg=INK if ok else ACCENT, font=self.f(9, bold=True, mono=True),
                 padx=int(6 * s)).pack(side="left")
        tk.Label(top, text=t.get("name", ""), bg=CARD, fg=INK, font=self.f(12, bold=True),
                 anchor="w").pack(side="left", padx=int(8 * s))

        tk.Label(wrap, text=t.get("desc", ""), bg=CARD, fg=MUTED, font=self.f(9),
                 wraplength=int(356 * s), justify="left", anchor="w").pack(fill="x", padx=int(12 * s),
                                                                           pady=(0, int(5 * s)))

        btns = tk.Frame(wrap, bg=CARD)
        btns.pack(fill="x", padx=int(12 * s), pady=(0, int(8 * s)))
        tk.Button(btns, text="启动" if ok else "未找到程序", relief="flat", bd=0, cursor="hand2",
                  bg=INK if ok else DISABLED, fg="white" if ok else MUTED,
                  activebackground=ACCENT, activeforeground="white", font=self.f(10),
                  padx=int(14 * s), pady=int(3 * s),
                  command=lambda p=exe: launch(p, self.root)).pack(side="left")
        tk.Button(btns, text="说明", relief="flat", bd=0, cursor="hand2", bg=CHIP, fg=INK,
                  font=self.f(10), padx=int(12 * s), pady=int(3 * s),
                  command=lambda p=resolve(self.here, t.get("help", "")): open_help(p, self.root)).pack(
            side="left", padx=int(8 * s))
        for v in t.get("variants", []):
            vp = resolve(self.here, v.get("exe", ""))
            tk.Button(btns, text=v.get("label", "变体"), relief="flat", bd=0, cursor="hand2",
                      bg=CHIP, fg=INK, font=self.f(9), padx=int(10 * s), pady=int(3 * s),
                      command=lambda p=vp: launch(p, self.root)).pack(side="left", padx=(0, int(6 * s)))


def main():
    enable_dpi_awareness()
    data, here = load_manifest()
    root = tk.Tk()
    App(root, data, here)
    root.mainloop()


if __name__ == "__main__":
    main()
