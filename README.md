# Mobile Biweekly Report / 手机双周报

在手机上一键生成双周报，无需电脑。

## How It Works / 工作原理

- **GitHub Actions** 提供 `workflow_dispatch` 触发器
- 你可以通过 **GitHub 手机 App** 直接触发运行
- 脚本自动分析 Git 提交历史，生成结构化的双周报
- 报告自动保存到 `reports/` 目录，并作为 Artifact 可下载

## How to Run from Phone / 手机上如何运行

### Step 1: 安装 GitHub 手机 App

- iOS: [App Store](https://apps.apple.com/app/github/id1477376905)
- Android: [Google Play](https://play.google.com/store/apps/details?id=com.github.android)

### Step 2: 在手机上触发双周报

1. 打开 GitHub App，进入本仓库
2. 点击底部 **Actions** 标签
3. 选择 **"Biweekly Report / 双周报"** workflow
4. 点击 **"Run workflow"**
5. 选择报告周期（7天 / 14天 / 30天）
6. 点击确认运行

### Step 3: 查看报告

- **在线查看**: Actions 运行完成后，点击进入该次运行，在 **Summary** 页面直接查看报告内容
- **下载文件**: 在 Artifacts 区域下载 `.md` 报告文件
- **仓库中查看**: 报告也会自动提交到 `reports/` 目录

## Auto Schedule / 自动定时

除了手动触发，workflow 也会在每月 **1日和15日** 的 UTC 9:00（北京时间 17:00）自动运行。

## Report Contents / 报告内容

每份双周报包含：

| Section / 板块 | Description / 说明 |
|---|---|
| Summary / 概览 | 提交数、贡献者、文件变更、代码增删统计 |
| By Contributor / 按贡献者 | 每位贡献者的提交明细 |
| Timeline / 时间线 | 按日期排列的提交记录 |

## Project Structure / 项目结构

```
.
├── .github/workflows/
│   └── biweekly-report.yml    # GitHub Actions workflow
├── scripts/
│   └── biweekly_report.py     # Report generation script
├── reports/                   # Generated reports (auto-created)
└── README.md
```
