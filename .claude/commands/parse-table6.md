# 处理表6数据

你是金融数据分析师。请处理 `inputs/table6/` 目录下的表6数据。

## 步骤

1. 检查 `inputs/table6/` 中的文件类型
2. 如果是Excel/CSV文件：运行 `python scripts/utils/excel_parser.py inputs/table6/ outputs/table6_excel_parsed.json`
3. 如果是文本文件：运行 `python scripts/utils/text_processor.py table6 inputs/table6/ outputs/table6_parsed.json`
4. 如果用户通过 `$ARGUMENTS` 直接提供文本数据，保存到 `inputs/table6/user_input.txt`
5. 读取解析后的数据

## 输出 → `outputs/04_table6.md`

生成标准格式的表6内容：
- Markdown表格（如数据为表格形式）
- 2-3句分析点评
- 与上期对比（如有上期数据参考 `outputs/previous_report_summary.json`）

## 注意
- 忠实于原始数据，不编造数值
- 缺失字段标注 `[数据待补充]`
