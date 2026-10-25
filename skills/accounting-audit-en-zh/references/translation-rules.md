# 财务报表中译：硬规则与判例

这份清单是从实际错译里反推出来的。**每一条都是「错了会被审计师一眼看穿」的点**，不是理论上可能错。

---

## 一、数字：零容忍

| 情形 | 原文 | 正确 | 错误 |
|---|---|---|---|
| 千分位 | 1,284,500 | 1,284,500 | 1284500（丢分隔仍可接受，但不要改写数值） |
| 括号负数 | (742,180) | （742,180）或 -742,180 | 742,180 |
| 破折号＝零 | — / – / - | —（保留破折号，表头注明「— 表示零」） | 0、无、N/A |
| 百分比 | 12.4% | 12.4% | 百分之十二点四（数字优先） |
| 每股金额 | $1.84 | 1.84 美元 | 1.84 元 |
| 股份数 | 100,000 | 100,000 股 | 10 万股（会丢精度） |

**校验动作**：把原文所有形如数字的串抽出来做集合，和译文数字集合求差。差集非空 → 退回重做。

---

## 二、单位：写在表头，不写在每行

| 原文 | 译法 |
|---|---|
| (in thousands) | （单位：千元／千美元） |
| (in millions) | （单位：百万元／百万美元） |
| (in thousands, except per share data) | （单位：千美元，每股数据除外） |
| $ in millions | 单位：百万美元 |
| € in thousands | 单位：千欧元 |

**禁止**：把 1,284,500（千美元）译成「128.45 亿美元」。数值不动，单位在表头说明，这是唯一正确做法。

---

## 三、日期与期间

| 原文 | 译法 |
|---|---|
| As of December 31, 2024 | 截至 2024 年 12 月 31 日 |
| For the year ended December 31, 2024 | 2024 年度／截至 2024 年 12 月 31 日止年度 |
| FY2024 / fiscal year 2024 | 2024 财年 |
| Q3 2024 | 2024 年第三季度 |
| YTD | 年初至今 |
| H1 | 上半年 |
| three months ended March 31 | 截至 3 月 31 日止三个月 |

---

## 四、易混词判例（按错误频率）

### income / revenue / profit / gain / earnings

| 英文 | 中文 | 判据 |
|---|---|---|
| revenue / sales | 收入／营业收入 | 主营销售收入 |
| income | 收益 | 广义，含利得；`income statement` 利润表 |
| profit | 利润 | 表内结论项（gross/operating/net） |
| gain | 利得 | 处置、公允价值变动等非主营 |
| earnings | 收益（EPS 语境） | `earnings per share` 每股收益 |

### provision / allowance / reserve / accrual

| 英文 | 中文 | 例 |
|---|---|---|
| provision | 预计负债（负债类）／（所得税语境）所得税费用 | `provision for income taxes` 所得税费用 |
| allowance | 备抵 | `allowance for doubtful accounts` 坏账准备 |
| reserve | 公积 | `capital reserve` 资本公积、`surplus reserve` 盈余公积 |
| accrual | 应计 | `accrued expenses` 应计费用 |

### material / significant / substantial

| 英文 | 中文 | 例 |
|---|---|---|
| material | 重大的（重要性） | `material misstatement` 重大错报 |
| raw materials | 原材料 | 只有这个语境是「材料」 |
| significant | 重要的 | `significant accounting policies` 重要会计政策 |
| substantial | 实质性的／大额的 | 看语境 |

### net / gross / consolidated / combined

| 英文 | 中文 |
|---|---|
| net of tax | 税后／扣除税款后 |
| net sales | 销售净额 |
| gross profit | 毛利（不是「总利润」） |
| consolidated | 合并（有控制关系） |
| combined | 汇总（无控制关系的并列） |

### equity / capital / shares

| 英文 | 中文 | 判据 |
|---|---|---|
| equity | 权益 | 报表项目（total equity 所有者权益合计） |
| equity interest | 股权 | 指持股比例时才是「股权」 |
| share capital | 股本 | |
| capital | 资本（`working capital` 营运资本） | 不要一律「资金」 |

---

## 五、术语一致性

同一份文件里：

- 一个英文词 → 一个中文词。`receivables` 不能一会儿「应收款」一会儿「应收账款」。
- 一个中文词 → 尽量只对应一个英文词。若原文本身混用（`sales` 与 `revenue` 交替），译文统一到「营业收入」，并在术语报告里记一笔。
- 术语库（`glossary.csv`）优先于语感。库里没有的词，第一次出现时用「中文（English）」标注，之后只用中文。

---

## 六、不译与保留

**保留英文原文**：
- 准则编号：IFRS 15、IAS 36、ASC 606、ISA 700、CAS 22
- 机构名：IASB、FASB、SEC、PCAOB、财政部
- 公司名、人名、地名：除非有官方中文名（Apple 苹果、HSBC 汇丰）
- 法律条文号、合同编号、股票代码

**必须译**：
- 报表标题、栏目名、附注标题
- 会计政策描述、审计意见表述
- 计量属性（amortised cost 摊余成本、fair value 公允价值）

---

## 七、语序与句式

英文报表句式的三种套路，中文各有固定落法：

| 英文套路 | 中文落法 | 例 |
|---|---|---|
| X is stated at Y | X 按 Y 列示／计量 | Inventories are stated at the lower of cost and NRV. → 存货按成本与可变现净值孰低计量。 |
| X is recognised when Y | X 在 Y 时确认 | Revenue is recognised when control transfers. → 收入在控制权转移时确认。 |
| X comprises / consists of Y | X 包括 Y | The Group comprises 12 subsidiaries. → 本集团包括 12 家子公司。 |
| X is measured at fair value through P&L | X 以公允价值计量且其变动计入当期损益 | FVTPL |
| Management has assessed… | 管理层已评估…… | 保持「已」字表完成 |

**不要**：把被动语态硬翻成「被……」，中文财务文本用「按……列示」「予以确认」更地道；但也不要为了通顺丢掉主语（谁确认、谁评估）。

---

## 八、交付形态

### 必须给的三样

1. **双语对照正文**：左英右中，行对行。
2. **术语一致性报告**：
   ```
   命中术语 128 条；未按术语库处理 3 条（列出）；自创译名 0 条。
   数字校验：原文 246 个数字，译文缺 0 个。
   ```
3. **不确定清单**：拿不准的词单独列，附两种译法 + 理由，让用户选。

### 不要做的

- 不要在译文里加「注：」「说明：」等原文没有的内容。
- 不要把附注合成段落（破坏可核对性）。
- 不要修正原文明显错误（原文写错就照译，另在报告里提示）。

---

## 九、审计语境的额外要求

审计底稿、询证函、管理层声明这类文件，译错会影响责任认定，额外守三条：

1. **情态动词不软化**：`shall` → 应（不是「可以」）；`may` → 可以；`must` → 必须；`should` → 应当。
2. **否定范围不改**：`except for` 保留为「除……外」，这是保留意见的标志词。
3. **主体不混**：`the auditor` 注册会计师／审计师；`management` 管理层；`those charged with governance` 治理层。三者不能互换。
