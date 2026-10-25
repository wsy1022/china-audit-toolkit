<p align="center">
  <img src="docs/banner.svg" alt="中国审计机关常用工具包 China Audit Toolkit" width="1000">
</p>

<p align="center">
  <a href="https://github.com/wsy1022/china-audit-toolkit/releases"><img src="https://img.shields.io/github/v/release/wsy1022/china-audit-toolkit?label=release" alt="release"></a>
  <a href="https://github.com/wsy1022/china-audit-toolkit/actions/workflows/build.yml"><img src="https://github.com/wsy1022/china-audit-toolkit/actions/workflows/build.yml/badge.svg" alt="build"></a>
  <img src="https://img.shields.io/badge/license-MIT%20%2B%20CC%20BY%204.0-blue" alt="license">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776ab" alt="python">
</p>

<p align="center">
  18 个审计数据处理工具的启动台 + 中文技能文档。全离线，双击即用；<br>
  另附一个把英文财报译成中文的翻译器（第 18 个）。
</p>

---

## 这个包是什么

一个**启动台**（10 MB 单文件 exe）加 **18 份技能文档**。启动台读同目录的 `tools.json`，把工具按分类铺成卡片：点「启动」运行，点「说明」看该工具的用法文档；程序不在预期位置时整张卡降级成「未找到程序」，不会点了没反应。

技能文档是给 AI 助手看的：每份 `SKILL.md` 写清什么场景用这个工具、怎么准备输入、输出怎么验收、哪里容易踩坑。丢进 Claude Code / Codex / Hermes 的 skills 目录，助手就知道该在什么时候调用哪个工具。

## 这个包不是什么

- **不含审计署工具的可执行文件**。这些工具的著作权归原发布单位，本仓库只提供清单、启动台、技能文档与校验脚本。工具请从原发布渠道取得，按 `tools.json` 里的相对路径放进 `组件/`。
- 不产生审计结论，不替代复核与职业判断。
- 翻译器只做语言转换，不做汇率换算、不做单位缩放。

## 18 个工具

| 编号 | 工具 | 分类 | 解决什么 |
|---|---|---|---|
| 01 | 批量Word文档关键字检索 | 文档检索 | 批量检索 Word 文档中的关键字，输出命中文件与段落清单到 Excel，支持正则。 |
| 01B | 批量Word检索(支持doc老格式) | 文档检索 | 同上，检索范围含老式 `.doc`（自动转 docx，需本机装有 WPS 或 Office）。 |
| 07 | 文本文档比对工具 | 文档检索 | 两段文本左右对照，增删改高亮；支持粘贴或导入 txt/doc/docx/wps。 |
| 02 | 数据分析关联查询工具 | 表格分析 | Excel/CSV 表 A 与表 B 做左/右/内/外关联查询并导出。 |
| 03 | 表格数据关联工具 | 表格分析 | Sheet 转关系表，连线可视化建关联，生成合并数据。 |
| 12 | Excel单表拆分 | 表格分析 | 一个 Excel 按指定字段拆成多个文件（QT 版 / 轻量 TK 版）。 |
| 13 | Excel多表合一 | 表格分析 | 多个 Excel 合并成一个（QT 版 / 轻量 TK 版）。 |
| 14 | Excel多页合表 | 表格分析 | 一个 Excel 的多个 Sheet 合成一张表（QT 版 / 轻量 TK 版）。 |
| 04 | 图片文字识别工具 | OCR识别 | 图片 / 图片式 PDF 转 Word，本地 PaddleOCR，无需联网。 |
| 08 | 发票识别工具 | OCR识别 | 发票图片识别成表格并导出 Excel，本地识别。 |
| 09 | 发票信息批量提取工具 | OCR识别 | 批量 PDF 电子发票结构化提取到表格（QT 版 / 轻量 TK 版）。 |
| 10 | 身份证手机号识别工具 | OCR识别 | 身份证 OCR 取结构化信息；身份证号 / 手机号归属地查询，支持 Excel 批量。 |
| 05 | PDF文件内容提取工具 | PDF处理 | 文本式 PDF 正文转 Word、表格转 CSV。 |
| 06A | PDF数据提取工具 | PDF处理 | PDF 文本 / 表格 → Word 或 Excel，银行流水、账户协查类 PDF 首选。 |
| 06B | PDF文件转换工具 | PDF处理 | PDF 全文转换。 |
| 11 | 语音识别工具 | 语音比对 | 录音转文字，本地 sherpa-ncnn 中英双语模型，完全离线。 |
| S | 关键词搜索工具 | 搜索工具 | 全盘文档搜索（含扫描件 OCR），段落级摘要、命中高亮。 |
| 15 | 财务报表中英翻译器 | 翻译 | 英文财报译成中英对照 Word，术语锁定、数字校验、报表逐行对齐。 |

## 怎么用

**用工具**——把官方工具放到 `组件/` 下对应路径，然后双击启动台：

```
中国审计机关常用工具包.exe
```

**用技能**——把 `skills/` 下需要的目录拷进助手的 skills 目录，例如：

```bash
cp -r skills/excel-split ~/.claude/skills/
```

之后对助手说「把这三年的凭证表按供应商拆开，每家一个文件」，它会按 `excel-split` 的流程走：先查表头和主键，再拆，最后核对行数守恒。

**校验工具是否齐全**：

```bash
python scripts/verify_toolbox.py --root "E:\审计数据处理工具箱"
```

逐个核对 18 个工具的路径、大小与 SHA-256，缺哪个报哪个，版本被换过也会指出来。

## 第 18 个工具：财务报表中英翻译器

审计境外主体、跨境项目、外资企业年报时，英文报表要读成中文。机翻错的地方集中在三处——术语漂移、数字丢失、行错位——这个工具对三处各设一道闸：750 条会计审计术语定向注入并译后核对、全文数字比对、报表型输入逐行对齐。

源码在 `apps/translator/`，exe 在 Releases，完整技能与术语表在 [`wsy1022/accounting-audit-en-zh`](https://github.com/wsy1022/accounting-audit-en-zh)。

## 怎么往清单里加自己的工具

`tools.json` 是唯一的数据源，加一条就多一张卡：

```json
{
  "id": "16",
  "name": "往来款账龄分析",
  "cat": "表格分析",
  "desc": "按科目和账龄区间汇总往来款，输出账龄表。",
  "exe": "组件/自建工具/16往来款账龄分析/往来款账龄分析.exe",
  "help": "组件/说明/16往来款账龄分析.txt",
  "keywords": "账龄 往来 应收 应付",
  "variants": [{"label": "轻量版(TK)", "exe": "组件/自建工具/16往来款账龄分析/往来款账龄分析_TK.exe"}]
}
```

`cat` 不在 `categories` 里就新开一个分类页；`help` 指向的 txt 会被「说明」按钮用系统默认程序打开。

## 仓库结构

```
china-audit-toolkit/
├── tools.json                    清单：18 个工具
├── tools.sha256                  22 个文件的大小与哈希（含 4 个轻量变体）
├── launcher/toolbox.py           启动台源码（tkinter，单文件）
├── skills/                       18 份 SKILL.md
│   ├── 00-overview/              该用哪个工具：按任务分流的决策表
│   ├── word-keyword-search/ …    01 / 01B / 07 / S
│   ├── table-join/ …             02 / 03 / 12 / 13 / 14
│   ├── ocr-image/ …              04 / 08 / 09 / 10
│   ├── pdf-extract/ …            05 / 06A / 06B
│   ├── speech-to-text/           11
│   └── accounting-audit-en-zh/   15，含 750 条术语表与 155 组句式
├── apps/translator/              翻译器源码 + 术语库
├── scripts/
│   ├── verify_toolbox.py         路径 / 大小 / 哈希核对
│   └── build_exe.bat             一键打包启动台
└── docs/                         banner、图标、界面截图
```

## 自己打包

```bash
pip install pyinstaller
cd launcher && pyinstaller --noconfirm --onefile --windowed \
  --name "中国审计机关常用工具包" --add-data "../tools.json;." --icon ../docs/app.ico toolbox.py
```

产物在 `launcher/dist/`。

## 著作权与来源

- 21 个审计署工具的可执行文件**不在本仓库**，著作权归原发布单位；本仓库不重新分发它们，只提供索引与启动能力。
- `tools.sha256` 记录的是本机核对过的取值，方便你判断手上的工具版本是否被替换过。
- 本仓库自有的代码（启动台、翻译器、校验脚本）MIT；技能文档 CC BY 4.0。
- 详见 [NOTICE.md](NOTICE.md)。

<p align="center">
  <sub><b>中文</b> · <a href="README.en.md">English</a></sub>
</p>
