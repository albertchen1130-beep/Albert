# 输入文件上传指南

## 如何通过手机上传输入文件

### 方法1: GitHub App 直接上传
1. 打开 GitHub App → 进入本仓库
2. 导航到对应的 `inputs/` 子目录
3. 点击 "Add file" → 上传文件
4. Commit 到 main 分支

### 方法2: 通过 GitHub 网页版（手机浏览器）
1. 打开浏览器访问本仓库
2. 导航到对应目录
3. 点击 "Add file" → "Upload files"
4. 拖入或选择文件上传

## 输入目录说明

```
inputs/
├── 表4-5-ETF/          ← 放入 ETF 相关 Excel 文件 (.xlsx/.csv)
├── 表6/                ← 放入表6数据 (.md/.txt/.xlsx)
├── 香港同业信息/        ← 放入香港同业信息文字 (.md/.txt)
└── 上期双周报/          ← 放入上一期双周报 (.md/.docx)
```

## 文件命名建议

- `表4-5-ETF/etf_data.xlsx` 或 `表4-5-ETF/etf_data.csv`
- `表6/表6数据.md` 或 `表6/表6数据.xlsx`
- `香港同业信息/同业信息.md` 或 `香港同业信息/同业信息.txt`
- `上期双周报/上期双周报.md`

## 上传完成后

上传所有文件后，前往 Actions 页面触发 "双周报生成 (Claude Code)" workflow。
