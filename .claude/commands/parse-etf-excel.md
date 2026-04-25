# 解析ETF Excel数据（表4-5）

你是ETF数据处理专家。请解析 `inputs/etf_data/` 目录下的Excel/CSV文件，生成表4和表5的内容。

## 步骤

1. 确保已安装 openpyxl：`pip install openpyxl`
2. 运行 `python scripts/utils/excel_parser.py inputs/etf_data/ outputs/etf_parsed.json`
3. 读取 `outputs/etf_parsed.json`，理解数据结构
4. 如果用户通过 `$ARGUMENTS` 直接提供了CSV数据，将其保存到 `inputs/etf_data/user_input.csv` 后再解析

## 输出要求

### 表4: ETF持仓明细 → `outputs/03_table4_etf_holdings.md`

生成Markdown表格，包含：
- ETF名称/代码
- 持仓数量
- 当前市值
- 占比
- 较上期变动（如有上期数据）

### 表5: ETF交易记录 → `outputs/03_table5_etf_trades.md`

生成Markdown表格，包含：
- 交易日期
- ETF名称/代码
- 买入/卖出方向
- 数量、价格、金额

### ETF分析总结 → `outputs/03_etf_summary.md`

2-3段分析文字，总结本期ETF操作要点。

## 注意
- 数值保留2位小数
- 金额注明单位（元/万元/亿元）
- 不要编造任何数据，严格基于Excel内容
