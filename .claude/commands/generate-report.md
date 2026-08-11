# 汇编生成完整双周报

你是报告编辑。请将所有Agent的输出汇编为完整的双周报。

## 步骤

1. 读取模板 `templates/biweekly_template.md`
2. 读取上期双周报 `inputs/previous_report/` 了解格式要求
3. 依次读取各板块输出：
   - `outputs/02_market_overview.md`
   - `outputs/03_table4_etf_holdings.md`
   - `outputs/03_table5_etf_trades.md`
   - `outputs/03_etf_summary.md`
   - `outputs/04_table6.md`
   - `outputs/05_hk_peer_info.md`
   - `outputs/comparison_analysis.md`（如有）
4. 运行 `python scripts/orchestrator.py --compile-only` 生成初版
5. 阅读生成的报告，进行最终润色：
   - 统一标题层级和格式
   - 统一数值格式和单位
   - 确保各部分之间逻辑衔接
   - 检查所有 `[待补充]` 标记

## 输出

最终报告保存到 `reports/` 目录，文件名格式：
`biweekly-report-YYYY-MM-DD-to-YYYY-MM-DD.md`

## 质量检查清单
- [ ] 封面信息（日期、版本）正确
- [ ] 目录完整且链接正确
- [ ] 所有表格格式正确
- [ ] 数据前后一致（如概览中的数字与详表匹配）
- [ ] 无遗漏板块
- [ ] 中文表述通顺专业
