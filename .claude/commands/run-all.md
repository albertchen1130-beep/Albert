# 一键运行所有双周报 Agent

你是双周报系统的总调度 agent。你的任务是按顺序运行所有子 agent，完成完整的双周报生成流程。

## 执行流程

请严格按照以下顺序执行：

### 第一阶段：数据处理（可并行）

1. **检查输入文件**: 首先检查 `inputs/` 各子目录是否有有效输入文件
   - `inputs/表4-5-ETF/` — 至少一个 .xlsx/.csv/.md/.txt 文件
   - `inputs/表6/` — 至少一个数据文件
   - `inputs/香港同业信息/` — 至少一个 .md/.txt 文件
   - `inputs/上期双周报/` — 上期双周报文件

2. **准备输出目录**: 确保 `outputs/sections/` 目录存在
   ```bash
   mkdir -p outputs/sections
   ```

3. **处理表4-5 ETF数据**:
   - 读取 `inputs/表4-5-ETF/` 中的文件
   - 如果有 Excel 文件，先运行 `python3 scripts/excel_to_markdown.py inputs/表4-5-ETF/`
   - 解析数据，生成格式化的 Markdown 表格
   - 保存到 `outputs/sections/表4-5-ETF数据.md`

4. **处理表6信息**:
   - 读取 `inputs/表6/` 中的文件
   - 如果有 Excel 文件，先运行 `python3 scripts/excel_to_markdown.py inputs/表6/`
   - 整理格式，保存到 `outputs/sections/表6信息.md`

5. **处理香港同业信息**:
   - 读取 `inputs/香港同业信息/` 中的文件
   - 整理内容，保存到 `outputs/sections/8-香港同业信息.md`

### 第二阶段：报告汇编

6. **汇编完整双周报**:
   - 读取 `inputs/上期双周报/` 中的上期双周报作为格式参考
   - 读取 `outputs/sections/` 中所有章节文件
   - 读取 `templates/report-template.md` 了解报告结构
   - 汇编完整报告，保存到 `outputs/双周报-{日期}.md` 和 `reports/双周报-{日期}.md`

### 第三阶段：质量审查

7. **张总审查**:
   - 读取生成的双周报
   - 对比上期双周报检查格式一致性
   - 检查内容完整性、数据准确性、文字质量、格式规范
   - 生成审查意见到 `outputs/审查意见.md`
   - 如有必须修改的问题，自动修正并重新保存

### 第四阶段：输出确认

8. **最终确认**:
   - 列出所有生成的文件
   - 显示报告摘要
   - 显示审查结果摘要

## 注意事项

- 每个步骤完成后，确认输出文件已正确生成
- 如果某个输入缺失，跳过对应步骤但在报告中标注
- 保持所有数据的准确性，不做推测或编造
- 最终报告格式与上期双周报保持一致

$ARGUMENTS
