# 双周报全流程生成

你是双周报生成系统的编排者。请按以下步骤依次运行所有Agent，生成完整的双周报。

## 执行流程

### Phase 0: 输入检查

1. 运行 `python scripts/validate_inputs.py` 检查所有输入文件
2. 如果用户通过 `$ARGUMENTS` 提供了文本数据，将其保存到对应的 `inputs/` 子目录
3. 确认以下输入是否就绪：
   - `inputs/etf_data/` - 表4-5 ETF Excel
   - `inputs/table6/` - 表6信息
   - `inputs/hk_peer_info/` - 香港同业信息文字
   - `inputs/previous_report/` - 上期双周报
4. 对缺失的输入，标注 `[待补充]`，但不中断流程

### Phase 1: 数据预处理

运行 `python scripts/orchestrator.py --preprocess-only`

这会：
- 解析ETF Excel文件为JSON
- 处理表6文本/Excel数据
- 整理香港同业信息
- 分析上期双周报结构

### Phase 2: 各板块内容生成

依次执行以下Agent（每个Agent读取 `outputs/` 中的预处理数据，生成对应板块内容）：

#### Agent 02: 市场概览
- 读取 `outputs/etf_parsed.json` 和 `outputs/previous_report_summary.json`
- 参考 `agents/02_market_overview.md` 中的指令
- 基于ETF数据反映的市场趋势撰写市场概览
- 输出到 `outputs/02_market_overview.md`

#### Agent 03: ETF数据分析
- 读取 `outputs/etf_parsed.json`
- 参考 `agents/03_etf_analysis.md` 中的指令
- 生成表4（持仓明细）和表5（交易记录）
- 输出到 `outputs/03_table4_etf_holdings.md`、`outputs/03_table5_etf_trades.md`、`outputs/03_etf_summary.md`

#### Agent 04: 表6分析
- 读取 `outputs/table6_parsed.json`
- 参考 `agents/04_table6_analysis.md` 中的指令
- 输出到 `outputs/04_table6.md`

#### Agent 05: 香港同业信息
- 读取 `outputs/hk_peer_parsed.txt`
- 参考 `agents/05_hk_peer_info.md` 中的指令
- 整理润色香港同业信息
- 输出到 `outputs/05_hk_peer_info.md`

### Phase 3: 报告汇编

运行 `python scripts/orchestrator.py --compile-only`

这会：
- 读取报告模板 `templates/biweekly_template.md`
- 插入各Agent输出
- 生成完整双周报到 `reports/` 目录

### Phase 4: 审核准备

- 读取最终报告，生成审核摘要
- 检查所有 `[待补充]` 标记
- 列出需要张总关注的事项
- 输出审核摘要到 `outputs/07_review_summary.md`

### Phase 5: Git操作

1. 将所有输出和报告文件 add 到 git
2. 创建有意义的 commit message
3. 推送到当前分支
4. 创建 Draft PR，PR body 中包含审核摘要
5. 通知用户PR已创建，等待张总审核

## 重要约束

- **不要编造数据**：只基于用户提供的输入生成内容
- **保持中文专业风格**：金融术语要准确
- **标注缺失**：缺少数据的地方标注 `[待补充]` 而非编造
- **格式一致**：与上期双周报的格式保持一致
