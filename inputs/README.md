# 输入文件说明

请将以下文件放入对应目录，然后运行双周报生成。

## 目录结构

```
inputs/
├── etf_data/           ← 表4-5 ETF Excel文件 (.xlsx/.csv)
├── table6/             ← 表6信息 (.txt/.xlsx)
├── hk_peer_info/       ← 香港同业信息文字 (.txt)
└── previous_report/    ← 上期双周报 (.md/.txt)
```

## 提交方式

### 方式一：直接上传文件
在 Claude Code Web 中上传文件到对应目录。

### 方式二：在聊天中粘贴文本
直接在 Claude Code 对话中粘贴文本内容，系统会自动保存到对应目录。

### 方式三：通过 GitHub Issue 提交
使用 Issue 模板提交文字内容（适合手机操作，文字类输入）。
Excel文件仍需通过方式一或二上传。

## 注意事项
- Excel文件支持 `.xlsx`、`.xls`、`.csv` 格式
- 文本文件支持 `UTF-8` 和 `GBK` 编码
- 上期双周报用于格式参考和数据对比
