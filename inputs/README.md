# 双周报输入文件 / Biweekly Report Inputs

在运行双周报生成之前，请将以下文件放入此目录：

## 必需文件

| 文件名 | 说明 | 格式 |
|--------|------|------|
| `hk_peers.txt` | 香港同业信息原始文字 (文字8) | 纯文本 |
| `table6.txt` | 表6原始数据 | 纯文本 |
| `etf_data.xlsx` | 表4-5 ETF数据 | Excel (.xlsx) |

## 可选文件

| 文件名 | 说明 | 格式 |
|--------|------|------|
| `previous_report.md` | 上期双周报（用于对比分析） | Markdown |

> **提示**: 如果 `reports/` 目录中已有历史报告，系统会自动找到最近一期作为上期报告。

## 手机上传方法

1. 在 GitHub App 或手机浏览器中打开本仓库
2. 进入 `inputs/` 目录
3. 点击 **"Add file"** → **"Upload files"**
4. 选择要上传的文件
5. 点击 **"Commit changes"**

或者使用 Issue 模板提交文字数据（见 Issues → New Issue → 双周报数据提交）。
