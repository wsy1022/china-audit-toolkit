# 英文财务报表结构速查

翻译前先认清这是哪张表、走什么列报顺序。**同一科目在不同准则下叫法不同，这是最容易翻错的地方。**

---

## 1. 资产负债表 Balance Sheet / Statement of Financial Position

### 两种格式

| 格式 | 结构 | 常见于 |
|---|---|---|
| 账户式 account form | 资产在左，负债与权益在右 | 英文年报少见 |
| 报告式 report form | 资产 → 负债 → 权益，竖排 | 绝大多数英文年报 |

### 列报顺序的坑

- **IFRS**：通常按「非流动在前」（non-current first，即反向流动性），欧洲公司常见。
- **US GAAP**：按流动性从强到弱（current first），美国公司常见。

看到 `Property, plant and equipment` 排在第一行不要以为是错，那是 IFRS 反向列报。

### 行项目对照

| English | 中文 | 备注 |
|---|---|---|
| **ASSETS 资产** | | |
| Cash and cash equivalents | 现金及现金等价物 | CAS 口径叫「货币资金」 |
| Short-term investments | 短期投资 | |
| Trade and other receivables | 应收账款及其他应收款 | trade = 交易性/经营性 |
| Inventories | 存货 | US 也用 inventories；英式用 stocks |
| Prepayments | 预付款项 | 英式 prepayments，美式 prepaid expenses |
| **Total current assets** | **流动资产合计** | |
| Property, plant and equipment (PP&E) | 固定资产 | 英式 fixed assets |
| Right-of-use assets | 使用权资产 | IFRS 16 后必备 |
| Investment property | 投资性房地产 | 只在 IFRS 有 |
| Intangible assets | 无形资产 | |
| Goodwill | 商誉 | 不减值不摊销，只做 impairment test |
| Deferred tax assets | 递延所得税资产 | |
| **Total assets** | **资产总计** | |
| **LIABILITIES 负债** | | |
| Trade and other payables | 应付账款及其他应付款 | |
| Contract liabilities | 合同负债 | IFRS 15 后取代大部分 deferred revenue |
| Employee benefits payable | 应付职工薪酬 | |
| Current tax liabilities | 当期所得税负债 | |
| Borrowings | 借款 | 短期+长期常分列 |
| Lease liabilities | 租赁负债 | |
| Provisions | 预计负债 | 注意不是「准备」 |
| **Total liabilities** | **负债合计** | |
| **EQUITY 所有者权益** | | |
| Share capital | 股本 | 美式 common stock |
| Share premium / Additional paid-in capital | 股本溢价 / 资本公积 | 美式 APIC |
| Retained earnings | 留存收益（未分配利润） | CAS 报表列「未分配利润」 |
| Other components of equity | 其他权益项目 | |
| Treasury shares | 库存股 | 减项 |
| Equity attributable to owners of the parent | 归属于母公司所有者权益 | |
| Non-controlling interests | 少数股东权益 | 旧称 minority interests |
| **Total equity** | **所有者权益合计** | |
| **Total liabilities and equity** | **负债和所有者权益总计** | 必须等于 total assets |

---

## 2. 利润表 Income Statement

### 两种格式

| 格式 | 特征 | 判读 |
|---|---|---|
| Multi-step 多步式 | 分段算毛利、营业利润、税前利润 | 英文年报主流，信息量大 |
| Single-step 单步式 | 收入合计 − 费用合计 = 净利润 | 简单，常见于小公司 |

### 行项目对照（多步式顺序）

| English | 中文 |
|---|---|
| Revenue / Sales / Turnover | 营业收入（turnover 为英式） |
| Cost of sales / Cost of revenue / Cost of goods sold | 营业成本 |
| **Gross profit** | **毛利** |
| Selling and distribution expenses | 销售费用 |
| General and administrative expenses | 管理费用 |
| Research and development expenses | 研发费用 |
| Other income | 其他收益 |
| Other gains and losses | 营业外收支净额 |
| **Operating profit / Operating income** | **营业利润** |
| Finance income / Finance costs | 财务收益 / 财务费用 |
| Share of profit of associates and joint ventures | 对联营及合营企业的投资收益 |
| **Profit before tax (PBT)** | **利润总额** |
| Income tax expense / Provision for income taxes | 所得税费用 |
| **Net profit / Net income / Profit for the year** | **净利润** |
| Attributable to: owners of the parent / NCI | 归属于：母公司股东 / 少数股东 |
| Basic / Diluted earnings per share | 基本 / 稀释每股收益 |

### 三个易混

- `Revenue` ≠ `Income`。revenue 是主营收入；income 是收益（含利得），广义。
- `Profit` 是利润（表内结论），`Earnings` 多用于 EPS 语境，`Gain` 是处置等非主营利得。
- `Turnover` 在英式报表里就是 revenue，不是「周转率」（周转率是 turnover ratio，看上下文）。

---

## 3. 现金流量表 Statement of Cash Flows

### 三大活动（顺序固定）

| English | 中文 |
|---|---|
| Cash flows from operating activities | 经营活动产生的现金流量 |
| Cash flows from investing activities | 投资活动产生的现金流量 |
| Cash flows from financing activities | 筹资活动产生的现金流量 |

### 间接法调整项（operating 段的固定套路）

从 `Profit before tax` 出发，往回加：

| English | 中文 | 方向 |
|---|---|---|
| Adjustments for: | 调整项： | — |
| Depreciation and amortisation | 折旧及摊销 | ＋ |
| Impairment losses | 减值损失 | ＋ |
| Finance costs | 财务费用 | ＋ |
| Gain on disposal of PP&E | 处置固定资产的收益 | − |
| Share of profit of associates | 对联营企业的投资收益 | − |
| Increase in inventories | 存货的增加 | −（占用资金） |
| Increase in trade receivables | 应收账款的增加 | − |
| Increase in trade payables | 应付账款的增加 | ＋ |
| Interest paid | 支付的利息 | − |
| Income taxes paid | 支付的所得税 | − |
| **Net cash from operating activities** | **经营活动产生的现金流量净额** | |

**方向判断口诀**：资产增加＝花钱（−），负债增加＝收钱（＋）。译的时候方向词不能丢。

### 投资/筹资段高频项

| English | 中文 |
|---|---|
| Purchases of property, plant and equipment | 购建固定资产支付的现金 |
| Proceeds from disposal of assets | 处置资产收到的现金 |
| Acquisition of subsidiaries, net of cash acquired | 收购子公司支付的现金净额 |
| Proceeds from borrowings | 取得借款收到的现金 |
| Repayment of borrowings | 偿还债务支付的现金 |
| Dividends paid | 分配股利支付的现金 |
| Proceeds from issue of shares | 发行股份收到的现金 |
| Net increase in cash and cash equivalents | 现金及现金等价物净增加额 |
| Effect of exchange rate changes on cash | 汇率变动对现金的影响 |

---

## 4. 所有者权益变动表 Statement of Changes in Equity

| English | 中文 |
|---|---|
| Balance at 1 January | 1 月 1 日期初余额 |
| Total comprehensive income | 综合收益总额 |
| Profit for the year | 年度利润 |
| Other comprehensive income | 其他综合收益 |
| Transactions with owners | 与所有者的交易 |
| Issue of shares | 发行股份 |
| Dividends declared / paid | 宣告 / 支付股利 |
| Appropriation to surplus reserve | 提取盈余公积 |
| Balance at 31 December | 12 月 31 日期末余额 |

---

## 5. 附注 Notes to the Financial Statements

### 开头固定三件套

1. `Basis of preparation` 编制基础 — 声明按 IFRS/GAAP 编制、是否合并、计量基础。
2. `Significant accounting policies` 重要会计政策 — 逐条：收入确认、存货计价、固定资产折旧、金融工具分类。
3. `Critical accounting estimates and judgements` 关键会计估计与判断 — 减值测试假设、预计负债、递延所得税。

### 高频附注标题

| English | 中文 |
|---|---|
| Segment information | 分部信息 |
| Related party transactions | 关联方交易 |
| Contingent liabilities | 或有负债 |
| Commitments | 承诺事项 |
| Events after the reporting period | 资产负债表日后事项 |
| Fair value measurement | 公允价值计量 |
| Financial risk management | 金融风险管理 |
| Business combinations | 企业合并 |
| Leases | 租赁 |
| Share-based payment | 股份支付 |

### 附注语言的三个句式

- `…are stated at …` → 「……按……列示/计量」
- `…are recognised when …` → 「……在……时确认」
- `…is estimated based on …` → 「……依据……估计」

---

## 6. 审计报告 Independent Auditor's Report

### 标准结构（ISA 700 顺序）

| English | 中文 |
|---|---|
| Opinion | 审计意见 |
| Basis for Opinion | 形成审计意见的基础 |
| Key Audit Matters (KAM) | 关键审计事项 |
| Responsibilities of Management | 管理层责任 |
| Auditor's Responsibilities | 注册会计师的责任 |
| Other Information | 其他信息 |
| Report on Other Legal and Regulatory Requirements | 其他法律法规要求事项 |

### 四种意见（固定译法，不能混）

| English | 中文 | 触发情形 |
|---|---|---|
| Unqualified / Clean opinion | 无保留意见 | 报表公允反映 |
| Qualified opinion | 保留意见 | 错报重大但不广泛 |
| Adverse opinion | 否定意见 | 错报重大且广泛 |
| Disclaimer of opinion | 无法表示意见 | 无法获取充分证据且影响广泛 |

**易错**：`disclaimer of opinion` 是「无法表示意见」，不是「免责声明」；`emphasis of matter` 是「强调事项」，不是「重要事项」（重要事项是 KAM）。

### 关键句

| English | 中文 |
|---|---|
| present fairly, in all material respects | 在所有重大方面公允反映 |
| give a true and fair view | 真实、公允地反映 |
| in accordance with IFRS | 按照国际财务报告准则 |
| material uncertainty related to going concern | 与持续经营相关的重大不确定性 |
| we conducted our audit in accordance with ISAs | 我们按照国际审计准则执行了审计 |

---

## 7. 表头与单位（翻译前必须先定这三行）

| English | 中文 |
|---|---|
| Consolidated statements of operations | 合并利润表 |
| For the years ended December 31, 2024 and 2023 | 截至 2024 年及 2023 年 12 月 31 日止年度 |
| (in thousands, except per share data) | （单位：千美元，每股数据除外） |
| (unaudited) | （未经审计） |
| As restated | （经重述） |
| $ in millions | 单位：百万美元 |
